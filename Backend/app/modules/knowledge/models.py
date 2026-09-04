"""
Knowledge domain models — retrieval artifact hierarchy.

Defines the three-level retrieval representation:

    KnowledgeDocument  →  governed knowledge unit
    KnowledgeSection   →  structural context inside a document
    KnowledgeChunk     →  primary retrieval unit

Design principles:
    - Metadata, provenance, and relationships are structurally separate.
    - Enums are derived from the knowledge-base taxonomy to enforce type safety.
    - No database coupling — these are pure domain models.
    - Chunk identity is deterministic (see identity.py).
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ──────────────────────────────────────────────
# Enums — derived from knowledge-base taxonomy
# ──────────────────────────────────────────────


class Domain(str, Enum):
    """Top-level knowledge domains from the knowledge taxonomy."""

    PRODUCTS = "products"
    SERVICES = "services"
    POLICIES_AND_COMPLIANCE = "policies-and-compliance"
    CUSTOMER_SUPPORT = "customer-support"
    REFERENCE_DATA = "reference-data"
    FORMS_AND_DOCUMENTATION = "forms-and-documentation"
    CROSS_CUTTING = "cross-cutting"


class Category(str, Enum):
    """Functional categories within domains."""

    ACCOUNTS = "accounts"
    DEPOSITS = "deposits"
    LOANS = "loans"
    CARDS = "cards"
    DIGITAL_BANKING = "digital-banking"
    PAYMENTS = "payments"
    BANKING_SERVICES = "banking-services"
    POLICIES = "policies"
    SECURITY = "security"
    SUPPORT = "support"
    CHARGES = "charges"
    INTEREST_RATES = "interest-rates"
    FORMS = "forms"
    FAQS = "faqs"
    SCENARIOS = "scenarios"
    DECISION_GUIDES = "decision-guides"
    GLOSSARY = "glossary"


class DocumentType(str, Enum):
    """Nature of the knowledge document."""

    PRODUCT = "product"
    SERVICE = "service"
    POLICY = "policy"
    PROCESS = "process"
    REFERENCE = "reference"
    FAQ = "faq"
    SCENARIO = "scenario"
    DECISION_GUIDE = "decision-guide"
    GLOSSARY = "glossary"
    TROUBLESHOOTING = "troubleshooting"
    FORM = "form"


class DocumentStatus(str, Enum):
    """Document lifecycle status — matches knowledge-base metadata schema."""

    DRAFT = "draft"
    IN_REVIEW = "in-review"
    APPROVED = "approved"
    PUBLISHED = "published"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"
    CURRENT = "current"
    FUTURE = "future"
    SUPERSEDED = "superseded"
    EXPIRED = "expired"
    WITHDRAWN = "withdrawn"
    UNKNOWN = "unknown"
    UNVERIFIED = "unverified"


class ChunkType(str, Enum):
    """Type of content within a chunk."""

    PARAGRAPH = "paragraph"
    TABLE = "table"
    LIST = "list"
    FAQ_ENTRY = "faq_entry"
    GLOSSARY_ENTRY = "glossary_entry"
    HEADING = "heading"


class RelationshipType(str, Enum):
    """Typed relationships between knowledge entities.

    Derived from the knowledge-base relationship registry and
    the task's required relationship types.
    """

    GOVERNED_BY = "governed_by"
    REQUIRES = "requires"
    EXPLAINED_BY = "explained_by"
    APPLIES_TO = "applies_to"
    REFERENCES = "references"
    COMPLEMENTS = "complements"
    ALTERNATIVE_TO = "alternative_to"
    PARENT_OF = "parent_of"
    SUPERSEDES = "supersedes"
    SUMMARISES = "summarises"
    COMPARES = "compares"


class Priority(str, Enum):
    """Retrieval priority hint."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Confidentiality(str, Enum):
    """Access level classification."""

    PUBLIC = "public"
    CUSTOMER_ONLY = "customer-only"
    RESTRICTED = "restricted"


# ──────────────────────────────────────────────
# Nested value objects
# ──────────────────────────────────────────────

class DocumentMetadata(BaseModel):
    """Metadata attached to a governed knowledge document."""

    domain: Domain
    category: Category
    sub_category: str
    document_type: DocumentType

    # Optional filtering dimensions
    product: Optional[str] = None
    customer_segment: Optional[str] = None
    channel: Optional[str] = None

    region: str = "IN"
    language: str = "en"

    # Retrieval fields
    keywords: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    search_aliases: list[str] = Field(default_factory=list)

    # Ranking / governance
    priority: Priority = Priority.MEDIUM
    owner: str = Field(..., description="Document owner")
    authority: Optional[str] = None
    status: DocumentStatus = DocumentStatus.DRAFT
    compliance_classification: Optional[str] = None
    confidentiality: Confidentiality = Confidentiality.PUBLIC
    dynamic_content: bool = False

    # Temporal validity
    effective_from: Optional[date] = None
    effective_until: Optional[date] = None


