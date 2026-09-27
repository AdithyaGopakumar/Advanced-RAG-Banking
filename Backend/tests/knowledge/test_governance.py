"""Governance build tests for corpus status, hashes, and conflicts."""

from datetime import date
from pathlib import Path

from app.modules.knowledge.governance import build_knowledge

KNOWLEDGE_ROOT = Path(__file__).resolve().parents[3] / "knowledge-base"
AS_OF = date(2026, 9, 27)


def _article(
    *,
    document_id: str,
    slug: str,
    status: str = "current",
    version: str = "1.0",
    body: str = "# Savings\n\n## Overview\n\nResident individuals.\n",
    extra: str = "",
    sub_category: str = "savings-account",
) -> str:
    return (
        "---\n"
        f'id: "{document_id}"\n'
        'title: "Savings"\n'
        f'slug: "{slug}"\n'
        "document_type: product\n"
        f'sub_category: "{sub_category}"\n'
        f'version: "{version}"\n'
        f'status: "{status}"\n'
        'owner: "Retail Banking SME"\n'
        f"{extra}"
        "---\n\n"
        f"{body}"
    )


def test_corpus_uses_approved_and_current_as_live_knowledge():
    build = build_knowledge(KNOWLEDGE_ROOT, as_of=AS_OF)
    by_id = {record.document_id: record for record in build.documents}

    bsbda = by_id["ACCT-BSBDA-001"]
    charges = by_id["CHG-ACCT-001"]
    card = by_id["CARD-CC-001"]
    faq = by_id["FAQ-ACCT-001"]

    assert bsbda.status == "approved"
    assert bsbda.eligible is True
    assert charges.status == "current"
    assert charges.eligible is True
    assert card.status == "draft"
    assert card.eligible is False
    assert any(issue.code == "STATUS_NOT_ELIGIBLE" for issue in card.issues)
    assert faq.eligible is True
    assert any(issue.code == "TITLE_H1_MISMATCH" for issue in faq.issues)

    assert all(chunk.content_hash for chunk in build.chunks)
    eligible_ids = [chunk.chunk_id for chunk in build.eligible_chunks]
    assert len(eligible_ids) == len(set(eligible_ids))
    assert all(chunk.document_id != "CARD-CC-001" for chunk in build.eligible_chunks)
    assert build.manifest_hash == build_knowledge(KNOWLEDGE_ROOT, as_of=AS_OF).manifest_hash


def test_published_is_not_treated_as_live(tmp_path: Path):
    source = tmp_path / "savings.md"
    source.write_text(
        _article(document_id="ACCT-X-001", slug="savings", status="published"),
        encoding="utf-8",
    )

    record = build_knowledge(tmp_path, as_of=AS_OF).documents[0]

    assert record.status == "published"
    assert record.eligible is False
    assert any(issue.code == "STATUS_NOT_ELIGIBLE" for issue in record.issues)


def test_blank_effective_until_stays_open(tmp_path: Path):
    source = tmp_path / "savings.md"
    source.write_text(
        _article(
            document_id="ACCT-X-001",
            slug="savings",
            extra='effective_from: "2026-08-01"\neffective_until: ""\n',
        ),
        encoding="utf-8",
    )

    record = build_knowledge(tmp_path, as_of=AS_OF).documents[0]

    assert record.eligible is True
    assert not any(issue.code == "INVALID_DATE" for issue in record.issues)


def test_future_and_invalid_windows_are_not_eligible(tmp_path: Path):
    future = tmp_path / "future.md"
    future.write_text(
        _article(
            document_id="ACCT-X-001",
            slug="future",
            extra='effective_from: "2026-10-01"\n',
        ),
        encoding="utf-8",
    )
    invalid = tmp_path / "invalid.md"
    invalid.write_text(
        _article(
            document_id="ACCT-X-002",
            slug="invalid",
            version="1",
            extra='effective_from: "2026-09-01"\neffective_until: "2026-01-01"\n',
        ),
        encoding="utf-8",
    )

    records = {record.document_id: record for record in build_knowledge(tmp_path, as_of=AS_OF).documents}

    assert records["ACCT-X-001"].eligible is False
    assert any(issue.code == "NOT_YET_EFFECTIVE" for issue in records["ACCT-X-001"].issues)
    assert records["ACCT-X-002"].eligible is False
    assert any(issue.code == "INVALID_VERSION" for issue in records["ACCT-X-002"].issues)
    assert any(issue.code == "INVALID_EFFECTIVE_WINDOW" for issue in records["ACCT-X-002"].issues)


