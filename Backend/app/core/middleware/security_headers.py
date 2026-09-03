"""
Security headers middleware.

Adds standard security headers to every response to mitigate
common web vulnerabilities (clickjacking, MIME sniffing, XSS, etc.).
"""

import logging

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)

# Default security headers applied to every response
_SECURITY_HEADERS: dict[str, str] = {
    # Prevent MIME-type sniffing
    "X-Content-Type-Options": "nosniff",

    # Prevent clickjacking — deny all framing
    "X-Frame-Options": "DENY",

    # Enable browser XSS filter
    "X-XSS-Protection": "1; mode=block",

    # Only send referrer origin (no full URL with path/query)
    "Referrer-Policy": "strict-origin-when-cross-origin",

    # Restrict browser features (camera, mic, geolocation, etc.)
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",

    # Prevent content from being loaded in other contexts
    "Cross-Origin-Opener-Policy": "same-origin",
}


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Inject security headers into every HTTP response."""

    def __init__(self, app, hsts_enabled: bool = False, hsts_max_age: int = 31536000):
        """
        Args:
            app: ASGI application.
            hsts_enabled: Enable HSTS header (only enable when behind HTTPS).
            hsts_max_age: HSTS max-age in seconds (default: 1 year).
        """
        super().__init__(app)
        self.hsts_enabled = hsts_enabled
        self.hsts_max_age = hsts_max_age

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)

        # Apply all standard security headers
        for header, value in _SECURITY_HEADERS.items():
            response.headers[header] = value

        # HSTS — only enable when serving over HTTPS
        if self.hsts_enabled:
            response.headers["Strict-Transport-Security"] = (
                f"max-age={self.hsts_max_age}; includeSubDomains"
            )

        return response
