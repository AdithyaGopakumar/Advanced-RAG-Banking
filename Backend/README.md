# Cognibank AI — Hybrid, Multi-Turn RAG Agent — Backend

Production-oriented FastAPI backend for Cognibank AI — Hybrid, Multi-Turn RAG Agent. Built around the **modular monolith** pattern — code is organized by domain, not by technical layer.

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
│   │   ├── system/                 # Health check & observability status
│   │   ├── chat/                   # Banking chat agent endpoint & service
│   │   └── knowledge/              # Knowledge domain models & identity
│   │       ├── models.py           # KnowledgeDocument, KnowledgeSection, KnowledgeChunk
│   │       └── identity.py         # Deterministic chunk IDs & content hashing
│   │
│   ├── ingestion/                  # Knowledge → retrieval artifact pipeline (CLI/job-driven)
│   │
│   ├── ai/                         # AI & RAG infrastructure
│   │   ├── embeddings/             # Embedding utilities (sentence-transformers / OpenAI)
│   │   ├── prompts/                # Versioned prompt templates
│   │   ├── providers/              # LLM provider adapters (OpenAI / mock)
│   │   ├── memory/                 # Multi-turn memory (store.py, context.py anaphora engine, models.py)
│   │   ├── rag/                    # Dense/lexical retrieval, MQE, RRF, reranking, context
│   │   ├── guardrails/             # Input/output safety, PII detection, NeMo Colang rails
│   │   ├── graphs/                 # LangGraph state machine & agent workflow
│   │   └── observability/          # LangSmith distributed tracing & metadata tagging
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

- Python 3.10 – 3.12 (Recommended: Python 3.10. Note: Python 3.14+ is currently not supported by upstream ML dependencies like PyYAML, PyTorch, etc. without Microsoft C++ Build Tools)
- pip

### Local Setup

```powershell
# 1. Navigate to the Backend folder
cd Backend

# 2. Create & activate virtual environment (.venv)
python -m venv .venv

# Windows PowerShell:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass   # Run if script execution is restricted
.\.venv\Scripts\Activate.ps1

# macOS / Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env           # On Windows: copy .env.example .env

# 5. Start the backend server
python run.py
# (or uvicorn main:app --reload)

# 6. Launch the Streamlit UI (in a new terminal)
.\.venv\Scripts\streamlit.exe run ../frontend/app.py
```

The backend server runs at **http://localhost:8000** (Swagger docs at `/docs`).
The Streamlit interface runs at **http://localhost:8501**.

### Knowledge ingestion

Run this from the `Backend` directory after the virtual environment is active and dependencies are installed. The first run with the default embedding model downloads `paraphrase-MiniLM-L6-v2`, so the machine needs network access.

```powershell
# Windows PowerShell, from Backend/
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

Dense vectors are stored in Pinecone only when both `PINECONE_API_KEY` and `PINECONE_INDEX_NAME` are set. Create that index first with **384 dimensions** and the **cosine** metric. The command does not create it. A successful Pinecone run writes `INDEX_MANIFEST_PATH` (default `.index/manifest.json`) so the next run upserts changed chunks and deletes removed ids. With Pinecone unset, vectors stay in memory for that process and the manifest is not written. The lexical index stays in Elasticsearch. Set `ELASTICSEARCH_URL` and either `ELASTICSEARCH_API_KEY` or `ELASTICSEARCH_USERNAME` and `ELASTICSEARCH_PASSWORD` in `.env`.

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
| `ELASTICSEARCH_URL` | `http://localhost:9200` | Elasticsearch endpoint. Set this to the Elastic Cloud URL |
| `ELASTICSEARCH_INDEX` | `knowledge-chunks` | Lexical index name |
| `ELASTICSEARCH_API_KEY` | empty | Elastic Cloud API key |
| `ELASTICSEARCH_USERNAME` | empty | Basic-auth user, used when no API key is set |
| `ELASTICSEARCH_PASSWORD` | empty | Basic-auth password, used when no API key is set |

Copy `.env.example` to `.env` and edit those values there. `.env` is loaded from the current directory, so run `python ingest.py` from `Backend`.

### Docker

From `Backend`, with Docker running. This builds the API image and installs the backend requirements. Elasticsearch credentials in `.env` are the cloud cluster.

```bash
docker compose up --build
```

The API is at `http://localhost:8000`.

