"""Chat module routes."""

from fastapi import APIRouter, Depends, Query, Request

from app.ai.graphs.workflow import AgentResources
from app.core.middleware.auth import require_auth
from app.core.middleware.rate_limiter import limiter
from app.core.responses import success_response
from app.modules.chat.dependencies import get_agent_resources
from app.modules.chat.schemas import ChatRequest
from app.modules.chat.service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])


def get_chat_service(resources: AgentResources = Depends(get_agent_resources)) -> ChatService:
    return ChatService(resources)


@router.post("", dependencies=[Depends(require_auth)])
@router.post("/", dependencies=[Depends(require_auth)])
@router.post("/test", dependencies=[Depends(require_auth)])
@limiter.limit("60/minute")
async def chat_post(
    request: Request,
    payload: ChatRequest,
    full_trace: bool | None = Query(None, alias="fullTrace", description="Optional query parameter override for full trace"),
    service: ChatService = Depends(get_chat_service),
):
    """Ask a banking question via POST with question/query in request body."""
    if full_trace is not None:
        payload.full_trace = full_trace
    data = service.ask(payload)
    return success_response(data=data.model_dump())


@router.get("", dependencies=[Depends(require_auth)])
@router.get("/", dependencies=[Depends(require_auth)])
@router.get("/test", dependencies=[Depends(require_auth)])
@limiter.limit("60/minute")
async def chat_get(
    request: Request,
    question: str | None = Query(None, description="User question"),
    query: str | None = Query(None, description="Alternative alias for question"),
    full_trace: bool = Query(False, alias="fullTrace", description="Include step-by-step trace"),
    service: ChatService = Depends(get_chat_service),
):
    """Ask a banking question via GET for quick testing."""
    payload = ChatRequest(question=question, query=query, full_trace=full_trace)
    data = service.ask(payload)
    return success_response(data=data.model_dump())

