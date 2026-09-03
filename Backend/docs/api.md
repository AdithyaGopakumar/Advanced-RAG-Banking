# API Reference

Base URL: `http://localhost:8000`

## Versioning

All endpoints are versioned under `/api/v1`. Future versions will use `/api/v2`, etc.

---

## System

### Health Check

```
GET /api/v1/system/health
```

**Auth**: Required (`require_auth` — currently passthrough)
**Rate Limit**: 30 requests/minute per IP

**Response** `200 OK`:
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "app_name": "AI Recruitment Assistant",
    "version": "0.1.0",
    "environment": "development",
    "timestamp": "2026-07-24T16:52:00+00:00",
    "uptime_seconds": 123.45
  }
}
```

---

## Standard Response Format

### Success

```json
{
  "success": true,
  "data": { ... }
}
```

### Error

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description",
    "details": null
  }
}
```

### Error Codes

| Code | HTTP | Description |
|------|------|-------------|
| `UNAUTHORIZED` | 401 | Missing or invalid authentication |
| `FORBIDDEN` | 403 | Authenticated but insufficient permissions |
| `NOT_FOUND` | 404 | Route or resource not found |
| `VALIDATION_ERROR` | 422 | Request body/params failed validation |
| `RATE_LIMITED` | 429 | Too many requests (includes `Retry-After` header) |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

### Validation Error Details

`422` responses include field-level error details:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "body → email",
        "message": "value is not a valid email address",
        "type": "value_error"
      }
    ]
  }
}
```

---

## Common Headers

### Request Headers

| Header | Required | Description |
|--------|----------|-------------|
| `X-API-Key` | Depends on route | API key (when auth is enforced) |
| `Content-Type` | For POST/PUT | `application/json` |

### Response Headers

| Header | Description |
|--------|-------------|
| `X-Process-Time` | Request processing duration (e.g., `2.30ms`) |
| `Retry-After` | Seconds to wait (only on `429` responses) |

---

## Interactive Docs

Available in development mode (`DEBUG=true`):

| URL | Format |
|-----|--------|
| `/docs` | Swagger UI |
| `/redoc` | ReDoc |
| `/openapi.json` | Raw OpenAPI spec |
