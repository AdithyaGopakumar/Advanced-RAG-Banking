"""LangGraph workflow for one banking question.

The graph routes; retrieval, grounding, and wording stay in their own modules.
A failed retrieval or model call stops at a fixed message instead of guessing.
"""

from datetime import date
import logging
from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict, Field
from langgraph.graph import END, START, StateGraph

from app.ai.embeddings.provider import EmbeddingProvider
from app.ai.graphs.state import AgentState
from app.ai.guardrails.input import check_input
from app.ai.guardrails.nemo_adapter import get_nemo_service
from app.ai.guardrails.output import SAFE_FALLBACK, output_is_safe, sanitize_output
from app.ai.memory import (
    ConversationSession,
    SessionStore,
    format_history_for_prompt,
    resolve_contextual_query,
)
from app.ai.observability.tracer import build_trace_config
from app.ai.providers.llm import LLMNotConfiguredError, LLMProvider
from app.ai.rag.generation.answer import GENERATION_FAILED_TEXT, compose_answer, render_response
from app.ai.rag.generation.answer import GenerationFailed
from app.ai.rag.generation.grounding import assess
from app.ai.rag.generation.models import GroundingDecision
from app.ai.rag.indexing.filters import MetadataFilter
from app.ai.rag.retrieval.context import assemble_context, select_evidence
from app.ai.rag.retrieval.hybrid import LexicalSearcher, retrieve_detailed
from app.ai.rag.retrieval.models import EvidenceContext
from app.ai.rag.retrieval.mqe import QueryExpander
from app.ai.rag.retrieval.reranker import CrossEncoderReranker
from app.ai.rag.indexing.vector_store import VectorStore

logger = logging.getLogger(__name__)

_RESPONSE_TYPES = {
    "fully_supported": "answer",
    "partially_supported": "partial",
    "ambiguous": "clarification",
    "contradictory_evidence": "conflict",
    "insufficient_evidence": "unavailable",
    "no_relevant_evidence": "unavailable",
}


class AgentTurn(BaseModel):
    """The user-facing result of one graph run."""

    model_config = ConfigDict(extra="forbid")

    conversation_id: str | None = None
    resolved_query: str | None = None
    response: str
    response_type: str
    support_level: str | None = None
    reason_code: str | None = None
    chunk_ids: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    trace: dict[str, object] | None = None


@dataclass
class AgentResources:
    """Dependencies the graph closes over. Tests inject fakes here."""

    embedder: EmbeddingProvider
    vector_store: VectorStore
    lexical_index: LexicalSearcher
    expander: QueryExpander
    reranker: CrossEncoderReranker
    llm: LLMProvider
    session_store: SessionStore | None = None
    max_memory_turns: int = 5
    metadata_filter: MetadataFilter | None = None
    top_k: int = 8
    candidates_per_query: int = 20
    rrf_k: int = 60
    evidence_top_k: int = 5
    token_budget: int = 3000
    min_score: float | None = None
    input_max_chars: int = 2000
    compiled_graph: object = None

    def get_graph(self) -> object:
        """Return the compiled LangGraph workflow, compiling and caching it once."""
        if self.compiled_graph is None:
            self.compiled_graph = build_agent(self)
        return self.compiled_graph


def run_agent(
    message: str,
    resources: AgentResources,
    *,
    conversation_id: str | None = None,
    full_trace: bool = False,
    request_id: str | None = None,
    metadata: dict[str, object] | None = None,
) -> AgentTurn:
    """Run one question through input checks, retrieval, grounding, and output checks."""
    graph = resources.get_graph()
    config = build_trace_config(
        request_id=request_id,
        run_name="banking_agent_turn",
        metadata={
            "conversation_id": conversation_id,
            "full_trace": full_trace,
            "top_k": resources.top_k,
            "evidence_top_k": resources.evidence_top_k,
            "token_budget": resources.token_budget,
            **(metadata or {}),
        },
    )
    state = graph.invoke(
        {
            "conversation_id": conversation_id,
            "user_message": message,
            "full_trace": full_trace,
            "errors": [],
            "trace": {},
        },
        config=config,
    )
    return AgentTurn(
        conversation_id=conversation_id,
        resolved_query=state.get("resolved_query"),
        response=state.get("response", ""),
        response_type=state.get("response_type", "error"),
        support_level=state.get("support_level"),
        reason_code=state.get("reason_code"),
        chunk_ids=list(state.get("chunk_ids") or []),
        errors=list(state.get("errors") or []),
        trace=state.get("trace") if full_trace else None,
    )


