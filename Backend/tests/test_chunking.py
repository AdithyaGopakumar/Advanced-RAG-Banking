"""
Tests for Knowledge-Type-Aware Chunking (Phase 1A / Step 2).
"""
import pytest

from app.ingestion.chunker import ChunkingEngine
from app.ingestion.splitter import controlled_split
from app.modules.knowledge.models import (
    Category,
    ChunkContext,
    DocumentMetadata,
    DocumentProvenance,
    DocumentStatus,
    DocumentType,
    Domain,
    KnowledgeDocument,
    KnowledgeSection,
    Priority,
    Confidentiality
)

def create_mock_doc(doc_type: DocumentType, sections_data: list[tuple[str, int, str]]) -> KnowledgeDocument:
    doc_id = "TEST-001"
    
    sections = []
    parent_id = None
    for i, (heading, level, content) in enumerate(sections_data):
        section_id = f"{doc_id}::sec-{i}"
        
        # Simple parent tracking for test
        if level > 1 and i > 0:
            parent_id = f"{doc_id}::sec-{i-1}"
            
        sections.append(
            KnowledgeSection(
                section_id=section_id,
                document_id=doc_id,
                heading=heading,
                level=level,
                position=i,
                content=content,
                parent_section_id=parent_id if level > 1 else None
            )
        )
        
    return KnowledgeDocument(
        document_id=doc_id,
        title="Test Document",
        slug="test-doc",
        metadata=DocumentMetadata(
            domain=Domain.PRODUCTS,
            category=Category.ACCOUNTS,
            sub_category="test",
            document_type=doc_type,
            owner="Test",
            status=DocumentStatus.PUBLISHED,
        ),
        provenance=DocumentProvenance(
            source="Test Source",
            source_location="test.md",
            version="1.0"
        ),
        content="",
        sections=sections
    )

def test_semantic_section_strategy():
    engine = ChunkingEngine(max_size=2000)
    sections_data = [
        ("Account", 1, "# Account\n\nIntro text."),
        ("Eligibility", 2, "## Eligibility\n\nMust be 18."),
        ("Age", 3, "### Age\n\n18+ years."),
    ]
    doc = create_mock_doc(DocumentType.PRODUCT, sections_data)
    chunks = engine.process(doc)
    
    assert len(chunks) == 3
    assert chunks[0].text == "# Account\n\nIntro text."
    assert chunks[1].text == "## Eligibility\n\nMust be 18."
    assert chunks[2].text == "### Age\n\n18+ years."
    
    # Check context preservation
    assert chunks[2].context.document_title == "Test Document"
    assert chunks[2].context.heading_path == ["Account", "Eligibility", "Age"]
    
def test_faq_strategy():
    engine = ChunkingEngine(max_size=2000)
    sections_data = [
        ("FAQ Overview", 1, "# FAQ Overview"),
        ("1. How to open?", 2, "## 1. How to open?\n\nOnline."),
        ("2. Fees?", 2, "## 2. Fees?\n\nZero."),
    ]
    doc = create_mock_doc(DocumentType.FAQ, sections_data)
    chunks = engine.process(doc)
    
    # Root section skipped if it's just the title
    assert len(chunks) == 2
    assert chunks[0].text == "## 1. How to open?\n\nOnline."
    assert chunks[1].text == "## 2. Fees?\n\nZero."

def test_scenario_strategy_reasonably_sized():
    engine = ChunkingEngine(max_size=2000)
    sections_data = [
        ("Account Upgrade", 1, "# Account Upgrade"),
        ("Situation", 2, "## Situation\n\nCustomer wants premium."),
        ("Action", 2, "## Action\n\nUpgrade them."),
    ]
    doc = create_mock_doc(DocumentType.SCENARIO, sections_data)
    chunks = engine.process(doc)
    
    # Combined into one cohesive chunk
    assert len(chunks) == 1
    assert "Customer wants premium." in chunks[0].text
    assert "Upgrade them." in chunks[0].text

def test_scenario_strategy_oversized_triggers_split():
    # Set a tiny max size to force the scenario to split
    engine = ChunkingEngine(max_size=15)
    sections_data = [
        ("Account Upgrade", 1, "# Account Upgrade"),
        ("Situation", 2, "## Situation\n\nCustomer wants premium."),
        ("Action", 2, "## Action\n\nUpgrade them."),
    ]
    doc = create_mock_doc(DocumentType.SCENARIO, sections_data)
    chunks = engine.process(doc)
    
    # Must be split due to size
    assert len(chunks) > 1

def test_decision_guide_strategy():
    engine = ChunkingEngine(max_size=2000)
    sections_data = [
        ("Guide", 1, "# Guide"),
        ("Condition A", 2, "## Condition A\n\nDecision A"),
        ("Condition B", 2, "## Condition B\n\nDecision B"),
    ]
    doc = create_mock_doc(DocumentType.DECISION_GUIDE, sections_data)
    chunks = engine.process(doc)
    
    # Skipped root, 2 chunks for decision rules
    assert len(chunks) == 2
    assert chunks[0].text == "## Condition A\n\nDecision A"
    assert chunks[1].text == "## Condition B\n\nDecision B"

def test_controlled_split_tables_intact():
    text = "Intro\n\n| H1 | H2 |\n|---|---|\n| 1 | 2 |\n\nOutro"
    # Max size too small for the whole thing, forces split
    segments = controlled_split(text, max_size=20)
    assert len(segments) > 1
    # Table should remain entirely intact in one chunk despite the strict size limit
    table_chunk = next(c for c in segments if "| H1 |" in c)
    assert "|---|---|" in table_chunk
    assert "| 1 | 2 |" in table_chunk

def test_controlled_split_list_items_intact():
    text = "Intro\n\n- Item 1\n- Item 2\n\nOutro"
    # Max size too small, forces split
    segments = controlled_split(text, max_size=15)
    assert len(segments) > 1
    # Fallback to single newline split preserves list item boundaries
    assert "- Item 1" in segments
    assert "- Item 2" in segments

def test_metadata_provenance_identity_determinism():
    engine = ChunkingEngine(max_size=2000)
    sections_data = [
        ("Rule", 2, "## Rule\n\nTest text."),
    ]
    doc = create_mock_doc(DocumentType.POLICY, sections_data)
    chunks1 = engine.process(doc)
    chunks2 = engine.process(doc)
    
    assert chunks1[0].chunk_id == chunks2[0].chunk_id
    assert chunks1[0].content_hash == chunks2[0].content_hash
    
    # Metadata check
    assert chunks1[0].metadata.document_type == DocumentType.POLICY
    assert chunks1[0].provenance.source == "Test Source"
