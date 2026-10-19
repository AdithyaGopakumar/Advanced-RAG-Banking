"""Deterministic checks on the user message before retrieval."""

import re
from pydantic import BaseModel, ConfigDict, Field

from app.ai.guardrails.pii import redact_pii
from app.ai.guardrails.scope import check_scope

# Control characters below ASCII 32 excluding newline (\n=0x0a), tab (\t=0x09), and carriage return (\r=0x0d)
_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")

# Direct prompt injection attempts trying to override system boundaries
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
    """Validate message, check injection & scope, and mask sensitive PII.

    Deterministic Pipeline:
    1. Fast raw length boundary guard (DoS prevention)
    2. Non-printable control characters scan
    3. Whitespace normalization & empty message validation
    4. Normalized length verification
    5. Direct prompt injection regex pattern match
    6. Transaction & operational scope refusal
    7. Indian banking PII detection and redaction
    """
    # 1. Fast boundary guard: reject massive inputs immediately before expensive processing
    if len(message) > max_chars * 2:
        return InputDecision(
            allowed=False,
            reason_code="INPUT_TOO_LARGE",
            response="That message is too long to answer. Please send a shorter question.",
        )

    # 2. Control characters scan (reject binary payloads / terminal escapes)
    if _CONTROL_CHARS.search(message):
        return InputDecision(allowed=False, reason_code="MALFORMED_INPUT", response=_REJECTED)

    # 3. Whitespace normalization & empty message validation
    normalized = " ".join(message.split())
    if not normalized:
        return InputDecision(allowed=False, reason_code="MALFORMED_INPUT", response="A question is required.")

    # 4. Normalized character length verification
    if len(normalized) > max_chars:
        return InputDecision(
            allowed=False,
            reason_code="INPUT_TOO_LARGE",
            response="That message is too long to answer. Please send a shorter question.",
        )

    # 5. Direct prompt injection scan
    if _INJECTION.search(normalized):
        return InputDecision(allowed=False, reason_code="PROMPT_INJECTION", response=_REJECTED)

    # 6. Transaction & operational scope refusal (transfers, card blocks, account changes)
    scope = check_scope(normalized)
    if not scope.allowed:
        return InputDecision(
            allowed=False,
            reason_code=scope.reason_code,
            response=scope.response,
        )

    # 7. Redact sensitive Indian banking PII (Aadhaar, PAN, Cards, IFSC, Mobile)
    sanitized, pii_matches = redact_pii(normalized)
    detected_categories = sorted(list({m.category for m in pii_matches}))

    return InputDecision(
        allowed=True,
        normalized=sanitized,
        pii_detected=detected_categories,
    )
