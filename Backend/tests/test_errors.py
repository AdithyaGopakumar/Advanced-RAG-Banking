"""
Tests for error handling — 404, validation, exception envelope.
"""

import pytest


class TestErrorHandling:
    """Verify global exception handlers return consistent envelopes."""

    async def test_404_returns_not_found(self, client):
        """Unknown routes should return 404 with error envelope."""
        response = await client.get("/api/v1/nonexistent")
        assert response.status_code == 404

        body = response.json()
        assert body["success"] is False
        assert body["error"]["code"] == "NOT_FOUND"

    async def test_error_envelope_structure(self, client):
        """Error responses should have consistent structure."""
        response = await client.get("/api/v1/nonexistent")
        body = response.json()

        assert "success" in body
        assert "error" in body
        assert "code" in body["error"]
        assert "message" in body["error"]