class DocumentProvenance(BaseModel):
    """Provenance for a governed knowledge document."""

    source: Optional[str] = None
    source_location: str  # file path within the knowledge-base
    version: str


class ChunkMetadata(BaseModel):
    """Metadata attached to a retrieval chunk.

    Structurally separate from chunk content.  These fields enable
    filtering, faceted search, and retrieval ranking without
    concatenating metadata into the chunk text.
    """

    domain: Domain
    category: Category
    sub_category: str
    document_type: DocumentType

    # Optional filtering dimensions
    product: Optional[str] = None
    customer_segment: Optional[str] = None
    channel: Optional[str] = None

    region: str = "IN"
    language: str = "en"

    # Retrieval fields
    keywords: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    search_aliases: list[str] = Field(default_factory=list)

    # Ranking / governance
    priority: Priority = Priority.MEDIUM
    authority: Optional[str] = None
    status: DocumentStatus = DocumentStatus.DRAFT
    confidentiality: Confidentiality = Confidentiality.PUBLIC

    # Temporal validity
    effective_from: Optional[date] = None
    effective_until: Optional[date] = None


class ChunkProvenance(BaseModel):
    """Provenance — traces a chunk back to its governed knowledge source.

    Supports the chain:
        Answer → Evidence Chunk → Section → Knowledge Document → Source → Version
    """

    source: Optional[str] = None
    document_version: str
    section: str
    source_location: str  # file path within the knowledge-base


class ChunkContext(BaseModel):
    """Contextual breadcrumbs for the chunk.
    
    Preserves structural context separately from the canonical chunk text,
    allowing downstream embeddings to reconstruct the full context hierarchy.
    """
    document_title: str
    heading_path: list[str] = Field(default_factory=list)


class KnowledgeRelationship(BaseModel):
    """A typed, directed relationship between knowledge entities.

    Relationships are stored as simple typed records, not as graph edges.
    No graph database is required.
    """

    relationship_type: RelationshipType
    target_id: str  # document ID or chunk ID


# ──────────────────────────────────────────────
# Core domain models — the retrieval artifact hierarchy
# ──────────────────────────────────────────────


class KnowledgeDocument(BaseModel):
    """A governed knowledge unit.

    Represents a complete document from the knowledge base (product doc,
    policy, FAQ, decision guide, scenario, etc.).

    This is NOT the retrieval unit — chunks are.  The document provides
    the governance context that chunks inherit.
    """

    document_id: str = Field(
        ...,
        description="Stable document ID, e.g. 'ACCT-SA-001'",
    )
    title: str
    slug: str

    metadata: DocumentMetadata
    provenance: DocumentProvenance

    content: str = Field(
        ...,
        description="Raw markdown content of the document (excluding front matter)",
    )

    sections: list[KnowledgeSection] = Field(default_factory=list)

    # Flat related-document list from knowledge-base frontmatter.
    # Typed relationships exist on KnowledgeChunk for the retrieval layer.
    related_documents: list[str] = Field(default_factory=list)
    relationships: list[KnowledgeRelationship] = Field(default_factory=list)


class KnowledgeSection(BaseModel):
    """Structural context inside a document.

    Represents an H2 or H3 section.  Sections provide the heading
    context that chunks need for self-contained retrieval.
    """

    section_id: str = Field(
        ...,
        description="Deterministic: 'DOC_ID::heading-slug'",
    )
    document_id: str
    heading: str
    level: int = Field(..., description="Heading level (1 for root, 2+ for subsections)")
    position: int = Field(..., ge=0, description="Ordinal position within document")
    content: str = Field(
        ...,
        description="Raw Markdown content preserving structure (paragraphs, lists, etc.)",
    )
    parent_section_id: Optional[str] = Field(
        default=None,
        description="ID of the parent section (e.g. H2 ID for an H3 section)",
    )


class KnowledgeChunk(BaseModel):
    """The primary retrieval unit.

    A chunk is the atomic unit retrieved by the RAG pipeline.
    It carries its own metadata, provenance, and typed relationships
    so that downstream components (context builder, citation engine)
    have everything they need without re-querying the source.

    Identity:
        chunk_id is deterministic — see identity.generate_chunk_id().
        content_hash is a SHA-256 digest of the chunk text.

    Principles:
        - Retrieval unit ≠ generation context.
        - Metadata is first-class, not concatenated into text.
        - Provenance is mandatory.
        - Relationships are typed and structured.
    """

    chunk_id: str = Field(
        ...,
        description="Deterministic: 'DOC_ID::section-slug::NNN'",
    )
    document_id: str
    section_id: str
    parent_chunk_id: Optional[str] = None

    chunk_type: ChunkType
    position: int = Field(..., ge=0, description="Ordinal position within section")
    text: str

    content_hash: str = Field(
        ...,
        description="SHA-256 hex digest of the chunk text",
    )

    # Structurally separate concerns
    metadata: ChunkMetadata
    provenance: ChunkProvenance
    context: ChunkContext
    relationships: list[KnowledgeRelationship] = Field(default_factory=list)
