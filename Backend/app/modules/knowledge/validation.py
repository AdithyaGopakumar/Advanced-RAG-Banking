"""Structural validation for Phase 1A documents.

Blocking checks are limited to parseability and document identity.
Schema enums, uniqueness, and retrieval eligibility are later phases.
Title and slug mismatches are warnings so a structurally sound document
is still returned for inspection.
"""

from pathlib import Path

from app.modules.knowledge.models import ValidationIssue
from app.modules.knowledge.parser import ParsedBody

IDENTITY_FIELDS: tuple[str, ...] = (
    "id",
    "title",
    "slug",
    "document_type",
    "version",
    "status",
)


def validate_metadata(data: dict[str, object] | None) -> list[ValidationIssue]:
    """Check that front matter exists and identity fields are non-empty strings."""
    if data is None:
        return [
            ValidationIssue(
                code="MISSING_FRONT_MATTER",
                message="Document is missing a YAML front matter block",
                severity="error",
            )
        ]

    issues: list[ValidationIssue] = []
    for field_name in IDENTITY_FIELDS:
        value = data.get(field_name)
        if not isinstance(value, str) or not value.strip():
            issues.append(
                ValidationIssue(
                    code="MISSING_FIELD",
                    message=f"Front matter field '{field_name}' must be a non-empty string",
                    severity="error",
                    field=field_name,
                )
            )
    return issues


def validate_body(body: ParsedBody, metadata: dict[str, object]) -> list[ValidationIssue]:
    """Check the H1 and record non-blocking title or slug disagreements."""
    issues: list[ValidationIssue] = []
    if body.h1 is None:
        issues.append(
            ValidationIssue(
                code="MISSING_H1",
                message="Document body must contain an H1 heading",
                severity="error",
            )
        )
        return issues

    if body.h1_count > 1:
        issues.append(
            ValidationIssue(
                code="MULTIPLE_H1",
                message="Document body contains more than one H1 heading; the first is used",
                severity="warning",
            )
        )

    title = metadata.get("title")
    if isinstance(title, str) and title.strip() and title != body.h1:
        issues.append(
            ValidationIssue(
                code="TITLE_H1_MISMATCH",
                message="Front matter title does not match the H1 heading",
                severity="warning",
                field="title",
            )
        )
    return issues


def validate_slug_filename(slug: object, source_path: str) -> list[ValidationIssue]:
    """Warn when the slug does not match the Markdown filename."""
    filename = Path(source_path).name
    if not filename.endswith(".md") or not isinstance(slug, str):
        return []
    if slug != filename[: -len(".md")]:
        return [
            ValidationIssue(
                code="SLUG_FILENAME_MISMATCH",
                message="Front matter slug does not match the filename",
                severity="warning",
                field="slug",
            )
        ]
    return []


def has_errors(issues: list[ValidationIssue]) -> bool:
    return any(issue.severity == "error" for issue in issues)
