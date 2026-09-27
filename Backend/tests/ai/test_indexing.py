"""Tests for dense indexing, BM25, and metadata filters."""

from app.ai.embeddings.deterministic import DeterministicEmbeddingProvider
from app.ai.rag.indexing.bm25 import BM25Index, tokenize
from app.ai.rag.indexing.filters import ChunkMetadata, MetadataFilter, matches_filter, to_pinecone_filter
from app.ai.rag.indexing.indexer import index_knowledge
from app.ai.rag.indexing.vector_store import (
    InMemoryVectorStore,
    PineconeVectorStore,
    VectorRecord,
    create_vector_store,
)
from app.core.config import Settings
from app.modules.knowledge.models import KnowledgeChunk


def _chunk(
    chunk_id: str,
    text: str,
    *,
    content_hash: str = "hash",
    eligible: bool = True,
    status: str = "approved",
    product: str = "bsbda",
    effective_from: str | None = "2026-01-01",
    effective_until: str | None = None,
) -> KnowledgeChunk:
    return KnowledgeChunk(
        chunk_id=chunk_id,
        document_id=chunk_id.split("#")[0],
        document_version="1.0",
        document_type="reference",
        document_title="Account",
        heading_path=["Account", "Eligibility"],
        chunk_index=1,
        chunk_type="section",
        status=status,
        effective_from=effective_from,
        effective_until=effective_until,
        product=product,
        jurisdiction="IN",
        audience="customer",
        source_location="Eligibility",
        source_path="docs/accounts/bsbda.md",
        content=text,
        text=text,
        content_hash=content_hash,
        eligible=eligible,
    )


def _metadata(**overrides: object) -> ChunkMetadata:
    values: dict[str, object] = {
        "chunk_id": "ACCT#c0001",
        "document_id": "ACCT",
        "document_version": "1.0",
        "document_type": "reference",
        "document_title": "Account",
        "status": "approved",
        "product": "bsbda",
        "jurisdiction": "IN",
        "audience": "customer",
        "effective_from": "2026-01-01",
        "source_path": "docs/accounts/bsbda.md",
        "content_hash": "hash",
    }
    values.update(overrides)
    return ChunkMetadata(**values)  # type: ignore[arg-type]


def test_tokenizer_keeps_product_codes_and_amounts():
    assert tokenize("BSBDA minimum balance is Rs 500") == ["bsbda", "minimum", "balance", "is", "rs", "500"]


def test_bm25_prefers_the_chunk_that_uses_the_product_name():
    index = BM25Index()
    index.replace(
        [
            ("A savings account has a minimum balance.", _metadata(chunk_id="A#c0001", product="savings")),
            ("BSBDA accounts have no minimum balance requirement.", _metadata(chunk_id="B#c0001")),
        ]
    )

    hits = index.search("BSBDA minimum balance", top_k=1)

    assert [hit.chunk_id for hit in hits] == ["B#c0001"]
    assert hits[0].source == "bm25"


def test_metadata_filter_is_applied_before_top_k():
    index = BM25Index()
    index.replace(
        [
            ("BSBDA BSBDA BSBDA loan limit", _metadata(chunk_id="LOAN#c0001", product="loan")),
            ("BSBDA account eligibility", _metadata(chunk_id="ACCT#c0001", product="bsbda")),
        ]
    )

    hits = index.search("BSBDA", top_k=1, metadata_filter=MetadataFilter(product="bsbda"))

    assert [hit.chunk_id for hit in hits] == ["ACCT#c0001"]


def test_effective_window_keeps_open_ended_documents_and_drops_expired_ones():
    current = _metadata()
    expired = _metadata(chunk_id="OLD#c0001", effective_until="2026-01-31")
    future = _metadata(chunk_id="NEW#c0001", effective_from="2026-12-01")
    constraint = MetadataFilter(as_of="2026-06-01")

    assert matches_filter(current, constraint) is True
    assert matches_filter(expired, constraint) is False
    assert matches_filter(future, constraint) is False
    assert matches_filter(_metadata(status="draft"), MetadataFilter()) is False


def test_in_memory_dense_search_filters_then_limits():
    store = InMemoryVectorStore()
    store.upsert(
        [
            VectorRecord(chunk_id="LOAN#c0001", vector=[1.0, 0.0], metadata=_metadata(chunk_id="LOAN#c0001", product="loan"), text="loan"),
            VectorRecord(chunk_id="ACCT#c0001", vector=[0.2, 0.8], metadata=_metadata(), text="bsbda"),
        ]
    )

    hits = store.query([1.0, 0.0], top_k=1, metadata_filter=MetadataFilter(product="bsbda"))

    assert [hit.chunk_id for hit in hits] == ["ACCT#c0001"]
    assert hits[0].source == "dense"


