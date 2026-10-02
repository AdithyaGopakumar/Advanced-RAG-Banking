"""Elasticsearch lexical index.

Elasticsearch owns the inverted index and BM25 score. This module only sends
eligible chunk text, applies the existing metadata filters, and maps hits
back to RetrievalHit.
"""

from datetime import datetime
from typing import Protocol

from app.ai.rag.indexing.filters import ChunkMetadata, MetadataFilter
from app.ai.rag.indexing.models import RetrievalHit
from app.core.config import Settings, get_settings

_BM25_K1 = 1.5
_BM25_B = 0.75
_DATE = "%Y-%m-%d"


class LexicalIndexError(Exception):
    """The Elasticsearch lexical index cannot be used."""


class _Indices(Protocol):
    def exists(self, *, index: str) -> bool:
        """Return whether the lexical index is already present."""

    def create(self, *, index: str, settings: dict[str, object], mappings: dict[str, object]) -> object:
        """Create the lexical index."""


class _ElasticsearchClient(Protocol):
    """The Elasticsearch calls this index uses."""

    indices: _Indices

    def bulk(self, *, operations: list[dict[str, object]], refresh: bool) -> object:
        """Index a batch of chunks."""

    def delete_by_query(self, *, index: str, query: dict[str, object], refresh: bool) -> object:
        """Remove chunks that are no longer eligible."""

    def search(self, *, index: str, **kwargs: object) -> object:
        """Run a BM25 query."""


class ElasticsearchLexicalIndex:
    """Persistent BM25 index backed by one Elasticsearch index."""

    def __init__(self, client: _ElasticsearchClient, *, index_name: str) -> None:
        if not index_name.strip():
            raise LexicalIndexError("ELASTICSEARCH_INDEX is required")
        self._client = client
        self.index_name = index_name.strip()

    def sync(self, documents: list[tuple[str, ChunkMetadata]]) -> None:
        """Index the eligible chunks and drop ids that are no longer eligible."""
        self._ensure_index()
        operations: list[dict[str, object]] = []
        chunk_ids: list[str] = []
        for text, metadata in documents:
            chunk_ids.append(metadata.chunk_id)
            operations.append({"index": {"_index": self.index_name, "_id": metadata.chunk_id}})
            operations.append(_source(text, metadata))
        if operations:
            self._client.bulk(operations=operations, refresh=True)
        if chunk_ids:
            query: dict[str, object] = {"bool": {"must_not": [{"ids": {"values": chunk_ids}}]}}
        else:
            query = {"match_all": {}}
        self._client.delete_by_query(index=self.index_name, query=query, refresh=True)

    def search(
        self,
        query: str,
        *,
        top_k: int,
        metadata_filter: MetadataFilter | None = None,
    ) -> list[RetrievalHit]:
        """Return the top Elasticsearch BM25 hits that satisfy the metadata filter."""
        if top_k <= 0:
            return []
        constraint = metadata_filter or MetadataFilter()
        response = self._client.search(
            index=self.index_name,
            **_search_arguments(query, top_k, constraint),
        )
        hits: list[RetrievalHit] = []
        for hit in _hits(response):
            source = dict(hit.get("_source") or {})
            metadata = _metadata_from_source(source, chunk_id=str(hit.get("_id") or ""))
            hits.append(
                RetrievalHit(
                    chunk_id=metadata.chunk_id,
                    document_id=metadata.document_id,
                    score=float(hit.get("_score") or 0.0),
                    source="bm25",
                    metadata=metadata,
                    text=str(source.get("text") or ""),
                )
            )
        return hits

    def _ensure_index(self) -> None:
        exists = self._client.indices.exists(index=self.index_name)
        if exists:
            return
        self._client.indices.create(
            index=self.index_name,
            settings=_index_settings(),
            mappings=_index_mappings(),
        )


def create_lexical_index(settings: Settings | None = None) -> ElasticsearchLexicalIndex:
    """Open the configured Elasticsearch index. There is no other lexical backend."""
    current = settings if settings is not None else get_settings()
    url = current.ELASTICSEARCH_URL.strip()
    index_name = current.ELASTICSEARCH_INDEX.strip()
    if not url or not index_name:
        raise LexicalIndexError("Set ELASTICSEARCH_URL and ELASTICSEARCH_INDEX before lexical indexing.")
    try:
        from elasticsearch import Elasticsearch
    except ImportError as exc:
        raise LexicalIndexError("elasticsearch is not installed") from exc
    return ElasticsearchLexicalIndex(Elasticsearch(url), index_name=index_name)


def _index_settings() -> dict[str, object]:
    return {
        "similarity": {
            "chunk_bm25": {
                "type": "BM25",
                "k1": _BM25_K1,
                "b": _BM25_B,
            }
        },
        "analysis": {
            "analyzer": {
                "chunk_text": {
                    "type": "custom",
                    "tokenizer": "letter_digit",
                    "filter": ["lowercase"],
                }
            },
            "tokenizer": {
                "letter_digit": {
                    "type": "pattern",
                    "pattern": "[^A-Za-z0-9]+",
                }
            },
        },
    }


def _index_mappings() -> dict[str, object]:
    keyword = {"type": "keyword"}
    date = {"type": "date", "format": "yyyy-MM-dd"}
    return {
        "properties": {
            "text": {
                "type": "text",
                "analyzer": "chunk_text",
                "similarity": "chunk_bm25",
            },
            "chunk_id": keyword,
            "document_id": keyword,
            "document_version": keyword,
            "document_type": keyword,
            "document_title": keyword,
            "status": keyword,
            "product": keyword,
            "jurisdiction": keyword,
            "audience": keyword,
            "effective_from": keyword,
            "effective_until": keyword,
            "effective_from_date": date,
            "effective_until_date": date,
            "effective_from_invalid": {"type": "boolean"},
            "effective_until_invalid": {"type": "boolean"},
            "source_path": keyword,
            "content_hash": keyword,
            "heading_path": keyword,
            "embedding_model": keyword,
        }
    }


