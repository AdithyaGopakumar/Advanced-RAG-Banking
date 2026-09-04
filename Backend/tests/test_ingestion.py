"""
Tests for the knowledge ingestion pipeline (Phase 1A).
"""
import pytest
from pathlib import Path

from app.ingestion.discovery import discover_knowledge_files
from app.ingestion.parser import (
    parse_knowledge_file,
    extract_sections,
    MissingFrontMatterError,
    MalformedYAMLError,
)
from app.ingestion.normalizer import normalize_document
from app.ingestion.pipeline import run_ingestion, DuplicateDocumentIDError
from app.modules.knowledge.models import DocumentStatus

# ──────────────────────────────────────────────
# Discovery Tests
# ──────────────────────────────────────────────

def test_discovery_finds_md_files(tmp_path: Path):
    (tmp_path / "doc1.md").touch()
    (tmp_path / "doc2.md").touch()
    (tmp_path / "not_doc.txt").touch()
    sub_dir = tmp_path / "sub"
    sub_dir.mkdir()
    (sub_dir / "doc3.md").touch()

    files = discover_knowledge_files(tmp_path)
    
    # Should find 3 markdown files
    assert len(files) == 3
    # Should be deterministically sorted
    assert files[0].name == "doc1.md"
    assert files[1].name == "doc2.md"
    assert files[2].name == "doc3.md"

def test_discovery_ignores_hidden_dirs(tmp_path: Path):
    hidden = tmp_path / ".git"
    hidden.mkdir()
    (hidden / "hidden.md").touch()
    (tmp_path / "visible.md").touch()

    files = discover_knowledge_files(tmp_path)
    assert len(files) == 1
    assert files[0].name == "visible.md"


# ──────────────────────────────────────────────
# Parser Tests
# ──────────────────────────────────────────────

def test_parse_valid_knowledge_file(tmp_path: Path):
    file_path = tmp_path / "valid.md"
    content = """---
id: TEST-001
title: Test Document
---
# Heading
Content here
"""
    file_path.write_text(content, encoding="utf-8")
    
    fm, md = parse_knowledge_file(file_path)
    
    assert fm["id"] == "TEST-001"
    assert fm["title"] == "Test Document"
    assert md.strip() == "# Heading\nContent here"

def test_parse_missing_front_matter(tmp_path: Path):
    file_path = tmp_path / "missing.md"
    file_path.write_text("# Just markdown", encoding="utf-8")
    
    with pytest.raises(MissingFrontMatterError):
        parse_knowledge_file(file_path)

def test_parse_malformed_yaml(tmp_path: Path):
    file_path = tmp_path / "malformed.md"
    content = """---
id: [unclosed list
title: Test
---
# Heading
"""
    file_path.write_text(content, encoding="utf-8")
    
    with pytest.raises(MalformedYAMLError):
        parse_knowledge_file(file_path)

def test_extract_sections_hierarchy():
    markdown = """
# Document Title
Intro text

## Section 1
Content 1

### Subsection 1.1
Content 1.1

## Section 2
Content 2
"""
    sections = extract_sections(markdown.strip())
    
    assert len(sections) == 4
    
    # Section 1: H1 (Root context)
    assert sections[0][0] == "Document Title"
    assert sections[0][1] == 1
    assert "Intro text" in sections[0][2]
    
    # Section 2: H2
    assert sections[1][0] == "Section 1"
    assert sections[1][1] == 2
    assert "Content 1" in sections[1][2]
    
    # Section 3: H3
    assert sections[2][0] == "Subsection 1.1"
    assert sections[2][1] == 3
    assert "Content 1.1" in sections[2][2]
    
    # Section 4: H2
    assert sections[3][0] == "Section 2"
    assert sections[3][1] == 2
    assert "Content 2" in sections[3][2]

def test_extract_sections_preserves_structure():
    markdown = """## Lists and Tables
- Item 1
- Item 2

| A | B |
|---|---|
| 1 | 2 |

> Blockquote
"""
    sections = extract_sections(markdown.strip())
    assert len(sections) == 1
    content = sections[0][2]
    assert "- Item 1" in content
    assert "| A | B |" in content
    assert "> Blockquote" in content

def test_extract_sections_ignores_code_blocks():
    markdown = """## Real Section
```bash
# This is a comment, not an H1
echo "Hello"
```
### Another Section
"""
    sections = extract_sections(markdown.strip())
    assert len(sections) == 2
    assert sections[0][0] == "Real Section"
    assert sections[1][0] == "Another Section"


# ──────────────────────────────────────────────
# Normalizer Tests
# ──────────────────────────────────────────────

@pytest.fixture
def valid_front_matter():
    return {
        "id": "ACCT-001",
        "title": "Account",
        "slug": "account",
        "version": "1.0",
        "domain": "products",
        "category": "accounts",
        "sub_category": "savings",
        "document_type": "product",
        "owner": "Banking Ops",
        "status": "published",
        "source": "Internal",
        "relationships": [
            {"type": "governed_by", "target_id": "POL-001"}
        ]
    }

def test_normalize_valid_document(tmp_path: Path, valid_front_matter):
    md = "# Account\n## Eligibility\nText."
    sections = [("Account", 1, "# Account"), ("Eligibility", 2, "## Eligibility\nText.")]
    
    doc = normalize_document(tmp_path / "test.md", valid_front_matter, md, sections)
    
    assert doc.document_id == "ACCT-001"
    assert doc.metadata.domain == "products"
    assert doc.provenance.version == "1.0"
    assert doc.content == md
    assert len(doc.sections) == 2
    assert doc.sections[1].heading == "Eligibility"
    assert doc.sections[1].level == 2
    assert len(doc.relationships) == 1
    assert doc.relationships[0].target_id == "POL-001"

def test_normalize_tracks_parent_section(tmp_path: Path, valid_front_matter):
    sections = [
        ("Account", 1, "# Account"),
        ("Features", 2, "## Features"),
        ("Debit Card", 3, "### Debit Card"),
        ("Fees", 2, "## Fees")
    ]
    doc = normalize_document(tmp_path / "test.md", valid_front_matter, "", sections)
    
    assert len(doc.sections) == 4
    
    # H1
    assert doc.sections[0].parent_section_id is None
    
    # H2 (Features) -> parent is H1
    h1_id = doc.sections[0].section_id
    assert doc.sections[1].parent_section_id == h1_id
    
    # H3 (Debit Card) -> parent is H2 (Features)
    h2_features_id = doc.sections[1].section_id
    assert doc.sections[2].parent_section_id == h2_features_id
    
    # H2 (Fees) -> parent is H1
    assert doc.sections[3].parent_section_id == h1_id


# ──────────────────────────────────────────────
# Pipeline Tests
# ──────────────────────────────────────────────

def test_pipeline_detects_duplicate_ids(tmp_path: Path):
    content1 = """---
id: DUP-001
title: Doc 1
slug: doc-1
domain: products
category: accounts
sub_category: savings
document_type: product
owner: Ops
---
"""
    content2 = """---
id: DUP-001
title: Doc 2
slug: doc-2
domain: products
category: accounts
sub_category: savings
document_type: product
owner: Ops
---
"""
    (tmp_path / "file1.md").write_text(content1, encoding="utf-8")
    (tmp_path / "file2.md").write_text(content2, encoding="utf-8")
    
    with pytest.raises(DuplicateDocumentIDError):
        run_ingestion(tmp_path)
