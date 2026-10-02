# RAG Bank — Backend

Production-oriented FastAPI backend for the RAG Bank advanced banking assistant. Built around the **modular monolith** pattern — code is organized by domain, not by technical layer.

## Highlights

- **Modular monolith** — domain-oriented modules under `app/modules/`
- **Application factory** — `create_app()` in `main.py` wires middleware, routes, and exception handlers
- **Pydantic Settings** — type-safe, env-driven configuration with production validators
- **Middleware stack** — CORS, GZip, trusted hosts, security headers, request ID, request logging
- **Per-route auth & rate limiting** — opt-in via FastAPI dependencies and `@limiter.limit()` decorators
- **Consistent error responses** — structured JSON envelope for all errors (401, 403, 404, 422, 429, 500)
- **Structured logging** — human-readable in development, JSON in production
- **Docker-ready** — multi-stage `Dockerfile` + `docker-compose.yml` for development
- **Knowledge domain models** — retrieval artifact hierarchy (Document → Section → Chunk) with deterministic identity, content hashing, typed relationships, and structured provenance
- **AI infrastructure scaffold** — placeholder structure for embeddings, providers, prompts, and RAG pipeline

---

## Project Structure

```
├── run.py                          # Entry point — signal handlers, launches uvicorn
├── main.py                         # App factory — wires middleware, routes, handlers
├── requirements.txt
├── .env / .env.example
├── Dockerfile
├── docker-compose.yml
│
├── app/
│   ├── core/                       # Shared kernel — cross-cutting concerns
│   │   ├── config.py               # Pydantic Settings (singleton via @lru_cache)
│   │   ├── exceptions.py           # APIException hierarchy + global error handlers
│   │   ├── responses.py            # success_response() / error_response() envelope
│   │   ├── lifecycle.py            # FastAPI lifespan (startup / shutdown hooks)
│   │   └── middleware/
│   │       ├── auth.py             # Auth dependencies (require_auth, require_admin)
│   │       ├── rate_limiter.py     # slowapi limiter + custom 429 handler
│   │       ├── request_id.py       # Generate / propagate X-Request-ID
│   │       ├── request_logger.py   # Log method, path, status, duration per request
│   │       └── security_headers.py # HSTS, X-Content-Type-Options, etc.
│   │
│   ├── api/                        # Thin route aggregation
│   │   └── v1/
│   │       └── router.py           # Mounts all module routers under /api/v1
│   │
│   ├── modules/                    # Domain modules — each is self-contained
│   │   ├── system/                 # Health check (implemented)
│   │   └── knowledge/              # Knowledge domain models & identity
│   │       ├── models.py           # KnowledgeDocument, KnowledgeSection, KnowledgeChunk
│   │       └── identity.py         # Deterministic chunk IDs & content hashing
│   │
│   ├── ingestion/                  # Knowledge → retrieval artifact pipeline (CLI/job-driven)
│   │
│   ├── ai/                         # AI infrastructure (scaffold)
│   │   ├── embeddings/             # Embedding utilities
│   │   ├── prompts/                # Prompt templates
│   │   ├── providers/              # LLM provider adapters
│   │   └── rag/                    # RAG pipeline
│   │
│   ├── shared/                     # Shared utilities (utc_now, helpers)
│   ├── db/                         # Database layer (placeholder)
│   └── models/                     # Data models (placeholder)
│
├── workers/                        # Background workers (placeholder)
├── tests/                          # Test suite
└── docs/                           # Extended documentation
```

---

## Quick Start

### Prerequisites

- Python 3.10+
- pip

### Local Setup

```bash
# 1. Clone the repo
git clone <repo-url> && cd <repo-name>

# 2. Create & activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env           # edit as needed

# 5. Start the server
python run.py
```

The server starts at **http://localhost:8000** with hot-reload enabled in development.

### Knowledge ingestion

Run this from the `Backend` directory after the virtual environment is active and dependencies are installed. The first run with the default embedding model downloads `paraphrase-MiniLM-L6-v2`, so the machine needs network access.

```powershell
# Windows, from Backend/
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python ingest.py
```

```bash
# macOS / Linux, from Backend/
source .venv/bin/activate
pip install -r requirements.txt
python ingest.py
```

Optional arguments:

```bash
python ingest.py --as-of 2026-09-27
python ingest.py --knowledge-root ../knowledge-base
```

