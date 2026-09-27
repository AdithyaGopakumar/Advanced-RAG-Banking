"""Build the embedding provider named in settings.

The current development adapter is sentence-transformers. A configured model
whose provider is not registered is rejected with the model name intact so a
later benchmark choice can be wired in without changing callers.
"""

from collections.abc import Callable

from app.ai.embeddings.deterministic import DeterministicEmbeddingProvider
from app.ai.embeddings.errors import EmbeddingNotConfiguredError, EmbeddingProviderUnavailableError
from app.ai.embeddings.provider import EmbeddingProvider
from app.core.config import Settings, get_settings

ProviderBuilder = Callable[[str, int | None], EmbeddingProvider]


def _build_deterministic(model_name: str, dimensions: int | None) -> EmbeddingProvider:
    if dimensions is None:
        raise EmbeddingNotConfiguredError(
            "EMBEDDING_DIMENSIONS is required when EMBEDDING_PROVIDER is 'deterministic'"
        )
    return DeterministicEmbeddingProvider(model_name, dimensions)


def _build_sentence_transformers(model_name: str, dimensions: int | None) -> EmbeddingProvider:
    from app.ai.embeddings.sentence_transformer import SentenceTransformerEmbeddingProvider

    return SentenceTransformerEmbeddingProvider(model_name, dimensions)


_PROVIDERS: dict[str, ProviderBuilder] = {
    "deterministic": _build_deterministic,
    "sentence-transformers": _build_sentence_transformers,
}


def register_embedding_provider(name: str, builder: ProviderBuilder) -> None:
    """Register an adapter that can be selected with EMBEDDING_PROVIDER."""
    key = name.strip().lower()
    if not key:
        raise EmbeddingNotConfiguredError("Embedding provider name is required")
    _PROVIDERS[key] = builder


def create_embedding_provider(settings: Settings | None = None) -> EmbeddingProvider:
    """Return the configured provider.

    Raises:
        EmbeddingNotConfiguredError: provider or model name is still unset.
        EmbeddingProviderUnavailableError: the model is configured, but no adapter is registered.
    """
    current = settings if settings is not None else get_settings()
    provider_name = current.EMBEDDING_PROVIDER.strip().lower()
    model_name = current.EMBEDDING_MODEL.strip()
    if not provider_name or not model_name:
        raise EmbeddingNotConfiguredError(
            "Embedding model is not selected. Set EMBEDDING_PROVIDER and EMBEDDING_MODEL "
            "after the benchmark choice."
        )
    builder = _PROVIDERS.get(provider_name)
    if builder is None:
        raise EmbeddingProviderUnavailableError(
            f"Embedding provider '{provider_name}' is not registered. "
            f"Model '{model_name}' is configured and can be added when its adapter is implemented."
        )
    return builder(model_name, current.EMBEDDING_DIMENSIONS)
