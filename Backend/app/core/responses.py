"""
Standardized API response envelope.

Every endpoint returns a consistent shape:
  Success: { "success": true,  "data": { ... } }
  Error:   { "success": false, "error": { "code": "...", "message": "...", "details": ... } }
"""

from typing import Any

from fastapi.responses import JSONResponse
from starlette import status


def success_response(data: Any, status_code: int = status.HTTP_200_OK) -> JSONResponse:
    """Wrap successful data in the standard envelope."""
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "data": data,
        },
    )


def error_response(
    code: str,
    message: str,
    status_code: int = status.HTTP_400_BAD_REQUEST,
    details: Any = None,
) -> JSONResponse:
    """Wrap error information in the standard envelope."""
    error_body: dict[str, Any] = {
        "code": code,
        "message": message,
    }
    if details is not None:
        error_body["details"] = details

    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": error_body,
        },
    )