def test_pinecone_adapter_sends_equality_filters_and_applies_dates_locally():
    class FakeIndex:
        def __init__(self) -> None:
            self.upserts: list[tuple[list[dict[str, object]], str]] = []
            self.deletes: list[tuple[list[str], str]] = []
            self.queries: list[dict[str, object]] = []

        def upsert(self, *, vectors: list[dict[str, object]], namespace: str) -> None:
            self.upserts.append((vectors, namespace))

        def delete(self, *, ids: list[str], namespace: str) -> None:
            self.deletes.append((ids, namespace))

        def query(self, **kwargs: object) -> dict[str, object]:
            self.queries.append(kwargs)
            return {
                "matches": [
                    {
                        "id": "OLD#c0001",
                        "score": 0.99,
                        "metadata": {
                            **_metadata(chunk_id="OLD#c0001", effective_until="2025-01-01").as_filter_dict(),
                            "text": "old fee",
                        },
                    },
                    {
                        "id": "ACCT#c0001",
                        "score": 0.4,
                        "metadata": {**_metadata().as_filter_dict(), "text": "current fee"},
                    },
                ]
            }

    index = FakeIndex()
    store = PineconeVectorStore(index, namespace="knowledge")
    store.upsert(
        [VectorRecord(chunk_id="ACCT#c0001", vector=[0.1, 0.2], metadata=_metadata(), text="current fee")]
    )
    store.delete(["OLD#c0001"])
    hits = store.query(
        [0.1, 0.2],
        top_k=2,
        metadata_filter=MetadataFilter(product="bsbda", as_of="2026-06-01"),
    )

    payload, namespace = index.upserts[0]
    metadata = payload[0]["metadata"]
    assert namespace == "knowledge"
    assert payload[0]["id"] == "ACCT#c0001"
    assert isinstance(metadata, dict)
    assert metadata["text"] == "current fee"
    assert index.deletes == [(["OLD#c0001"], "knowledge")]
    assert index.queries[0]["filter"] == to_pinecone_filter(MetadataFilter(product="bsbda", as_of="2026-06-01"))
    assert [hit.chunk_id for hit in hits] == ["ACCT#c0001"]
    assert hits[0].text == "current fee"


def test_unconfigured_pinecone_uses_memory():
    store = create_vector_store(Settings(PINECONE_API_KEY="", PINECONE_INDEX_NAME=""))

    assert isinstance(store, InMemoryVectorStore)


class _CountingEmbedder(DeterministicEmbeddingProvider):
    def __init__(self) -> None:
        super().__init__("paraphrase-MiniLM-L6-v2", 4)
        self.calls: list[list[str]] = []

    def embed_texts(self, texts, *, purpose):
        self.calls.append(list(texts))
        return super().embed_texts(texts, purpose=purpose)


def test_reindex_upserts_changed_hashes_and_deletes_removed_ids():
    embedder = _CountingEmbedder()
    store = InMemoryVectorStore()
    lexical = BM25Index()
    first = _chunk("ACCT#c0001", "BSBDA has no minimum balance", content_hash="aaa")
    second = _chunk("ACCT#c0002", "RTGS cutoff is 7 pm", content_hash="bbb", product="rtgs")
    draft = _chunk("CARD#c0001", "Draft credit card limit", content_hash="ccc", eligible=False, status="draft")

    manifest = index_knowledge(
        [first, second, draft],
        embedder,
        store,
        lexical,
        embedding_provider="deterministic",
    )
    changed = _chunk("ACCT#c0001", "BSBDA has no minimum balance requirement", content_hash="aaa-2")
    updated = index_knowledge(
        [changed],
        embedder,
        store,
        lexical,
        embedding_provider="deterministic",
        previous=manifest,
    )

    assert [record.chunk_id for record in manifest.records] == ["ACCT#c0001", "ACCT#c0002"]
    assert embedder.calls[0] == ["BSBDA has no minimum balance", "RTGS cutoff is 7 pm"]
    assert embedder.calls[1] == ["BSBDA has no minimum balance requirement"]
    assert [record.content_hash for record in updated.records] == ["aaa-2"]
    assert updated.manifest_hash == index_knowledge(
        [changed],
        _CountingEmbedder(),
        InMemoryVectorStore(),
        BM25Index(),
        embedding_provider="deterministic",
    ).manifest_hash
    dense = store.query(embedder.embed_query("RTGS").vector, top_k=5)
    lexical_hits = lexical.search("RTGS", top_k=5)
    assert [hit.chunk_id for hit in dense] == ["ACCT#c0001"]
    assert lexical_hits == []
