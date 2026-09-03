"""
FastAPI application factory.

Creates and configures the FastAPI app with all middleware,
exception handlers, routes, and lifespan hooks.

Usage:
    from main import create_app
    app = create_app()
"""

import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pythonjsonlogger.json import JsonFormatter
from slowapi.errors import RateLimitExceeded

from app.api.v1.router import v1_router
from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.lifecycle import lifespan
from app.core.middleware.rate_limiter import limiter, rate_limit_exceeded_handler
from app.core.middleware.request_id import RequestIDMiddleware
from app.core.middleware.request_logger import RequestLoggerMiddleware
from app.core.middleware.security_headers import SecurityHeadersMiddleware


def _configure_logging(settings) -> None:
    """
    Set up logging.

    - Development: human-readable plaintext format
    - Production: structured JSON for log aggregators (ELK, Datadog, CloudWatch)
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

    # Clear any existing handlers
    root_logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)

    if settings.is_production:
        # Structured JSON logging for production
        formatter = JsonFormatter(
            fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
            rename_fields={
                "asctime": "timestamp",
                "levelname": "level",
                "name": "logger",
            },
        )
    else:
        # Human-readable format for development
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    handler.setFormatter(formatter)
    root_logger.addHandler(handler)


def create_app() -> FastAPI:
    """
    Build and return the fully configured FastAPI application.

    Middleware execution order (outermost → innermost):
        1. Trusted Host            — reject unknown Host headers
        2. CORS                    — handle preflight / origin checks
        3. Security Headers        — inject security response headers
        4. Request ID              — generate/propagate trace ID
        5. Request Logger          — log method, path, status, duration

    Auth is handled per-route via dependencies, not globally.
    """
    settings = get_settings()

    # ─── 1. Logging ───
    _configure_logging(settings)
    logger = logging.getLogger(__name__)

    # ─── 2. FastAPI instance ───
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # ─── 3. Rate limiter ───
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

    # ─── 4. Middleware stack (outermost → innermost) ───

    # GZip — compress responses larger than 500 bytes
    app.add_middleware(GZipMiddleware, minimum_size=500)

    # Trusted Host — reject requests with spoofed Host headers
    # In production, set ALLOWED_HOSTS to your actual domains
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
        expose_headers=["X-Process-Time", "X-Request-ID"],
    )

    # Security headers (HSTS only in production behind HTTPS)
    app.add_middleware(
        SecurityHeadersMiddleware,
        hsts_enabled=settings.is_production,
    )

    # Request ID — generate/propagate correlation ID
    app.add_middleware(RequestIDMiddleware)

    # Request logger — logs timing and status for every request
    app.add_middleware(RequestLoggerMiddleware)

    # ─── 5. Exception handlers ───
    register_exception_handlers(app)

    # ─── 6. Routes ───
    app.include_router(v1_router)

    logger.info(
        "Application created: %s v%s (%s)",
        settings.APP_NAME,
        settings.APP_VERSION,
        settings.ENVIRONMENT,
    )

    return app


# Module-level app instance for uvicorn
app = create_app()
