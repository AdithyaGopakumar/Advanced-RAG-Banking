"""
Tests for the system module — health check endpoint.
"""

import pytest


class TestHealthCheck:
    """GET /api/v1/system/health"""

    async def test_health_returns_200(self, client):
        """Health endpoint should return 200 with app status."""
        response = await client.get("/api/v1/system/health")
        assert response.status_code == 200

        body = response.json()
        assert body["success"] is True
        assert body["data"]["status"] == "healthy"

    async def test_health_contains_app_info(self, client):
        """Health response should include app name, version, environment."""
        response = await client.get("/api/v1/system/health")
        data = response.json()["data"]

        assert "app_name" in data
        assert "version" in data
        assert "environment" in data
        assert "uptime_seconds" in data
        assert "timestamp" in data

    async def test_health_returns_request_id(self, client):
        """Response should include X-Request-ID header."""
        response = await client.get("/api/v1/system/health")
        assert "x-request-id" in response.headers

    async def test_health_propagates_client_request_id(self, client):
        """If client sends X-Request-ID, it should be echoed back."""
        custom_id = "test-trace-12345"
        response = await client.get(
            "/api/v1/system/health",
            headers={"X-Request-ID": custom_id},
        )
        assert response.headers["x-request-id"] == custom_id

    async def test_health_returns_process_time(self, client):
        """Response should include X-Process-Time header."""
        response = await client.get("/api/v1/system/health")
        assert "x-process-time" in response.headers

    async def test_health_returns_security_headers(self, client):
        """Response should include security headers."""
        response = await client.get("/api/v1/system/health")
        headers = response.headers

        assert headers.get("x-content-type-options") == "nosniff"
        assert headers.get("x-frame-options") == "DENY"
        assert headers.get("x-xss-protection") == "1; mode=block"
