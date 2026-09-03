"""
System service — health check and system diagnostics.

Contains the business logic for health checks, system status,
and diagnostics. The API layer imports from here.
"""

import time

from app.core.config import get_settings
from app.shared.utils import utc_now_iso

# Recorded at module load time — approximates server boot
_BOOT_TIME: float = time.time()


def get_health() -> dict:
    """
    Build the health check response payload.

    Returns:
        dict with status, app info, uptime, and timestamp.
    """
    settings = get_settings()
    uptime_seconds = round(time.time() - _BOOT_TIME, 2)

    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": utc_now_iso(),
        "uptime_seconds": uptime_seconds,
    }
