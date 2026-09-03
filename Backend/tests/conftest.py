"""
Shared test fixtures.

Provides:
    - `app`: Fresh FastAPI application instance (per session)
    - `client`: Async HTTP test client (per test)
    - `settings`: Application settings override for testing
"""

import os

# Set test environment BEFORE any app imports
os.environ["ENVIRONMENT"] = "development"
os.environ["DEBUG"] = "true"
os.environ["API_KEY"] = "test-api-key"
os.environ["ALLOWED_HOSTS"] = '["*"]'

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import Settings, get_settings


@pytest.fixture(scope="session")
def app():
    """Create a fresh FastAPI app for the test session."""
    # Clear cached settings so test env vars take effect
    get_settings.cache_clear()

    from main import create_app
    test_app = create_app()
    yield test_app

    # Cleanup
    get_settings.cache_clear()


@pytest.fixture
def settings() -> Settings:
    """Access test settings."""
    return get_settings()


@pytest.fixture
async def client(app):
    """Async HTTP client for testing endpoints."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
