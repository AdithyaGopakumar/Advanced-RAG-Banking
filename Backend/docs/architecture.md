# Architecture

## Modular Monolith

The backend follows a **modular monolith** pattern — code is organized by domain, not by technical layer. Each module is self-contained and can be extracted into a microservice with minimal refactoring.

## Project Structure

```
Backend/
├── run.py                          # Entry point — uvicorn launcher + exit/signal handlers
├── main.py                         # App factory — wires middleware, routes, handlers
├── requirements.txt
├── .env / .env.example
│
├── app/
│   ├── core/                       # Shared kernel — cross-cutting framework concerns
│   │   ├── config.py               # Pydantic Settings (singleton via @lru_cache)
│   │   ├── exceptions.py           # APIException hierarchy + global error handlers
│   │   ├── responses.py            # success_response() / error_response() envelope
│   │   ├── lifecycle.py            # FastAPI lifespan (startup/shutdown hooks)
│   │   └── middleware/
│   │       ├── auth.py             # Auth dependencies (require_auth, require_admin)
│   │       ├── request_logger.py   # Logs method, path, status, duration per request
│   │       └── rate_limiter.py     # slowapi limiter + custom 429 handler
│   │
│   ├── api/                        # API layer — thin route aggregation
│   │   └── v1/
│   │       └── router.py           # Imports & mounts all module routers under /api/v1
│   │
│   ├── modules/                    # Domain modules — each is self-contained
│   │   ├── system/                 # System module (health check)
│   │   │   ├── router.py           # Route definitions
│   │   │   └── service.py          # Business logic
│   │
│   ├── ai/                         # AI agent orchestration (placeholder structure)
│   │   ├── agents/                 # Agent implementations
│   │   ├── graphs/                 # Workflow graph definitions
│   │   ├── prompts/                # Prompt templates
│   │   ├── tools/                  # Agent tools
│   │   ├── providers/              # LLM provider adapters
│   │   ├── embeddings/             # Embedding utilities
│   │   ├── rag/                    # RAG pipeline
│   │   └── modules/                # AI services (orchestrator, registry)
│   │
│   ├── shared/                     # Shared utilities (utc_now, helpers)
│   ├── db/                         # Database layer (placeholder)
│   └── models/                     # Data models (placeholder)
│
├── workers/                        # Background workers (placeholder)
├── tests/                          # Test suite (placeholder)
└── docs/                           # Documentation (you are here)
```

## Request Flow

```
Client Request
  │
  ├─ CORS Middleware           (outermost — handles preflight)
  │
  ├─ Request Logger            (times the request, adds X-Process-Time header)
  │
  ├─ Rate Limiter              (per-route via @limiter.limit decorator)
  │
  ├─ Auth Dependency           (per-route via Depends(require_auth))
  │
  ├─ Route Handler             (module router → service → response)
  │
  └─ Exception Handlers        (APIException, ValidationError, 404, 500)
```

## Middleware Stack

Registered in `main.py` via `create_app()`. Order matters — outermost runs first:

| Order | Component | Type | Scope |
|-------|-----------|------|-------|
| 1 | CORS | Middleware (global) | All requests |
| 2 | Request Logger | Middleware (global) | All requests |
| 3 | Rate Limiter | Decorator (per-route) | Routes with `@limiter.limit()` |
| 4 | Auth | Dependency (per-route) | Routes with `Depends(require_auth)` |

## Error Handling

All errors return a consistent JSON envelope:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": null
  }
}
```

| Error Code | HTTP Status | Trigger |
|------------|-------------|---------|
| `UNAUTHORIZED` | 401 | Auth dependency failure |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Unknown route |
| `VALIDATION_ERROR` | 422 | Pydantic validation failure |
| `RATE_LIMITED` | 429 | Rate limit exceeded |
| `INTERNAL_ERROR` | 500 | Unhandled exception |

## Configuration

All settings are managed via `app/core/config.py` using Pydantic Settings. Values are loaded from `.env` with type-safe defaults.

Key settings:

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `development` | `development` / `production` |
| `DEBUG` | `true` | Enables Swagger docs & detailed errors |
| `API_KEY` | `dev-secret-key` | Dummy API key (for future auth) |
| `RATE_LIMIT` | `100/minute` | Global default rate limit |
| `ALLOWED_ORIGINS` | `localhost:3000,5173` | CORS allowed origins |

## Entry Points

| File | Purpose |
|------|---------|
| `run.py` | Process-level: signal handlers, uncaught exception hook, `atexit`, launches uvicorn |
| `main.py` | App-level: `create_app()` factory, wires middleware/routes/handlers |
