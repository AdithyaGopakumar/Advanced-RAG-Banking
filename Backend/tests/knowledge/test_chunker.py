"""Chunking tests for section, scenario, table, and procedure behavior."""

from pathlib import Path

from app.modules.knowledge.chunker import chunk_document
from app.modules.knowledge.loader import load_document
from app.modules.knowledge.models import DocumentMetadata, KnowledgeDocument, KnowledgeSection

KNOWLEDGE_ROOT = Path(__file__).resolve().parents[3] / "knowledge-base"
BSBDA = KNOWLEDGE_ROOT / "docs" / "accounts" / "bsbda.md"
ACCOUNTS_FAQ = KNOWLEDGE_ROOT / "faqs" / "accounts-faq.md"
LOST_CARD = KNOWLEDGE_ROOT / "scenarios" / "lost-card-replacement.md"
ACCOUNT_GUIDE = KNOWLEDGE_ROOT / "decision-guides" / "choose-right-account.md"


def _metadata(**overrides: object) -> DocumentMetadata:
    values: dict[str, object] = {
        "id": "ACCT-X-001",
        "title": "Savings",
        "slug": "savings",
        "document_type": "product",
        "version": "1.0",
        "status": "approved",
        "region": "IN",
        "sub_category": "savings-account",
        "target_audience": "customer",
    }
    values.update(overrides)
    return DocumentMetadata.model_validate(values)


def _section(
    heading: str,
    content: str,
    *,
    level: int = 2,
    path: list[str] | None = None,
    section_id: str = "ACCT-X-001#s0001",
) -> KnowledgeSection:
    return KnowledgeSection(
        section_id=section_id,
        document_id="ACCT-X-001",
        heading=heading,
        heading_level=level,
        heading_path=path or ["Savings", heading],
        content=content,
        source_location="docs/accounts/savings.md:1-2",
    )


def _document(
    sections: list[KnowledgeSection],
    *,
    document_type: str = "product",
    h1: str = "Savings",
) -> KnowledgeDocument:
    return KnowledgeDocument(
        document_id="ACCT-X-001",
        metadata=_metadata(document_type=document_type),
        h1=h1,
        sections=sections,
        source_path="docs/accounts/savings.md",
    )


def test_bsbda_eligibility_chunk_keeps_the_table_and_breadcrumbs():
    document = load_document(BSBDA, knowledge_root=KNOWLEDGE_ROOT)
    chunks = chunk_document(document)
    eligibility = next(
        chunk
        for chunk in chunks
        if chunk.heading_path[-1] == "Eligibility"
    )

    assert eligibility.text.startswith(
        "# Basic Savings Bank Deposit Account (BSBDA)\n## Eligibility\n\n"
    )
    assert "| Age | 18 years and above" in eligibility.content
    assert "| Residency | Resident Indian |" in eligibility.text
    assert eligibility.chunk_type == "section"
    assert eligibility.section_id == "ACCT-BSBDA-001#s0005"
    assert eligibility.status == "approved"
    assert eligibility.document_version == "1.0"
    assert eligibility.jurisdiction == "IN"
    assert eligibility.product == "basic-savings-bank-deposit-account"
    assert eligibility.oversized is False
    assert not eligibility.content.startswith("#")


def test_empty_parent_section_is_not_its_own_chunk():
    document = load_document(BSBDA, knowledge_root=KNOWLEDGE_ROOT)
    chunks = chunk_document(document)
    title = "Basic Savings Bank Deposit Account (BSBDA)"

    assert all(
        chunk.heading_path != [title, "Features and Benefits"]
        for chunk in chunks
    )
    features = next(chunk for chunk in chunks if chunk.heading_path[-1] == "Key features")
    assert features.heading_path == [
        title,
        "Features and Benefits",
        "Key features",
    ]
    assert features.text.startswith(
        f"# {title}\n## Features and Benefits\n### Key features\n\n"
    )


def test_chunk_identifiers_are_deterministic():
    document = load_document(BSBDA, knowledge_root=KNOWLEDGE_ROOT)
    first = chunk_document(document)
    second = chunk_document(document)

    assert [chunk.model_dump() for chunk in first] == [chunk.model_dump() for chunk in second]
    assert [chunk.chunk_id for chunk in first] == [
        f"ACCT-BSBDA-001#c{index:04d}" for index in range(len(first))
    ]
    assert len({chunk.chunk_id for chunk in first}) == len(first)


