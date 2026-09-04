"""
Deterministic identity and content hashing for retrieval artifacts.

Provides:
    generate_chunk_id    — deterministic chunk identity
    generate_section_id  — deterministic section identity
    content_hash         — SHA-256 content fingerprint
    slugify_heading      — heading → URL-safe slug

Design rationale:
    - Deterministic IDs enable idempotent ingestion: re-processing the same
      knowledge source produces the same chunk IDs.
    - Content hashes enable change detection: if the text changes, the hash
      changes, signalling that downstream artifacts (embeddings, indexes)
      need updating.
    - Together they support reproducible indexing, debugging, and versioning
      without requiring a database for deduplication.
"""

import hashlib
import re
import unicodedata


def slugify_heading(heading: str) -> str:
    """Convert a section heading to a URL-safe slug.

    Matches the anchor-ID convention used by Markdown renderers and
    the knowledge-base citation strategy.

    Examples:
        >>> slugify_heading("Eligibility for Home Loan")
        'eligibility-for-home-loan'
        >>> slugify_heading("Q: What is the minimum balance?")
        'q-what-is-the-minimum-balance'
        >>> slugify_heading("Interest Rates (2026)")
        'interest-rates-2026'
    """
    # Normalize unicode → ASCII-compatible form
    text = unicodedata.normalize("NFKD", heading)
    text = text.encode("ascii", "ignore").decode("ascii")

    # Lowercase
    text = text.lower()

    # Replace non-alphanumeric characters with hyphens
    text = re.sub(r"[^a-z0-9]+", "-", text)

    # Strip leading/trailing hyphens
    text = text.strip("-")

    return text


def generate_section_id(document_id: str, heading_slug: str) -> str:
    """Build a deterministic section ID.

    Format: ``DOCUMENT_ID::heading-slug``

    Args:
        document_id: The parent document's stable ID (e.g. ``"ACCT-SA-001"``).
        heading_slug: Slugified section heading (e.g. ``"eligibility"``).

    Returns:
        Section ID, e.g. ``"ACCT-SA-001::eligibility"``.

    Raises:
        ValueError: If either argument is empty.
    """
    if not document_id:
        raise ValueError("document_id must not be empty")
    if not heading_slug:
        raise ValueError("heading_slug must not be empty")

    return f"{document_id}::{heading_slug}"


def generate_chunk_id(
    document_id: str,
    section_slug: str,
    position: int,
) -> str:
    """Build a deterministic chunk ID.

    Format: ``DOCUMENT_ID::section-slug::NNN``

    The same inputs always produce the same ID, enabling idempotent
    ingestion and reproducible indexing.

    Args:
        document_id: The parent document's stable ID (e.g. ``"ACCT-SA-001"``).
        section_slug: Slugified section heading (e.g. ``"eligibility"``).
        position: Zero-based ordinal position of the chunk within its section.

    Returns:
        Chunk ID, e.g. ``"ACCT-SA-001::eligibility::001"``.

    Raises:
        ValueError: If document_id or section_slug is empty, or position is negative.
    """
    if not document_id:
        raise ValueError("document_id must not be empty")
    if not section_slug:
        raise ValueError("section_slug must not be empty")
    if position < 0:
        raise ValueError("position must be non-negative")

    return f"{document_id}::{section_slug}::{position:03d}"


def content_hash(text: str) -> str:
    """Compute a SHA-256 hex digest of the given text.

    Used for change detection: if the chunk text changes, the hash
    changes, signalling that derived artifacts (embeddings, vector
    indexes) need to be regenerated.

    The text is encoded as UTF-8 before hashing for consistency.

    Args:
        text: The chunk text to hash.

    Returns:
        64-character lowercase hex string.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
