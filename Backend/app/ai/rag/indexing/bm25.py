"""In-memory BM25 index over eligible knowledge chunks.

The index is rebuilt from the full eligible set on each index run because
BM25 scores depend on corpus-wide term statistics.
"""

import math
import re
from collections import Counter

from app.ai.rag.indexing.filters import ChunkMetadata, MetadataFilter, matches_filter
from app.ai.rag.indexing.models import RetrievalHit

_TOKEN = re.compile(r"[a-z0-9]+")


class BM25Index:
    """Lexical index using BM25 Okapi."""

    def __init__(self, *, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self._documents: list[_Document] = []
        self._avg_length = 0.0
        self._doc_freq: Counter[str] = Counter()

    def replace(self, documents: list[tuple[str, ChunkMetadata]]) -> None:
        """Replace the index with the current eligible chunks."""
        stored = [
            _Document(text=text, metadata=metadata, terms=tokenize(text))
            for text, metadata in documents
        ]
        frequencies: Counter[str] = Counter()
        for document in stored:
            frequencies.update(set(document.terms))
        total_length = sum(len(document.terms) for document in stored)
        self._documents = stored
        self._doc_freq = frequencies
        self._avg_length = total_length / len(stored) if stored else 0.0

    def search(self, query: str, *, top_k: int, metadata_filter: MetadataFilter | None = None) -> list[RetrievalHit]:
        """Rank chunks whose metadata matches, then return the top scores."""
        if top_k <= 0 or not self._documents:
            return []
        query_terms = tokenize(query)
        if not query_terms:
            return []
        constraint = metadata_filter or MetadataFilter()
        scored: list[RetrievalHit] = []
        for document in self._documents:
            if not matches_filter(document.metadata, constraint):
                continue
            score = self._score(document.terms, query_terms)
            if score <= 0:
                continue
            scored.append(
                RetrievalHit(
                    chunk_id=document.metadata.chunk_id,
                    document_id=document.metadata.document_id,
                    score=score,
                    source="bm25",
                    metadata=document.metadata,
                    text=document.text,
                )
            )
        scored.sort(key=lambda hit: (-hit.score, hit.chunk_id))
        return scored[:top_k]

    def _score(self, terms: list[str], query_terms: list[str]) -> float:
        if not terms or self._avg_length == 0:
            return 0.0
        counts = Counter(terms)
        score = 0.0
        for term in query_terms:
            frequency = counts.get(term, 0)
            if frequency == 0:
                continue
            doc_freq = self._doc_freq.get(term, 0)
            idf = math.log(1 + (len(self._documents) - doc_freq + 0.5) / (doc_freq + 0.5))
            denominator = frequency + self.k1 * (1 - self.b + self.b * len(terms) / self._avg_length)
            score += idf * (frequency * (self.k1 + 1)) / denominator
        return score


class _Document:
    def __init__(self, *, text: str, metadata: ChunkMetadata, terms: list[str]) -> None:
        self.text = text
        self.metadata = metadata
        self.terms = terms


def tokenize(text: str) -> list[str]:
    """Lowercase tokens that keep product names and numbers intact."""
    return _TOKEN.findall(text.lower())
