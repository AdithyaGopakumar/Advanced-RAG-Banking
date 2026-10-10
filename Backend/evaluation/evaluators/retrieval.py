"""Retrieval evaluation metrics: Recall@K, Precision@K, MRR, nDCG, Hit Rate.

Evaluates the retrieval pipeline independently of generation.
"""

import math
from evaluation.schemas.models import RetrievalMetrics


def hit_rate(retrieved: list[str], required: list[str]) -> float:
    """Return 1.0 if any required chunk appears in retrieved, else 0.0."""
    if not required:
        return 1.0
    return 1.0 if any(r in retrieved for r in required) else 0.0


def recall_at_k(retrieved: list[str], required: list[str], k: int) -> float:
    """Fraction of required chunks found in the top-k retrieved chunks."""
    if not required:
        return 1.0
    top_k = retrieved[:k]
    matched = sum(1 for req in required if req in top_k)
    return matched / len(required)


def precision_at_k(retrieved: list[str], required: list[str], k: int) -> float:
    """Fraction of top-k retrieved chunks that are in the required set."""
    if not retrieved or k <= 0:
        return 0.0
    top_k = retrieved[:k]
    matched = sum(1 for item in top_k if item in required)
    return matched / len(top_k)


def mean_reciprocal_rank(retrieved: list[str], required: list[str]) -> float:
    """Reciprocal rank of the first relevant chunk retrieved."""
    if not required:
        return 1.0
    for rank, chunk_id in enumerate(retrieved, start=1):
        if chunk_id in required:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(retrieved: list[str], required: list[str], k: int) -> float:
    """Normalized Discounted Cumulative Gain at rank k with binary relevance."""
    if not required:
        return 1.0
    top_k = retrieved[:k]
    dcg = 0.0
    for rank, chunk_id in enumerate(top_k, start=1):
        relevance = 1.0 if chunk_id in required else 0.0
        dcg += relevance / math.log2(rank + 1)

    # Ideal DCG: all required items appear in top positions
    ideal_hits = min(len(required), k)
    if ideal_hits == 0:
        return 0.0
    idcg = sum(1.0 / math.log2(rank + 1) for rank in range(1, ideal_hits + 1))
    return dcg / idcg if idcg > 0 else 0.0


def compute_retrieval_metrics(retrieved: list[str], required: list[str]) -> RetrievalMetrics:
    """Compute all standard retrieval metrics for one query result."""
    return RetrievalMetrics(
        hit_rate=hit_rate(retrieved, required),
        recall_at_1=recall_at_k(retrieved, required, 1),
        recall_at_3=recall_at_k(retrieved, required, 3),
        recall_at_5=recall_at_k(retrieved, required, 5),
        recall_at_8=recall_at_k(retrieved, required, 8),
        precision_at_5=precision_at_k(retrieved, required, 5),
        mrr=mean_reciprocal_rank(retrieved, required),
        ndcg_at_5=ndcg_at_k(retrieved, required, 5),
    )