def test_scenario_and_decision_guide_stay_one_chunk_when_they_fit():
    scenario = chunk_document(load_document(LOST_CARD, knowledge_root=KNOWLEDGE_ROOT))
    guide = chunk_document(load_document(ACCOUNT_GUIDE, knowledge_root=KNOWLEDGE_ROOT))

    assert len(scenario) == 1
    assert scenario[0].chunk_type == "scenario"
    assert "## Situation" in scenario[0].text
    assert "Unauthorized Transactions" in scenario[0].text
    assert "Card Temporarily Misplaced" in scenario[0].text

    assert len(guide) == 1
    assert guide[0].chunk_type == "decision_guide"
    assert "## Decision Logic" in guide[0].text
    assert "## Exceptions" in guide[0].text


def test_faq_answer_is_its_own_chunk():
    document = load_document(ACCOUNTS_FAQ, knowledge_root=KNOWLEDGE_ROOT)
    chunks = chunk_document(document)
    opening = next(chunk for chunk in chunks if "How do I open a savings account?" in chunk.text)

    assert opening.heading_path[-1] == "Intent: `open_account`"
    assert opening.document_title == document.h1


def test_table_is_not_split_when_the_section_exceeds_the_budget():
    table = "\n".join(
        [
            "Fees for this savings account are listed below.",
            "",
            "| Item | Amount |",
            "|---|---|",
            "| Cheque book | 100 |",
            "| Duplicate statement | 50 |",
        ]
    )
    document = _document([_section("Fees", table)])
    chunks = chunk_document(document, max_size=80)

    assert len(chunks) == 1
    assert chunks[0].chunk_type == "table"
    assert chunks[0].oversized is True
    assert "| Cheque book | 100 |" in chunks[0].content
    assert "| Duplicate statement | 50 |" in chunks[0].content
    assert "Fees for this savings account are listed below." in chunks[0].content


def test_procedure_splits_only_between_steps():
    steps = "\n".join(
        f"{number}. Complete step {number} with the required documents."
        for number in range(1, 7)
    )
    document = _document([_section("How to Apply", f"Follow these steps.\n\n{steps}")])
    chunks = chunk_document(document, max_size=160)

    assert len(chunks) > 1
    assert all(chunk.chunk_type == "procedure" for chunk in chunks)
    assert chunks[0].procedure_step_start == 1
    assert "Follow these steps." in chunks[0].content
    assert "Follow these steps." not in chunks[1].content
    numbers: list[int] = []
    for chunk in chunks:
        assert chunk.procedure_step_start is not None
        assert chunk.procedure_step_end is not None
        assert chunk.procedure_step_start <= chunk.procedure_step_end
        found = [
            number
            for number in range(1, 7)
            if f"{number}. Complete step {number}" in chunk.content
        ]
        assert found == list(range(chunk.procedure_step_start, chunk.procedure_step_end + 1))
        numbers.extend(found)
    assert numbers == [1, 2, 3, 4, 5, 6]


def test_paragraphs_stay_intact_when_the_section_is_split():
    paragraphs = [
        "Alpha " * 12,
        "Beta " * 12,
        "Gamma " * 12,
    ]
    document = _document([_section("Overview", "\n\n".join(paragraphs))])
    chunks = chunk_document(document, max_size=180)

    assert len(chunks) >= 2
    for paragraph in paragraphs:
        owners = [chunk for chunk in chunks if paragraph.strip() in chunk.content]
        assert len(owners) == 1


def test_oversized_scenario_keeps_exception_text_together():
    situation = "The customer needs help. " * 40
    exceptions = "\n".join(
        [
            "- Unauthorized use routes to fraud reporting.",
            "- A misplaced card can be locked temporarily.",
        ]
    )
    document = _document(
        [
            _section("Situation", situation, section_id="ACCT-X-001#s0001"),
            _section(
                "Exceptions",
                exceptions,
                section_id="ACCT-X-001#s0002",
                path=["Savings", "Exceptions"],
            ),
        ],
        document_type="scenario",
        h1="Lost Card Scenario",
    )
    chunks = chunk_document(document, max_size=220)

    assert len(chunks) > 1
    assert all(chunk.document_type == "scenario" for chunk in chunks)
    exception_chunks = [chunk for chunk in chunks if "Unauthorized use" in chunk.content]
    assert len(exception_chunks) == 1
    assert "locked temporarily" in exception_chunks[0].content
