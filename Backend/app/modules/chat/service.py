"""Chat service executing the agent graph and building response objects."""

import uuid

from app.ai.graphs.workflow import AgentResources, run_agent
from app.modules.chat.schemas import ChatRequest, ChatResponseData, PipelineTrace


class ChatService:
    """Coordinates agent graph execution for user queries."""

    def __init__(self, resources: AgentResources) -> None:
        self._resources = resources

    def ask(self, request: ChatRequest, *, request_id: str | None = None) -> ChatResponseData:
        """Execute one query against the agent graph."""
        query_text = request.effective_message
        full_trace = request.full_trace
        conversation_id = request.conversation_id or str(uuid.uuid4())

        turn = run_agent(
            query_text,
            self._resources,
            conversation_id=conversation_id,
            full_trace=full_trace,
            request_id=request_id,
        )

        trace_model = PipelineTrace.model_validate(turn.trace) if turn.trace else None

        return ChatResponseData(
            conversation_id=turn.conversation_id or conversation_id,
            question=query_text,
            query=query_text,
            resolved_query=turn.resolved_query,
            response=turn.response,
            response_type=turn.response_type,
            support_level=turn.support_level,
            reason_code=turn.reason_code,
            chunk_ids=turn.chunk_ids,
            errors=turn.errors,
            trace=trace_model,
            request_id=request_id,
        )

