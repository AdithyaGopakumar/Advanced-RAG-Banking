"""API client for connecting Streamlit frontend to the FastAPI backend."""

from __future__ import annotations

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class BackendClient:
    """HTTP client communicating with the RAG Bank FastAPI backend."""

    def __init__(self, base_url: str = "http://localhost:8000", timeout: float = 90.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def check_health(self) -> dict[str, Any] | None:
        """Fetch system health status."""
        try:
            url = f"{self.base_url}/api/v1/system/health"
            with httpx.Client(timeout=3.0) as client:
                res = client.get(url)
                if res.status_code == 200:
                    return res.json().get("data", {})
        except Exception as exc:
            logger.debug("Health check failed: %s", exc)
        return None

    def check_guardrails(self) -> dict[str, Any] | None:
        """Fetch guardrails status."""
        try:
            url = f"{self.base_url}/api/v1/system/guardrails"
            with httpx.Client(timeout=3.0) as client:
                res = client.get(url)
                if res.status_code == 200:
                    return res.json().get("data", {})
        except Exception as exc:
            logger.debug("Guardrails check failed: %s", exc)
        return None

    def check_observability(self) -> dict[str, Any] | None:
        """Fetch observability and LangSmith tracing status."""
        try:
            url = f"{self.base_url}/api/v1/system/observability"
            with httpx.Client(timeout=3.0) as client:
                res = client.get(url)
                if res.status_code == 200:
                    return res.json().get("data", {})
        except Exception as exc:
            logger.debug("Observability check failed: %s", exc)
        return None

    def send_chat(
        self,
        query: str,
        *,
        conversation_id: str | None = None,
        full_trace: bool = True,
    ) -> dict[str, Any]:
        """Send a banking question to POST /api/v1/chat."""
        url = f"{self.base_url}/api/v1/chat"
        payload = {
            "query": query,
            "conversationId": conversation_id,
            "fullTrace": full_trace,
        }
        try:
            with httpx.Client(timeout=self.timeout) as client:
                res = client.post(url, json=payload)
                body = res.json()
                if res.status_code == 200 and body.get("success"):
                    return {"success": True, "data": body.get("data", {})}
                
                # API returned structured error envelope
                err = body.get("error", {})
                return {
                    "success": False,
                    "error": {
                        "code": err.get("code", f"HTTP_{res.status_code}"),
                        "message": err.get("message", "An unexpected error occurred from the backend."),
                        "details": err.get("details"),
                    },
                }
        except httpx.ConnectError:
            return {
                "success": False,
                "error": {
                    "code": "CONNECTION_OFFLINE",
                    "message": f"Unable to connect to RAG Bank backend at {self.base_url}. Ensure the server is running (`cd Backend && python run.py`).",
                },
            }
        except httpx.TimeoutException:
            return {
                "success": False,
                "error": {
                    "code": "REQUEST_TIMEOUT",
                    "message": "The backend request timed out while processing evidence retrieval or grounding.",
                },
            }
        except Exception as exc:
            return {
                "success": False,
                "error": {
                    "code": "CLIENT_ERROR",
                    "message": str(exc),
                },
            }
