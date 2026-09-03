"""
Application lifespan — startup and shutdown hooks.

Uses FastAPI's `lifespan` context manager for clean resource management.
"""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.

    Startup:
        - Logs application info
        - Placeholder for DB / cache / queue connections
        - Placeholder for AI agent registry initialization

    Shutdown:
        - Logs shutdown
        - Placeholder for connection teardown
    """
    settings = get_settings()

    # ─── Startup ───
    logger.info("=" * 60)
    logger.info("  %s v%s", settings.APP_NAME, settings.APP_VERSION)
    logger.info("  Environment: %s", settings.ENVIRONMENT)
    logger.info("  Debug: %s", settings.DEBUG)
    logger.info("=" * 60)

    # TODO: Initialize database connections
    # TODO: Initialize cache (Redis)
    # TODO: Initialize message queue connections
    # TODO: Initialize AI agent registry

    logger.info("Startup complete — ready to accept requests")

    yield

    # ─── Shutdown ───
    logger.info("Shutting down %s...", settings.APP_NAME)

    # TODO: Close database connections
    # TODO: Close cache connections
    # TODO: Drain message queues

    logger.info("Shutdown complete")
