"""Tests for dense indexing, BM25, and metadata filters."""

import pytest

from app.ai.embeddings.deterministic import DeterministicEmbeddingProvider
from app.ai.rag.indexing.lexical import (
    ElasticsearchLexicalIndex,
    LexicalIndexError,
    _index_mappings,
    _index_settings,
    create_lexical_index,
)
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


class _Indices:
    def __init__(self) -> None:
        self.created: list[dict[str, object]] = []
        self._exists = False

    def exists(self, *, index: str) -> bool:
        return self._exists

    def create(self, *, index: str, settings: dict[str, object], mappings: dict[str, object]) -> None:
        self.created.append({"index": index, "settings": settings, "mappings": mappings})
        self._exists = True


class _Elasticsearch:
    def __init__(self) -> None:
        self.indices = _Indices()
        self.bulks: list[list[dict[str, object]]] = []
        self.deletes: list[dict[str, object]] = []
        self.searches: list[dict[str, object]] = []
        self.response: dict[str, object] = {"hits": {"hits": []}}

    def bulk(self, *, operations: list[dict[str, object]], refresh: bool) -> None:
        self.bulks.append(operations)

    def delete_by_query(self, *, index: str, query: dict[str, object], refresh: bool) -> None:
        self.deletes.append(query)

    def search(self, *, index: str, **kwargs: object) -> dict[str, object]:
        self.searches.append({"index": index, **kwargs})
        return self.response


def _lexical() -> tuple[ElasticsearchLexicalIndex, _Elasticsearch]:
    client = _Elasticsearch()
    return ElasticsearchLexicalIndex(client, index_name="knowledge-chunks"), client


def test_lexical_index_uses_native_bm25_over_chunk_text():
    index, client = _lexical()
    index.sync([("BSBDA minimum balance is Rs 500", _metadata(chunk_id="B#c0001"))])

    settings = client.indices.created[0]["settings"]
    mappings = client.indices.created[0]["mappings"]
    assert settings == _index_settings()
    assert mappings == _index_mappings()
    similarity = settings["similarity"]["chunk_bm25"]  # type: ignore[index]
    assert similarity == {"type": "BM25", "k1": 1.5, "b": 0.75}
    text_field = mappings["properties"]["text"]  # type: ignore[index]
    assert text_field["analyzer"] == "chunk_text"
    assert "stemmer" not in str(settings)
    operation, source = client.bulks[0]
    assert operation == {"index": {"_index": "knowledge-chunks", "_id": "B#c0001"}}
    assert source["text"] == "BSBDA minimum balance is Rs 500"


def test_search_returns_a_bm25_retrieval_hit():
    index, client = _lexical()
    source = {
        "text": "BSBDA accounts have no minimum balance requirement.",
        "chunk_id": "B#c0001",
        "document_id": "B",
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
        "heading_path": ["Account", "Eligibility"],
    }
    client.response = {"hits": {"hits": [{"_id": "B#c0001", "_score": 2.4, "_source": source}]}}

    hits = index.search("BSBDA minimum balance", top_k=1)

    assert client.searches[0]["size"] == 1
    assert client.searches[0]["query"] == {
        "bool": {
            "must": [{"match": {"text": "BSBDA minimum balance"}}],
            "filter": [{"terms": {"status": ["approved", "current"]}}],
        }
    }
    assert hits[0].chunk_id == "B#c0001"
    assert hits[0].score == 2.4
    assert hits[0].source == "bm25"
    assert hits[0].text == source["text"]
    assert hits[0].metadata.product == "bsbda"


def test_metadata_filter_is_applied_before_top_k():
    index, client = _lexical()

    index.search("BSBDA", top_k=1, metadata_filter=MetadataFilter(product="bsbda", as_of="2026-06-01"))

    query = client.searches[0]["query"]
    assert isinstance(query, dict)
    filters = query["bool"]["filter"]
    assert client.searches[0]["size"] == 1
    assert {"term": {"product": "bsbda"}} in filters
    assert query["bool"]["must"] == [{"match": {"text": "BSBDA"}}]
    assert {"range": {"effective_from_date": {"lte": "2026-06-01"}}} in filters[2]["bool"]["should"]
    assert {"range": {"effective_until_date": {"gte": "2026-06-01"}}} in filters[3]["bool"]["should"]


def test_search_with_no_lexical_match_returns_no_hits():
    index, _client = _lexical()

    assert index.search("zzzyyy", top_k=5) == []


def test_sync_removes_chunks_that_are_no_longer_eligible():
    index, client = _lexical()
    index.sync(
        [
            ("BSBDA has no minimum balance", _metadata(chunk_id="ACCT#c0001")),
            ("RTGS cutoff is 7 pm", _metadata(chunk_id="ACCT#c0002", product="rtgs")),
        ]
    )
    index.sync([("BSBDA has no minimum balance requirement", _metadata(chunk_id="ACCT#c0001"))])

    assert client.deletes[-1] == {"bool": {"must_not": [{"ids": {"values": ["ACCT#c0001"]}}]}}


def test_unconfigured_elasticsearch_fails():
    with pytest.raises(LexicalIndexError):
        create_lexical_index(Settings(ELASTICSEARCH_URL="", ELASTICSEARCH_INDEX=""))


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
    lexical, _client = _lexical()
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
        _lexical()[0],
        embedding_provider="deterministic",
    ).manifest_hash
    dense = store.query(embedder.embed_query("RTGS").vector, top_k=5)
    lexical_hits = lexical.search("RTGS", top_k=5)
    assert [hit.chunk_id for hit in dense] == ["ACCT#c0001"]
    assert lexical_hits == []
