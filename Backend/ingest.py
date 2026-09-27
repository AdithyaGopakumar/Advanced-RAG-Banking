"""Run the knowledge ingestion pipeline.

Usage (from the Backend directory, with the virtual environment active):

    python ingest.py
    python ingest.py --as-of 2026-09-27
    python ingest.py --knowledge-root ../knowledge-base
"""

from app.ingestion.pipeline import main

if __name__ == "__main__":
    raise SystemExit(main())
