"""
Application entry point.

Handles:
    - Uncaught exception hook (sys.excepthook)
    - atexit cleanup
    - Launches uvicorn programmatically

Note: Signal handling (SIGINT, SIGTERM) is delegated to uvicorn,
which manages graceful shutdown of in-flight requests internally.

Usage:
    py run.py
"""

import atexit
import logging
import sys

import uvicorn

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Exit & exception handlers
# ──────────────────────────────────────────────


def _uncaught_exception_handler(exc_type, exc_value, exc_traceback):
    """Global hook for uncaught exceptions — logs and exits."""
    if issubclass(exc_type, KeyboardInterrupt):
        # Let KeyboardInterrupt pass through normally
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.critical(
        "Uncaught exception",
        exc_info=(exc_type, exc_value, exc_traceback),
    )


def _atexit_handler():
    """Final cleanup hook — runs on normal interpreter exit."""
    logger.info("Process exiting - cleanup complete")


# ──────────────────────────────────────────────
# Bootstrap
# ──────────────────────────────────────────────


def main() -> None:
    """Configure handlers and launch the server."""

    # Install global exception hook
    sys.excepthook = _uncaught_exception_handler

    # Register atexit cleanup
    atexit.register(_atexit_handler)

    # Load settings
    from app.core.config import get_settings
    settings = get_settings()

    # Launch uvicorn — it handles SIGINT/SIGTERM gracefully,
    # draining in-flight requests before shutting down.
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.is_development,
        log_level=settings.LOG_LEVEL.lower(),
    )


if __name__ == "__main__":
    main()
