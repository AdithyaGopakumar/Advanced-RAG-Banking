"""Reciprocal rank fusion of independently ranked retrieval lists.

Each list contributes ``1 / (k + rank)`` using 1-based ranks. The same chunk
in several lists is one candidate. Its score is the sum of those contributions,
and the stored rank for a source is the best rank that source gave it.
"""

from app.ai.rag.indexing.models import RetrievalHit
from app.ai.rag.retrieval.models import FusedCandidate, RetrievalSource


def fuse_rankings(ranked_lists: list[list[RetrievalHit]], *, rrf_k: int) -> list[FusedCandidate]:
    """Deduplicate chunk ids and rank them by reciprocal rank fusion."""
    if rrf_k < 0:
        raise ValueError("RRF k must be zero or greater")
    scores: dict[str, float] = {}
    dense_ranks: dict[str, int] = {}
    lexical_ranks: dict[str, int] = {}
    chosen: dict[str, RetrievalHit] = {}
    for hits in ranked_lists:
        seen: set[str] = set()
        for position, hit in enumerate(hits, start=1):
            if hit.chunk_id in seen:
                continue
            seen.add(hit.chunk_id)
            scores[hit.chunk_id] = scores.get(hit.chunk_id, 0.0) + 1.0 / (rrf_k + position)
            chosen.setdefault(hit.chunk_id, hit)
            if hit.source == "dense":
                dense_ranks[hit.chunk_id] = min(position, dense_ranks.get(hit.chunk_id, position))
            else:
                lexical_ranks[hit.chunk_id] = min(position, lexical_ranks.get(hit.chunk_id, position))
    candidates = [
        _candidate(
            hit=chosen[chunk_id],
            score=score,
            dense_rank=dense_ranks.get(chunk_id),
            bm25_rank=lexical_ranks.get(chunk_id),
        )
        for chunk_id, score in scores.items()
    ]
    candidates.sort(key=lambda item: (-item.rrf_score, item.chunk_id))
    return candidates


def _candidate(
    *,
    hit: RetrievalHit,
    score: float,
    dense_rank: int | None,
    bm25_rank: int | None,
) -> FusedCandidate:
    sources: list[RetrievalSource] = []
    if dense_rank is not None:
        sources.append("dense")
    if bm25_rank is not None:
        sources.append("bm25")
    return FusedCandidate(
        chunk_id=hit.chunk_id,
        document_id=hit.document_id,
        document_version=hit.metadata.document_version,
        text=hit.text,
        metadata=hit.metadata,
        retrieval_sources=sources,
        dense_rank=dense_rank,
        bm25_rank=bm25_rank,
        rrf_score=score,
    )
