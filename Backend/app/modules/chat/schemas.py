"""Request and response schemas for the chat module."""

from pydantic import BaseModel, ConfigDict, Field

from app.ai.rag.generation.models import ClaimSupport
from app.ai.rag.indexing.models import RetrievalHit
from app.ai.rag.retrieval.models import FusedCandidate, RankedEvidence


class ChatRequest(BaseModel):
    """User query payload."""

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    question: str | None = Field(default=None, description="The user's banking question.")
    query: str | None = Field(default=None, description="Alternative alias for question.")
    message: str | None = Field(default=None, description="Alternative alias for question.")
    full_trace: bool = Field(default=False, alias="fullTrace", description="Return full trace of each step.")

    @property
    def effective_message(self) -> str:
        """Return the effective question/query text."""
        for candidate in (self.question, self.query, self.message):
            if candidate is not None and candidate.strip():
                return candidate.strip()
        return (self.question or self.query or self.message or "").strip()



class StepInputGuardrail(BaseModel):
    """Output of input guardrail check."""

    model_config = ConfigDict(extra="ignore")

    allowed: bool
    normalized_query: str = ""
    reason_code: str | None = None
    response: str | None = None
    pii_detected: list[str] = Field(default_factory=list)
    nemo_decision: dict[str, object] | None = None


class StepMQE(BaseModel):
    """Output of Multi-Query Expansion."""

    model_config = ConfigDict(extra="ignore")

    queries: list[str] = Field(default_factory=list)


class QueryHits(BaseModel):
    """Search hits for one query formulation."""

    model_config = ConfigDict(extra="ignore")

    query: str
    hits: list[RetrievalHit] = Field(default_factory=list)


class StepRRF(BaseModel):
    """Output of Reciprocal Rank Fusion."""

    model_config = ConfigDict(extra="ignore")

    fused_candidates: list[FusedCandidate] = Field(default_factory=list)
    total_fused: int = 0


class StepReranking(BaseModel):
    """Output of semantic reranking."""

    model_config = ConfigDict(extra="ignore")

    ranked_evidence: list[RankedEvidence] = Field(default_factory=list)
    total_ranked: int = 0


class StepContext(BaseModel):
    """Context assembled for the LLM."""

    model_config = ConfigDict(extra="ignore")

    text: str = ""
    item_count: int = 0
    omitted: int = 0
    exceeds_budget: bool = False
    estimated_tokens: int = 0


class StepGrounding(BaseModel):
    """Claim-level assessment and support status."""

    model_config = ConfigDict(extra="ignore")

    status: str
    claims: list[ClaimSupport] = Field(default_factory=list)
    clarification: str | None = None


class StepGeneration(BaseModel):
    """Model drafting and rendered response."""

    model_config = ConfigDict(extra="ignore")

    draft_answer: str | None = None
    rendered_response: str = ""


class StepOutputGuardrail(BaseModel):
    """Output guardrail safety check."""

    model_config = ConfigDict(extra="ignore")

    output_ok: bool
    fallback_triggered: bool = False
    final_response: str = ""
    nemo_decision: dict[str, object] | None = None


class PipelineTrace(BaseModel):
    """Full step-by-step trace of intermediate outputs."""

    model_config = ConfigDict(extra="ignore")

    input_guardrail: StepInputGuardrail | None = None
    mqe: StepMQE | None = None
    vector_search: list[QueryHits] | None = None
    bm25_search: list[QueryHits] | None = None
    rrf: StepRRF | None = None
    reranking: StepReranking | None = None
    context: StepContext | None = None
    grounding: StepGrounding | None = None
    generation: StepGeneration | None = None
    output_guardrail: StepOutputGuardrail | None = None


class ChatResponseData(BaseModel):
    """Chat response payload inside the standard envelope."""

    model_config = ConfigDict(extra="ignore")

    question: str = ""
    query: str = ""
    response: str
    response_type: str
    support_level: str | None = None
    reason_code: str | None = None
    chunk_ids: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    trace: PipelineTrace | None = None
    request_id: str | None = None

