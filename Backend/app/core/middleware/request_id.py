"""
Request ID middleware.

Generates a unique UUID for each incoming request, attaches it to
`request.state.request_id`, and returns it in the `X-Request-ID`
response header for end-to-end tracing.

If the client sends an `X-Request-ID` header, that value is reused
(useful for propagating trace IDs across microservices).
"""

import uuid
import logging

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Attach a unique request ID to every request/response cycle."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Reuse client-provided ID or generate a new one
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())

        # Store on request state for downstream access
        request.state.request_id = request_id

        # Process the request
        response = await call_next(request)

        # Echo the ID back in the response
        response.headers["X-Request-ID"] = request_id

        return response
