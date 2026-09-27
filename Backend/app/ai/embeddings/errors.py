"""Embedding configuration and input errors."""


class EmbeddingError(Exception):
    """Base error for embedding operations."""


class EmbeddingNotConfiguredError(EmbeddingError):
    """No embedding provider and model have been selected yet."""


class EmbeddingProviderUnavailableError(EmbeddingError):
    """The configured provider does not have an adapter yet."""


class EmbeddingInputError(EmbeddingError):
    """A text submitted for embedding is empty."""
