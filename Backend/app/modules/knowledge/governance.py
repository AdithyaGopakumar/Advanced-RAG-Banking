"""Governance build for parsed knowledge.

Live retrieval follows the statuses the corpus actually uses:
``approved`` and ``current``. ``draft`` is kept in the build and marked
ineligible. ``published`` is a schema value, not a corpus value, so it is
not treated as live.

The build reports duplicate content and conflicting amounts. It does not
choose a surviving document.
"""

import hashlib
import json
import re
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

from app.modules.knowledge.chunker import chunk_document
from app.modules.knowledge.loader import load_documents, resolve_knowledge_root
from app.modules.knowledge.models import (
    ContradictionFinding,
    DocumentInspection,
    DocumentRecord,
    DuplicateFinding,
    KnowledgeBuild,
    KnowledgeChunk,
    KnowledgeDocument,
    ValidationIssue,
)

# Schema vocabulary. Eligibility is narrower and comes from the corpus.
KNOWN_STATUSES = frozenset(
    {
        "draft",
        "in-review",
        "approved",
        "published",
        "deprecated",
        "archived",
        "current",
        "future",
        "superseded",
        "expired",
        "withdrawn",
        "unknown",
        "unverified",
    }
)
ELIGIBLE_STATUSES = frozenset({"approved", "current"})

PIPELINE_VERSION = "knowledge-1c"
_VERSION = re.compile(r"^\d+\.\d+$")
_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_AMOUNT = re.compile(r"(?:₹|Rs\.?)\s*([0-9][0-9,]*)")
_TABLE_LINE = re.compile(r"^\|.+\|\s*$")


def build_knowledge(
    directory: str | Path | None = None,
    *,
    max_size: int | None = None,
    as_of: date | None = None,
) -> KnowledgeBuild:
    """Validate, hash, and chunk a knowledge directory into a build manifest."""
    root = resolve_knowledge_root(directory)
    loaded = load_documents(root)
    limit = _chunk_limit(max_size)
    on_date = as_of or date.today()
    config = _processing_config(limit)
    warnings_by_path = {item.source_path: item.issues for item in loaded.warnings}

    records: list[DocumentRecord] = []
    chunks: list[KnowledgeChunk] = []
    for document in loaded.documents:
        source_text = _read_source(root, document.source_path)
        content_hash = _document_hash(document, source_text, config)
        issues = [
            *warnings_by_path.get(document.source_path, []),
            *_metadata_issues(document),
            *_table_issues(document),
        ]
        document_chunks = [
            _with_hash(chunk, content_hash, config) for chunk in chunk_document(document, max_size=limit)
        ]
        issues.extend(_semantic_issues(document, document_chunks))
        eligible = _is_eligible(document, issues, on_date)
        stamped = [chunk.model_copy(update={"eligible": eligible}) for chunk in document_chunks]
        records.append(
            DocumentRecord(
                document_id=document.document_id,
                version=document.metadata.version,
                status=document.metadata.status,
                source_path=document.source_path,
                content_hash=content_hash,
                eligible=eligible,
                chunk_ids=[chunk.chunk_id for chunk in stamped],
                issues=issues,
            )
        )
        chunks.extend(stamped)

    records, chunks = _apply_duplicate_ids(records, chunks)
    duplicates = _duplicate_findings(records)
    contradictions = [
        *_supersession_conflicts(loaded.documents, records),
        *_amount_conflicts(chunks),
    ]
    rejected = list(loaded.failures)
    manifest_hash = _manifest_hash(
        chunk_max_size=limit,
        as_of=on_date,
        documents=records,
        chunks=chunks,
        duplicates=duplicates,
        contradictions=contradictions,
        rejected=rejected,
    )
    return KnowledgeBuild(
        manifest_hash=manifest_hash,
        chunk_max_size=limit,
        as_of=on_date.isoformat(),
        documents=records,
        chunks=chunks,
        duplicates=duplicates,
        contradictions=contradictions,
        rejected=rejected,
    )


def _chunk_limit(max_size: int | None) -> int:
    if max_size is None:
        from app.core.config import get_settings

        max_size = get_settings().CHUNK_MAX_SIZE
    if max_size <= 0:
        raise ValueError("Chunk size must be a positive character budget")
    return max_size


def _processing_config(max_size: int) -> str:
    return json.dumps(
        {"pipeline": PIPELINE_VERSION, "chunk_max_size": max_size},
        sort_keys=True,
        separators=(",", ":"),
    )


