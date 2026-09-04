"""
Knowledge domain module.

Represents governed knowledge concepts and their retrieval representations.
This module owns the domain boundary for:

    KnowledgeDocument  →  A governed knowledge unit (product, policy, FAQ, etc.)
    KnowledgeSection   →  Structural context inside a document (H2/H3 sections)
    KnowledgeChunk     →  The primary retrieval unit for the RAG pipeline

These concepts are intentionally kept separate from:

    app/ai/            →  AI infrastructure (embeddings, providers, prompts)
    app/ingestion/     →  Knowledge → retrieval artifact transformation (CLI/job-driven)

No HTTP routes are exposed from this module.  Ingestion is driven by CLI/jobs,
not by FastAPI endpoints.
"""
