"""Load governed Markdown documents into knowledge models."""

import logging
from pathlib import Path

from pydantic import ValidationError

from app.core.config import get_settings
from app.modules.knowledge.exceptions import KnowledgeValidationError
from app.modules.knowledge.models import (
    CorpusLoadResult,
    DocumentInspection,
    DocumentMetadata,
    KnowledgeDocument,
    KnowledgeSection,
    ValidationIssue,
)
from app.modules.knowledge.parser import parse_body, split_front_matter
from app.modules.knowledge.validation import (
    has_errors,
    validate_body,
    validate_metadata,
    validate_slug_filename,
)

logger = logging.getLogger(__name__)

# Repository areas that are standards and indexes, not customer knowledge.
EXCLUDED_DIRECTORY_NAMES = frozenset({"governance", "templates", "metadata", "assets"})
CONTENT_DIRECTORY_NAMES = frozenset(
    {"docs", "faqs", "scenarios", "decision-guides", "glossary"}
)


def resolve_knowledge_root(root: str | Path | None = None) -> Path:
    """Resolve the knowledge base directory from settings or an explicit path.

    Relative paths are resolved from the Backend directory so
    ``../knowledge-base`` does not depend on the process working directory.
    """
    if root is None:
        raw = Path(get_settings().KNOWLEDGE_ROOT)
    else:
        raw = Path(root)
    if raw.is_absolute():
        return raw
    backend_root = Path(__file__).resolve().parents[3]
    return (backend_root / raw).resolve()


def inspect_document(path: str | Path, *, knowledge_root: str | Path | None = None) -> DocumentInspection:
    """Parse and validate one Markdown file without raising."""
    source = Path(path)
    display_path = _display_path(source, knowledge_root)
    try:
        text = source.read_text(encoding="utf-8")
    except OSError as exc:
        return _rejected(
            display_path,
            code="UNREADABLE_SOURCE",
            message=f"Could not read source file: {exc.strerror or exc}",
        )

    try:
        front_matter = split_front_matter(text)
    except ValueError as exc:
        return _rejected(display_path, code="INVALID_FRONT_MATTER", message=str(exc))

    metadata_issues = validate_metadata(None if front_matter is None else front_matter.data)
    if front_matter is None or has_errors(metadata_issues):
        return DocumentInspection(source_path=display_path, issues=metadata_issues)

    document_title = str(front_matter.data.get("title") or "")
    body = parse_body(front_matter.body, front_matter.body_start_line, document_title)
    issues = [
        *metadata_issues,
        *validate_body(body, front_matter.data),
        *validate_slug_filename(front_matter.data.get("slug"), display_path),
    ]
    if has_errors(issues) or body.h1 is None:
        return DocumentInspection(source_path=display_path, issues=issues)

    try:
        metadata = DocumentMetadata.model_validate(front_matter.data)
    except ValidationError as exc:
        return _rejected(
            display_path,
            code="INVALID_METADATA",
            message=f"Front matter could not be modeled: {exc.error_count()} field error(s)",
        )

    sections = [
        KnowledgeSection(
            section_id=f"{metadata.id}#s{index:04d}",
            document_id=metadata.id,
            heading=section.heading,
            heading_level=section.heading_level,
            heading_path=section.heading_path,
            content=section.content,
            source_location=f"{display_path}:{section.start_line}-{section.end_line}",
        )
        for index, section in enumerate(body.sections, start=1)
    ]
    document = KnowledgeDocument(
        document_id=metadata.id,
        metadata=metadata,
        h1=body.h1,
        leading_content=body.leading_content,
        preamble=body.preamble,
        sections=sections,
        source_path=display_path,
    )
    return DocumentInspection(source_path=display_path, document=document, issues=issues)


def load_document(path: str | Path, *, knowledge_root: str | Path | None = None) -> KnowledgeDocument:
    """Load one accepted knowledge document.

    Raises:
        KnowledgeValidationError: the file is missing identity, an H1, or readable front matter.
    """
    inspection = inspect_document(path, knowledge_root=knowledge_root)
    if inspection.document is None:
        raise KnowledgeValidationError(inspection.source_path, inspection.issues)
    return inspection.document


def load_documents(directory: str | Path | None = None) -> CorpusLoadResult:
    """Load Markdown documents under a directory.

    The knowledge root loads the customer-facing content trees and does not
    descend into governance, templates, metadata, or assets. Passing one of
    those directories explicitly loads it.
    """
    root = resolve_knowledge_root(directory)
    if not root.exists():
        raise FileNotFoundError(f"Knowledge directory does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Knowledge path is not a directory: {root}")

    documents: list[KnowledgeDocument] = []
    failures: list[DocumentInspection] = []
    warnings: list[DocumentInspection] = []
    knowledge_root = root if _is_knowledge_root(root) else _find_knowledge_root(root)

    for path in _markdown_files(root):
        inspection = inspect_document(path, knowledge_root=knowledge_root)
        if inspection.document is None:
            failures.append(inspection)
            logger.warning(
                "Rejected knowledge source %s (%s)",
                inspection.source_path,
                ",".join(issue.code for issue in inspection.issues),
            )
            continue
        documents.append(inspection.document)
        if any(issue.severity == "warning" for issue in inspection.issues):
            warnings.append(inspection)

    documents.sort(key=lambda document: document.source_path)
    failures.sort(key=lambda inspection: inspection.source_path)
    warnings.sort(key=lambda inspection: inspection.source_path)
    return CorpusLoadResult(documents=documents, failures=failures, warnings=warnings)


def _markdown_files(start: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(start.rglob("*.md"), key=lambda item: item.as_posix().lower()):
        if _is_excluded(path, start):
            continue
        files.append(path)
    return files


def _is_excluded(path: Path, start: Path) -> bool:
    if _is_knowledge_root(start):
        try:
            relative_parts = path.resolve().relative_to(start.resolve()).parts
        except ValueError:
            return True
        if not relative_parts or relative_parts[0] not in CONTENT_DIRECTORY_NAMES:
            return True
    for parent in path.resolve().parents:
        if parent.resolve() == start.resolve():
            break
        if parent.name in EXCLUDED_DIRECTORY_NAMES:
            return True
    return False


def _is_knowledge_root(path: Path) -> bool:
    if not path.is_dir():
        return False
    names = {child.name for child in path.iterdir()}
    return CONTENT_DIRECTORY_NAMES.issubset(names)


def _find_knowledge_root(start: Path) -> Path | None:
    for candidate in (start, *start.resolve().parents):
        if _is_knowledge_root(candidate):
            return candidate
    return None


def _display_path(path: Path, knowledge_root: str | Path | None) -> str:
    resolved = path.resolve()
    if knowledge_root is not None:
        root = Path(knowledge_root).resolve()
        try:
            return resolved.relative_to(root).as_posix()
        except ValueError:
            pass
    return resolved.as_posix()


def _rejected(source_path: str, *, code: str, message: str) -> DocumentInspection:
    return DocumentInspection(
        source_path=source_path,
        issues=[ValidationIssue(code=code, message=message, severity="error")],
    )
