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
│   │       ├── rate_limiter.py     # slowapi limiter + custom 429 handler
│   │       ├── request_id.py       # Generate / propagate X-Request-ID
│   │       ├── request_logger.py   # Log method, path, status, duration per request
│   │       └── security_headers.py # HSTS, X-Content-Type-Options, etc.
│   │
│   ├── api/                        # API layer — thin route aggregation
│   │   └── v1/
│   │       └── router.py           # Imports & mounts all module routers under /api/v1
│   │
│   ├── modules/                    # Domain modules — each is self-contained
│   │   ├── system/                 # System module (health check)
│   │   │   ├── router.py           # Route definitions
│   │   │   └── service.py          # Business logic
│   │   │
│   │   └── knowledge/              # Knowledge domain module
│   │       ├── models.py           # KnowledgeDocument, KnowledgeSection, KnowledgeChunk
│   │       └── identity.py         # Deterministic chunk IDs & content hashing
│   │
│   ├── ingestion/                  # Knowledge → retrieval artifact transformation
│   │                               # (CLI/job-driven, NOT HTTP-dependent)
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
├── tests/                          # Test suite
└── docs/                           # Documentation (you are here)
```

## Domain Boundaries

The architecture separates three distinct concerns:

```
app/modules/knowledge/     Domain knowledge concepts (models, identity)
app/ai/                    AI infrastructure (embeddings, providers, prompts)
app/ingestion/             Knowledge → retrieval artifact transformation
```

**Why separate?**
- Knowledge models are domain concepts — they exist independently of AI.
- AI infrastructure may change (swap embedding providers, LLM providers) without touching domain models.
- Ingestion is a batch/CLI process, not an HTTP request handler.

## Retrieval Artifact Hierarchy

The retrieval representation follows a three-level hierarchy:

```
KnowledgeDocument          Governed knowledge unit (product, policy, FAQ, etc.)
       ↓
KnowledgeSection           Structural context inside a document (H2/H3 headings)
       ↓
KnowledgeChunk             Primary retrieval unit for the RAG pipeline
```

Each level has a distinct role:

| Level | Role | Example |
|-------|------|---------|
| KnowledgeDocument | Governance context — version, status, ownership | ACCT-SA-001 (Savings Account) |
| KnowledgeSection | Structural context — heading, position | ACCT-SA-001::eligibility |
| KnowledgeChunk | Retrieval unit — text + metadata + provenance | ACCT-SA-001::eligibility::001 |

**These concepts are NOT collapsed into a single `Document` model.**

### Deterministic Chunk Identity

Chunk IDs are deterministic — the same inputs always produce the same ID:

```
DOCUMENT_ID::section-slug::NNN
```

Examples:
```
ACCT-SA-001::eligibility::000
LOAN-HL-001::interest-rates::003
FAQ-ACCT-001::q-what-is-the-minimum-balance::000
```

This enables:
- **Idempotent ingestion** — re-processing produces the same IDs
- **Change detection** — content hash changes when text changes
- **Reproducible indexing** — same source → same artifacts
- **Debugging** — chunk ID traces directly to source document and section

### Content Hashing

Each chunk carries a SHA-256 content hash of its text. If the source text changes, the hash changes, signalling that derived artifacts (embeddings, vector indexes) need regeneration.

### Metadata, Provenance, and Relationships

These are **structurally separate** on each chunk:

| Concern | Model | Purpose |
|---------|-------|---------|
| **Metadata** | `ChunkMetadata` | Filtering, faceted search, retrieval ranking |
| **Provenance** | `ChunkProvenance` | Traces chunk → section → document → source → version |
| **Relationships** | `KnowledgeRelationship` | Typed links (governed_by, requires, etc.) |

**Metadata is first-class** — it is not concatenated into chunk text.

**Provenance is mandatory** — every retrieval artifact is traceable back to governed knowledge.

**Relationships are typed** — not arbitrary text references. Types include: `governed_by`, `requires`, `explained_by`, `applies_to`, `references`, `complements`, `alternative_to`, `parent_of`, `supersedes`, `summarises`, `compares`.

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

## Intentionally Deferred

The following are NOT implemented and are left for later phases:

| Component | Phase |
|-----------|-------|
| Database (PostgreSQL, SQLAlchemy, migrations) | When persistence is needed |
| Vector database (Qdrant, pgvector) | Phase 1B — indexing |
| Embedding providers (OpenAI, etc.) | Phase 1B — indexing |
| Hybrid retrieval (BM25 + Dense + RRF) | Phase 1B — retrieval |
| Reranker | Phase 1B — retrieval |
| LLM generation pipeline | Phase 2 — generation |
| Query router / intent detection | Phase 2 — query understanding |
| Live banking APIs | Future |
| Production authentication (JWT/OAuth2) | Production readiness |
| Redis / message queues | When async processing is needed |
| Agent frameworks | Future |
