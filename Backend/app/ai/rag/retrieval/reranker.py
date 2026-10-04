"""Semantic reranking of fused candidates against the original question.

The development model is a local cross-encoder. It scores the question
together with each chunk and does not write an answer. Replace the model
name after a reranker benchmark if a better one wins.
"""

from collections.abc import Callable, Sequence

from app.core.config import Settings, get_settings

PairScorer = Callable[[str, Sequence[str]], list[float]]


class RerankerNotConfiguredError(Exception):
    """No reranker model is configured."""


class CrossEncoderReranker:
    """Score question-chunk pairs with a sentence-transformers cross-encoder."""

    def __init__(self, model_name: str, *, scorer: PairScorer | None = None) -> None:
        if not model_name.strip():
            raise RerankerNotConfiguredError("Set RERANKER_MODEL before reranking.")
        self.model_name = model_name.strip()
        self._scorer = scorer
        self._model: object | None = None

    def score(self, query: str, texts: Sequence[str]) -> list[float]:
        """Return one relevance score per text, in input order."""
        if not texts:
            return []
        if self._scorer is not None:
            return [float(score) for score in self._scorer(query, texts)]
        model = self._load()
        predicted = model.predict([(query, text) for text in texts])  # type: ignore[attr-defined]
        return [float(score) for score in predicted]

    def _load(self) -> object:
        if self._model is not None:
            return self._model
        try:
            from sentence_transformers import CrossEncoder
        except ImportError as exc:
            raise RerankerNotConfiguredError(
                "sentence-transformers is not installed. Install it before reranking with "
                f"model '{self.model_name}'."
            ) from exc
        self._model = CrossEncoder(self.model_name)
        return self._model


def create_reranker(settings: Settings | None = None) -> CrossEncoderReranker:
    """Build the configured cross-encoder without loading its weights yet."""
    current = settings if settings is not None else get_settings()
    return CrossEncoderReranker(current.RERANKER_MODEL)
