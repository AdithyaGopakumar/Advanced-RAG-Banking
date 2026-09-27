"""Vector stores for dense indexing.

The in-memory store is the default when Pinecone is not configured. The
Pinecone adapter is used only when an API key and index name are set.
"""

import logging
import math
from collections.abc import Sequence
from typing import Protocol

from app.ai.rag.indexing.filters import (
    ChunkMetadata,
    MetadataFilter,
    matches_filter,
    to_pinecone_filter,
)
from app.ai.rag.indexing.models import RetrievalHit

logger = logging.getLogger(__name__)


class _PineconeIndex(Protocol):
    """The small part of a Pinecone index this adapter calls."""

    def upsert(self, *, vectors: list[dict[str, object]], namespace: str) -> object:
        """Insert or replace vectors."""

    def delete(self, *, ids: list[str], namespace: str) -> object:
        """Delete vectors by id."""

    def query(self, **kwargs: object) -> object:
        """Return nearest matches."""


class VectorRecord:
    """A chunk vector ready to upsert."""

    def __init__(self, *, chunk_id: str, vector: list[float], metadata: ChunkMetadata, text: str) -> None:
        self.chunk_id = chunk_id
        self.vector = vector
        self.metadata = metadata
        self.text = text


class VectorStore(Protocol):
    """Dense index used by the indexing pipeline."""

    backend_name: str

    def upsert(self, records: Sequence[VectorRecord]) -> None:
        """Insert or replace vectors by chunk id."""

    def delete(self, chunk_ids: Sequence[str]) -> None:
        """Remove vectors that are no longer eligible."""

    def query(
        self,
        vector: list[float],
        *,
        top_k: int,
        metadata_filter: MetadataFilter | None = None,
    ) -> list[RetrievalHit]:
        """Return the nearest chunks that satisfy the metadata filter."""


class InMemoryVectorStore:
    """Cosine-similarity index for tests and local runs without Pinecone."""

    backend_name = "memory"

    def __init__(self) -> None:
        self._records: dict[str, VectorRecord] = {}

    def upsert(self, records: Sequence[VectorRecord]) -> None:
        for record in records:
            self._records[record.chunk_id] = record

    def delete(self, chunk_ids: Sequence[str]) -> None:
        for chunk_id in chunk_ids:
            self._records.pop(chunk_id, None)

    def query(
        self,
        vector: list[float],
        *,
        top_k: int,
        metadata_filter: MetadataFilter | None = None,
    ) -> list[RetrievalHit]:
        if top_k <= 0:
            return []
        constraint = metadata_filter or MetadataFilter()
        scored: list[RetrievalHit] = []
        for record in self._records.values():
            if not matches_filter(record.metadata, constraint):
                continue
            score = _cosine(vector, record.vector)
            scored.append(
                RetrievalHit(
                    chunk_id=record.chunk_id,
                    document_id=record.metadata.document_id,
                    score=score,
                    source="dense",
                    metadata=record.metadata,
                    text=record.text,
                )
            )
        scored.sort(key=lambda hit: (-hit.score, hit.chunk_id))
        return scored[:top_k]


class PineconeVectorStore:
    """Pinecone adapter. The client object is injected so tests do not call Pinecone."""

    backend_name = "pinecone"

    def __init__(self, index: _PineconeIndex, *, namespace: str) -> None:
        self._index = index
        self.namespace = namespace

    def upsert(self, records: Sequence[VectorRecord]) -> None:
        if not records:
            return
        vectors = [
            {
                "id": record.chunk_id,
                "values": record.vector,
                "metadata": {**record.metadata.as_filter_dict(), "text": record.text},
            }
            for record in records
        ]
        for start in range(0, len(vectors), 100):
            self._index.upsert(vectors=vectors[start : start + 100], namespace=self.namespace)

    def delete(self, chunk_ids: Sequence[str]) -> None:
        ids = list(chunk_ids)
        if not ids:
            return
        self._index.delete(ids=ids, namespace=self.namespace)

    def query(
        self,
        vector: list[float],
        *,
        top_k: int,
        metadata_filter: MetadataFilter | None = None,
    ) -> list[RetrievalHit]:
        if top_k <= 0:
            return []
        constraint = metadata_filter or MetadataFilter()
        response = self._index.query(
            vector=vector,
            top_k=top_k,
            namespace=self.namespace,
            filter=to_pinecone_filter(constraint),
            include_metadata=True,
        )
        hits: list[RetrievalHit] = []
        for match in _matches(response):
            raw = dict(match.get("metadata") or {})
            text = str(raw.pop("text", ""))
            metadata = _metadata_from_payload(raw, chunk_id=str(match["id"]))
            if not matches_filter(metadata, constraint):
                continue
            hits.append(
                RetrievalHit(
                    chunk_id=metadata.chunk_id,
                    document_id=metadata.document_id,
                    score=float(match.get("score") or 0.0),
                    source="dense",
                    metadata=metadata,
                    text=text,
                )
            )
        return hits


def create_vector_store(settings: object | None = None) -> VectorStore:
    """Use Pinecone when credentials exist, otherwise an in-memory index."""
    if settings is None:
        from app.core.config import get_settings

        settings = get_settings()
    api_key = str(getattr(settings, "PINECONE_API_KEY", "") or "").strip()
    index_name = str(getattr(settings, "PINECONE_INDEX_NAME", "") or "").strip()
    namespace = str(getattr(settings, "PINECONE_NAMESPACE", "") or "knowledge").strip() or "knowledge"
    if not api_key or not index_name:
        logger.info("Pinecone is not configured; using the in-memory vector index")
        return InMemoryVectorStore()
    try:
        from pinecone import Pinecone
    except ImportError as exc:
        raise RuntimeError("pinecone is not installed") from exc
    client = Pinecone(api_key=api_key)
    return PineconeVectorStore(client.Index(index_name), namespace=namespace)


def _cosine(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right) or not left:
        return 0.0
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)


def _matches(response: object) -> list[dict[str, object]]:
    matches = response.get("matches") if isinstance(response, dict) else getattr(response, "matches", None)
    if not matches:
        return []
    normalized: list[dict[str, object]] = []
    for match in matches:
        if isinstance(match, dict):
            normalized.append(match)
            continue
        normalized.append(
            {
                "id": getattr(match, "id", ""),
                "score": getattr(match, "score", 0.0),
                "metadata": getattr(match, "metadata", {}) or {},
            }
        )
    return normalized


def _metadata_from_payload(payload: dict[str, object], *, chunk_id: str) -> ChunkMetadata:
    heading = payload.get("heading_path") or []
    heading_path = [str(item) for item in heading] if isinstance(heading, list) else []
    return ChunkMetadata(
        chunk_id=str(payload.get("chunk_id") or chunk_id),
        document_id=str(payload.get("document_id") or ""),
        document_version=str(payload.get("document_version") or ""),
        document_type=str(payload.get("document_type") or ""),
        document_title=str(payload.get("document_title") or ""),
        status=str(payload.get("status") or ""),
        product=_optional(payload.get("product")),
        jurisdiction=_optional(payload.get("jurisdiction")),
        audience=_optional(payload.get("audience")),
        effective_from=_optional(payload.get("effective_from")),
        effective_until=_optional(payload.get("effective_until")),
        source_path=str(payload.get("source_path") or ""),
        content_hash=str(payload.get("content_hash") or ""),
        heading_path=heading_path,
        embedding_model=str(payload.get("embedding_model") or ""),
    )


def _optional(value: object) -> str | None:
    if value is None or value == "":
        return None
    return str(value)
