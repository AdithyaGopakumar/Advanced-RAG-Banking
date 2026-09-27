"""Terminal entry for the knowledge ingestion pipeline."""

from app.ingestion.pipeline import run_ingestion

__all__ = ["run_ingestion"]
