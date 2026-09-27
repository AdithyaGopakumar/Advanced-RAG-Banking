"""Structural validation tests for the document foundation."""

import pytest

from app.modules.knowledge.exceptions import KnowledgeValidationError
from app.modules.knowledge.loader import inspect_document, load_document


def test_missing_front_matter_produces_no_document(tmp_path):
    source = tmp_path / "note.md"
    source.write_text("# Just a heading\n\nNo metadata.\n", encoding="utf-8")

    inspection = inspect_document(source)
    assert inspection.document is None
    assert inspection.issues[0].code == "MISSING_FRONT_MATTER"

    with pytest.raises(KnowledgeValidationError) as raised:
        load_document(source)
    assert raised.value.issues[0].code == "MISSING_FRONT_MATTER"


def test_missing_id_produces_no_document(tmp_path):
    source = tmp_path / "missing-id.md"
    source.write_text(
        "---\ntitle: Savings\nslug: missing-id\ndocument_type: product\n"
        "version: '1.0'\nstatus: approved\n---\n\n# Savings\n",
        encoding="utf-8",
    )

    inspection = inspect_document(source)
    assert inspection.document is None
    assert any(issue.field == "id" and issue.severity == "error" for issue in inspection.issues)


def test_missing_h1_produces_no_document(tmp_path):
    source = tmp_path / "no-h1.md"
    source.write_text(
        "---\nid: ACCT-X-001\ntitle: Savings\nslug: no-h1\n"
        "document_type: product\nversion: '1.0'\nstatus: approved\n---\n\n"
        "## Eligibility\n\nResident individuals.\n",
        encoding="utf-8",
    )

    inspection = inspect_document(source)
    assert inspection.document is None
    assert any(issue.code == "MISSING_H1" for issue in inspection.issues)


def test_malformed_front_matter_produces_no_document(tmp_path):
    source = tmp_path / "broken.md"
    source.write_text("---\nid: [unterminated\n---\n\n# Broken\n", encoding="utf-8")

    inspection = inspect_document(source)
    assert inspection.document is None
    assert inspection.issues[0].code == "INVALID_FRONT_MATTER"


def test_slug_filename_mismatch_warns_but_accepts_document(tmp_path):
    source = tmp_path / "savings.md"
    source.write_text(
        "---\nid: ACCT-X-001\ntitle: Savings\nslug: not-the-filename\n"
        "document_type: product\nversion: '1.0'\nstatus: approved\n---\n\n"
        "# Savings\n\n## Eligibility\n\nAdults.\n",
        encoding="utf-8",
    )

    inspection = inspect_document(source)
    assert inspection.accepted
    assert inspection.document is not None
    assert inspection.document.sections[0].heading_path == ["Savings", "Eligibility"]
    assert any(issue.code == "SLUG_FILENAME_MISMATCH" for issue in inspection.issues)