To run the local Elasticsearch and Kibana deployment later, start the `local` profile. That file points the API at the Compose cluster and ignores the cloud credentials for that run. Kibana is at `http://localhost:5601`.

```bash
docker compose --profile local -f docker-compose.yml -f docker-compose.local.yml up --build
```

```bash
# Image only
docker compose build

# Production-style run of the built image
docker build -t fastapi-app .
docker run -p 8000:8000 --env-file .env fastapi-app
```

### Verify

```bash
curl http://localhost:8000/api/v1/system/health
# → {"success": true, "data": {"status": "healthy", ...}}
```

### Chat & Retrieval Testing API

Ask questions and inspect step-by-step intermediate pipeline outputs (input guardrails, MQE, vector search, BM25 search, RRF, reranking, context assembly, grounding, generation, output guardrails):

**POST `/api/v1/chat`** *(or `/api/v1/chat/test`)*:

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is BSBDA?", "fullTrace": true}'
```

Request body fields:
- `question` (or `query` / `message`): The user's banking query.
- `fullTrace` (boolean, default `false`): When `true`, returns all intermediate pipeline step outputs in `data.trace`.

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
| `eval.py`  | Benchmark evaluation — execute golden test cases & compute metrics   |
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
| `LANGCHAIN_TRACING_V2` | `false`                        | Enable LangSmith distributed tracing |
| `LANGCHAIN_API_KEY`  | empty                            | LangSmith API key                   |
| `LANGCHAIN_PROJECT`  | `rag-bank-development`           | LangSmith project name              |
| `LANGCHAIN_ENDPOINT` | `https://api.smith.langchain.com` | LangSmith API endpoint              |
| `ENABLE_NEMO_GUARDRAILS` | `false`                      | Enable NeMo Guardrails & Colang flows |
| `NEMO_GUARDRAILS_CONFIG_PATH` | `app/ai/guardrails/nemo` | Path to NeMo config & Colang flows  |
| `ENABLE_CONVERSATION_MEMORY` | `true`                   | Enable multi-turn session state & memory |
| `MAX_MEMORY_TURNS`   | `5`                              | Maximum turns preserved in memory context |

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

## Evaluation & Benchmarking

The system includes a governed evaluation and benchmarking pipeline adhering to `docs/EVALUATION.md` (Phases E0–E3). Curated test cases reside in `evaluation/datasets/` across 5 categories (`fully_supported`, `partially_supported`, `unsupported`, `ambiguous`, `adversarial`).

### Running Evaluations

```powershell
# Run the complete evaluation suite
python eval.py

# Run a specific category
python eval.py --category adversarial
python eval.py --category fully_supported
python eval.py --category unsupported

# Specify custom report output directory
python eval.py --output-dir evaluation/reports
```

### Metrics Computed

- **Retrieval Metrics**: `Hit@K`, `Recall@K`, `Precision@K`, `MRR` (Mean Reciprocal Rank), `nDCG@K`.
- **Grounding & Policy Metrics**: `behavior_accuracy`, `policy_compliance`, `claim_coverage`, `unsupported_claim_rate`, forbidden claim violation checks.
- **RAGAS Integration**: RAGAS metric adapter with deterministic offline heuristic fallback.

Reports are automatically generated and saved to `evaluation/reports/` in both JSON (`eval_run_<id>.json`) and Markdown (`eval_run_<id>.md`) formats.

---

## Observability & LangSmith Tracing

The backend features integrated distributed tracing compliant with `docs/AGENT_DESIGN.md` and `docs/EVALUATION.md`. Tracing covers the entire LangGraph orchestration cycle: input guardrails, query processing (MQE), dense & lexical retrieval, Reciprocal Rank Fusion (RRF), semantic reranking, context assembly, grounding validation, and generation.

### Enabling Tracing

To enable LangSmith tracing, configure the following variables in `.env`:

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2_pt_...
LANGCHAIN_PROJECT=rag-bank-development
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

When disabled (`LANGCHAIN_TRACING_V2=false` or `LANGCHAIN_API_KEY` omitted), the pipeline operates with zero overhead and offline safety.

### Observability Diagnostic Endpoint

Check real-time tracing status via:

```bash
curl http://localhost:8000/api/v1/system/observability
```

Response envelope:
```json
{
  "success": true,
  "data": {
    "enabled": true,
    "project": "rag-bank-development",
    "endpoint": "https://api.smith.langchain.com",
    "langsmith_installed": true
  }
}
```

### Privacy & PII Protection

