"""Embedding provider contract.

Concrete vendors implement ``embed_texts``. Callers use ``embed_documents``
and ``embed_query`` so a later model can treat those purposes differently
without changing the indexing code.
"""

from abc import ABC, abstractmethod
from collections.abc import Sequence

from app.ai.embeddings.errors import EmbeddingInputError
from app.ai.embeddings.models import Embedding, EmbeddingBatch, EmbeddingPurpose


class EmbeddingProvider(ABC):
    """Vendor-neutral embedding boundary."""

    def __init__(self, model_name: str, dimensions: int | None = None) -> None:
        if not model_name.strip():
            raise EmbeddingInputError("Embedding model name is required")
        if dimensions is not None and dimensions <= 0:
            raise EmbeddingInputError("Embedding dimensions must be positive")
        self.model_name = model_name.strip()
        self.dimensions = dimensions

    def embed_documents(self, texts: Sequence[str]) -> EmbeddingBatch:
        """Embed knowledge text that will be stored in the vector index."""
        return self._embed_batch(texts, "document")

    def embed_query(self, text: str) -> Embedding:
        """Embed a user query for dense retrieval."""
        batch = self._embed_batch([text], "query")
        return batch.embeddings[0]

    @abstractmethod
    def embed_texts(self, texts: Sequence[str], *, purpose: EmbeddingPurpose) -> list[list[float]]:
        """Return one vector per text, in input order."""

    def _embed_batch(self, texts: Sequence[str], purpose: EmbeddingPurpose) -> EmbeddingBatch:
        cleaned = [_require_text(text) for text in texts]
        if not cleaned:
            return EmbeddingBatch(model=self.model_name, purpose=purpose)
        vectors = self.embed_texts(cleaned, purpose=purpose)
        if len(vectors) != len(cleaned):
            raise EmbeddingInputError("Embedding provider returned a different number of vectors than texts")
        embeddings = [
            Embedding(model=self.model_name, purpose=purpose, vector=_check_dimensions(vector, self.dimensions))
            for vector in vectors
        ]
        return EmbeddingBatch(model=self.model_name, purpose=purpose, embeddings=embeddings)


def _require_text(text: str) -> str:
    if not isinstance(text, str) or not text.strip():
        raise EmbeddingInputError("Embedding text must be a non-empty string")
    return text


def _check_dimensions(vector: list[float], dimensions: int | None) -> list[float]:
    if dimensions is not None and len(vector) != dimensions:
        raise EmbeddingInputError(
            f"Embedding provider returned {len(vector)} dimensions, expected {dimensions}"
        )
    return vector
