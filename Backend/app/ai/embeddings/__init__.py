"""Embedding provider boundary."""

from app.ai.embeddings.errors import (
    EmbeddingError,
    EmbeddingInputError,
    EmbeddingNotConfiguredError,
    EmbeddingProviderUnavailableError,
)
from app.ai.embeddings.factory import create_embedding_provider, register_embedding_provider
from app.ai.embeddings.models import Embedding, EmbeddingBatch
from app.ai.embeddings.provider import EmbeddingProvider

__all__ = [
    "Embedding",
    "EmbeddingBatch",
    "EmbeddingError",
    "EmbeddingInputError",
    "EmbeddingNotConfiguredError",
    "EmbeddingProvider",
    "EmbeddingProviderUnavailableError",
    "create_embedding_provider",
    "register_embedding_provider",
]
