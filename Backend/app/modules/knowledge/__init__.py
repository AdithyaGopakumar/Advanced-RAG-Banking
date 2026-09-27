"""Knowledge document foundation."""

from app.modules.knowledge.chunker import chunk_document
from app.modules.knowledge.exceptions import KnowledgeValidationError
from app.modules.knowledge.governance import ELIGIBLE_STATUSES, build_knowledge
from app.modules.knowledge.loader import inspect_document, load_document, load_documents
from app.modules.knowledge.models import (
    ContradictionFinding,
    CorpusLoadResult,
    DocumentInspection,
    DocumentMetadata,
    DocumentRecord,
    DuplicateFinding,
    KnowledgeBuild,
    KnowledgeChunk,
    KnowledgeDocument,
    KnowledgeSection,
    ValidationIssue,
)

__all__ = [
    "ELIGIBLE_STATUSES",
    "ContradictionFinding",
    "CorpusLoadResult",
    "DocumentInspection",
    "DocumentMetadata",
    "DocumentRecord",
    "DuplicateFinding",
    "KnowledgeBuild",
    "KnowledgeChunk",
    "KnowledgeDocument",
    "KnowledgeSection",
    "KnowledgeValidationError",
    "ValidationIssue",
    "build_knowledge",
    "chunk_document",
    "inspect_document",
    "load_document",
    "load_documents",
]
