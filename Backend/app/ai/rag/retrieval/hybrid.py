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
    """Expand one question, search dense and lexical indexes per query, and return fused results.

    Retrieval Pipeline Execution:
    1. Multi-Query Expansion (MQE) + Domain Keyword Extraction:
       Generates diverse semantic reformulations of the question while identifying
       key banking entities, products, and acronyms for targeted pre-filtering.
    2. Dual-Path Retrieval (Dense + BM25):
       For each query variant, retrieves top-k candidates from:
       - Dense Vector Store (Pinecone semantic cosine similarity)
       - Sparse Lexical Index (Elasticsearch native BM25 for precise token matching)
    3. Strategy 2 Soft Pre-Filtering with Graceful Fallback:
       - Tries initial retrieval with an active keyword filter ($in membership).
       - If the resulting candidate count falls below `min_fallback_candidates`,
         automatically triggers a fallback to unfiltered hybrid search (retaining
         authoritative status and date constraints) to eliminate false-negative recall collapse.
    4. Reciprocal Rank Fusion (RRF):
       Combines non-comparable score distributions across dense and lexical result sets
       using rank positions: RRF_score = sum(1 / (rrf_k + rank)).

    Args:
        query: The normalized or contextually resolved user banking question.
        embedder: Embedding provider used to generate dense query vectors.
        vector_store: Target vector store (Pinecone or InMemoryVectorStore).
        lexical_index: Target lexical index (Elasticsearch BM25).
        expander: Query expansion provider (LLMQueryExpander or OriginalQueryExpander).
        metadata_filter: Governed constraints (status, effective dates, product).
        top_k: Maximum number of fused candidate chunks to return.
        candidates_per_query: Candidate pool size retrieved per search engine per variant.
        rrf_k: Constant smoothing factor for Reciprocal Rank Fusion (default 60).
        min_fallback_candidates: Minimum candidate count required before triggering
            unfiltered search fallback to prevent zero-result recall drops.

    Returns:
        DetailedRetrieval containing query variants, extracted keywords, individual
        search steps, all fused candidates, and the top-k final candidates.
    """
    # ── Step 1: Input Validation & Normalization ──
    question = " ".join(query.split())
    if not question:
        raise RetrievalQueryError("A retrieval query must contain text")
    if top_k <= 0 or candidates_per_query <= 0:
        return DetailedRetrieval(queries=[question], searches=[], all_fused=[], top_candidates=[])

    # ── Step 2: Multi-Query Expansion (MQE) & Keyword Extraction ──
    # Single LLM call extracts both alternative search queries and domain keywords
    if hasattr(expander, "expand_detailed"):
        expansion = expander.expand_detailed(question)
        variants = expansion.queries
        extracted_keywords = list(expansion.keywords)
    else:
        variants = expander.expand(question)
        extracted_keywords = []

    # ── Step 3: Pre-Filter Construction ──
    # Attach extracted keywords to active filter if not explicitly constrained by caller
    active_filter = metadata_filter
    if extracted_keywords:
        expanded_keywords: set[str] = set()
        for kw in extracted_keywords:
            cleaned = kw.strip()
            if cleaned:
                expanded_keywords.add(cleaned)
                expanded_keywords.add(cleaned.lower())
                expanded_keywords.add(cleaned.title())
        kw_list = sorted(expanded_keywords)
        if metadata_filter is not None and metadata_filter.keywords is None:
            active_filter = metadata_filter.model_copy(update={"keywords": kw_list})
        elif metadata_filter is None:
            active_filter = MetadataFilter(keywords=kw_list)

    # Helper closure to execute dual-path search across all query variants
    def _execute_search(filter_to_use: MetadataFilter | None) -> tuple[list[list[RetrievalHit]], list[QuerySearchStep]]:
        ranked_hits: list[list[RetrievalHit]] = []
        search_steps: list[QuerySearchStep] = []
        for variant in variants:
            # Dense Vector Search (semantic similarity)
            vector = embedder.embed_query(variant).vector
            dense_hits = vector_store.query(vector, top_k=candidates_per_query, metadata_filter=filter_to_use)
            ranked_hits.append(dense_hits)

            # Sparse Lexical Search (BM25 exact token matching)
            bm25_hits = lexical_index.search(variant, top_k=candidates_per_query, metadata_filter=filter_to_use)
            ranked_hits.append(bm25_hits)

            search_steps.append(QuerySearchStep(query=variant, dense_hits=dense_hits, bm25_hits=bm25_hits))
        return ranked_hits, search_steps

    # ── Step 4: Primary Retrieval Execution & Score Fusion ──
    ranked, searches = _execute_search(active_filter)
    fused = fuse_rankings(ranked, rrf_k=rrf_k)

    # ── Step 5: Strategy 2 Recall Protection (Graceful Fallback) ──
    # If keyword filtering was applied but yielded insufficient candidates,
    # re-execute retrieval without the keyword filter while keeping authoritative
    # governance constraints (e.g. approved statuses and temporal dates) intact.
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

    # ── Step 6: Log Telemetry & Package Results ──
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