In compliance with banking security rules (`docs/SECURITY.md`), all deterministic PII guardrails run *before* context construction and generation. Customer identifiers (PAN, Aadhaar, account numbers, card numbers) are masked (`[REDACTED_PAN]`, etc.) prior to tracing and LLM prompt assembly, preventing leakage of sensitive financial data into trace backends.

---

## Guardrails & Safety Architecture

The system enforces a multi-layered defense architecture (`docs/GUARDRAILS.md`) combining deterministic controls and model-aware Colang dialog flows via NVIDIA NeMo Guardrails:

```
User Query
    ↓
1. Deterministic Input Guardrails (Length, regex injection, PII masking, transaction scope checks)
    ↓
2. NeMo Input Rails & Colang Flows (Greetings, off-topic deflection, speculative advice refusal, jailbreaks)
    ↓
3. Governed RAG Retrieval & Semantic Grounding Assessment
    ↓
4. LLM Generation (Strictly evidence-bounded)
    ↓
5. NeMo Output Rails (Forbidden claim detection & transaction commitment blocks)
    ↓
6. Deterministic Output Sanitization (Leak markers, prompt protection, PII masking)
    ↓
Final Response Envelope
```

### NeMo Guardrails & Colang Flows

Colang flow specifications reside under `app/ai/guardrails/nemo/`:
- `banking_dialog.co`: Natural conversation handling (greetings, identity, capabilities, and pass-through to retrieval).
- `off_topic.co`: Off-topic deflection (recipes, jokes, coding questions) and speculative financial advice refusals.
- `jailbreaks.co`: Active prompt injection and system jailbreak deflection.

### Enabling NeMo Guardrails

To enable NeMo Guardrails, set the following variable in `.env`:

```env
ENABLE_NEMO_GUARDRAILS=true
NEMO_GUARDRAILS_CONFIG_PATH="app/ai/guardrails/nemo"
```

When disabled (`ENABLE_NEMO_GUARDRAILS=false`), the system relies on the fast deterministic guardrail layer with zero overhead.

### Diagnostic Endpoint

Inspect live guardrails configuration, NeMo version, and safety layers via:

```bash
curl http://localhost:8000/api/v1/system/guardrails
```

---

## Multi-Turn Conversation Memory & Session Continuity

The chat agent supports continuous multi-turn conversations while enforcing the strict **Knowledge-Base-Only Policy** (`AGENTS.md` Sections 36 & 37, `docs/AGENT_DESIGN.md` Section 12).

### Information Hierarchy & Primacy Rules

```text
Governed Knowledge Base Evidence
        >
Conversation Memory (Context Only)
        >
LLM Pretrained Knowledge (Never Authoritative)
```

- **Reference Resolution Only**: Conversation memory is used strictly to resolve anaphora, pronouns ("it", "this card", "that account"), and inherit antecedent banking products/entities across follow-ups.
- **No Hallucinated Authority**: Facts or statements made in previous conversational turns cannot bypass retrieval grounding. Answering banking claims requires evidence from the governed knowledge base.

### API Usage

To maintain continuity across dialogue turns, pass the `conversationId` returned from turn 1 into subsequent requests:

#### Turn 1: Initial Question
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the Fixed Deposit interest rates?"}'
```
Response:
```json
{
  "success": true,
  "data": {
    "conversationId": "c92d5218-e8cb-469b-8f19-a1b7e4f9b231",
    "query": "What are the Fixed Deposit interest rates?",
    "resolvedQuery": "What are the Fixed Deposit interest rates?",
    "response": "Fixed deposit rates range up to 7.25% p.a. depending on tenure.",
    "response_type": "answer",
    "support_level": "fully_supported"
  }
}
```

#### Turn 2: Contextual Follow-up
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "conversationId": "c92d5218-e8cb-469b-8f19-a1b7e4f9b231",
    "query": "What about premature closure?",
    "fullTrace": true
  }'
```
The agent automatically loads recent session history, resolves the query to `"What about premature closure? for Fixed Deposit"`, and executes hybrid retrieval against the governed corpus.

---

## Tech Stack

| Category      | Technology                                   |
|---------------|----------------------------------------------|
| Framework     | FastAPI 0.139                                |
| Server        | Uvicorn (ASGI)                               |
| Orchestration | LangGraph 1.0                                |
| Guardrails    | NeMo Guardrails 0.24 (Colang) + Deterministic|
| Observability | LangSmith 0.14                               |
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