def _search_arguments(query: str, top_k: int, constraint: MetadataFilter) -> dict[str, object]:
    es_query = _query(query, constraint)
    return {
        "size": top_k,
        "query": es_query,
        "sort": [{"_score": "desc"}, {"chunk_id": "asc"}],
        "track_scores": True,
        "source": [
            "text",
            "chunk_id",
            "document_id",
            "document_version",
            "document_type",
            "document_title",
            "status",
            "product",
            "jurisdiction",
            "audience",
            "effective_from",
            "effective_until",
            "source_path",
            "content_hash",
            "heading_path",
            "embedding_model",
        ],
    }


def _query(text: str, constraint: MetadataFilter) -> dict[str, object]:
    filters = _filters(constraint)
    if filters is None:
        return {"match_none": {}}
    return {"bool": {"must": [{"match": {"text": text}}], "filter": filters}}


def _filters(constraint: MetadataFilter) -> list[dict[str, object]] | None:
    filters: list[dict[str, object]] = []
    if constraint.statuses is not None:
        if not constraint.statuses:
            return None
        filters.append({"terms": {"status": list(constraint.statuses)}})
    for field_name in ("product", "jurisdiction", "audience", "document_type", "document_id"):
        value = getattr(constraint, field_name)
        if value is not None:
            filters.append({"term": {field_name: value}})
    if constraint.as_of is not None:
        day = _valid_day(constraint.as_of)
        if day is None:
            return None
        filters.append(_window("effective_from", day, "lte"))
        filters.append(_window("effective_until", day, "gte"))
    return filters


def _window(field_name: str, day: str, operator: str) -> dict[str, object]:
    date_field = f"{field_name}_date"
    invalid_field = f"{field_name}_invalid"
    return {
        "bool": {
            "should": [
                {
                    "bool": {
                        "must_not": [
                            {"exists": {"field": date_field}},
                            {"term": {invalid_field: True}},
                        ]
                    }
                },
                {"range": {date_field: {operator: day}}},
            ],
            "minimum_should_match": 1,
        }
    }


def _source(text: str, metadata: ChunkMetadata) -> dict[str, object]:
    start = _valid_day(metadata.effective_from)
    end = _valid_day(metadata.effective_until)
    payload: dict[str, object] = {
        "text": text,
        "chunk_id": metadata.chunk_id,
        "document_id": metadata.document_id,
        "document_version": metadata.document_version,
        "document_type": metadata.document_type,
        "document_title": metadata.document_title,
        "status": metadata.status,
        "effective_from": metadata.effective_from or "",
        "effective_until": metadata.effective_until or "",
        "effective_from_invalid": bool(metadata.effective_from) and start is None,
        "effective_until_invalid": bool(metadata.effective_until) and end is None,
        "source_path": metadata.source_path,
        "content_hash": metadata.content_hash,
        "heading_path": list(metadata.heading_path),
        "embedding_model": metadata.embedding_model,
    }
    for field_name in ("product", "jurisdiction", "audience"):
        value = getattr(metadata, field_name)
        if value:
            payload[field_name] = value
    if start is not None:
        payload["effective_from_date"] = start
    if end is not None:
        payload["effective_until_date"] = end
    return payload


def _metadata_from_source(source: dict[str, object], *, chunk_id: str) -> ChunkMetadata:
    heading = source.get("heading_path") or []
    heading_path = [str(item) for item in heading] if isinstance(heading, list) else []
    return ChunkMetadata(
        chunk_id=str(source.get("chunk_id") or chunk_id),
        document_id=str(source.get("document_id") or ""),
        document_version=str(source.get("document_version") or ""),
        document_type=str(source.get("document_type") or ""),
        document_title=str(source.get("document_title") or ""),
        status=str(source.get("status") or ""),
        product=_optional(source.get("product")),
        jurisdiction=_optional(source.get("jurisdiction")),
        audience=_optional(source.get("audience")),
        effective_from=_optional(source.get("effective_from")),
        effective_until=_optional(source.get("effective_until")),
        source_path=str(source.get("source_path") or ""),
        content_hash=str(source.get("content_hash") or ""),
        heading_path=heading_path,
        embedding_model=str(source.get("embedding_model") or ""),
    )


def _optional(value: object) -> str | None:
    if value is None or value == "":
        return None
    return str(value)


def _valid_day(value: str | None) -> str | None:
    if value is None or not value.strip():
        return None
    try:
        datetime.strptime(value.strip(), _DATE)
    except ValueError:
        return None
    return value.strip()


def _hits(response: object) -> list[dict[str, object]]:
    outer = response.get("hits") if isinstance(response, dict) else getattr(response, "hits", None)
    if outer is None:
        return []
    raw_hits = outer.get("hits") if isinstance(outer, dict) else getattr(outer, "hits", None)
    if not raw_hits:
        return []
    normalized: list[dict[str, object]] = []
    for hit in raw_hits:
        if isinstance(hit, dict):
            normalized.append(hit)
            continue
        normalized.append(
            {
                "_id": getattr(hit, "id", ""),
                "_score": getattr(hit, "score", 0.0),
                "_source": getattr(hit, "source", {}) or {},
            }
        )
    return normalized
