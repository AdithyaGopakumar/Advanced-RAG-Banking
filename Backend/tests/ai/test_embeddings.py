"""Tests for the configurable embedding boundary."""

import pytest

from app.ai.embeddings.errors import (
    EmbeddingInputError,
    EmbeddingNotConfiguredError,
    EmbeddingProviderUnavailableError,
)
from app.ai.embeddings.factory import create_embedding_provider
from app.core.config import Settings


def _settings(**overrides: object) -> Settings:
    values: dict[str, object] = {
        "EMBEDDING_PROVIDER": "",
        "EMBEDDING_MODEL": "",
        "EMBEDDING_DIMENSIONS": None,
    }
    values.update(overrides)
    return Settings(**values)


def test_unset_embedding_model_is_not_configured():
    with pytest.raises(EmbeddingNotConfiguredError):
        create_embedding_provider(_settings())


def test_configured_model_without_an_adapter_is_left_for_later():
    settings = _settings(EMBEDDING_PROVIDER="openai", EMBEDDING_MODEL="text-embedding-3-small")

    with pytest.raises(EmbeddingProviderUnavailableError) as raised:
        create_embedding_provider(settings)

    message = str(raised.value)
    assert "text-embedding-3-small" in message
    assert "not registered" in message


def test_deterministic_provider_is_stable_and_purpose_aware():
    provider = create_embedding_provider(
        _settings(
            EMBEDDING_PROVIDER="deterministic",
            EMBEDDING_MODEL="benchmark-pending",
            EMBEDDING_DIMENSIONS=8,
        )
    )

    documents = provider.embed_documents(["BSBDA eligibility", "BSBDA eligibility"])
    query = provider.embed_query("BSBDA eligibility")

    assert provider.model_name == "benchmark-pending"
    assert documents.model == "benchmark-pending"
    assert documents.embeddings[0].vector == documents.embeddings[1].vector
    assert len(documents.embeddings[0].vector) == 8
    assert query.purpose == "query"
    assert query.vector != documents.embeddings[0].vector


def test_different_texts_get_different_vectors():
    provider = create_embedding_provider(
        _settings(
            EMBEDDING_PROVIDER="deterministic",
            EMBEDDING_MODEL="benchmark-pending",
            EMBEDDING_DIMENSIONS=4,
        )
    )

    batch = provider.embed_documents(["savings account", "home loan"])

    assert batch.vectors[0] != batch.vectors[1]


def test_empty_text_is_rejected():
    provider = create_embedding_provider(
        _settings(
            EMBEDDING_PROVIDER="deterministic",
            EMBEDDING_MODEL="benchmark-pending",
            EMBEDDING_DIMENSIONS=4,
        )
    )

    with pytest.raises(EmbeddingInputError):
        provider.embed_query("   ")


def test_sentence_transformer_is_the_configured_development_model():
    from app.ai.embeddings.sentence_transformer import SentenceTransformerEmbeddingProvider

    provider = create_embedding_provider(
        _settings(
            EMBEDDING_PROVIDER="sentence-transformers",
            EMBEDDING_MODEL="paraphrase-MiniLM-L6-v2",
            EMBEDDING_DIMENSIONS=384,
        )
    )

    assert isinstance(provider, SentenceTransformerEmbeddingProvider)
    assert provider.model_name == "paraphrase-MiniLM-L6-v2"
    assert provider.dimensions == 384
    assert Settings.model_fields["EMBEDDING_MODEL"].default == "paraphrase-MiniLM-L6-v2"
    assert Settings.model_fields["EMBEDDING_DIMENSIONS"].default == 384


def test_sentence_transformer_uses_the_supplied_encoder():
    from app.ai.embeddings.sentence_transformer import SentenceTransformerEmbeddingProvider

    seen: list[list[str]] = []

    def encode(texts: list[str]) -> list[list[float]]:
        seen.append(list(texts))
        return [[1.0, 0.0, 0.0, 0.0] for _ in texts]

    provider = SentenceTransformerEmbeddingProvider("paraphrase-MiniLM-L6-v2", 4, encoder=encode)

    document = provider.embed_documents(["BSBDA eligibility"])
    query = provider.embed_query("who can open a BSBDA")

    assert seen == [["BSBDA eligibility"], ["who can open a BSBDA"]]
    assert document.purpose == "document"
    assert query.purpose == "query"
    assert query.vector == [1.0, 0.0, 0.0, 0.0]


def test_missing_sentence_transformers_package_is_reported(monkeypatch: pytest.MonkeyPatch):
    import sys

    from app.ai.embeddings.sentence_transformer import SentenceTransformerEmbeddingProvider

    monkeypatch.setitem(sys.modules, "sentence_transformers", None)
    provider = SentenceTransformerEmbeddingProvider("paraphrase-MiniLM-L6-v2", 384)

    with pytest.raises(EmbeddingProviderUnavailableError, match="not installed"):
        provider.embed_query("BSBDA eligibility")


def test_empty_batch_returns_no_vectors():
    provider = create_embedding_provider(
        _settings(
            EMBEDDING_PROVIDER="deterministic",
            EMBEDDING_MODEL="benchmark-pending",
            EMBEDDING_DIMENSIONS=4,
        )
    )

    assert provider.embed_documents([]).embeddings == []
