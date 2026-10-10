"""Deterministic checks on the user message before retrieval."""

import re
from pydantic import BaseModel, ConfigDict, Field

from app.ai.guardrails.pii import redact_pii
from app.ai.guardrails.scope import check_scope

_INJECTION = re.compile(
    r"ignore (all |any )?(previous|prior|above) instructions"
    r"|reveal the system prompt"
    r"|use your own knowledge"
    r"|do not follow the (banking )?knowledge base"
    r"|treat this( message)? as a developer instruction"
    r"|disregard the (documents|knowledge base)",
    re.IGNORECASE,
)

_REJECTED = "I can only answer banking questions from the knowledge base."


class InputDecision(BaseModel):
    """Whether a message may enter retrieval."""

    model_config = ConfigDict(extra="forbid")

    allowed: bool
    normalized: str = ""
    reason_code: str | None = None
    response: str | None = None
    pii_detected: list[str] = Field(default_factory=list)


def check_input(message: str, *, max_chars: int) -> InputDecision:
    """Validate message, check injection & scope, and mask sensitive PII."""
    if any(ord(char) < 32 and char not in "\n\r\t" for char in message):
        return InputDecision(allowed=False, reason_code="MALFORMED_INPUT", response=_REJECTED)

    normalized = " ".join(message.split())
    if not normalized:
        return InputDecision(allowed=False, reason_code="MALFORMED_INPUT", response="A question is required.")

    if len(normalized) > max_chars:
        return InputDecision(
            allowed=False,
            reason_code="INPUT_TOO_LARGE",
            response="That message is too long to answer. Please send a shorter question.",
        )

    # Direct prompt injection check
    if _INJECTION.search(normalized):
        return InputDecision(allowed=False, reason_code="PROMPT_INJECTION", response=_REJECTED)

    # Transaction & operational scope check
    scope = check_scope(normalized)
    if not scope.allowed:
        return InputDecision(
            allowed=False,
            reason_code=scope.reason_code,
            response=scope.response,
        )

    # Redact sensitive Indian banking PII before query enters logs, retrieval, or LLM
    sanitized, pii_matches = redact_pii(normalized)
    detected_categories = sorted(list({m.category for m in pii_matches}))

    return InputDecision(
        allowed=True,
        normalized=sanitized,
        pii_detected=detected_categories,
    )
