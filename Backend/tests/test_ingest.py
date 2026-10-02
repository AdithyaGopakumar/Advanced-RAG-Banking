"""Tests for the terminal ingestion pipeline."""

from datetime import date
from pathlib import Path

from app.ai.embeddings.deterministic import DeterministicEmbeddingProvider
from app.ai.rag.indexing.lexical import ElasticsearchLexicalIndex
from app.ai.rag.indexing.models import IndexManifest
from app.ai.rag.indexing.vector_store import InMemoryVectorStore
from app.core.config import Settings
from app.ingestion.pipeline import format_report, main, run_ingestion


def _article(document_id: str, body: str, *, status: str = "approved") -> str:
    return (
        "---\n"
        f'id: "{document_id}"\n'
        'title: "Savings"\n'
        'slug: "savings"\n'
        "document_type: product\n"
        'sub_category: "savings-account"\n'
        'version: "1.0"\n'
        f'status: "{status}"\n'
        'owner: "Retail Banking SME"\n'
        "---\n\n"
        f"{body}"
    )


class _CountingEmbedder(DeterministicEmbeddingProvider):
    def __init__(self) -> None:
        super().__init__("paraphrase-MiniLM-L6-v2", 4)
        self.calls: list[list[str]] = []

    def embed_texts(self, texts, *, purpose):
        self.calls.append(list(texts))
        return super().embed_texts(texts, purpose=purpose)


class _Indices:
    def exists(self, *, index: str) -> bool:
        return True

    def create(self, *, index: str, settings: dict[str, object], mappings: dict[str, object]) -> None:
        return None


class _Elasticsearch:
    indices = _Indices()

    def bulk(self, *, operations: list[dict[str, object]], refresh: bool) -> None:
        return None

    def delete_by_query(self, *, index: str, query: dict[str, object], refresh: bool) -> None:
        return None


def _lexical() -> ElasticsearchLexicalIndex:
    return ElasticsearchLexicalIndex(_Elasticsearch(), index_name="knowledge-chunks")


class _PersistedStore(InMemoryVectorStore):
    backend_name = "pinecone"


def _settings() -> Settings:
    return Settings(
        EMBEDDING_PROVIDER="deterministic",
        EMBEDDING_MODEL="paraphrase-MiniLM-L6-v2",
        EMBEDDING_DIMENSIONS=4,
        PINECONE_API_KEY="",
        PINECONE_INDEX_NAME="",
    )


def test_ingestion_indexes_eligible_chunks_and_leaves_memory_unsaved(tmp_path: Path):
    (tmp_path / "savings.md").write_text(
        _article("ACCT-X-001", "# Savings\n\n## Overview\n\nResident individuals.\n"),
        encoding="utf-8",
    )
    (tmp_path / "draft.md").write_text(
        _article("CARD-X-001", "# Card\n\n## Overview\n\nDraft limit.\n", status="draft"),
        encoding="utf-8",
    )
    embedder = _CountingEmbedder()
    manifest_path = tmp_path / "manifest.json"

    result = run_ingestion(
        directory=tmp_path,
        as_of=date(2026, 9, 27),
        settings=_settings(),
        embedder=embedder,
        vector_store=InMemoryVectorStore(),
        lexical_index=_lexical(),
        manifest_path=manifest_path,
    )

    assert result.documents == 2
    assert result.eligible_chunks == 1
    assert result.indexed_records == 1
    assert result.upserted == 1
    assert result.vector_backend == "memory"
    assert result.manifest_path is None
    assert manifest_path.exists() is False
    assert len(embedder.calls) == 1
    assert "Resident individuals." in embedder.calls[0][0]
    assert "Draft" not in embedder.calls[0][0]
    assert "in memory" in format_report(result)


def test_pinecone_rerun_skips_unchanged_chunks_and_saves_the_manifest(tmp_path: Path):
    source = tmp_path / "savings.md"
    source.write_text(
        _article("ACCT-X-001", "# Savings\n\n## Overview\n\nResident individuals.\n"),
        encoding="utf-8",
    )
    embedder = _CountingEmbedder()
    store = _PersistedStore()
    manifest_path = tmp_path / "index" / "manifest.json"
    first = run_ingestion(
        directory=tmp_path,
        as_of=date(2026, 9, 27),
        settings=_settings(),
        embedder=embedder,
        vector_store=store,
        lexical_index=_lexical(),
        manifest_path=manifest_path,
    )
    second = run_ingestion(
        directory=tmp_path,
        as_of=date(2026, 9, 27),
        settings=_settings(),
        embedder=embedder,
        vector_store=store,
        lexical_index=_lexical(),
        manifest_path=manifest_path,
    )

    assert first.manifest_path == str(manifest_path)
    assert IndexManifest.model_validate_json(manifest_path.read_text(encoding="utf-8")).manifest_hash == first.manifest_hash
    assert second.upserted == 0
    assert second.deleted == 0
    assert len(embedder.calls) == 1


def test_changed_embedding_model_does_not_reuse_the_manifest(tmp_path: Path):
    (tmp_path / "savings.md").write_text(
        _article("ACCT-X-001", "# Savings\n\n## Overview\n\nResident individuals.\n"),
        encoding="utf-8",
    )
    manifest_path = tmp_path / "manifest.json"
    run_ingestion(
        directory=tmp_path,
        as_of=date(2026, 9, 27),
        settings=_settings(),
        embedder=_CountingEmbedder(),
        vector_store=_PersistedStore(),
        lexical_index=_lexical(),
        manifest_path=manifest_path,
    )
    stored = IndexManifest.model_validate_json(manifest_path.read_text(encoding="utf-8"))
    manifest_path.write_text(
        stored.model_copy(update={"embedding_model": "other-model"}).model_dump_json(),
        encoding="utf-8",
    )
    embedder = _CountingEmbedder()

    result = run_ingestion(
        directory=tmp_path,
        as_of=date(2026, 9, 27),
        settings=_settings(),
        embedder=embedder,
        vector_store=_PersistedStore(),
        lexical_index=_lexical(),
        manifest_path=manifest_path,
    )

    assert result.upserted == 1
    assert embedder.calls


def test_cli_reports_a_missing_knowledge_directory(tmp_path: Path, capsys):
    missing = tmp_path / "missing"

    code = main(["--knowledge-root", str(missing)])
    captured = capsys.readouterr()

    assert code == 2
    assert "does not exist" in captured.err


def test_cli_rejects_an_invalid_date(capsys):
    code = main(["--as-of", "27-09-2026"])

    assert code == 2
    assert "YYYY-MM-DD" in capsys.readouterr().err
