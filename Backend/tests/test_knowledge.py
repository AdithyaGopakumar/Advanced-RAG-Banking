"""
Tests for the knowledge domain module — models, identity, and hashing.
"""

from datetime import date

import pytest

from app.modules.knowledge.identity import (
    content_hash,
    generate_chunk_id,
    generate_section_id,
    slugify_heading,
)
from app.modules.knowledge.models import (
    Category,
    ChunkMetadata,
    ChunkProvenance,
    ChunkType,
    DocumentStatus,
    DocumentType,
    Domain,
    KnowledgeChunk,
    KnowledgeDocument,
    KnowledgeRelationship,
    KnowledgeSection,
    Priority,
    RelationshipType,
)


# ──────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────


@pytest.fixture
def sample_metadata() -> ChunkMetadata:
    """Typical chunk metadata for a savings-account product chunk."""
    return ChunkMetadata(
        domain=Domain.PRODUCTS,
        category=Category.ACCOUNTS,
        sub_category="savings-account",
        document_type=DocumentType.PRODUCT,
        product="savings-account",
        customer_segment="retail",
        channel="all",
        keywords=["savings account", "interest rate", "minimum balance"],
        tags=["product:savings-account", "segment:retail"],
        search_aliases=["SB account", "savings bank account"],
        priority=Priority.HIGH,
        status=DocumentStatus.PUBLISHED,
    )


@pytest.fixture
def sample_provenance() -> ChunkProvenance:
    return ChunkProvenance(
        source="RBI Master Direction on SB Accounts",
        document_version="1.0",
        section="eligibility",
        source_location="docs/accounts/savings-account.md",
    )


@pytest.fixture
def sample_chunk(sample_metadata, sample_provenance) -> KnowledgeChunk:
    """A fully populated chunk with metadata, provenance, and relationships."""
    text = (
        "To open a Savings Account with the Bank, you must be an Indian "
        "resident aged 18 years or above with a valid KYC document."
    )
    return KnowledgeChunk(
        chunk_id="ACCT-SA-001::eligibility::000",
        document_id="ACCT-SA-001",
        section_id="ACCT-SA-001::eligibility",
        chunk_type=ChunkType.PARAGRAPH,
        position=0,
        text=text,
        content_hash=content_hash(text),
        metadata=sample_metadata,
        provenance=sample_provenance,
        relationships=[
            KnowledgeRelationship(
                relationship_type=RelationshipType.GOVERNED_BY,
                target_id="POL-KYC-001",
            ),
            KnowledgeRelationship(
                relationship_type=RelationshipType.REQUIRES,
                target_id="FORM-ACCT-001",
            ),
        ],
    )


# ──────────────────────────────────────────────
# Slugify
# ──────────────────────────────────────────────


class TestSlugify:
    def test_basic_heading(self):
        assert slugify_heading("Eligibility") == "eligibility"

    def test_multi_word(self):
        assert slugify_heading("Eligibility for Home Loan") == "eligibility-for-home-loan"

    def test_special_characters(self):
        assert slugify_heading("Interest Rates (2026)") == "interest-rates-2026"

    def test_question_format(self):
        result = slugify_heading("Q: What is the minimum balance?")
        assert result == "q-what-is-the-minimum-balance"

    def test_unicode_normalization(self):
        # é → e after NFKD normalization
        assert slugify_heading("Résumé") == "resume"

    def test_leading_trailing_hyphens_stripped(self):
        assert slugify_heading("--heading--") == "heading"


# ──────────────────────────────────────────────
# Deterministic Identity
# ──────────────────────────────────────────────


class TestGenerateSectionId:
    def test_basic(self):
        result = generate_section_id("ACCT-SA-001", "eligibility")
        assert result == "ACCT-SA-001::eligibility"

    def test_deterministic(self):
        """Same inputs must produce the same ID."""
        a = generate_section_id("LOAN-HL-001", "interest-rates")
        b = generate_section_id("LOAN-HL-001", "interest-rates")
        assert a == b

    def test_different_inputs_different_ids(self):
        a = generate_section_id("ACCT-SA-001", "eligibility")
        b = generate_section_id("ACCT-SA-001", "features")
        assert a != b

    def test_empty_document_id_raises(self):
        with pytest.raises(ValueError, match="document_id"):
            generate_section_id("", "eligibility")

    def test_empty_heading_slug_raises(self):
        with pytest.raises(ValueError, match="heading_slug"):
            generate_section_id("ACCT-SA-001", "")


