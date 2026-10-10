"""Deterministic transaction and operational scope guardrail.

Rejects operational and transactional requests that are explicitly out-of-scope:
- Fund transfers and payments (NEFT/RTGS/IMPS/UPI execution)
- Personal account balance checks and statements
- Account modifications, PIN/password changes, card blocking
- Loan application execution

Legitimate informational and procedural questions (e.g. "How to transfer via NEFT?",
"What is the procedure to reset PIN?", "What are the rules for blocking a card?")
are allowed to proceed to retrieval.
"""

import re
from pydantic import BaseModel, ConfigDict

TRANSACTION_REJECT_RESPONSE = (
    "I am an informational banking assistant and cannot execute financial transactions, "
    "access personal account balances, or modify account settings. Please use our mobile banking app, "
    "net banking portal, or visit a branch for transaction services."
)

# Questions starting with informational cues should NOT be rejected as transaction execution
_INFORMATIONAL_PREFIXES = re.compile(
    r"^(?:"
    r"how (?:do|can|does|to|should)\b"
    r"|what (?:is|are) (?:the )?(?:steps|procedure|process|rules?|fees?|charges?|limits?|requirements?|timing|hours)\b"
    r"|can (?:i|a customer|someone)\b"
    r"|is it possible to\b"
    r"|explain (?:the|how)\b"
    r"|tell me (?:about|the procedure|the rules|how)\b"
    r"|where can (?:i|a customer)\b"
    r"|why (?:is|does|did)\b"
    r")",
    re.IGNORECASE,
)

# Transactional execution commands
_TRANSACTION_COMMANDS = [
    # Direct money transfer commands with amounts or beneficiaries
    re.compile(
        r"\b(?:transfer|send|wire|remit)\s+(?:(?:rs\.?|inr|\₹|\$)?\s*\d+|money|funds|cash)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:transfer|send)\b.*?\bto\s+(?:account|a/c|beneficiary|upi|mobile|phone|\+?\d{10})\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:pay|recharge)\s+(?:my\s+)?(?:bill|electricity|water|dth|mobile|credit card bill|fastag|broadband)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bmake\s+(?:a\s+)?payment\s+(?:of|for|to)\b", re.IGNORECASE),
    re.compile(r"\b(?:execute|initiate)\s+(?:a\s+)?(?:transfer|payment|transaction)\b", re.IGNORECASE),
    re.compile(r"\b(?:cancel|reverse)\s+(?:my\s+|the\s+)?(?:transaction|payment|transfer)\b", re.IGNORECASE),

    # Personal balance enquiry
    re.compile(
        r"\b(?:what is|tell me|check|view|show|display|get)\s+(?:me\s+)?(?:my\s+)?(?:current\s+|saving\s+|account\s+)?balance\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bhow much (?:money|cash|balance)\s+(?:is in my account|do i have)\b", re.IGNORECASE),
    re.compile(
        r"\b(?:view|download|show|email|send)\s+(?:me\s+)?(?:my\s+)?(?:bank\s+|account\s+)?statement\b",
        re.IGNORECASE,
    ),

    # Account modification & security credentials
    re.compile(
        r"\b(?:reset|change|update)\s+(?:my\s+)?(?:atm\s+)?(?:pin|password|mpin|tpin|net banking password)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:update|change)\s+(?:my\s+)?(?:phone|mobile|email|address|kyc details)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:block|unblock|freeze|hotlist|deactivate)\s+(?:my\s+)?(?:card|debit card|credit card|account)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\b(?:close|terminate)\s+(?:my\s+)?account\b", re.IGNORECASE),

    # Direct loan application submission
    re.compile(
        r"\b(?:apply for|submit|approve)\s+(?:a\s+)?(?:loan|credit card)\s+(?:for me|now|immediately)\b",
        re.IGNORECASE,
    ),
]


class ScopeDecision(BaseModel):
    """Scope classification result."""

    model_config = ConfigDict(extra="forbid")

    allowed: bool
    reason_code: str = "IN_SCOPE"
    response: str | None = None


def check_scope(query: str) -> ScopeDecision:
    """Determine whether the request is within informational scope or an out-of-scope transaction."""
    stripped = query.strip()
    if not stripped:
        return ScopeDecision(allowed=True, reason_code="IN_SCOPE")

    # If it is clearly an informational question, prioritize allowing it
    is_informational = bool(_INFORMATIONAL_PREFIXES.search(stripped))

    for pattern in _TRANSACTION_COMMANDS:
        if pattern.search(stripped):
            # If query has informational phrasing (e.g. "How to transfer money using NEFT"), allow it
            # UNLESS it specifies an actual amount/recipient execution (e.g. "How do I transfer 5000 to John right now")
            if is_informational and not re.search(r"\b(?:\d{3,}|[a-zA-Z]+@upi)\b", stripped):
                continue
            return ScopeDecision(
                allowed=False,
                reason_code="TRANSACTION_OUT_OF_SCOPE",
                response=TRANSACTION_REJECT_RESPONSE,
            )

    return ScopeDecision(allowed=True, reason_code="IN_SCOPE")
