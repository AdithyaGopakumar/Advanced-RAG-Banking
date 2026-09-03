# Development Guide

## Prerequisites

- Python 3.10+
- pip

## Local Setup

```bash
# 1. Navigate to the backend
cd Backend

# 2. Create virtual environment
py -m venv venv

# 3. Activate it
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment
cp .env.example .env
# Edit .env as needed

# 6. Run the server
py run.py
```

The server starts at `http://localhost:8000` with hot-reload enabled in development.

## Running the Server

### Option A: via run.py (recommended)

```bash
py run.py
```

Includes exit/signal handlers, uncaught exception hook, and reads host/port from `.env`.

### Option B: via uvicorn directly

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Useful when you need custom uvicorn flags.

## Verify It Works

```bash
# Health check
curl http://localhost:8000/api/v1/system/health

# Swagger docs
open http://localhost:8000/docs
```

---

## Adding a New Module

Each domain module is self-contained under `app/modules/`. Here's how to add one:

### 1. Create the module directory

```
app/modules/candidates/
├── __init__.py
├── router.py          # Route definitions
├── service.py         # Business logic
├── schemas.py         # Pydantic request/response models (optional)
```

### 2. Define the router — `router.py`

```python
from fastapi import APIRouter, Depends, Request

from app.core.middleware.auth import require_auth
from app.core.middleware.rate_limiter import limiter
from app.core.responses import success_response
from app.modules.candidates.service import list_candidates

router = APIRouter(prefix="/candidates", tags=["Candidates"])


@router.get("/", dependencies=[Depends(require_auth)])
@limiter.limit("60/minute")
async def get_candidates(request: Request):
    data = list_candidates()
    return success_response(data=data)
```

### 3. Define the service — `service.py`

```python
def list_candidates() -> list[dict]:
    # Business logic here
    return []
```

### 4. Register in the v1 router — `app/api/v1/router.py`

```python
from app.modules.candidates.router import router as candidates_router

v1_router.include_router(candidates_router)
```

That's it. The endpoint is now live at `GET /api/v1/candidates/`.

---

## Auth Dependencies

Auth is opt-in per route. Import and use as a FastAPI dependency:

```python
from fastapi import Depends
from app.core.middleware.auth import require_auth, require_admin

# Public — no dependency
@router.get("/public")
async def public_endpoint(): ...

# Requires authentication
@router.get("/protected", dependencies=[Depends(require_auth)])
async def protected_endpoint(): ...

# Requires admin role
@router.delete("/admin-only", dependencies=[Depends(require_admin)])
async def admin_endpoint(): ...

# Protect an entire router
router = APIRouter(dependencies=[Depends(require_auth)])
```

Both `require_auth` and `require_admin` are passthroughs for now — implement real validation when ready.

---

## Rate Limiting

Applied per-route via decorator. The `request: Request` parameter is **required** by slowapi.

```python
from app.core.middleware.rate_limiter import limiter

@router.get("/data")
@limiter.limit("100/minute")          # 100 requests per minute per IP
async def get_data(request: Request):
    ...

@router.post("/upload")
@limiter.limit("5/minute;50/hour")    # Multiple limits
async def upload(request: Request):
    ...
```

Format: `"<count>/<period>"` — period is `second`, `minute`, `hour`, or `day`.

---

## Project Conventions

| Convention | Example |
|-----------|---------|
| Module routers use a prefix | `APIRouter(prefix="/candidates")` |
| All responses use the envelope | `success_response(data=...)` / `error_response(...)` |
| Status codes use `starlette.status` | `status.HTTP_200_OK`, not `200` |
| Config access via singleton | `get_settings()` (cached with `@lru_cache`) |
| Logging per module | `logger = logging.getLogger(__name__)` |