class TestGenerateChunkId:
    def test_basic(self):
        result = generate_chunk_id("ACCT-SA-001", "eligibility", 0)
        assert result == "ACCT-SA-001::eligibility::000"

    def test_position_padding(self):
        result = generate_chunk_id("ACCT-SA-001", "features", 42)
        assert result == "ACCT-SA-001::features::042"

    def test_deterministic(self):
        """Same inputs must produce the same ID."""
        a = generate_chunk_id("LOAN-HL-001", "interest-rates", 3)
        b = generate_chunk_id("LOAN-HL-001", "interest-rates", 3)
        assert a == b

    def test_different_position_different_id(self):
        a = generate_chunk_id("ACCT-SA-001", "eligibility", 0)
        b = generate_chunk_id("ACCT-SA-001", "eligibility", 1)
        assert a != b

    def test_empty_document_id_raises(self):
        with pytest.raises(ValueError, match="document_id"):
            generate_chunk_id("", "eligibility", 0)

    def test_empty_section_slug_raises(self):
        with pytest.raises(ValueError, match="section_slug"):
            generate_chunk_id("ACCT-SA-001", "", 0)

    def test_negative_position_raises(self):
        with pytest.raises(ValueError, match="position"):
            generate_chunk_id("ACCT-SA-001", "eligibility", -1)


# ──────────────────────────────────────────────
# Content Hash
# ──────────────────────────────────────────────


class TestContentHash:
    def test_deterministic(self):
        """Same text must produce the same hash."""
        text = "The minimum balance is ₹5,000."
        assert content_hash(text) == content_hash(text)

    def test_different_text_different_hash(self):
        a = content_hash("Version 1 content")
        b = content_hash("Version 2 content")
        assert a != b

    def test_returns_64_char_hex(self):
        result = content_hash("test")
        assert len(result) == 64
        assert all(c in "0123456789abcdef" for c in result)

    def test_empty_string(self):
        """Empty string should still produce a valid hash."""
        result = content_hash("")
        assert len(result) == 64

    def test_unicode(self):
        """Unicode content should hash correctly."""
        result = content_hash("₹5,000 — savings account")
        assert len(result) == 64


# ──────────────────────────────────────────────
# Model Validation
# ──────────────────────────────────────────────


class TestKnowledgeDocument:
    def test_valid_document(self):
        doc = KnowledgeDocument(
            document_id="ACCT-SA-001",
            title="Savings Account",
            slug="savings-account",
            domain=Domain.PRODUCTS,
            category=Category.ACCOUNTS,
            sub_category="savings-account",
            document_type=DocumentType.PRODUCT,
            version="1.0",
            status=DocumentStatus.PUBLISHED,
        )
        assert doc.document_id == "ACCT-SA-001"
        assert doc.domain == Domain.PRODUCTS

    def test_missing_required_field(self):
        with pytest.raises(Exception):  # ValidationError
            KnowledgeDocument(
                document_id="ACCT-SA-001",
                # missing title, slug, domain, etc.
            )

    def test_invalid_domain_rejected(self):
        with pytest.raises(Exception):  # ValidationError
            KnowledgeDocument(
                document_id="ACCT-SA-001",
                title="Test",
                slug="test",
                domain="not-a-domain",
                category=Category.ACCOUNTS,
                sub_category="test",
                document_type=DocumentType.PRODUCT,
                version="1.0",
                status=DocumentStatus.DRAFT,
            )

    def test_related_documents_default_empty(self):
        doc = KnowledgeDocument(
            document_id="ACCT-SA-001",
            title="Test",
            slug="test",
            domain=Domain.PRODUCTS,
            category=Category.ACCOUNTS,
            sub_category="test",
            document_type=DocumentType.PRODUCT,
            version="1.0",
            status=DocumentStatus.DRAFT,
        )
        assert doc.related_documents == []


class TestKnowledgeSection:
    def test_valid_section(self):
        section = KnowledgeSection(
            section_id="ACCT-SA-001::eligibility",
            document_id="ACCT-SA-001",
            heading="Eligibility for Savings Account",
            level=2,
            position=1,
        )
        assert section.level == 2

    def test_invalid_heading_level_rejected(self):
        with pytest.raises(Exception):  # ValidationError
            KnowledgeSection(
                section_id="ACCT-SA-001::test",
                document_id="ACCT-SA-001",
                heading="Test",
                level=1,  # H1 is not allowed (min=2)
                position=0,
            )

    def test_negative_position_rejected(self):
        with pytest.raises(Exception):  # ValidationError
            KnowledgeSection(
                section_id="ACCT-SA-001::test",
                document_id="ACCT-SA-001",
                heading="Test",
                level=2,
                position=-1,
            )


# ──────────────────────────────────────────────
# Provenance
# ──────────────────────────────────────────────