def _document_hash(document: KnowledgeDocument, source_text: str, config: str) -> str:
    """Hash normalized body plus version and status, not the file path.

    Two copies with different ids still share a hash when the governed text
    and version are the same. A path is not part of the knowledge.
    """
    body = _normalized_body(source_text)
    payload = "\n".join(
        [
            config,
            document.metadata.version,
            document.metadata.status,
            body,
        ]
    )
    return _sha256(payload)


def _with_hash(chunk: KnowledgeChunk, document_hash: str, config: str) -> KnowledgeChunk:
    payload = "\n".join(
        [
            config,
            document_hash,
            chunk.document_version,
            chunk.chunk_type,
            " > ".join(chunk.heading_path),
            chunk.text,
        ]
    )
    return chunk.model_copy(update={"content_hash": _sha256(payload)})


def _sha256(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _normalized_body(source_text: str) -> str:
    from app.modules.knowledge.parser import split_front_matter

    normalized = source_text.removeprefix("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    try:
        front_matter = split_front_matter(normalized)
    except ValueError:
        return normalized
    if front_matter is None:
        return normalized
    return front_matter.body


def _read_source(root: Path, source_path: str) -> str:
    candidate = Path(source_path)
    path = candidate if candidate.is_absolute() else root / candidate
    return path.read_text(encoding="utf-8")


def _metadata_issues(document: KnowledgeDocument) -> list[ValidationIssue]:
    metadata = document.metadata
    issues: list[ValidationIssue] = []
    if metadata.status not in KNOWN_STATUSES:
        issues.append(
            ValidationIssue(
                code="INVALID_STATUS",
                message=f"Status '{metadata.status}' is not a known lifecycle value",
                severity="error",
                field="status",
            )
        )
    elif metadata.status not in ELIGIBLE_STATUSES:
        issues.append(
            ValidationIssue(
                code="STATUS_NOT_ELIGIBLE",
                message=(
                    f"Status '{metadata.status}' is not retrieval-eligible. "
                    "The corpus treats approved and current as live knowledge."
                ),
                severity="warning",
                field="status",
            )
        )

    if _VERSION.match(metadata.version) is None:
        issues.append(
            ValidationIssue(
                code="INVALID_VERSION",
                message="Version must use MAJOR.MINOR, for example 1.0",
                severity="error",
                field="version",
            )
        )

    if not metadata.owner or not str(metadata.owner).strip():
        issues.append(
            ValidationIssue(
                code="MISSING_OWNER",
                message="Document has no owner",
                severity="warning",
                field="owner",
            )
        )

    effective_from = _parse_date(metadata.effective_from, field_name="effective_from")
    effective_until = _parse_date(metadata.effective_until, field_name="effective_until")
    issues.extend(effective_from[1])
    issues.extend(effective_until[1])
    if (
        effective_from[0] is not None
        and effective_until[0] is not None
        and effective_from[0] > effective_until[0]
    ):
        issues.append(
            ValidationIssue(
                code="INVALID_EFFECTIVE_WINDOW",
                message="effective_from is after effective_until",
                severity="error",
                field="effective_from",
            )
        )

    if document.metadata.document_type == "reference" and effective_from[0] is None and not effective_from[1]:
        issues.append(
            ValidationIssue(
                code="MISSING_EFFECTIVE_FROM",
                message="Reference documents should declare effective_from",
                severity="warning",
                field="effective_from",
            )
        )
    return issues


def _parse_date(value: str | None, *, field_name: str) -> tuple[date | None, list[ValidationIssue]]:
    if value is None or not str(value).strip():
        return None, []
    text = str(value).strip()
    if _DATE.match(text) is None:
        return None, [
            ValidationIssue(
                code="INVALID_DATE",
                message=f"{field_name} must use YYYY-MM-DD",
                severity="error",
                field=field_name,
            )
        ]
    try:
        parsed = datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return None, [
            ValidationIssue(
                code="INVALID_DATE",
                message=f"{field_name} is not a calendar date",
                severity="error",
                field=field_name,
            )
        ]
    return parsed, []


def _window_issues(document: KnowledgeDocument, on_date: date) -> list[ValidationIssue]:
    effective_from, from_issues = _parse_date(document.metadata.effective_from, field_name="effective_from")
    effective_until, until_issues = _parse_date(document.metadata.effective_until, field_name="effective_until")
    if from_issues or until_issues:
        return []
    issues: list[ValidationIssue] = []
    if effective_from is not None and effective_from > on_date:
        issues.append(
            ValidationIssue(
                code="NOT_YET_EFFECTIVE",
                message=f"Document is not effective until {effective_from.isoformat()}",
                severity="warning",
                field="effective_from",
            )
        )
    if effective_until is not None and effective_until < on_date:
        issues.append(
            ValidationIssue(
                code="EXPIRED",
                message=f"Document effective window ended on {effective_until.isoformat()}",
                severity="warning",
                field="effective_until",
            )
        )
    return issues


def _is_eligible(document: KnowledgeDocument, issues: list[ValidationIssue], on_date: date) -> bool:
    window = _window_issues(document, on_date)
    issues.extend(window)
    if any(issue.severity == "error" for issue in issues):
        return False
    if document.metadata.status not in ELIGIBLE_STATUSES:
        return False
    if any(issue.code in {"NOT_YET_EFFECTIVE", "EXPIRED"} for issue in window):
        return False
    return True


def _table_issues(document: KnowledgeDocument) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for section in document.sections:
        lines = [
            line.strip()
            for line in section.content.splitlines()
            if _TABLE_LINE.match(line.strip()) is not None
        ]
        if len(lines) < 2:
            continue
        widths = {len([cell for cell in line.strip("|").split("|")]) for line in lines}
        if len(widths) > 1:
            issues.append(
                ValidationIssue(
                    code="TABLE_SHAPE",
                    message=f"Table in '{section.heading}' has rows with different column counts",
                    severity="warning",
                    field="content",
                )
            )
    return issues


def _semantic_issues(document: KnowledgeDocument, chunks: list[KnowledgeChunk]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if document.metadata.document_type in {"scenario", "decision-guide"} and len(chunks) > 1:
        issues.append(
            ValidationIssue(
                code="SCENARIO_SPLIT",
                message="Scenario or decision guide exceeded the chunk budget and was split",
                severity="warning",
            )
        )
    issues.extend(_procedure_gap_issues(chunks))
    for chunk in chunks:
        if not chunk.heading_path or not chunk.chunk_id or not chunk.content_hash:
            issues.append(
                ValidationIssue(
                    code="INCOMPLETE_CHUNK",
                    message=f"Chunk {chunk.chunk_id or '(missing id)'} is missing retrieval metadata",
                    severity="error",
                )
            )
    return issues


def _procedure_gap_issues(chunks: list[KnowledgeChunk]) -> list[ValidationIssue]:
    grouped: dict[str, list[int]] = defaultdict(list)
    for chunk in chunks:
        if chunk.chunk_type != "procedure" or chunk.procedure_step_start is None or chunk.procedure_step_end is None:
            continue
        key = chunk.section_id or chunk.chunk_id
        grouped[key].extend(range(chunk.procedure_step_start, chunk.procedure_step_end + 1))
    issues: list[ValidationIssue] = []
    for steps in grouped.values():
        ordered = sorted(set(steps))
        if ordered != list(range(ordered[0], ordered[-1] + 1)):
            issues.append(
                ValidationIssue(
                    code="PROCEDURE_GAP",
                    message="A split procedure is missing a step",
                    severity="warning",
                )
            )
    return issues


def _apply_duplicate_ids(
    records: list[DocumentRecord],
    chunks: list[KnowledgeChunk],
) -> tuple[list[DocumentRecord], list[KnowledgeChunk]]:
    counts: dict[str, int] = defaultdict(int)
    for record in records:
        counts[record.document_id] += 1
    duplicated = {document_id for document_id, count in counts.items() if count > 1}
    if not duplicated:
        return records, chunks
    updated_records = []
    for record in records:
        if record.document_id not in duplicated:
            updated_records.append(record)
            continue
        issue = ValidationIssue(
            code="DUPLICATE_DOCUMENT_ID",
            message=(
                f"Document id {record.document_id} is used by more than one source. "
                "None of the copies were selected."
            ),
            severity="error",
            field="id",
        )
        updated_records.append(
            record.model_copy(update={"eligible": False, "issues": [*record.issues, issue]})
        )
    updated_chunks = [
        chunk.model_copy(update={"eligible": False}) if chunk.document_id in duplicated else chunk
        for chunk in chunks
    ]
    return updated_records, updated_chunks


def _duplicate_findings(records: list[DocumentRecord]) -> list[DuplicateFinding]:
    findings: list[DuplicateFinding] = []
    by_id: dict[str, list[DocumentRecord]] = defaultdict(list)
    by_hash: dict[str, list[DocumentRecord]] = defaultdict(list)
    for record in records:
        by_id[record.document_id].append(record)
        by_hash[record.content_hash].append(record)

    for document_id, group in sorted(by_id.items()):
        if len(group) < 2:
            continue
        paths = sorted(record.source_path for record in group)
        findings.append(
            DuplicateFinding(
                code="DUPLICATE_DOCUMENT_ID",
                message=(
                    f"Document id {document_id} appears in {len(group)} sources. "
                    "No copy was preferred."
                ),
                document_ids=[document_id],
                source_paths=paths,
            )
        )

    for content_hash, group in sorted(by_hash.items()):
        ids = sorted({record.document_id for record in group})
        paths = sorted(record.source_path for record in group)
        if len(paths) < 2 or len(ids) < 2:
            continue
        findings.append(
            DuplicateFinding(
                code="DUPLICATE_CONTENT",
                message=(
                    "These documents have the same versioned body. "
                    "They were kept so governance can decide whether one is redundant."
                ),
                document_ids=ids,
                source_paths=paths,
                content_hash=content_hash,
            )
        )
    return findings


def _supersession_conflicts(
    documents: list[KnowledgeDocument],
    records: list[DocumentRecord],
) -> list[ContradictionFinding]:
    eligible_ids = {record.document_id for record in records if record.eligible}
    findings: list[ContradictionFinding] = []
    for document in documents:
        superseded = document.metadata.supersedes
        if not superseded or superseded not in eligible_ids:
            continue
        findings.append(
            ContradictionFinding(
                code="SUPERSEDED_STILL_ELIGIBLE",
                message=(
                    f"{document.document_id} supersedes {superseded}, "
                    "which is still retrieval-eligible. No document was withdrawn."
                ),
                document_ids=sorted({document.document_id, superseded}),
            )
        )
    return findings


def _amount_conflicts(chunks: list[KnowledgeChunk]) -> list[ContradictionFinding]:
    grouped: dict[tuple[str, str], dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for chunk in chunks:
        if not chunk.eligible or not chunk.product or not chunk.heading_path:
            continue
        amounts = {_normalize_amount(match) for match in _AMOUNT.findall(chunk.content)}
        amounts.discard("")
        if len(amounts) != 1:
            continue
        key = (chunk.product, chunk.heading_path[-1].casefold())
        grouped[key][chunk.document_id].add(next(iter(amounts)))

    findings: list[ContradictionFinding] = []
    for (product, heading), by_document in sorted(grouped.items()):
        amounts_by_document = {document_id: next(iter(values)) for document_id, values in by_document.items() if len(values) == 1}
        distinct = sorted(set(amounts_by_document.values()))
        if len(amounts_by_document) < 2 or len(distinct) < 2:
            continue
        findings.append(
            ContradictionFinding(
                code="CONTRADICTORY_AMOUNT",
                message=(
                    f"Eligible documents disagree on the amount for '{heading}' "
                    f"under {product}: {', '.join(distinct)}. No value was selected."
                ),
                document_ids=sorted(amounts_by_document),
                heading=heading,
                amounts=distinct,
            )
        )
    return findings


def _normalize_amount(raw: str) -> str:
    return raw.replace(",", "")


def _manifest_hash(
    *,
    chunk_max_size: int,
    as_of: date,
    documents: list[DocumentRecord],
    chunks: list[KnowledgeChunk],
    duplicates: list[DuplicateFinding],
    contradictions: list[ContradictionFinding],
    rejected: list[DocumentInspection],
) -> str:
    payload = {
        "as_of": as_of.isoformat(),
        "chunk_max_size": chunk_max_size,
        "pipeline": PIPELINE_VERSION,
        "documents": [
            {
                "chunk_ids": record.chunk_ids,
                "content_hash": record.content_hash,
                "document_id": record.document_id,
                "eligible": record.eligible,
                "issue_codes": [issue.code for issue in record.issues],
                "source_path": record.source_path,
                "status": record.status,
                "version": record.version,
            }
            for record in sorted(documents, key=lambda record: record.source_path)
        ],
        "chunks": [
            {
                "chunk_id": chunk.chunk_id,
                "content_hash": chunk.content_hash,
                "eligible": chunk.eligible,
                "source_path": chunk.source_path,
            }
            for chunk in sorted(chunks, key=lambda chunk: (chunk.source_path, chunk.chunk_index, chunk.chunk_id))
        ],
        "duplicates": [item.model_dump() for item in duplicates],
        "contradictions": [item.model_dump() for item in contradictions],
        "rejected": [
            {"source_path": item.source_path, "codes": [issue.code for issue in item.issues]}
            for item in sorted(rejected, key=lambda item: item.source_path)
        ],
    }
    return _sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
