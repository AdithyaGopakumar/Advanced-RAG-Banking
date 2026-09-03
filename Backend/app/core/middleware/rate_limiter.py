"""
Rate limiting configuration using slowapi.

Provides a pre-configured limiter instance and a default rate limit
dependency that can be applied globally or per-route.
"""

import logging

from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from app.core.config import get_settings
from app.core.responses import error_response

logger = logging.getLogger(__name__)

# Create limiter keyed by client IP
limiter = Limiter(key_func=get_remote_address)


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> Response:
    """Custom handler for rate limit exceeded errors using our standard envelope."""
    logger.warning(
        "Rate limited: %s %s from %s",
        request.method,
        request.url.path,
        get_remote_address(request),
    )

    response = error_response(
        code="RATE_LIMITED",
        message=f"Rate limit exceeded: {exc.detail}",
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
    )

    # Include Retry-After header if available
    retry_after = getattr(exc, "retry_after", None)
    if retry_after:
        response.headers["Retry-After"] = str(retry_after)

    return response


def get_default_rate_limit() -> str:
    """Get the default rate limit string from settings."""
    return get_settings().RATE_LIMIT
