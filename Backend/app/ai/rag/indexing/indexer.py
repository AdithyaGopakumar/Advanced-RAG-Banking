"""Build dense and lexical indexes from eligible knowledge chunks.

Vector records are upserted only when the chunk hash changed. Removed chunk
ids are deleted from the vector index. Eligible chunk text is sent to
Elasticsearch, which keeps the BM25 index.
"""

import logging
from collections.abc import Sequence
from typing import Literal

from app.ai.embeddings.provider import EmbeddingProvider
from app.ai.rag.indexing.filters import ChunkMetadata
from app.ai.rag.indexing.lexical import ElasticsearchLexicalIndex
from app.ai.rag.indexing.models import IndexManifest, IndexedRecord, manifest_hash
from app.ai.rag.indexing.vector_store import VectorRecord, VectorStore
from app.modules.knowledge.models import KnowledgeChunk

logger = logging.getLogger(__name__)


def index_knowledge(
    chunks: Sequence[KnowledgeChunk],
    embedder: EmbeddingProvider,
    vector_store: VectorStore,
    lexical_index: ElasticsearchLexicalIndex,
    *,
    embedding_provider: str,
    previous: IndexManifest | None = None,
) -> IndexManifest:
    """Index eligible chunks and return the manifest for the next re-index."""
    eligible = [chunk for chunk in chunks if chunk.eligible and chunk.content_hash]
    previous_hashes = previous.hashes_by_id() if previous is not None else {}
    to_upsert, to_delete = diff_chunks(previous_hashes, eligible)
    if to_upsert:
        embedded = embedder.embed_documents([chunk.text for chunk in to_upsert])
        records = [
            VectorRecord(
                chunk_id=chunk.chunk_id,
                vector=vector,
                metadata=_metadata(chunk, embedder.model_name),
                text=chunk.text,
            )
            for chunk, vector in zip(to_upsert, embedded.vectors)
        ]
        vector_store.upsert(records)
    vector_store.delete(to_delete)
    lexical_index.sync([(chunk.text, _metadata(chunk, embedder.model_name)) for chunk in eligible])
    logger.info(
        "Indexed knowledge chunks",
        extra={
            "eligible_chunks": len(eligible),
            "upserted_chunks": len(to_upsert),
            "deleted_chunks": len(to_delete),
            "embedding_model": embedder.model_name,
            "vector_backend": vector_store.backend_name,
        },
    )
    records = [
        IndexedRecord(
            chunk_id=chunk.chunk_id,
            document_id=chunk.document_id,
            content_hash=chunk.content_hash or "",
            source_path=chunk.source_path,
        )
        for chunk in sorted(eligible, key=lambda chunk: chunk.chunk_id)
    ]
    dimensions = embedder.dimensions if embedder.dimensions is not None else 0
    backend = _backend_name(vector_store.backend_name)
    return IndexManifest(
        embedding_provider=embedding_provider,
        embedding_model=embedder.model_name,
        dimensions=dimensions,
        vector_backend=backend,
        records=records,
        manifest_hash=manifest_hash(
            embedding_provider=embedding_provider,
            embedding_model=embedder.model_name,
            dimensions=dimensions,
            vector_backend=backend,
            records=records,
        ),
    )


def diff_chunks(
    previous_hashes: dict[str, str],
    eligible: Sequence[KnowledgeChunk],
) -> tuple[list[KnowledgeChunk], list[str]]:
    """Return chunks to upsert and chunk ids to delete.

    A chunk is upserted when it is new or its content hash changed. Ids that
    disappeared from the eligible set are deleted. Unchanged hashes are left
    in place.
    """
    current = {chunk.chunk_id: chunk for chunk in eligible}
    to_upsert = [
        chunk
        for chunk_id, chunk in sorted(current.items())
        if previous_hashes.get(chunk_id) != chunk.content_hash
    ]
    to_delete = sorted(chunk_id for chunk_id in previous_hashes if chunk_id not in current)
    return to_upsert, to_delete


def _backend_name(name: str) -> Literal["memory", "pinecone"]:
    if name == "memory":
        return "memory"
    if name == "pinecone":
        return "pinecone"
    raise ValueError(f"Unsupported vector backend '{name}'")


def _metadata(chunk: KnowledgeChunk, embedding_model: str) -> ChunkMetadata:
    return ChunkMetadata(
        chunk_id=chunk.chunk_id,
        document_id=chunk.document_id,
        document_version=chunk.document_version,
        document_type=chunk.document_type,
        document_title=chunk.document_title,
        status=chunk.status,
        product=chunk.product,
        jurisdiction=chunk.jurisdiction,
        audience=chunk.audience,
        effective_from=chunk.effective_from or None,
        effective_until=chunk.effective_until or None,
        source_path=chunk.source_path,
        content_hash=chunk.content_hash or "",
        heading_path=list(chunk.heading_path),
        embedding_model=embedding_model,
    )
