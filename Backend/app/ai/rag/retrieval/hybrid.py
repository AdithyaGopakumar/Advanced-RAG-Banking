"""Search the dense and lexical indexes and fuse their rankings."""

import logging
from typing import Protocol

from app.ai.embeddings.provider import EmbeddingProvider
from app.ai.rag.indexing.filters import MetadataFilter
from app.ai.rag.indexing.models import RetrievalHit
from app.ai.rag.indexing.vector_store import VectorStore
from app.ai.rag.retrieval.models import FusedCandidate
from app.ai.rag.retrieval.mqe import QueryExpander
from app.ai.rag.retrieval.rrf import fuse_rankings

logger = logging.getLogger(__name__)


class RetrievalQueryError(ValueError):
    """The question has no text to search."""


class LexicalSearcher(Protocol):
    """BM25 search over the lexical index."""

    def search(
        self,
        query: str,
        *,
        top_k: int,
        metadata_filter: MetadataFilter | None = None,
    ) -> list[RetrievalHit]:
        """Return the top lexical hits."""


def retrieve(
    query: str,
    *,
    embedder: EmbeddingProvider,
    vector_store: VectorStore,
    lexical_index: LexicalSearcher,
    expander: QueryExpander,
    metadata_filter: MetadataFilter | None = None,
    top_k: int = 8,
    candidates_per_query: int = 20,
    rrf_k: int = 60,
) -> list[FusedCandidate]:
    """Expand one question, search both indexes, and return the fused top chunks."""
    question = " ".join(query.split())
    if not question:
        raise RetrievalQueryError("A retrieval query must contain text")
    if top_k <= 0 or candidates_per_query <= 0:
        return []
    variants = expander.expand(question)
    ranked: list[list[RetrievalHit]] = []
    for variant in variants:
        vector = embedder.embed_query(variant).vector
        ranked.append(vector_store.query(vector, top_k=candidates_per_query, metadata_filter=metadata_filter))
        ranked.append(lexical_index.search(variant, top_k=candidates_per_query, metadata_filter=metadata_filter))
    fused = fuse_rankings(ranked, rrf_k=rrf_k)
    logger.info(
        "Fused hybrid retrieval",
        extra={
            "query_variants": len(variants),
            "ranked_lists": len(ranked),
            "fused_candidates": len(fused),
            "returned_candidates": min(top_k, len(fused)),
        },
    )
    return fused[:top_k]
