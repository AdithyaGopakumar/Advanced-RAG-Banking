"""
Ingestion package — Knowledge → Retrieval Artifact transformation.

This package is architecturally separate from HTTP.  Ingestion is driven
by CLI commands, batch jobs, or background workers — NOT by FastAPI routes.

The pipeline will eventually:

    1. Read governed knowledge documents from the knowledge-base
    2. Parse YAML frontmatter + Markdown content
    3. Split into sections (H2/H3 boundaries)
    4. Chunk sections into retrieval units
    5. Generate deterministic IDs and content hashes
    6. Produce KnowledgeChunk artifacts with metadata, provenance,
       and typed relationships

Downstream consumers (embedding, indexing) will read these artifacts.

Implementation will be added in Phase 1A.
"""
