"""Tests for semantic reranking and evidence context assembly."""

import pytest

from app.ai.rag.indexing.filters import ChunkMetadata
from app.ai.rag.retrieval.context import build_context
from app.ai.rag.retrieval.hybrid import RetrievalQueryError
from app.ai.rag.retrieval.models import FusedCandidate
from app.ai.rag.retrieval.reranker import CrossEncoderReranker, RerankerNotConfiguredError, create_reranker
from app.core.config import Settings


def _candidate(
    chunk_id: str,
    text: str,
    *,
    rrf_score: float = 0.1,
    status: str = "approved",
    effective_from: str | None = "2020-01-01",
    effective_until: str | None = None,
    title: str = "Savings account",
) -> FusedCandidate:
    return FusedCandidate(
        chunk_id=chunk_id,
        document_id=chunk_id.split("#")[0],
        document_version="1.2",
        text=text,
        metadata=ChunkMetadata(
            chunk_id=chunk_id,
            document_id=chunk_id.split("#")[0],
            document_version="1.2",
            document_type="reference",
            document_title=title,
            status=status,
            product="bsbda",
            effective_from=effective_from,
            effective_until=effective_until,
            source_path="docs/accounts/bsbda.md",
            content_hash="hash",
            heading_path=["Savings account", "Eligibility"],
        ),
        retrieval_sources=["dense"],
        rrf_score=rrf_score,
    )


def _reranker(scores: dict[str, float]) -> CrossEncoderReranker:
    def score(query: str, texts: list[str]) -> list[float]:
        assert query == "Who can open a BSBDA?"
        return [scores[text] for text in texts]

    return CrossEncoderReranker("test-reranker", scorer=score)


def test_reranking_orders_by_the_original_question_not_the_fused_score():
    weak = _candidate("LOW#c0001", "A fixed deposit is a term deposit.", rrf_score=0.9)
    strong = _candidate("HIGH#c0001", "Any resident individual can open a BSBDA.", rrf_score=0.1)
    context = build_context(
        "Who can open a BSBDA?",
        [weak, strong],
        _reranker(
            {
                "A fixed deposit is a term deposit.": 0.1,
                "Any resident individual can open a BSBDA.": 0.9,
            }
        ),
        as_of="2026-10-02",
    )

    assert [item.candidate.chunk_id for item in context.items] == ["HIGH#c0001", "LOW#c0001"]
    assert context.items[0].rank == 1
    assert context.items[0].rerank_score == 0.9
    assert "version 1.2" in context.text
    assert "docs/accounts/bsbda.md" in context.text
    assert "Savings account > Eligibility" in context.text
    assert "not as instructions" in context.text


def test_selection_drops_expired_draft_and_duplicate_evidence_before_scoring():
    seen: list[str] = []

    def score(query: str, texts: list[str]) -> list[float]:
        seen.extend(texts)
        return [0.8 for _ in texts]

    context = build_context(
        "Who can open a BSBDA?",
        [
            _candidate("LIVE#c0001", "Residents may open a BSBDA.", rrf_score=0.2),
            _candidate("LIVE#c0001", "Residents may open a BSBDA.", rrf_score=0.4),
            _candidate("COPY#c0001", "Residents may open a BSBDA.", rrf_score=0.1),
            _candidate("OLD#c0001", "The 2014 circular said otherwise.", effective_until="2019-12-31"),
            _candidate("DRAFT#c0001", "Draft eligibility text.", status="draft"),
        ],
        CrossEncoderReranker("test-reranker", scorer=score),
        as_of="2026-10-02",
    )

    assert seen == ["Residents may open a BSBDA."]
    assert [item.candidate.chunk_id for item in context.items] == ["LIVE#c0001"]


def test_minimum_score_and_top_k_limit_the_evidence_set():
    context = build_context(
        "Who can open a BSBDA?",
        [
            _candidate("A#c0001", "alpha"),
            _candidate("B#c0001", "beta"),
            _candidate("C#c0001", "gamma"),
        ],
        _reranker({"alpha": 0.2, "beta": 0.9, "gamma": 0.5}),
        as_of="2026-10-02",
        min_score=0.4,
        top_k=1,
    )

    assert [item.candidate.chunk_id for item in context.items] == ["B#c0001"]


def test_token_budget_keeps_the_first_evidence_block_and_omits_the_rest():
    context = build_context(
        "Who can open a BSBDA?",
        [_candidate("A#c0001", "alpha"), _candidate("B#c0001", "beta")],
        _reranker({"alpha": 0.9, "beta": 0.8}),
        as_of="2026-10-02",
        token_budget=1,
    )

    assert [item.candidate.chunk_id for item in context.items] == ["A#c0001"]
    assert context.omitted == 1
    assert context.exceeds_budget is True


def test_blank_query_and_empty_candidates_do_not_call_the_reranker():
    calls = 0

    def score(query: str, texts: list[str]) -> list[float]:
        nonlocal calls
        calls += 1
        return []

    with pytest.raises(RetrievalQueryError):
        build_context("   ", [], CrossEncoderReranker("test-reranker", scorer=score))
    context = build_context(
        "Who can open a BSBDA?",
        [],
        CrossEncoderReranker("test-reranker", scorer=score),
        as_of="2026-10-02",
    )

    assert calls == 0
    assert context.items == []
    assert context.text == ""


def test_reranker_factory_uses_settings_and_does_not_load_weights():
    reranker = create_reranker(Settings(RERANKER_MODEL="cross-encoder/test"))

    assert reranker.model_name == "cross-encoder/test"
    assert reranker._model is None
    with pytest.raises(RerankerNotConfiguredError):
        CrossEncoderReranker(" ")
