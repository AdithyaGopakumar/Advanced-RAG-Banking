"""Pydantic schemas for the evaluation subsystem."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class EvalCategory(str, Enum):
    """Evaluation case category."""

    FULLY_SUPPORTED = "fully_supported"
    PARTIALLY_SUPPORTED = "partially_supported"
    UNSUPPORTED = "unsupported"
    AMBIGUOUS = "ambiguous"
    ADVERSARIAL = "adversarial"
    MULTI_HOP = "multi_hop"


class ExpectedBehavior(str, Enum):
    """Expected pipeline behavior."""

    ANSWER = "answer"
    PARTIAL = "partial"
    CLARIFICATION = "clarification"
    REJECTION = "rejection"
    UNAVAILABLE = "unavailable"


class ClaimExpectation(BaseModel):
    """Specific claim expected to be present or supported."""

    model_config = ConfigDict(extra="ignore")

    claim: str
    required_evidence_ids: list[str] = Field(default_factory=list)


class EvaluationCase(BaseModel):
    """A curated test case from the evaluation dataset."""

    model_config = ConfigDict(extra="ignore")

    id: str
    category: EvalCategory
    query: str
    expected_behavior: ExpectedBehavior
    expected_answer: str | None = None
    required_chunk_ids: list[str] = Field(
        default_factory=list,
        description="Ground-truth chunk IDs required for complete evidence recall.",
    )
    expected_claims: list[ClaimExpectation] = Field(default_factory=list)
    forbidden_claims: list[str] = Field(
        default_factory=list,
        description="Claims that must NOT appear in the answer (e.g. unsupported banking facts).",
    )
    metadata: dict[str, Any] = Field(default_factory=dict)


class RetrievalMetrics(BaseModel):
    """Metrics assessing retrieval quality independently from generation."""

    model_config = ConfigDict(extra="ignore")

    hit_rate: float = Field(0.0, description="1.0 if at least one required chunk was retrieved, else 0.0")
    recall_at_1: float = 0.0
    recall_at_3: float = 0.0
    recall_at_5: float = 0.0
    recall_at_8: float = 0.0
    precision_at_5: float = 0.0
    mrr: float = Field(0.0, description="Mean Reciprocal Rank of the first relevant chunk")
    ndcg_at_5: float = 0.0


class GroundingMetrics(BaseModel):
    """Metrics assessing groundedness and policy adherence."""

    model_config = ConfigDict(extra="ignore")

    behavior_correct: bool = False
    policy_compliant: bool = False
    unsupported_claim_rate: float = 0.0
    claim_coverage: float = 0.0
    forbidden_claims_detected: list[str] = Field(default_factory=list)


class CaseEvaluationResult(BaseModel):
    """Evaluation result for one test case."""

    model_config = ConfigDict(extra="ignore")

    case_id: str
    category: EvalCategory
    query: str
    expected_behavior: ExpectedBehavior
    actual_response_type: str
    actual_support_level: str | None = None
    actual_response: str
    retrieved_chunk_ids: list[str] = Field(default_factory=list)
    retrieval_metrics: RetrievalMetrics | None = None
    grounding_metrics: GroundingMetrics | None = None
    passed: bool = False
    failure_reasons: list[str] = Field(default_factory=list)
    latency_ms: float = 0.0


class EvaluationReport(BaseModel):
    """Aggregate benchmark report across test cases."""

    model_config = ConfigDict(extra="ignore")

    run_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    total_cases: int = 0
    passed_cases: int = 0
    pass_rate: float = 0.0
    average_latency_ms: float = 0.0
    retrieval_aggregates: dict[str, float] = Field(default_factory=dict)
    grounding_aggregates: dict[str, float] = Field(default_factory=dict)
    category_summary: dict[str, dict[str, Any]] = Field(default_factory=dict)
    results: list[CaseEvaluationResult] = Field(default_factory=list)
