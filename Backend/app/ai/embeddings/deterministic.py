"""Deterministic stand-in used to exercise the embedding boundary.

The vectors are hashes, not semantic embeddings. This provider exists so
tests and local wiring can run before a benchmark model is selected.
"""

import hashlib
from collections.abc import Sequence

from app.ai.embeddings.models import EmbeddingPurpose
from app.ai.embeddings.provider import EmbeddingProvider


class DeterministicEmbeddingProvider(EmbeddingProvider):
    """Map text to a stable vector of the configured width."""

    def __init__(self, model_name: str, dimensions: int) -> None:
        super().__init__(model_name, dimensions)
        if self.dimensions is None:
            raise ValueError("Deterministic embeddings require EMBEDDING_DIMENSIONS")

    def embed_texts(self, texts: Sequence[str], *, purpose: EmbeddingPurpose) -> list[list[float]]:
        width = self.dimensions or 0
        return [_hash_vector(purpose, self.model_name, text, width) for text in texts]


def _hash_vector(purpose: str, model_name: str, text: str, dimensions: int) -> list[float]:
    seed = hashlib.sha256(f"{purpose}\n{model_name}\n{text}".encode("utf-8")).digest()
    values: list[float] = []
    counter = 0
    while len(values) < dimensions:
        block = hashlib.sha256(seed + counter.to_bytes(4, "big")).digest()
        counter += 1
        for offset in range(0, len(block), 4):
            raw = int.from_bytes(block[offset : offset + 4], "big")
            values.append((raw / 2**32) * 2 - 1)
            if len(values) == dimensions:
                break
    return values
