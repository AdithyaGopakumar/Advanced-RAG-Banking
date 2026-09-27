"""Index records and the manifest used to re-index changed chunks."""

import hashlib
import json
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.ai.rag.indexing.filters import ChunkMetadata


class RetrievalHit(BaseModel):
    """One ranked chunk from a single index."""

    model_config = ConfigDict(extra="forbid")

    chunk_id: str
    document_id: str
    score: float
    source: Literal["dense", "bm25"]
    metadata: ChunkMetadata
    text: str


class IndexedRecord(BaseModel):
    """Hash of a chunk the last index build stored."""

    model_config = ConfigDict(extra="forbid")

    chunk_id: str
    document_id: str
    content_hash: str
    source_path: str


class IndexManifest(BaseModel):
    """Reproducible description of what the indexes contain."""

    model_config = ConfigDict(extra="forbid")

    embedding_provider: str
    embedding_model: str
    dimensions: int
    vector_backend: Literal["memory", "pinecone"]
    records: list[IndexedRecord] = Field(default_factory=list)
    manifest_hash: str

    def hashes_by_id(self) -> dict[str, str]:
        return {record.chunk_id: record.content_hash for record in self.records}


def manifest_hash(
    *,
    embedding_provider: str,
    embedding_model: str,
    dimensions: int,
    vector_backend: str,
    records: list[IndexedRecord],
) -> str:
    payload = {
        "dimensions": dimensions,
        "embedding_model": embedding_model,
        "embedding_provider": embedding_provider,
        "records": [record.model_dump() for record in sorted(records, key=lambda item: item.chunk_id)],
        "vector_backend": vector_backend,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()
