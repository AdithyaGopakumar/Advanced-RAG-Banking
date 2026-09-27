"""Run governance and indexing from the terminal.

The BM25 index is rebuilt in memory on every run. Dense vectors are kept
only when Pinecone is configured. The manifest is saved in that case so the
next run can upsert changed chunks and delete removed ids.
"""

import argparse
import logging
import sys
from datetime import date
from pathlib import Path

from pydantic import BaseModel, ConfigDict, ValidationError

from app.ai.embeddings.factory import create_embedding_provider
from app.ai.embeddings.provider import EmbeddingProvider
from app.ai.rag.indexing.bm25 import BM25Index
from app.ai.rag.indexing.indexer import diff_chunks, index_knowledge
from app.ai.rag.indexing.models import IndexManifest
from app.ai.rag.indexing.vector_store import VectorStore, create_vector_store
from app.core.config import Settings, get_settings
from app.modules.knowledge.governance import build_knowledge

logger = logging.getLogger(__name__)


class IngestionResult(BaseModel):
    """Operator summary of one ingestion run. Chunk text is not included."""

    model_config = ConfigDict(extra="forbid")

    documents: int
    eligible_chunks: int
    rejected: int
    duplicates: int
    contradictions: int
    embedding_provider: str
    embedding_model: str
    dimensions: int
    vector_backend: str
    indexed_records: int
    upserted: int
    deleted: int
    manifest_hash: str
    manifest_path: str | None = None


def run_ingestion(
    *,
    directory: str | Path | None = None,
    as_of: date | None = None,
    settings: Settings | None = None,
    embedder: EmbeddingProvider | None = None,
    vector_store: VectorStore | None = None,
    lexical_index: BM25Index | None = None,
    manifest_path: Path | None = None,
) -> IngestionResult:
    """Validate the knowledge base and index every eligible chunk."""
    current = settings if settings is not None else get_settings()
    embedder = embedder if embedder is not None else create_embedding_provider(current)
    vector_store = vector_store if vector_store is not None else create_vector_store(current)
    lexical_index = lexical_index if lexical_index is not None else BM25Index()
    destination = manifest_path if manifest_path is not None else resolve_manifest_path(current.INDEX_MANIFEST_PATH)

    build = build_knowledge(directory, as_of=as_of)
    eligible = build.eligible_chunks
    previous = _load_previous(destination, embedder, vector_store)
    previous_hashes = previous.hashes_by_id() if previous is not None else {}
    to_upsert, to_delete = diff_chunks(previous_hashes, eligible)
    manifest = index_knowledge(
        eligible,
        embedder,
        vector_store,
        lexical_index,
        embedding_provider=current.EMBEDDING_PROVIDER.strip().lower(),
        previous=previous,
    )
    saved = _save_manifest(destination, manifest)
    return IngestionResult(
        documents=len(build.documents),
        eligible_chunks=len(eligible),
        rejected=len(build.rejected),
        duplicates=len(build.duplicates),
        contradictions=len(build.contradictions),
        embedding_provider=manifest.embedding_provider,
        embedding_model=manifest.embedding_model,
        dimensions=manifest.dimensions,
        vector_backend=manifest.vector_backend,
        indexed_records=len(manifest.records),
        upserted=len(to_upsert),
        deleted=len(to_delete),
        manifest_hash=manifest.manifest_hash,
        manifest_path=str(destination) if saved else None,
    )


def resolve_manifest_path(path: str | Path | None) -> Path:
    """Resolve a manifest path from the Backend directory when it is relative."""
    raw = Path(path) if path else Path(".index/manifest.json")
    if raw.is_absolute():
        return raw
    backend_root = Path(__file__).resolve().parents[2]
    return (backend_root / raw).resolve()


def format_report(result: IngestionResult) -> str:
    """Plain-text summary for the terminal."""
    lines = [
        "Knowledge ingestion",
        f"  documents accepted: {result.documents}",
        f"  eligible chunks: {result.eligible_chunks}",
        f"  rejected: {result.rejected}",
        f"  duplicates: {result.duplicates}",
        f"  contradictions: {result.contradictions}",
        f"  embedding: {result.embedding_provider} / {result.embedding_model} ({result.dimensions})",
        f"  vector backend: {result.vector_backend}",
        f"  indexed records: {result.indexed_records}",
        f"  upserted: {result.upserted}",
        f"  deleted: {result.deleted}",
        f"  manifest hash: {result.manifest_hash}",
    ]
    if result.manifest_path:
        lines.append(f"  manifest saved: {result.manifest_path}")
    else:
        lines.append("  dense vectors were kept in memory for this process only")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """Parse terminal arguments and run ingestion."""
    parser = argparse.ArgumentParser(
        description="Validate the knowledge base and index eligible chunks."
    )
    parser.add_argument(
        "--knowledge-root",
        default=None,
        help="Knowledge directory. Defaults to KNOWLEDGE_ROOT.",
    )
    parser.add_argument(
        "--as-of",
        default=None,
        help="Effective date as YYYY-MM-DD. Defaults to today.",
    )
    args = parser.parse_args(argv)
    try:
        on_date = date.fromisoformat(args.as_of) if args.as_of else None
    except ValueError:
        print("--as-of must be YYYY-MM-DD", file=sys.stderr)
        return 2
    try:
        result = run_ingestion(directory=args.knowledge_root, as_of=on_date)
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(format_report(result))
    return 0


def _load_previous(
    path: Path,
    embedder: EmbeddingProvider,
    vector_store: VectorStore,
) -> IndexManifest | None:
    """Reuse a Pinecone manifest when the model and backend still match."""
    if vector_store.backend_name != "pinecone" or not path.is_file():
        return None
    try:
        manifest = IndexManifest.model_validate_json(path.read_text(encoding="utf-8"))
    except (OSError, ValidationError, ValueError) as exc:
        logger.warning("Ignoring unreadable index manifest at %s: %s", path, exc)
        return None
    dimensions = embedder.dimensions if embedder.dimensions is not None else manifest.dimensions
    if (
        manifest.embedding_model != embedder.model_name
        or manifest.dimensions != dimensions
        or manifest.vector_backend != "pinecone"
    ):
        logger.warning("Ignoring index manifest because the embedding model or backend changed")
        return None
    return manifest


def _save_manifest(path: Path, manifest: IndexManifest) -> bool:
    if manifest.vector_backend != "pinecone":
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")
    temporary.replace(path)
    return True
