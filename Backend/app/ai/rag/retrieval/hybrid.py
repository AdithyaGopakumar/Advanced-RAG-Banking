"""Search the dense and lexical indexes and fuse their rankings."""

from dataclasses import dataclass, field
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


@dataclass
class QuerySearchStep:
    """Hits from dense and lexical retrieval for one query variant."""

    query: str
    dense_hits: list[RetrievalHit] = field(default_factory=list)
    bm25_hits: list[RetrievalHit] = field(default_factory=list)


@dataclass
class DetailedRetrieval:
    """Detailed intermediate outputs from hybrid retrieval."""

    queries: list[str]
    searches: list[QuerySearchStep]
    all_fused: list[FusedCandidate]
    top_candidates: list[FusedCandidate]


def retrieve_detailed(
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
) -> DetailedRetrieval:
    """Expand one question, search both indexes per query, and return detailed results."""
    question = " ".join(query.split())
    if not question:
        raise RetrievalQueryError("A retrieval query must contain text")
    if top_k <= 0 or candidates_per_query <= 0:
        return DetailedRetrieval(queries=[question], searches=[], all_fused=[], top_candidates=[])

    # Perform Multi Query Expansion (MQE)
    variants = expander.expand(question)
    
    ranked: list[list[RetrievalHit]] = []
    searches: list[QuerySearchStep] = []

    # Perform dense and lexical search for each query variant
    for variant in variants:
        # Create dense embedding for the variant query
        vector = embedder.embed_query(variant).vector
        # Perform dense search using the vector
        dense_hits = vector_store.query(vector, top_k=candidates_per_query, metadata_filter=metadata_filter)
        ranked.append(dense_hits)
        # Perform lexical search using the variant query
        bm25_hits = lexical_index.search(variant, top_k=candidates_per_query, metadata_filter=metadata_filter)
        ranked.append(bm25_hits)
        # Store the search results
        searches.append(QuerySearchStep(query=variant, dense_hits=dense_hits, bm25_hits=bm25_hits))
    # Fuse the ranked hits using RRF
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
    return DetailedRetrieval(
        queries=variants,
        searches=searches,
        all_fused=fused,
        top_candidates=fused[:top_k],
    )


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
    return retrieve_detailed(
        query,
        embedder=embedder,
        vector_store=vector_store,
        lexical_index=lexical_index,
        expander=expander,
        metadata_filter=metadata_filter,
        top_k=top_k,
        candidates_per_query=candidates_per_query,
        rrf_k=rrf_k,
    ).top_candidates

