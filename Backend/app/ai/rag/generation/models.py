"""Support decisions and the answer produced from them."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

GroundingStatus = Literal[
    "fully_supported",
    "partially_supported",
    "insufficient_evidence",
    "contradictory_evidence",
    "no_relevant_evidence",
    "ambiguous",
]

ClaimSupportLabel = Literal["supported", "unsupported", "ambiguous", "contradictory"]


class ClaimSupport(BaseModel):
    """One part of a question and whether the evidence supports it."""

    model_config = ConfigDict(extra="forbid")

    text: str
    support: ClaimSupportLabel
    evidence_ids: list[str] = Field(default_factory=list)


class GroundingDecision(BaseModel):
    """Claim-level support and the status that selects a response."""

    model_config = ConfigDict(extra="forbid")

    status: GroundingStatus
    claims: list[ClaimSupport] = Field(default_factory=list)
    clarification: str | None = None


class GeneratedAnswer(BaseModel):
    """A response that stays inside the grounding decision."""

    model_config = ConfigDict(extra="forbid")

    query: str
    status: GroundingStatus
    claims: list[ClaimSupport] = Field(default_factory=list)
    text: str
    clarification: str | None = None