The command loads `KNOWLEDGE_ROOT` (default `../knowledge-base`, resolved from the Backend directory), keeps documents whose status is `approved` or `current` and whose effective dates include `--as-of` (today when omitted), embeds eligible chunks, and writes `chunk.text` to the Elasticsearch BM25 index. README files without front matter are rejected and listed in the summary counts.

Dense vectors are stored in Pinecone only when both `PINECONE_API_KEY` and `PINECONE_INDEX_NAME` are set. Create that index first with **384 dimensions** and the **cosine** metric. The command does not create it. A successful Pinecone run writes `INDEX_MANIFEST_PATH` (default `.index/manifest.json`) so the next run upserts changed chunks and deletes removed ids. With Pinecone unset, vectors stay in memory for that process and the manifest is not written. The lexical index stays in Elasticsearch. Start it with `docker compose up elasticsearch kibana` before ingesting. Kibana is at `http://localhost:5601`.

| Variable | Default | Purpose |
|---|---|---|
| `KNOWLEDGE_ROOT` | `../knowledge-base` | Governed Markdown corpus |
| `CHUNK_MAX_SIZE` | `2000` | Character budget for a chunk, including heading breadcrumbs |
| `EMBEDDING_PROVIDER` | `sentence-transformers` | Embedding adapter |
| `EMBEDDING_MODEL` | `paraphrase-MiniLM-L6-v2` | Local embedding model |
| `EMBEDDING_DIMENSIONS` | `384` | Vector width expected from that model |
| `PINECONE_API_KEY` | empty | Pinecone credential; empty selects the in-memory vector index |
| `PINECONE_INDEX_NAME` | empty | Existing Pinecone index name |
| `PINECONE_NAMESPACE` | `knowledge` | Pinecone namespace |
| `INDEX_MANIFEST_PATH` | `.index/manifest.json` | Saved after a Pinecone run; relative paths start at `Backend/` |
| `ELASTICSEARCH_URL` | `http://localhost:9200` | Elasticsearch cluster for the BM25 index |
| `ELASTICSEARCH_INDEX` | `knowledge-chunks` | Lexical index name |

Copy `.env.example` to `.env` and edit those values there. `.env` is loaded from the current directory, so run `python ingest.py` from `Backend`.

### Docker

```bash
# Development (with hot-reload & source mount)
docker compose up --build

# Production
docker build -t fastapi-app .
docker run -p 8000:8000 --env-file .env fastapi-app
```

### Verify

```bash
curl http://localhost:8000/api/v1/system/health
# → {"success": true, "data": {"status": "healthy", ...}}
```

Interactive docs (development only):

| URL              | Format      |
|------------------|-------------|
| `/docs`          | Swagger UI  |
| `/redoc`         | ReDoc       |
| `/openapi.json`  | OpenAPI spec |

---

## Entry Points

| File       | Role                                                                 |
|------------|----------------------------------------------------------------------|
| `run.py`   | Process-level — uncaught exception hook, `atexit` cleanup, launches uvicorn |
| `ingest.py`| Knowledge ingestion — validate, chunk, and index eligible documents          |
| `main.py`  | App-level — `create_app()` factory, wires middleware / routes / handlers    |

**Running directly with uvicorn** is also supported:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## Middleware Stack

Registered in `create_app()`. Order matters — outermost runs first:

| Order | Middleware          | Scope       | Description                              |
|-------|---------------------|-------------|------------------------------------------|
| 1     | GZip                | Global      | Compress responses > 500 bytes           |
| 2     | Trusted Host        | Global      | Reject spoofed `Host` headers            |
| 3     | CORS                | Global      | Handle preflight & origin checks         |
| 4     | Security Headers    | Global      | HSTS (prod), X-Content-Type-Options, etc.|
| 5     | Request ID          | Global      | Generate / propagate `X-Request-ID`      |
| 6     | Request Logger      | Global      | Log method, path, status, duration       |
| —     | Rate Limiter        | Per-route   | `@limiter.limit()` decorator             |
| —     | Auth                | Per-route   | `Depends(require_auth)` dependency       |

---

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

| Code               | HTTP | Trigger                         |
|--------------------|------|---------------------------------|
| `UNAUTHORIZED`     | 401  | Missing / invalid auth          |
| `FORBIDDEN`        | 403  | Insufficient permissions        |
| `NOT_FOUND`        | 404  | Unknown route or resource       |
| `VALIDATION_ERROR` | 422  | Pydantic validation failure     |
| `RATE_LIMITED`      | 429  | Rate limit exceeded             |
| `INTERNAL_ERROR`   | 500  | Unhandled exception             |

---

## Configuration

