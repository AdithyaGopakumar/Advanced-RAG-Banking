"""
Custom exception classes and global exception handlers.

Register handlers via `register_exception_handlers(app)` in the app factory.
"""

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.responses import error_response

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Custom exception classes
# ──────────────────────────────────────────────


class APIException(Exception):
    """Base exception for all application-level errors."""

    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: str = "BAD_REQUEST",
        message: str = "An error occurred",
        details: Any = None,
    ) -> None:
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.details = details
        super().__init__(self.message)


class UnauthorizedException(APIException):
    def __init__(self, message: str = "Authentication required") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="UNAUTHORIZED",
            message=message,
        )


class ForbiddenException(APIException):
    def __init__(self, message: str = "Access denied") -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="FORBIDDEN",
            message=message,
        )


class NotFoundException(APIException):
    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND",
            message=message,
        )


class RateLimitedException(APIException):
    def __init__(self, message: str = "Rate limit exceeded") -> None:
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMITED",
            message=message,
        )


# ──────────────────────────────────────────────
# Global exception handlers
# ──────────────────────────────────────────────


async def api_exception_handler(request: Request, exc: APIException):
    """Handle custom APIException subclasses."""
    logger.warning(
        "APIException: %s %s → %d %s",
        request.method,
        request.url.path,
        exc.status_code,
        exc.error_code,
    )
    return error_response(
        code=exc.error_code,
        message=exc.message,
        status_code=exc.status_code,
        details=exc.details,
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    """Handle Pydantic / FastAPI request validation errors."""
    details = []
    for error in exc.errors():
        details.append(
            {
                "field": " → ".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"],
            }
        )

    logger.warning(
        "Validation error: %s %s → %d field error(s)",
        request.method,
        request.url.path,
        len(details),
    )
    return error_response(
        code="VALIDATION_ERROR",
        message="Request validation failed",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        details=details,
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle Starlette/FastAPI HTTPExceptions (404, 405, etc.)."""
    code_map = {
        status.HTTP_404_NOT_FOUND: "NOT_FOUND",
        status.HTTP_405_METHOD_NOT_ALLOWED: "METHOD_NOT_ALLOWED",
    }
    error_code = code_map.get(exc.status_code, "HTTP_ERROR")

    logger.warning(
        "HTTP %d: %s %s → %s",
        exc.status_code,
        request.method,
        request.url.path,
        exc.detail,
    )
    return error_response(
        code=error_code,
        message=str(exc.detail),
        status_code=exc.status_code,
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    """Catch-all for unhandled exceptions — returns 500, hides details in production."""
    from app.core.config import get_settings

    settings = get_settings()

    logger.exception(
        "Unhandled exception: %s %s",
        request.method,
        request.url.path,
    )

    message = (
        str(exc)
        if settings.is_development
        else "An unexpected error occurred"
    )

    return error_response(
        code="INTERNAL_ERROR",
        message=message,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all global exception handlers on the FastAPI app."""
    app.add_exception_handler(APIException, api_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
