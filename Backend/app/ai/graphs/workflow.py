"""LangGraph workflow for one banking question.

The graph routes; retrieval, grounding, and wording stay in their own modules.
A failed retrieval or model call stops at a fixed message instead of guessing.
"""

import logging
from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict, Field
from langgraph.graph import END, START, StateGraph

from app.ai.embeddings.provider import EmbeddingProvider
from app.ai.graphs.state import AgentState
from app.ai.guardrails.input import check_input
from app.ai.guardrails.output import SAFE_FALLBACK, output_is_safe
from app.ai.providers.llm import LLMNotConfiguredError, LLMProvider
from app.ai.rag.generation.answer import GENERATION_FAILED_TEXT, compose_answer, render_response
from app.ai.rag.generation.answer import GenerationFailed
from app.ai.rag.generation.grounding import assess
from app.ai.rag.generation.models import GroundingDecision
from app.ai.rag.indexing.filters import MetadataFilter
from app.ai.rag.retrieval.context import build_context
from app.ai.rag.retrieval.hybrid import LexicalSearcher, retrieve
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

    response: str
    response_type: str
    support_level: str | None = None
    reason_code: str | None = None
    chunk_ids: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


@dataclass
class AgentResources:
    """Dependencies the graph closes over. Tests inject fakes here."""

    embedder: EmbeddingProvider
    vector_store: VectorStore
    lexical_index: LexicalSearcher
    expander: QueryExpander
    reranker: CrossEncoderReranker
    llm: LLMProvider
    metadata_filter: MetadataFilter | None = None
    top_k: int = 8
    candidates_per_query: int = 20
    rrf_k: int = 60
    evidence_top_k: int = 5
    token_budget: int = 3000
    min_score: float | None = None
    input_max_chars: int = 2000


def run_agent(message: str, resources: AgentResources) -> AgentTurn:
    """Run one question through input checks, retrieval, grounding, and output checks."""
    graph = build_agent(resources)
    state = graph.invoke({"user_message": message, "errors": []})
    return AgentTurn(
        response=state.get("response", ""),
        response_type=state.get("response_type", "error"),
        support_level=state.get("support_level"),
        reason_code=state.get("reason_code"),
        chunk_ids=list(state.get("chunk_ids") or []),
        errors=list(state.get("errors") or []),
    )


def build_agent(resources: AgentResources):
    """Compile the workflow. Conversation persistence is intentionally absent."""

    def input_guard(state: AgentState) -> dict[str, object]:
        decision = check_input(state["user_message"], max_chars=resources.input_max_chars)
        if not decision.allowed:
            return {
                "response": decision.response or "",
                "response_type": "rejected",
                "reason_code": decision.reason_code or "MALFORMED_INPUT",
            }
        return {"normalized_query": decision.normalized}

    def retrieve_node(state: AgentState) -> dict[str, object]:
        question = state["normalized_query"]
        try:
            candidates = retrieve(
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
            evidence = build_context(
                question,
                candidates,
                resources.reranker,
                min_score=resources.min_score,
                top_k=resources.evidence_top_k,
                token_budget=resources.token_budget,
            )
        except Exception as exc:
            logger.warning("Retrieval failed", extra={"error_type": type(exc).__name__})
            return _failure("RETRIEVAL_FAILURE", type(exc).__name__, state)
        return {
            "evidence": evidence.model_dump(),
            "chunk_ids": [item.candidate.chunk_id for item in evidence.items],
        }

    def assess_node(state: AgentState) -> dict[str, object]:
        evidence = EvidenceContext.model_validate(state["evidence"])
        try:
            decision = assess(state["normalized_query"], evidence, resources.llm)
        except LLMNotConfiguredError as exc:
            return _failure("LLM_NOT_CONFIGURED", type(exc).__name__, state)
        return {
            "decision": decision.model_dump(),
            "support_level": decision.status,
        }

    def generate_node(state: AgentState) -> dict[str, object]:
        evidence = EvidenceContext.model_validate(state["evidence"])
        decision = GroundingDecision.model_validate(state["decision"])
        try:
            generated = compose_answer(state["normalized_query"], evidence, decision, resources.llm)
        except (GenerationFailed, LLMNotConfiguredError) as exc:
            code = "LLM_NOT_CONFIGURED" if isinstance(exc, LLMNotConfiguredError) else "GENERATION_FAILED"
            return _failure(code, type(exc).__name__, state)
        return _from_answer(generated.text, decision)

    def policy_node(state: AgentState) -> dict[str, object]:
        decision = GroundingDecision.model_validate(state["decision"])
        return _from_answer(render_response(decision, None), decision)

    def output_guard(state: AgentState) -> dict[str, object]:
        return {"output_ok": output_is_safe(state.get("response", ""))}

    def fallback(state: AgentState) -> dict[str, object]:
        errors = list(state.get("errors") or [])
        errors.append("OUTPUT_UNSAFE")
        return {
            "response": SAFE_FALLBACK,
            "response_type": "fallback",
            "reason_code": "OUTPUT_UNSAFE",
            "output_ok": True,
            "errors": errors,
        }

    graph = StateGraph(AgentState)
    graph.add_node("input_guard", input_guard)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("assess", assess_node)
    graph.add_node("generate", generate_node)
    graph.add_node("policy", policy_node)
    graph.add_node("output_guard", output_guard)
    graph.add_node("fallback", fallback)
    graph.add_edge(START, "input_guard")
    graph.add_conditional_edges("input_guard", _route_input, {"reject": END, "retrieve": "retrieve"})
    graph.add_conditional_edges("retrieve", _route_retrieve, {"fail": "output_guard", "assess": "assess"})
    graph.add_conditional_edges(
        "assess",
        _route_assess,
        {"generate": "generate", "policy": "policy", "fail": "output_guard"},
    )
    graph.add_edge("generate", "output_guard")
    graph.add_edge("policy", "output_guard")
    graph.add_conditional_edges("output_guard", _route_output, {"fallback": "fallback", "done": END})
    graph.add_edge("fallback", END)
    return graph.compile()


def _route_input(state: AgentState) -> str:
    if state.get("response_type") == "rejected":
        return "reject"
    return "retrieve"


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
    return {
        "response": GENERATION_FAILED_TEXT,
        "response_type": "error",
        "reason_code": reason_code,
        "errors": errors,
    }


def _from_answer(text: str, decision: GroundingDecision) -> dict[str, object]:
    return {
        "response": text,
        "response_type": _RESPONSE_TYPES.get(decision.status, "unavailable"),
        "support_level": decision.status,
        "reason_code": decision.status.upper(),
    }
