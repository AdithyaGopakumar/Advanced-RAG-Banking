"""
Request logging middleware.

Logs every request with method, path, status code, response time,
and request ID (for correlation). Adds an `X-Process-Time` header
to every response for client-side observability.
"""

import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    """Logs request details and response timing."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.perf_counter()

        # Process the request
        response = await call_next(request)

        # Calculate duration
        duration_ms = (time.perf_counter() - start_time) * 1000

        # Add timing header
        response.headers["X-Process-Time"] = f"{duration_ms:.2f}ms"

        # Get request ID (set by RequestIDMiddleware upstream)
        request_id = getattr(request.state, "request_id", "-")

        # Determine log level based on status code
        status_code = response.status_code
        if status_code >= 500:
            log_fn = logger.error
        elif status_code >= 400:
            log_fn = logger.warning
        else:
            log_fn = logger.info

        log_fn(
            "%s %s -> %d [%.2fms] [%s]",
            request.method,
            request.url.path,
            status_code,
            duration_ms,
            request_id,
        )

        return response
