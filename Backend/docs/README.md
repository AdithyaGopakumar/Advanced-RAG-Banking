# AI Recruitment Assistant — Backend Documentation

> Living documentation — updated as the project evolves.

## Table of Contents

| Document | Description |
|----------|-------------|
| [Architecture](./architecture.md) | Project structure, modular monolith design, middleware stack |
| [API Reference](./api.md) | Endpoints, request/response formats, error codes |
| [Development Guide](./development.md) | Local setup, running the server, adding new modules |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| ASGI Server | Uvicorn |
| Config | Pydantic Settings + `.env` |
| Rate Limiting | slowapi |
| AI Orchestration | Custom framework (planned) |
| Database | TBD |
| Background Workers | TBD |

## Quick Start

```bash
cd Backend
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
py run.py
```

Server starts at `http://localhost:8000`. Swagger docs at `/docs`.