def test_duplicate_ids_are_kept_and_not_selected(tmp_path: Path):
    (tmp_path / "one.md").write_text(
        _article(document_id="ACCT-X-001", slug="one", body="# Savings\n\n## Overview\n\nFirst copy.\n"),
        encoding="utf-8",
    )
    (tmp_path / "two.md").write_text(
        _article(document_id="ACCT-X-001", slug="two", body="# Savings\n\n## Overview\n\nSecond copy.\n"),
        encoding="utf-8",
    )

    build = build_knowledge(tmp_path, as_of=AS_OF)

    assert [record.eligible for record in build.documents] == [False, False]
    assert build.duplicates[0].code == "DUPLICATE_DOCUMENT_ID"
    assert build.eligible_chunks == []


def test_identical_bodies_are_reported_without_being_dropped(tmp_path: Path):
    body = "# Savings\n\n## Overview\n\nThe same governed text.\n"
    (tmp_path / "one.md").write_text(
        _article(document_id="ACCT-X-001", slug="one", body=body),
        encoding="utf-8",
    )
    (tmp_path / "two.md").write_text(
        _article(document_id="ACCT-X-002", slug="two", body=body),
        encoding="utf-8",
    )

    build = build_knowledge(tmp_path, as_of=AS_OF)

    assert all(record.eligible for record in build.documents)
    assert build.documents[0].content_hash == build.documents[1].content_hash
    assert build.duplicates[0].code == "DUPLICATE_CONTENT"
    assert set(build.duplicates[0].document_ids) == {"ACCT-X-001", "ACCT-X-002"}


def test_amount_conflicts_are_reported_without_a_winner(tmp_path: Path):
    (tmp_path / "one.md").write_text(
        _article(
            document_id="ACCT-X-001",
            slug="one",
            body="# Savings\n\n## Fees\n\nThe fee is ₹100.\n",
        ),
        encoding="utf-8",
    )
    (tmp_path / "two.md").write_text(
        _article(
            document_id="ACCT-X-002",
            slug="two",
            body="# Savings\n\n## Fees\n\nThe fee is ₹150.\n",
        ),
        encoding="utf-8",
    )

    build = build_knowledge(tmp_path, as_of=AS_OF)
    conflict = build.contradictions[0]

    assert all(record.eligible for record in build.documents)
    assert conflict.code == "CONTRADICTORY_AMOUNT"
    assert conflict.amounts == ["100", "150"]
    assert set(conflict.document_ids) == {"ACCT-X-001", "ACCT-X-002"}


def test_content_hash_changes_when_the_body_changes(tmp_path: Path):
    source = tmp_path / "savings.md"
    source.write_text(
        _article(document_id="ACCT-X-001", slug="savings"),
        encoding="utf-8",
    )
    before = build_knowledge(tmp_path, as_of=AS_OF)

    source.write_text(
        _article(
            document_id="ACCT-X-001",
            slug="savings",
            body="# Savings\n\n## Overview\n\nResident individuals only.\n",
        ),
        encoding="utf-8",
    )
    after = build_knowledge(tmp_path, as_of=AS_OF)

    assert before.documents[0].content_hash != after.documents[0].content_hash
    assert before.chunks[0].content_hash != after.chunks[0].content_hash


def test_malformed_table_is_a_warning_and_stays_eligible(tmp_path: Path):
    source = tmp_path / "savings.md"
    source.write_text(
        _article(
            document_id="ACCT-X-001",
            slug="savings",
            body="# Savings\n\n## Fees\n\n| Item | Amount |\n|---|---|\n| Cheque book |\n",
        ),
        encoding="utf-8",
    )

    record = build_knowledge(tmp_path, as_of=AS_OF).documents[0]

    assert record.eligible is True
    assert any(issue.code == "TABLE_SHAPE" for issue in record.issues)
