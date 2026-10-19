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
    keywords: list[str] = field(default_factory=list)


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
    min_fallback_candidates: int = 3,
) -> DetailedRetrieval:
    """Expand one question, search both indexes per query, and return detailed results.

    Applies Strategy 2 (Soft Pre-filtering with Graceful Fallback):
    If domain keywords are extracted, search is executed with keyword pre-filtering.
    If the filtered candidates are fewer than min_fallback_candidates, automatically
    falls back to unfiltered hybrid retrieval to prevent recall collapse.
    """
    question = " ".join(query.split())
    if not question:
        raise RetrievalQueryError("A retrieval query must contain text")
    if top_k <= 0 or candidates_per_query <= 0:
        return DetailedRetrieval(queries=[question], searches=[], all_fused=[], top_candidates=[])

    # Perform Multi Query Expansion (MQE) with keyword extraction
    if hasattr(expander, "expand_detailed"):
        expansion = expander.expand_detailed(question)
        variants = expansion.queries
        extracted_keywords = list(expansion.keywords)
    else:
        variants = expander.expand(question)
        extracted_keywords = []

    # Prepare initial filter with keywords if available and not already provided
    active_filter = metadata_filter
    if extracted_keywords:
        if metadata_filter is not None and metadata_filter.keywords is None:
            active_filter = metadata_filter.model_copy(update={"keywords": extracted_keywords})
        elif metadata_filter is None:
            active_filter = MetadataFilter(keywords=extracted_keywords)

    def _execute_search(filter_to_use: MetadataFilter | None) -> tuple[list[list[RetrievalHit]], list[QuerySearchStep]]:
        ranked_hits: list[list[RetrievalHit]] = []
        search_steps: list[QuerySearchStep] = []
        for variant in variants:
            vector = embedder.embed_query(variant).vector
            dense_hits = vector_store.query(vector, top_k=candidates_per_query, metadata_filter=filter_to_use)
            ranked_hits.append(dense_hits)
            bm25_hits = lexical_index.search(variant, top_k=candidates_per_query, metadata_filter=filter_to_use)
            ranked_hits.append(bm25_hits)
            search_steps.append(QuerySearchStep(query=variant, dense_hits=dense_hits, bm25_hits=bm25_hits))
        return ranked_hits, search_steps

    ranked, searches = _execute_search(active_filter)
    fused = fuse_rankings(ranked, rrf_k=rrf_k)

    # Strategy 2: Graceful fallback if keyword filtering caused a recall drop
    threshold = min(top_k, min_fallback_candidates)
    if active_filter is not metadata_filter and len(fused) < threshold:
        logger.info(
            "Keyword pre-filter returned insufficient candidates; falling back to unfiltered search",
            extra={
                "keyword_candidates": len(fused),
                "extracted_keywords": extracted_keywords,
                "fallback_threshold": threshold,
            },
        )
        ranked, searches = _execute_search(metadata_filter)
        fused = fuse_rankings(ranked, rrf_k=rrf_k)

    logger.info(
        "Fused hybrid retrieval",
        extra={
            "query_variants": len(variants),
            "ranked_lists": len(ranked),
            "fused_candidates": len(fused),
            "returned_candidates": min(top_k, len(fused)),
            "extracted_keywords": len(extracted_keywords),
        },
    )
    return DetailedRetrieval(
        queries=variants,
        searches=searches,
        all_fused=fused,
        top_candidates=fused[:top_k],
        keywords=extracted_keywords,
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

