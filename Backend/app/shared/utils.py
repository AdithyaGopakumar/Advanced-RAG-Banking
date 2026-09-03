"""
Shared utility functions.
"""

from datetime import datetime, timezone


def utc_now() -> datetime:
    """Return the current UTC timestamp (timezone-aware)."""
    return datetime.now(timezone.utc)


def utc_now_iso() -> str:
    """Return the current UTC timestamp as an ISO 8601 string."""
    return utc_now().isoformat()
