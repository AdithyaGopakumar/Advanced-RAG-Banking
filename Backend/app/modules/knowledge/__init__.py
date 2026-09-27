"""Knowledge document foundation."""

from app.modules.knowledge.exceptions import KnowledgeValidationError
from app.modules.knowledge.loader import inspect_document, load_document, load_documents
from app.modules.knowledge.models import (
    CorpusLoadResult,
    DocumentInspection,
    DocumentMetadata,
    KnowledgeDocument,
    KnowledgeSection,
    ValidationIssue,
)

__all__ = [
    "CorpusLoadResult",
    "DocumentInspection",
    "DocumentMetadata",
    "KnowledgeDocument",
    "KnowledgeSection",
    "KnowledgeValidationError",
    "ValidationIssue",
    "inspect_document",
    "load_document",
    "load_documents",
]
