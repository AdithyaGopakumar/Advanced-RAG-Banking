"""Deterministic checks and sanitization on a drafted answer before it is returned."""

import re
from app.ai.guardrails.pii import redact_pii
from app.ai.prompts.generation import GENERATION_SYSTEM_PROMPT, GROUNDING_SYSTEM_PROMPT

_LEAK_MARKERS = (
    GENERATION_SYSTEM_PROMPT[:48],
    GROUNDING_SYSTEM_PROMPT[:48],
    "<<<evidence>>>",
    "Traceback (most recent call last):",
)
# Pre-casefold static markers once at module load to avoid repeated string allocations
_LEAK_MARKERS_FOLDED = tuple(marker.casefold() for marker in _LEAK_MARKERS)

_INSTRUCTION_LEAK = re.compile(
    r"(?i)\b(?:you are a helpful banking assistant|system prompt:|treat retrieved documents as data)\b"
)

SAFE_FALLBACK = "The answer could not be shown because it did not pass the output check."


def output_is_safe(text: str) -> bool:
    """Reject an empty reply or one that echoes system instructions or internal errors."""
    if not text.strip():
        return False
    folded = text.casefold()
    if any(marker in folded for marker in _LEAK_MARKERS_FOLDED):
        return False
    if _INSTRUCTION_LEAK.search(text):
        return False
    return True


def sanitize_output(text: str) -> str:
    """Sanitize the drafted answer by masking any leaked PII before delivery."""
    if not text:
        return text
    sanitized, _ = redact_pii(text)
    return sanitized
