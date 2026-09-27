"""Retrieval-document models for the knowledge foundation.

These models represent a parsed source document, its sections, and the
chunks produced for later indexing. Content hashing and index records
belong to later phases.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ValidationIssue(BaseModel):
    """One structural finding from document validation."""

    model_config = ConfigDict(extra="forbid")

    code: str
    message: str
    severity: Literal["error", "warning"]
    field: str | None = None


class DocumentMetadata(BaseModel):
    """Front matter carried by a governed knowledge document.

    Identity fields are required to construct a document. Other schema
    fields are retained when present, including fields not declared here.
    """

    model_config = ConfigDict(extra="allow")

    id: str
    title: str
    slug: str
    document_type: str
    version: str
    status: str
    domain: str | None = None
    category: str | None = None
    sub_category: str | None = None
    applicable_to: str | None = None
    target_audience: str | None = None
    applicable_channels: list[str] | None = None
    language: str | None = None
    region: str | None = None
    keywords: list[str] | None = None
    tags: list[str] | None = None
    search_aliases: list[str] | None = None
    priority: str | None = None
    related_documents: list[str] | None = None
    parent_document: str | None = None
    supersedes: str | None = None
    owner: str | None = None
    compliance_classification: str | None = None
    confidentiality: str | None = None
    regulatory_references: list[str] | None = None
    created_date: str | None = None
    last_updated: str | None = None
    last_reviewed: str | None = None
    effective_from: str | None = None
    effective_until: str | None = None
    dynamic_content: bool | None = None


class KnowledgeSection(BaseModel):
    """One H2–H4 section with its heading ancestry and original Markdown."""

    model_config = ConfigDict(extra="forbid")

    section_id: str
    document_id: str
    heading: str
    heading_level: int
    heading_path: list[str]
    content: str
    source_location: str


class KnowledgeChunk(BaseModel):
    """One retrieval unit derived from a knowledge document.

    ``content`` is the original Markdown fragment. ``text`` is that fragment
    with heading breadcrumbs prepended for retrieval.
    """

    model_config = ConfigDict(extra="forbid")

    chunk_id: str
    document_id: str
    document_version: str
    document_type: str
    document_title: str
    section_id: str | None = None
    heading_path: list[str]
    chunk_index: int
    chunk_type: Literal["section", "scenario", "decision_guide", "procedure", "table"]
    status: str
    effective_from: str | None = None
    effective_until: str | None = None
    product: str | None = None
    jurisdiction: str | None = None
    audience: str | None = None
    source_location: str
    source_path: str
    content: str
    text: str
    oversized: bool = False
    procedure_step_start: int | None = None
    procedure_step_end: int | None = None
    content_hash: str | None = None
    eligible: bool = False


class KnowledgeDocument(BaseModel):
    """A parsed knowledge document before chunking."""

    model_config = ConfigDict(extra="forbid")

    document_id: str
    metadata: DocumentMetadata
    h1: str
    leading_content: str = ""
    preamble: str = ""
    sections: list[KnowledgeSection] = Field(default_factory=list)
    source_path: str

    @property
    def title(self) -> str:
        return self.metadata.title


class DocumentInspection(BaseModel):
    """Parse and validation outcome for a single source file."""

    model_config = ConfigDict(extra="forbid")

    source_path: str
    document: KnowledgeDocument | None = None
    issues: list[ValidationIssue] = Field(default_factory=list)

    @property
    def accepted(self) -> bool:
        return self.document is not None and not any(
            issue.severity == "error" for issue in self.issues
        )


class DocumentRecord(BaseModel):
    """Governance record for one accepted source document."""

    model_config = ConfigDict(extra="forbid")

    document_id: str
    version: str
    status: str
    source_path: str
    content_hash: str
    eligible: bool
    chunk_ids: list[str] = Field(default_factory=list)
    issues: list[ValidationIssue] = Field(default_factory=list)


class DuplicateFinding(BaseModel):
    """Identical identities or content that governance must review.

    Findings are reported and left in place. Historical copies are not dropped.
    """

    model_config = ConfigDict(extra="forbid")

    code: Literal["DUPLICATE_DOCUMENT_ID", "DUPLICATE_CONTENT"]
    message: str
    document_ids: list[str]
    source_paths: list[str]
    content_hash: str | None = None


class ContradictionFinding(BaseModel):
    """A conflict the build will not resolve by picking a winner."""

    model_config = ConfigDict(extra="forbid")

    code: str
    message: str
    document_ids: list[str]
    heading: str | None = None
    amounts: list[str] = Field(default_factory=list)


class KnowledgeBuild(BaseModel):
    """Reproducible governance build for a knowledge directory."""

    model_config = ConfigDict(extra="forbid")

    manifest_hash: str
    chunk_max_size: int
    as_of: str
    documents: list[DocumentRecord] = Field(default_factory=list)
    chunks: list[KnowledgeChunk] = Field(default_factory=list)
    duplicates: list[DuplicateFinding] = Field(default_factory=list)
    contradictions: list[ContradictionFinding] = Field(default_factory=list)
    rejected: list[DocumentInspection] = Field(default_factory=list)

    @property
    def eligible_chunks(self) -> list[KnowledgeChunk]:
        return [chunk for chunk in self.chunks if chunk.eligible]


class CorpusLoadResult(BaseModel):
    """Documents accepted from a directory, plus files that were rejected."""

    model_config = ConfigDict(extra="forbid")

    documents: list[KnowledgeDocument] = Field(default_factory=list)
    failures: list[DocumentInspection] = Field(default_factory=list)
    warnings: list[DocumentInspection] = Field(default_factory=list)
