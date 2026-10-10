"""LangSmith observability and distributed tracing integration.

Provides:
- Environment and client setup for LangSmith tracing
- Tracing status diagnostics
- RunnableConfig building for LangGraph workflow execution
- Safe fallback when LangSmith is disabled (offline/development mode)
"""

import logging
import os
from typing import Any

from app.core.config import Settings, get_settings

logger = logging.getLogger(__name__)


def setup_observability(settings: Settings | None = None) -> bool:
    """Configure LangSmith tracing environment variables if enabled in settings."""
    cfg = settings or get_settings()

    if cfg.LANGCHAIN_TRACING_V2 and cfg.LANGCHAIN_API_KEY:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = cfg.LANGCHAIN_API_KEY
        os.environ["LANGCHAIN_PROJECT"] = cfg.LANGCHAIN_PROJECT
        os.environ["LANGCHAIN_ENDPOINT"] = cfg.LANGCHAIN_ENDPOINT

        logger.info(
            "LangSmith tracing enabled (Project: %s, Endpoint: %s)",
            cfg.LANGCHAIN_PROJECT,
            cfg.LANGCHAIN_ENDPOINT,
        )
        return True

    # Disable LangSmith tracing in environment if not explicitly enabled
    os.environ["LANGCHAIN_TRACING_V2"] = "false"
    logger.debug("LangSmith tracing is disabled (offline/local mode)")
    return False


def get_observability_status() -> dict[str, Any]:
    """Return diagnostic status of LangSmith observability."""
    settings = get_settings()
    is_env_enabled = os.environ.get("LANGCHAIN_TRACING_V2", "").lower() in ("true", "1")

    status: dict[str, Any] = {
        "enabled": is_env_enabled and bool(settings.LANGCHAIN_API_KEY),
        "project": settings.LANGCHAIN_PROJECT,
        "endpoint": settings.LANGCHAIN_ENDPOINT,
        "has_api_key": bool(settings.LANGCHAIN_API_KEY),
    }

    try:
        import langsmith

        status["langsmith_version"] = getattr(langsmith, "__version__", "unknown")
        status["available"] = True
    except ImportError:
        status["langsmith_version"] = None
        status["available"] = False

    return status


def build_trace_config(
    *,
    request_id: str | None = None,
    run_name: str = "banking_agent_turn",
    metadata: dict[str, Any] | None = None,
    tags: list[str] | None = None,
) -> dict[str, Any]:
    """Build a RunnableConfig dictionary for LangGraph invoke with tracing metadata."""
    settings = get_settings()

    run_tags = ["banking-agent", settings.ENVIRONMENT]
    if tags:
        run_tags.extend(tags)

    run_metadata: dict[str, Any] = {
        "app_name": settings.APP_NAME,
        "app_version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }
    if request_id:
        run_metadata["request_id"] = request_id
    if metadata:
        run_metadata.update(metadata)

    return {
        "run_name": run_name,
        "tags": run_tags,
        "metadata": run_metadata,
    }
