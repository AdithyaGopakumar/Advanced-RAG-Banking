"""Unit and integration tests for LangSmith observability and tracing."""

import os
import pytest
from httpx import ASGITransport, AsyncClient

from app.ai.observability.tracer import (
    build_trace_config,
    get_observability_status,
    setup_observability,
)
from app.core.config import Settings
from main import app


def test_setup_observability_when_enabled():
    mock_settings = Settings(
        LANGCHAIN_TRACING_V2=True,
        LANGCHAIN_API_KEY="lsv2_test_api_key_12345",
        LANGCHAIN_PROJECT="test-rag-project",
        LANGCHAIN_ENDPOINT="https://api.smith.langchain.com",
    )
    enabled = setup_observability(mock_settings)
    assert enabled is True
    assert os.environ.get("LANGCHAIN_TRACING_V2") == "true"
    assert os.environ.get("LANGCHAIN_API_KEY") == "lsv2_test_api_key_12345"
    assert os.environ.get("LANGCHAIN_PROJECT") == "test-rag-project"


def test_setup_observability_when_disabled():
    mock_settings = Settings(
        LANGCHAIN_TRACING_V2=False,
        LANGCHAIN_API_KEY="",
    )
    enabled = setup_observability(mock_settings)
    assert enabled is False
    assert os.environ.get("LANGCHAIN_TRACING_V2") == "false"


def test_get_observability_status():
    status = get_observability_status()
    assert isinstance(status, dict)
    assert "project" in status
    assert "endpoint" in status
    assert "has_api_key" in status
    assert "available" in status


def test_build_trace_config():
    config = build_trace_config(
        request_id="req-999",
        run_name="custom_turn",
        metadata={"custom_key": "val"},
        tags=["eval"],
    )
    assert config["run_name"] == "custom_turn"
    assert "eval" in config["tags"]
    assert config["metadata"]["request_id"] == "req-999"
    assert config["metadata"]["custom_key"] == "val"


@pytest.mark.asyncio
async def test_system_observability_endpoint():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/system/observability")
        assert response.status_code == 200
        payload = response.json()
        assert payload["success"] is True
        assert "project" in payload["data"]
        assert "available" in payload["data"]


@pytest.mark.asyncio
async def test_chat_api_propagates_request_id():
    custom_id = "trace-req-unique-987"
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/chat",
            json={"question": "Transfer 5000 rupees to John"},
            headers={"X-Request-ID": custom_id},
        )
        assert response.status_code == 200
        assert response.headers.get("X-Request-ID") == custom_id
        payload = response.json()
        assert payload["data"]["request_id"] == custom_id
        assert payload["data"]["response_type"] == "rejected"