All settings live in `app/core/config.py` (Pydantic Settings) and are loaded from `.env`.

| Variable             | Default                          | Description                         |
|----------------------|----------------------------------|-------------------------------------|
| `ENVIRONMENT`        | `development`                    | `development` / `production`        |
| `DEBUG`              | `true`                           | Enables Swagger docs & detailed errors |
| `HOST`               | `0.0.0.0`                        | Server bind address                 |
| `PORT`               | `8000`                           | Server port                         |
| `API_KEY`            | `dev-secret-key`                 | API key for auth (placeholder)      |
| `ALLOWED_ORIGINS`    | `localhost:3000, localhost:5173`  | CORS allowed origins                |
| `ALLOWED_HOSTS`      | `*`                              | Trusted host header values          |
| `RATE_LIMIT`         | `100/minute`                     | Default rate limit                  |
| `LOG_LEVEL`          | `INFO`                           | Logging verbosity                   |

**Production validators** automatically reject unsafe config (e.g. `DEBUG=true`, wildcard hosts, default API key).

---

## Adding a New Module

Each domain module is self-contained under `app/modules/`.

### 1. Create the module

```
app/modules/documents/
├── __init__.py
├── router.py      # Route definitions
├── service.py     # Business logic
└── schemas.py     # Pydantic request / response models (optional)
```

### 2. Define routes — `router.py`

```python
from fastapi import APIRouter, Depends, Request

from app.core.middleware.auth import require_auth
from app.core.middleware.rate_limiter import limiter
from app.core.responses import success_response
from app.modules.documents.service import list_documents

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("/", dependencies=[Depends(require_auth)])
@limiter.limit("60/minute")
async def get_documents(request: Request):
    data = list_documents()
    return success_response(data=data)
```

### 3. Implement logic — `service.py`

```python
def list_documents() -> list[dict]:
    return []
```

### 4. Register in the v1 router — `app/api/v1/router.py`

```python
from app.modules.documents.router import router as documents_router

v1_router.include_router(documents_router)
```

The endpoint is now live at `GET /api/v1/documents/`.

---

## Auth

Auth is **opt-in per route** via FastAPI dependencies:

```python
from app.core.middleware.auth import require_auth, require_admin

# Public
@router.get("/public")
async def public_endpoint(): ...

# Authenticated
@router.get("/protected", dependencies=[Depends(require_auth)])
async def protected_endpoint(): ...

# Admin only
@router.delete("/admin-only", dependencies=[Depends(require_admin)])
async def admin_endpoint(): ...
```

Both `require_auth` and `require_admin` are **passthroughs** — swap in real validation when ready.

---

## Rate Limiting

Applied per-route with `slowapi`. The `request: Request` parameter is **required**.

```python
from app.core.middleware.rate_limiter import limiter

@router.get("/data")
@limiter.limit("100/minute")
async def get_data(request: Request): ...

@router.post("/upload")
@limiter.limit("5/minute;50/hour")      # multiple limits
async def upload(request: Request): ...
```

Format: `"<count>/<period>"` — period is `second`, `minute`, `hour`, or `day`.

---

## Testing

```bash
# Run the test suite
pytest

# Quick smoke test (server must be running)
python test_smoke.py
```

---

## Tech Stack

| Category      | Technology                                   |
|---------------|----------------------------------------------|
| Framework     | FastAPI 0.139                                |
| Server        | Uvicorn (ASGI)                               |
| Config        | Pydantic Settings                            |
| Rate Limiting | slowapi                                      |
| Logging       | stdlib `logging` + `python-json-logger`      |
| Testing       | pytest + httpx + pytest-asyncio              |
| Container     | Docker (multi-stage) + Docker Compose        |

---

## Conventions

| Convention                          | Example                                          |
|-------------------------------------|--------------------------------------------------|
| Module routers use a prefix         | `APIRouter(prefix="/candidates")`                |
| All responses use the envelope      | `success_response(data=...)` / `error_response(...)` |
| Status codes use `starlette.status` | `status.HTTP_200_OK`, not `200`                  |
| Config access via singleton         | `get_settings()` (cached with `@lru_cache`)      |
| Logging per module                  | `logger = logging.getLogger(__name__)`           |

---

## Documentation

Extended docs are available under [`docs/`](docs/):

- [Architecture](docs/architecture.md) — modular monolith design, request flow, middleware stack
- [Development Guide](docs/development.md) — setup, adding modules, auth, rate limiting
- [API Reference](docs/api.md) — endpoints, response format, error codes

---
