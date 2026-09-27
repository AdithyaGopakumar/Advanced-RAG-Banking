"""Knowledge document foundation."""

from app.modules.knowledge.chunker import chunk_document
from app.modules.knowledge.exceptions import KnowledgeValidationError
from app.modules.knowledge.loader import inspect_document, load_document, load_documents
from app.modules.knowledge.models import (
    CorpusLoadResult,
    DocumentInspection,
    DocumentMetadata,
    KnowledgeChunk,
    KnowledgeDocument,
    KnowledgeSection,
    ValidationIssue,
)

__all__ = [
    "CorpusLoadResult",
    "DocumentInspection",
    "DocumentMetadata",
    "KnowledgeChunk",
    "KnowledgeDocument",
    "KnowledgeSection",
    "KnowledgeValidationError",
    "ValidationIssue",
    "chunk_document",
    "inspect_document",
    "load_document",
    "load_documents",
]
