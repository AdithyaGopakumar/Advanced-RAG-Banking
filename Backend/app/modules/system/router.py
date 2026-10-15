"""
System module routes.

Defines health check and system diagnostic endpoints.
"""

from fastapi import APIRouter, Depends, Request

from app.core.middleware.auth import require_auth
from app.core.middleware.rate_limiter import limiter
from app.core.responses import success_response
from app.modules.system.service import get_health

router = APIRouter(prefix="/system", tags=["System"])


@router.get("/health", dependencies=[Depends(require_auth)])
@limiter.limit("30/minute")
async def health_check(request: Request):
    """
    Application health check.

    Returns current status, version, environment, and uptime.
    """
    return success_response(data=get_health())


@router.get("/observability", dependencies=[Depends(require_auth)])
@limiter.limit("30/minute")
async def observability_status(request: Request):
    """
    Return LangSmith tracing and observability status.
    """
    from app.ai.observability.tracer import get_observability_status

    return success_response(data=get_observability_status())


@router.get("/guardrails", dependencies=[Depends(require_auth)])
@limiter.limit("30/minute")
async def guardrails_status(request: Request):
    """
    Return active guardrails and NeMo status diagnostics.
    """
    from app.core.config import get_settings

    settings = get_settings()
    try:
        import nemoguardrails
        nemo_installed = True
        nemo_version = getattr(nemoguardrails, "__version__", "unknown")
    except ImportError:
        nemo_installed = False
        nemo_version = None

    data = {
        "nemo_guardrails_enabled": settings.ENABLE_NEMO_GUARDRAILS,
        "nemo_config_path": settings.NEMO_GUARDRAILS_CONFIG_PATH,
        "nemo_installed": nemo_installed,
        "nemo_version": nemo_version,
        "deterministic_layers": {
            "input_length_validation": True,
            "pii_redaction": True,
            "scope_classification": True,
            "retrieval_governance": True,
            "claim_grounding": True,
            "output_sanitization": True,
        },
        "policies": [
            "KB_ONLY",
            "NO_FABRICATION",
            "PARTIAL_SUPPORT",
            "CLARIFICATION_POLICY",
            "TRANSACTION_EXECUTION_OUT_OF_SCOPE",
        ],
    }
    return success_response(data=data)
