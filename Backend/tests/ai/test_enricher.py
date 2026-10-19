"""Tests for chunk metadata enrichment using a language model."""

import json
from app.ai.rag.indexing.enricher import (
    LLMChunkEnricher,
    NoOpChunkEnricher,
    create_chunk_enricher,
    _merge_keywords,
)
from app.core.config import Settings
from app.modules.knowledge.models import KnowledgeChunk


def _sample_chunk(
    chunk_id: str,
    *,
    title: str = "BSBDA Account",
    text: str = "A zero balance savings account with no minimum balance penalty.",
    keywords: list[str] | None = None,
) -> KnowledgeChunk:
    return KnowledgeChunk(
        chunk_id=chunk_id,
        document_id=chunk_id.split("#")[0],
        document_version="1.0",
        document_type="product",
        document_title=title,
        heading_path=[title, "Features"],
        chunk_index=0,
        chunk_type="section",
        status="approved",
        product="bsbda",
        keywords=keywords or ["BSBDA", "zero balance"],
        source_location="Features",
        source_path="docs/accounts/bsbda.md",
        content=text,
        text=text,
        content_hash="hash123",
        eligible=True,
    )


class _MockLLM:
    def __init__(self, response_text: str = "") -> None:
        self.response_text = response_text
        self.calls: list[dict[str, str]] = []

    def complete(self, *, system: str, user: str) -> str:
        self.calls.append({"system": system, "user": user})
        return self.response_text


class _FailingLLM:
    def complete(self, *, system: str, user: str) -> str:
        raise RuntimeError("OpenAI rate limit exceeded")


def test_noop_chunk_enricher_returns_chunks_unmodified():
    chunk = _sample_chunk("ACCT#c0001")
    enricher = NoOpChunkEnricher()
    result = enricher.enrich([chunk])

    assert len(result) == 1
    assert result[0].keywords == ["BSBDA", "zero balance"]


def test_llm_chunk_enricher_merges_and_deduplicates_keywords():
    response = json.dumps(
        {
            "ACCT#c0001": ["zero balance", "fee waiver", "ATM limit"],
        }
    )
    llm = _MockLLM(response)
    enricher = LLMChunkEnricher(llm, batch_size=5)

    chunk = _sample_chunk("ACCT#c0001", keywords=["BSBDA", "zero balance"])
    result = enricher.enrich([chunk])

    assert len(result) == 1
    # Existing "BSBDA", "zero balance" preserved; new "fee waiver", "ATM limit" added; duplicates ignored
    assert result[0].keywords == ["BSBDA", "zero balance", "fee waiver", "ATM limit"]
    assert len(llm.calls) == 1
    assert "ACCT#c0001" in llm.calls[0]["user"]


def test_llm_chunk_enricher_handles_invalid_json_gracefully():
    llm = _MockLLM("Here are your keywords: fee waiver, ATM limit")
    enricher = LLMChunkEnricher(llm, batch_size=5)

    chunk = _sample_chunk("ACCT#c0001", keywords=["BSBDA"])
    result = enricher.enrich([chunk])

    # Falls back to original chunk with existing keywords
    assert len(result) == 1
    assert result[0].keywords == ["BSBDA"]


def test_llm_chunk_enricher_handles_llm_failure_gracefully():
    enricher = LLMChunkEnricher(_FailingLLM(), batch_size=5)

    chunk = _sample_chunk("ACCT#c0001", keywords=["BSBDA"])
    result = enricher.enrich([chunk])

    # Does not crash; gracefully returns chunk with existing keywords
    assert len(result) == 1
    assert result[0].keywords == ["BSBDA"]


def test_llm_chunk_enricher_batches_multiple_chunks():
    chunks = [
        _sample_chunk("ACCT#c0001"),
        _sample_chunk("ACCT#c0002"),
        _sample_chunk("ACCT#c0003"),
    ]
    response = json.dumps(
        {
            "ACCT#c0001": ["kw1"],
            "ACCT#c0002": ["kw2"],
            "ACCT#c0003": ["kw3"],
        }
    )
    llm = _MockLLM(response)
    enricher = LLMChunkEnricher(llm, batch_size=2)

    result = enricher.enrich(chunks)

    assert len(result) == 3
    # 3 chunks with batch_size=2 should produce 2 LLM calls
    assert len(llm.calls) == 2


def test_create_chunk_enricher_returns_noop_when_disabled():
    settings = Settings(ENABLE_METADATA_ENRICHMENT=False, OPENAI_API_KEY="test-key")
    enricher = create_chunk_enricher(settings)

    assert isinstance(enricher, NoOpChunkEnricher)


def test_create_chunk_enricher_returns_noop_when_no_api_key():
    settings = Settings(ENABLE_METADATA_ENRICHMENT=True, OPENAI_API_KEY="")
    enricher = create_chunk_enricher(settings)

    assert isinstance(enricher, NoOpChunkEnricher)


def test_merge_keywords_deduplication():
    existing = ["BSBDA", "zero balance"]
    additive = ["Zero Balance", "ATM limit", "bsbda", "FEE WAIVER"]
    merged = _merge_keywords(existing, additive)

    assert merged == ["BSBDA", "zero balance", "ATM limit", "FEE WAIVER"]
