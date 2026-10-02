"""Fused retrieval candidates."""

from typing import Literal

from pydantic import BaseModel, ConfigDict

from app.ai.rag.indexing.filters import ChunkMetadata

RetrievalSource = Literal["dense", "bm25"]


class FusedCandidate(BaseModel):
    """One chunk after dense and lexical lists are fused."""

    model_config = ConfigDict(extra="forbid")

    chunk_id: str
    document_id: str
    document_version: str
    text: str
    metadata: ChunkMetadata
    retrieval_sources: list[RetrievalSource]
    dense_rank: int | None = None
    bm25_rank: int | None = None
    rrf_score: float
