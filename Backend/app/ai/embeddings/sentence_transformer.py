"""Sentence Transformers adapter.

paraphrase-MiniLM-L6-v2 has no query/document task prefixes, so both
purposes use the same encoding. The purpose label is still returned with
the vector for later models that do distinguish them.
"""

from collections.abc import Callable, Sequence

from app.ai.embeddings.errors import EmbeddingProviderUnavailableError
from app.ai.embeddings.models import EmbeddingPurpose
from app.ai.embeddings.provider import EmbeddingProvider

Encoder = Callable[[Sequence[str]], list[list[float]]]


class SentenceTransformerEmbeddingProvider(EmbeddingProvider):
    """Embed text with a local Sentence Transformers model."""

    def __init__(
        self,
        model_name: str,
        dimensions: int | None = None,
        *,
        encoder: Encoder | None = None,
    ) -> None:
        super().__init__(model_name, dimensions)
        self._encoder = encoder
        self._model: object | None = None

    def embed_texts(self, texts: Sequence[str], *, purpose: EmbeddingPurpose) -> list[list[float]]:
        del purpose
        if self._encoder is not None:
            return [list(vector) for vector in self._encoder(texts)]
        model = self._load_model()
        encoded = model.encode(list(texts), normalize_embeddings=True)
        return [list(vector) for vector in encoded]

    def _load_model(self) -> object:
        if self._model is not None:
            return self._model
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise EmbeddingProviderUnavailableError(
                "sentence-transformers is not installed. Install it before embedding with "
                f"model '{self.model_name}'."
            ) from exc
        self._model = SentenceTransformer(self.model_name)
        return self._model
