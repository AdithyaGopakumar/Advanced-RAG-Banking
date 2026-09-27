"""Parser tests against governed knowledge documents."""

from pathlib import Path

from app.modules.knowledge.loader import inspect_document, load_document

KNOWLEDGE_ROOT = Path(__file__).resolve().parents[3] / "knowledge-base"
BSBDA = KNOWLEDGE_ROOT / "docs" / "accounts" / "bsbda.md"
ACCOUNTS_FAQ = KNOWLEDGE_ROOT / "faqs" / "accounts-faq.md"
KYC_POLICY = KNOWLEDGE_ROOT / "docs" / "policies" / "kyc-policy.md"


def _section(document, heading: str):
    matches = [section for section in document.sections if section.heading == heading]
    assert len(matches) == 1
    return matches[0]


def test_bsbda_document_identity_and_heading_path():
    document = load_document(BSBDA, knowledge_root=KNOWLEDGE_ROOT)

    assert document.document_id == "ACCT-BSBDA-001"
    assert document.title == "Basic Savings Bank Deposit Account (BSBDA)"
    assert document.h1 == document.title
    assert document.metadata.status == "approved"
    assert document.metadata.version == "1.0"
    assert document.source_path == "docs/accounts/bsbda.md"

    eligibility = _section(document, "Eligibility")
    assert eligibility.heading_level == 2
    assert eligibility.heading_path == [
        "Basic Savings Bank Deposit Account (BSBDA)",
        "Eligibility",
    ]
    assert eligibility.section_id == "ACCT-BSBDA-001#s0005"
    assert "| Age | 18 years and above" in eligibility.content

    features = _section(document, "Key features")
    assert features.heading_path == [
        "Basic Savings Bank Deposit Account (BSBDA)",
        "Features and Benefits",
        "Key features",
    ]
    assert "- Zero Minimum Average Balance (MAB) requirement" in features.content
    assert not features.content.startswith("###")


def test_bsbda_preamble_is_not_a_section():
    document = load_document(BSBDA, knowledge_root=KNOWLEDGE_ROOT)

    assert document.sections[0].heading == "Overview"
    assert "## Overview" not in document.preamble
    assert all(section.heading != document.h1 for section in document.sections)


def test_parse_is_deterministic():
    first = load_document(BSBDA, knowledge_root=KNOWLEDGE_ROOT)
    second = load_document(BSBDA, knowledge_root=KNOWLEDGE_ROOT)

    assert first.model_dump() == second.model_dump()


def test_policy_sections_keep_original_markdown():
    document = load_document(KYC_POLICY, knowledge_root=KNOWLEDGE_ROOT)
    provisions = _section(document, "1. Customer Identification Program (CIP)")

    assert document.document_id == "POL-KYC-001"
    assert document.h1 == "KYC Policy"
    assert provisions.heading_path == [
        "KYC Policy",
        "Key Provisions",
        "1. Customer Identification Program (CIP)",
    ]
    assert "Prevention of Money Laundering Act, 2002 (PMLA)" in _section(
        document, "Regulatory Basis"
    ).content
    assert "**Officially Valid Documents (OVDs)**" in provisions.content


def test_faq_title_mismatch_is_a_warning_and_document_is_kept():
    inspection = inspect_document(ACCOUNTS_FAQ, knowledge_root=KNOWLEDGE_ROOT)

    assert inspection.accepted
    assert inspection.document is not None
    assert inspection.document.h1 == "Accounts — Frequently Asked Questions"
    assert any(issue.code == "TITLE_H1_MISMATCH" for issue in inspection.issues)
    assert any(issue.code == "MULTIPLE_H1" for issue in inspection.issues)
    opening = _section(inspection.document, "Intent: `open_account`")
    assert "How do I open a savings account?" in opening.content
    assert opening.heading_path == [
        inspection.document.h1,
        "1. Opening an Account",
        "Intent: `open_account`",
    ]
