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
@limiter.limit("60/minute")
async def chat(
    request: Request,
    payload: ChatRequest,
    full_trace: bool | None = Query(None, alias="fullTrace", description="Query param override for full trace"),
    service: ChatService = Depends(get_chat_service),
):
    """Ask a banking question. Expects JSON body with query, conversationId, fullTrace."""
    if full_trace is not None:
        payload.full_trace = full_trace
    request_id = getattr(request.state, "request_id", None)
    data = service.ask(payload, request_id=request_id)
    return success_response(data=data.model_dump())

