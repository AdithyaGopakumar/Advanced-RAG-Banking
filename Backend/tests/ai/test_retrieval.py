"""Tests for query expansion, reciprocal rank fusion, and hybrid retrieval."""

import pytest

from app.ai.embeddings.deterministic import DeterministicEmbeddingProvider
from app.ai.rag.indexing.filters import ChunkMetadata, MetadataFilter
from app.ai.rag.indexing.models import RetrievalHit
from app.ai.rag.indexing.vector_store import InMemoryVectorStore, VectorRecord
from app.ai.rag.retrieval.hybrid import RetrievalQueryError, retrieve
from app.ai.rag.retrieval.mqe import LLMQueryExpander, OriginalQueryExpander, create_query_expander, normalize_queries
from app.ai.rag.retrieval.rrf import fuse_rankings
from app.core.config import Settings


def _metadata(chunk_id: str, *, product: str = "bsbda") -> ChunkMetadata:
    return ChunkMetadata(
        chunk_id=chunk_id,
        document_id=chunk_id.split("#")[0],
        document_version="1.0",
        document_type="reference",
        document_title="Account",
        status="approved",
        product=product,
        source_path="docs/accounts/bsbda.md",
        content_hash="hash",
    )


def _hit(chunk_id: str, source: str, score: float, text: str) -> RetrievalHit:
    metadata = _metadata(chunk_id)
    return RetrievalHit(
        chunk_id=chunk_id,
        document_id=metadata.document_id,
        score=score,
        source=source,  # type: ignore[arg-type]
        metadata=metadata,
        text=text,
    )


def test_rrf_prefers_a_chunk_found_by_both_indexes():
    fused = fuse_rankings(
        [
            [_hit("ONLY#c0001", "dense", 0.9, "dense only"), _hit("BOTH#c0001", "dense", 0.2, "both")],
            [_hit("BOTH#c0001", "bm25", 3.0, "both")],
        ],
        rrf_k=60,
    )

    both = next(item for item in fused if item.chunk_id == "BOTH#c0001")
    only = next(item for item in fused if item.chunk_id == "ONLY#c0001")
    assert fused[0].chunk_id == "BOTH#c0001"
    assert both.retrieval_sources == ["dense", "bm25"]
    assert both.dense_rank == 2
    assert both.bm25_rank == 1
    assert both.rrf_score == pytest.approx(1 / 62 + 1 / 61)
    assert only.retrieval_sources == ["dense"]
    assert only.dense_rank == 1
    assert only.bm25_rank is None
    assert len(fused) == 2


def test_rrf_keeps_the_best_rank_when_a_list_repeats_a_chunk():
    fused = fuse_rankings(
        [[_hit("ACCT#c0001", "dense", 0.4, "first"), _hit("ACCT#c0001", "dense", 0.1, "second")]],
        rrf_k=60,
    )

    assert len(fused) == 1
    assert fused[0].dense_rank == 1
    assert fused[0].rrf_score == pytest.approx(1 / 61)


def test_query_expansion_keeps_the_original_question_and_unique_rephrasings():
    queries = normalize_queries(
        "What are the charges for opening a BSBDA account?",
        """```json
        ["BSBDA account opening charges", "bsbda account opening charges", "charges applicable when opening a Basic Savings Bank Deposit Account", "extra"]
        ```""",
        max_queries=3,
    )

    assert queries == [
        "What are the charges for opening a BSBDA account?",
        "BSBDA account opening charges",
        "charges applicable when opening a Basic Savings Bank Deposit Account",
    ]


def test_invalid_expansion_output_uses_the_original_question():
    assert normalize_queries("BSBDA charges", "not json", max_queries=4) == ["BSBDA charges"]


def test_llm_expander_keeps_the_original_question_ahead_of_model_variants():
    class FakeModel:
        def complete(self, *, system: str, user: str) -> str:
            assert user == "BSBDA charges"
            return '["BSBDA account charges"]'

    queries = LLMQueryExpander(FakeModel(), max_queries=4).expand("BSBDA charges")

    assert queries == ["BSBDA charges", "BSBDA account charges"]


def test_unconfigured_expansion_does_not_call_a_model():
    assert create_query_expander(Settings(OPENAI_API_KEY="")).expand("BSBDA charges") == ["BSBDA charges"]


def test_hybrid_retrieval_fuses_dense_and_lexical_hits_and_limits_top_k():
    embedder = DeterministicEmbeddingProvider("paraphrase-MiniLM-L6-v2", 4)
    store = InMemoryVectorStore()
    both = embedder.embed_query("BSBDA charges").vector
    store.upsert(
        [
            VectorRecord(chunk_id="BOTH#c0001", vector=both, metadata=_metadata("BOTH#c0001"), text="BSBDA charges"),
            VectorRecord(
                chunk_id="DENSE#c0001",
                vector=[1.0, 0.0, 0.0, 0.0],
                metadata=_metadata("DENSE#c0001", product="loan"),
                text="loan",
            ),
        ]
    )

    class Lexical:
        def __init__(self) -> None:
            self.queries: list[str] = []

        def search(self, query: str, *, top_k: int, metadata_filter: MetadataFilter | None = None) -> list[RetrievalHit]:
            self.queries.append(query)
            assert top_k == 5
            assert metadata_filter is not None
            assert metadata_filter.product == "bsbda"
            return [_hit("BOTH#c0001", "bm25", 2.0, "BSBDA charges"), _hit("LEX#c0001", "bm25", 1.0, "fees")]

    lexical = Lexical()
    results = retrieve(
        "  BSBDA   charges ",
        embedder=embedder,
        vector_store=store,
        lexical_index=lexical,
        expander=OriginalQueryExpander(),
        metadata_filter=MetadataFilter(product="bsbda"),
        top_k=1,
        candidates_per_query=5,
        rrf_k=60,
    )

    assert lexical.queries == ["BSBDA charges"]
    assert [item.chunk_id for item in results] == ["BOTH#c0001"]
    assert results[0].retrieval_sources == ["dense", "bm25"]


def test_each_query_variant_is_searched_in_both_indexes():
    embedder = DeterministicEmbeddingProvider("paraphrase-MiniLM-L6-v2", 4)
    store = InMemoryVectorStore()
    seen: list[str] = []

    class Lexical:
        def search(self, query: str, *, top_k: int, metadata_filter: MetadataFilter | None = None) -> list[RetrievalHit]:
            seen.append(query)
            return []

    class Expander:
        def expand(self, query: str) -> list[str]:
            return [query, "BSBDA opening charges"]

    retrieve(
        "BSBDA charges",
        embedder=embedder,
        vector_store=store,
        lexical_index=Lexical(),
        expander=Expander(),
        top_k=3,
        candidates_per_query=2,
    )

    assert seen == ["BSBDA charges", "BSBDA opening charges"]


def test_blank_query_is_rejected():
    class Lexical:
        def search(self, query: str, *, top_k: int, metadata_filter: MetadataFilter | None = None) -> list[RetrievalHit]:
            return []

    with pytest.raises(RetrievalQueryError):
        retrieve(
            "   ",
            embedder=DeterministicEmbeddingProvider("paraphrase-MiniLM-L6-v2", 4),
            vector_store=InMemoryVectorStore(),
            lexical_index=Lexical(),
            expander=OriginalQueryExpander(),
        )
