"""Metadata constraints applied to dense and lexical candidates."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

# Live statuses used by the governed corpus.
DEFAULT_ELIGIBLE_STATUSES = ("approved", "current")


class MetadataFilter(BaseModel):
    """Equality and effective-date constraints shared by both indexes."""

    model_config = ConfigDict(extra="forbid")

    statuses: tuple[str, ...] | None = DEFAULT_ELIGIBLE_STATUSES
    product: str | None = None
    jurisdiction: str | None = None
    audience: str | None = None
    document_type: str | None = None
    document_id: str | None = None
    as_of: str | None = None


class ChunkMetadata(BaseModel):
    """Filterable provenance stored with a chunk in both indexes."""

    model_config = ConfigDict(extra="forbid")

    chunk_id: str
    document_id: str
    document_version: str
    document_type: str
    document_title: str
    status: str
    product: str | None = None
    jurisdiction: str | None = None
    audience: str | None = None
    effective_from: str | None = None
    effective_until: str | None = None
    source_path: str
    content_hash: str
    heading_path: list[str] = Field(default_factory=list)
    embedding_model: str = ""

    def as_filter_dict(self) -> dict[str, str | list[str]]:
        """Metadata safe to send to Pinecone. Empty optional fields are omitted."""
        payload: dict[str, str | list[str]] = {
            "chunk_id": self.chunk_id,
            "document_id": self.document_id,
            "document_version": self.document_version,
            "document_type": self.document_type,
            "document_title": self.document_title,
            "status": self.status,
            "source_path": self.source_path,
            "content_hash": self.content_hash,
            "embedding_model": self.embedding_model,
        }
        if self.heading_path:
            payload["heading_path"] = list(self.heading_path)
        for field_name in ("product", "jurisdiction", "audience", "effective_from", "effective_until"):
            value = getattr(self, field_name)
            if value:
                payload[field_name] = value
        return payload


def matches_filter(metadata: ChunkMetadata, constraint: MetadataFilter) -> bool:
    """Return whether a chunk may be retrieved under the constraint."""
    if constraint.statuses is not None and metadata.status not in constraint.statuses:
        return False
    if constraint.product is not None and metadata.product != constraint.product:
        return False
    if constraint.jurisdiction is not None and metadata.jurisdiction != constraint.jurisdiction:
        return False
    if constraint.audience is not None and metadata.audience != constraint.audience:
        return False
    if constraint.document_type is not None and metadata.document_type != constraint.document_type:
        return False
    if constraint.document_id is not None and metadata.document_id != constraint.document_id:
        return False
    if constraint.as_of is not None and not _is_effective(metadata, constraint.as_of):
        return False
    return True


def to_pinecone_filter(constraint: MetadataFilter) -> dict[str, object] | None:
    """Equality filters Pinecone can apply. Effective dates are checked afterwards."""
    clauses: list[dict[str, object]] = []
    if constraint.statuses:
        clauses.append({"status": {"$in": list(constraint.statuses)}})
    for field_name in ("product", "jurisdiction", "audience", "document_type", "document_id"):
        value = getattr(constraint, field_name)
        if value is not None:
            clauses.append({field_name: {"$eq": value}})
    if not clauses:
        return None
    if len(clauses) == 1:
        return clauses[0]
    return {"$and": clauses}


def _is_effective(metadata: ChunkMetadata, as_of: str) -> bool:
    on_date = _parse_date(as_of)
    if on_date is None:
        return False
    starts = _parse_date(metadata.effective_from)
    ends = _parse_date(metadata.effective_until)
    if metadata.effective_from and starts is None:
        return False
    if metadata.effective_until and ends is None:
        return False
    if starts is not None and starts > on_date:
        return False
    if ends is not None and ends < on_date:
        return False
    return True


def _parse_date(value: str | None) -> datetime | None:
    if value is None or not value.strip():
        return None
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d")
    except ValueError:
        return None