def build_agent(resources: AgentResources):
    """Compile the workflow. Conversation persistence is intentionally absent."""

    def input_guard(state: AgentState) -> dict[str, object]:
        decision = check_input(state["user_message"], max_chars=resources.input_max_chars)
        is_full_trace = state.get("full_trace", False)
        trace = dict(state.get("trace") or {})
        if not decision.allowed:
            if is_full_trace:
                trace["input_guardrail"] = {
                    "allowed": False,
                    "normalized_query": decision.normalized,
                    "reason_code": decision.reason_code,
                    "response": decision.response,
                    "pii_detected": decision.pii_detected,
                    "nemo_decision": None,
                }
            return {
                "response": decision.response or "",
                "response_type": "rejected",
                "reason_code": decision.reason_code or "MALFORMED_INPUT",
                "trace": trace,
            }

        nemo_service = get_nemo_service()
        nemo_res = nemo_service.check_input_sync(decision.normalized)

        if is_full_trace:
            trace["input_guardrail"] = {
                "allowed": decision.allowed and nemo_res.allowed,
                "normalized_query": decision.normalized,
                "reason_code": nemo_res.reason_code if not nemo_res.allowed else decision.reason_code,
                "response": nemo_res.response if not nemo_res.allowed else decision.response,
                "pii_detected": decision.pii_detected,
                "nemo_decision": nemo_res.model_dump(),
            }

        if not nemo_res.allowed:
            return {
                "response": nemo_res.response or "I can only answer banking questions from the knowledge base.",
                "response_type": "rejected",
                "reason_code": nemo_res.reason_code,
                "trace": trace,
            }

        return {"normalized_query": decision.normalized, "trace": trace}

    def load_context_node(state: AgentState) -> dict[str, object]:
        conversation_id = state.get("conversation_id")
        normalized_query = state.get("normalized_query", "")
        is_full_trace = state.get("full_trace", False)
        trace = dict(state.get("trace") or {})

        history_messages = []
        formatted_history = []
        if conversation_id and resources.session_store is not None:
            session = resources.session_store.get(conversation_id)
            if session:
                history_messages = session.get_recent_messages(max_turns=resources.max_memory_turns)
                formatted_history = format_history_for_prompt(history_messages)

        # Contextualize follow-up query using recent turn history
        resolved = resolve_contextual_query(
            normalized_query,
            history_messages,
        )

        if is_full_trace:
            trace["conversation"] = {
                "conversation_id": conversation_id,
                "history_turns": len(history_messages) // 2,
                "resolved_query": resolved,
                "context": formatted_history,
            }

        return {
            "conversation_context": formatted_history,
            "resolved_query": resolved,
            "trace": trace,
        }

    def retrieve_node(state: AgentState) -> dict[str, object]:
        question = state.get("resolved_query") or state["normalized_query"]
        is_full_trace = state.get("full_trace", False)
        trace = dict(state.get("trace") or {})
        try:
            retrieval = retrieve_detailed(
                question,
                embedder=resources.embedder,
                vector_store=resources.vector_store,
                lexical_index=resources.lexical_index,
                expander=resources.expander,
                metadata_filter=resources.metadata_filter,
                top_k=resources.top_k,
                candidates_per_query=resources.candidates_per_query,
                rrf_k=resources.rrf_k,
            )
            ranked_evidence = select_evidence(
                question,
                retrieval.top_candidates,
                resources.reranker,
                as_of=date.today().isoformat(),
                min_score=resources.min_score,
                top_k=resources.evidence_top_k,
            )
            evidence = assemble_context(
                question,
                ranked_evidence,
                token_budget=resources.token_budget,
            )
        except Exception as exc:
            logger.warning("Retrieval failed", extra={"error_type": type(exc).__name__})
            return _failure("RETRIEVAL_FAILURE", type(exc).__name__, state)

        if is_full_trace:
            trace["mqe"] = {"queries": retrieval.queries}
            trace["vector_search"] = [
                {"query": step.query, "hits": [hit.model_dump() for hit in step.dense_hits]}
                for step in retrieval.searches
            ]
            trace["bm25_search"] = [
                {"query": step.query, "hits": [hit.model_dump() for hit in step.bm25_hits]}
                for step in retrieval.searches
            ]
            trace["rrf"] = {
                "fused_candidates": [candidate.model_dump() for candidate in retrieval.all_fused],
                "total_fused": len(retrieval.all_fused),
            }
            trace["reranking"] = {
                "ranked_evidence": [item.model_dump() for item in ranked_evidence],
                "total_ranked": len(ranked_evidence),
            }
            trace["context"] = {
                "text": evidence.text,
                "item_count": len(evidence.items),
                "omitted": evidence.omitted,
                "exceeds_budget": evidence.exceeds_budget,
                "estimated_tokens": max(1, len(evidence.text) // 4) if evidence.text else 0,
            }

        return {
            "evidence": evidence.model_dump(),
            "chunk_ids": [item.candidate.chunk_id for item in evidence.items],
            "trace": trace,
        }

    def assess_node(state: AgentState) -> dict[str, object]:
        evidence = EvidenceContext.model_validate(state["evidence"])
        is_full_trace = state.get("full_trace", False)
        trace = dict(state.get("trace") or {})
        try:
            decision = assess(state["normalized_query"], evidence, resources.llm)
        except LLMNotConfiguredError as exc:
            return _failure("LLM_NOT_CONFIGURED", type(exc).__name__, state)

        if is_full_trace:
            trace["grounding"] = decision.model_dump()

        return {
            "decision": decision.model_dump(),
            "support_level": decision.status,
            "trace": trace,
        }

    def generate_node(state: AgentState) -> dict[str, object]:
        evidence = EvidenceContext.model_validate(state["evidence"])
        decision = GroundingDecision.model_validate(state["decision"])
        is_full_trace = state.get("full_trace", False)
        trace = dict(state.get("trace") or {})
        try:
            generated = compose_answer(state["normalized_query"], evidence, decision, resources.llm)
        except (GenerationFailed, LLMNotConfiguredError) as exc:
            code = "LLM_NOT_CONFIGURED" if isinstance(exc, LLMNotConfiguredError) else "GENERATION_FAILED"
            return _failure(code, type(exc).__name__, state)

        if is_full_trace:
            trace["generation"] = {
                "draft_answer": generated.text,
                "rendered_response": generated.text,
            }

        out = _from_answer(generated.text, decision)
        out["trace"] = trace
        return out

    def policy_node(state: AgentState) -> dict[str, object]:
        decision = GroundingDecision.model_validate(state["decision"])
        is_full_trace = state.get("full_trace", False)
        trace = dict(state.get("trace") or {})
        rendered = render_response(decision, None)

        if is_full_trace:
            trace["generation"] = {
                "draft_answer": None,
                "rendered_response": rendered,
            }

        out = _from_answer(rendered, decision)
        out["trace"] = trace
        return out

    def output_guard(state: AgentState) -> dict[str, object]:
        raw_response = state.get("response", "")
        safe = output_is_safe(raw_response)
        nemo_res = None
        if safe:
            nemo_service = get_nemo_service()
            nemo_res = nemo_service.check_output_sync(
                message=state.get("user_message", ""),
                drafted_answer=raw_response,
            )
            if not nemo_res.allowed:
                safe = False

        if not safe:
            if nemo_res and not nemo_res.allowed and nemo_res.response:
                sanitized = nemo_res.response
            else:
                sanitized = SAFE_FALLBACK
        else:
            sanitized = sanitize_output(raw_response)

        is_full_trace = state.get("full_trace", False)
        trace = dict(state.get("trace") or {})
        if is_full_trace:
            trace["output_guardrail"] = {
                "output_ok": safe,
                "fallback_triggered": not safe,
                "final_response": sanitized,
                "nemo_decision": nemo_res.model_dump() if nemo_res else None,
            }
        return {"output_ok": safe, "response": sanitized, "trace": trace}

    def fallback(state: AgentState) -> dict[str, object]:
        errors = list(state.get("errors") or [])
        errors.append("OUTPUT_UNSAFE")
        is_full_trace = state.get("full_trace", False)
        trace = dict(state.get("trace") or {})
        if is_full_trace:
            trace["output_guardrail"] = {
                "output_ok": False,
                "fallback_triggered": True,
                "final_response": SAFE_FALLBACK,
            }
        return {
            "response": SAFE_FALLBACK,
            "response_type": "fallback",
            "reason_code": "OUTPUT_UNSAFE",
            "output_ok": True,
            "errors": errors,
            "trace": trace,
        }

    def persist_node(state: AgentState) -> dict[str, object]:
        conversation_id = state.get("conversation_id")
        if conversation_id and resources.session_store is not None:
            session = resources.session_store.get(conversation_id) or ConversationSession(
                conversation_id=conversation_id
            )
            session.add_turn(
                user_content=state.get("user_message", ""),
                assistant_content=state.get("response", ""),
                response_type=state.get("response_type"),
                reason_code=state.get("reason_code"),
                chunk_ids=state.get("chunk_ids"),
            )
            resources.session_store.save(session)
        return {}

    graph = StateGraph(AgentState)
    graph.add_node("input_guard", input_guard)
    graph.add_node("load_context", load_context_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("assess", assess_node)
    graph.add_node("generate", generate_node)
    graph.add_node("policy", policy_node)
    graph.add_node("output_guard", output_guard)
    graph.add_node("fallback", fallback)
    graph.add_node("persist", persist_node)

    graph.add_edge(START, "input_guard")
    graph.add_conditional_edges("input_guard", _route_input, {"reject": END, "allowed": "load_context"})
    graph.add_edge("load_context", "retrieve")
    graph.add_conditional_edges("retrieve", _route_retrieve, {"fail": "output_guard", "assess": "assess"})
    graph.add_conditional_edges(
        "assess",
        _route_assess,
        {"generate": "generate", "policy": "policy", "fail": "output_guard"},
    )
    graph.add_edge("generate", "output_guard")
    graph.add_edge("policy", "output_guard")
    graph.add_conditional_edges("output_guard", _route_output, {"fallback": "fallback", "done": "persist"})
    graph.add_edge("fallback", "persist")
    graph.add_edge("persist", END)
    return graph.compile()


def _route_input(state: AgentState) -> str:
    if state.get("response_type") == "rejected":
        return "reject"
    return "allowed"


def _route_retrieve(state: AgentState) -> str:
    if state.get("reason_code") == "RETRIEVAL_FAILURE":
        return "fail"
    return "assess"


def _route_assess(state: AgentState) -> str:
    if state.get("response_type") == "error":
        return "fail"
    status = state.get("support_level")
    claims = (state.get("decision") or {}).get("claims") or []
    supported = any(isinstance(claim, dict) and claim.get("support") == "supported" for claim in claims)
    if status in {"fully_supported", "partially_supported"} or (status == "ambiguous" and supported):
        return "generate"
    return "policy"


def _route_output(state: AgentState) -> str:
    if state.get("output_ok"):
        return "done"
    return "fallback"


def _failure(reason_code: str, error_type: str, state: AgentState) -> dict[str, object]:
    errors = list(state.get("errors") or [])
    errors.append(error_type)
    trace = dict(state.get("trace") or {})
    return {
        "response": GENERATION_FAILED_TEXT,
        "response_type": "error",
        "reason_code": reason_code,
        "errors": errors,
        "trace": trace,
    }



def _from_answer(text: str, decision: GroundingDecision) -> dict[str, object]:
    return {
        "response": text,
        "response_type": _RESPONSE_TYPES.get(decision.status, "unavailable"),
        "support_level": decision.status,
        "reason_code": decision.status.upper(),
    }