class TestProvenance:
    def test_provenance_attached_to_chunk(self, sample_chunk):
        """Provenance must remain attached to the retrieval artifact."""
        assert sample_chunk.provenance.document_version == "1.0"
        assert sample_chunk.provenance.section == "eligibility"
        assert sample_chunk.provenance.source_location == "docs/accounts/savings-account.md"

    def test_provenance_source_optional(self):
        prov = ChunkProvenance(
            document_version="1.0",
            section="overview",
            source_location="docs/accounts/savings-account.md",
        )
        assert prov.source is None

    def test_provenance_traceback_chain(self, sample_chunk):
        """A chunk should carry enough information to trace back to the source."""
        chunk = sample_chunk
        # Chunk → Section (via section_id)
        assert chunk.section_id == "ACCT-SA-001::eligibility"
        # Section → Document (via document_id)
        assert chunk.document_id == "ACCT-SA-001"
        # Document → Source (via provenance)
        assert chunk.provenance.source == "RBI Master Direction on SB Accounts"
        # Document → Version (via provenance)
        assert chunk.provenance.document_version == "1.0"


# ──────────────────────────────────────────────
# Relationships
# ──────────────────────────────────────────────


class TestRelationships:
    def test_typed_relationship_validates(self):
        rel = KnowledgeRelationship(
            relationship_type=RelationshipType.GOVERNED_BY,
            target_id="POL-KYC-001",
        )
        assert rel.relationship_type == RelationshipType.GOVERNED_BY
        assert rel.target_id == "POL-KYC-001"

    def test_invalid_relationship_type_rejected(self):
        with pytest.raises(Exception):  # ValidationError
            KnowledgeRelationship(
                relationship_type="not-a-valid-type",
                target_id="SOME-ID",
            )

    def test_chunk_carries_relationships(self, sample_chunk):
        """Typed relationships should be attached to the chunk."""
        assert len(sample_chunk.relationships) == 2
        types = {r.relationship_type for r in sample_chunk.relationships}
        assert RelationshipType.GOVERNED_BY in types
        assert RelationshipType.REQUIRES in types

    def test_empty_relationships_allowed(self, sample_metadata, sample_provenance):
        """A chunk with no relationships should be valid."""
        chunk = KnowledgeChunk(
            chunk_id="ACCT-SA-001::overview::000",
            document_id="ACCT-SA-001",
            section_id="ACCT-SA-001::overview",
            chunk_type=ChunkType.PARAGRAPH,
            position=0,
            text="Overview text.",
            content_hash=content_hash("Overview text."),
            metadata=sample_metadata,
            provenance=sample_provenance,
            relationships=[],
        )
        assert chunk.relationships == []


# ──────────────────────────────────────────────
# Chunk — full integration
# ──────────────────────────────────────────────


class TestKnowledgeChunk:
    def test_full_chunk_creation(self, sample_chunk):
        """A fully populated chunk should validate successfully."""
        assert sample_chunk.chunk_id == "ACCT-SA-001::eligibility::000"
        assert sample_chunk.document_id == "ACCT-SA-001"
        assert sample_chunk.section_id == "ACCT-SA-001::eligibility"
        assert sample_chunk.chunk_type == ChunkType.PARAGRAPH
        assert sample_chunk.position == 0
        assert len(sample_chunk.text) > 0
        assert len(sample_chunk.content_hash) == 64

    def test_metadata_structurally_separate(self, sample_chunk):
        """Metadata should be accessible as a nested object, not embedded in text."""
        assert sample_chunk.metadata.domain == Domain.PRODUCTS
        assert sample_chunk.metadata.priority == Priority.HIGH
        assert "savings account" in sample_chunk.metadata.keywords

    def test_content_hash_matches_text(self, sample_chunk):
        """The stored hash must match the hash of the actual text."""
        expected = content_hash(sample_chunk.text)
        assert sample_chunk.content_hash == expected

    def test_hierarchy_ids_link_correctly(self, sample_chunk):
        """Document → Section → Chunk IDs should form a consistent hierarchy."""
        chunk = sample_chunk
        # Chunk ID contains document ID
        assert chunk.chunk_id.startswith(chunk.document_id)
        # Chunk ID contains section slug
        assert chunk.section_id.startswith(chunk.document_id)
        # Section ID is a prefix of chunk ID (minus position)
        chunk_prefix = "::".join(chunk.chunk_id.split("::")[:2])
        assert chunk_prefix == chunk.section_id


class TestChunkMetadata:
    def test_temporal_validity(self):
        meta = ChunkMetadata(
            domain=Domain.REFERENCE_DATA,
            category=Category.INTEREST_RATES,
            sub_category="deposit-interest-rates",
            document_type=DocumentType.REFERENCE,
            effective_from=date(2026, 8, 1),
            effective_until=date(2027, 8, 1),
        )
        assert meta.effective_from == date(2026, 8, 1)
        assert meta.effective_until == date(2027, 8, 1)

    def test_defaults(self):
        meta = ChunkMetadata(
            domain=Domain.PRODUCTS,
            category=Category.ACCOUNTS,
            sub_category="savings-account",
            document_type=DocumentType.PRODUCT,
        )
        assert meta.priority == Priority.MEDIUM
        assert meta.region == "IN"
        assert meta.language == "en"
        assert meta.keywords == []
        assert meta.tags == []
