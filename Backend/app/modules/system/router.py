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
