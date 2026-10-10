"""Retrieval guardrails and indirect prompt-injection sanitization.

Defends against untrusted instruction injection inside retrieved knowledge chunks.
Treats all retrieved knowledge strictly as data and neutralizes instruction override
attempts before context assembly. Also validates chunk governance status.
"""

import re
from typing import NamedTuple

# Indirect injection patterns that could attempt to hijack model execution
_INDIRECT_INJECTION_PATTERNS = [
    re.compile(r"(?i)\bignore (?:all |any )?(?:previous|prior|above) instructions\b"),
    re.compile(r"(?i)\breveal (?:the )?system prompt\b"),
    re.compile(r"(?i)\byou are now (?:in developer mode|unrestricted|jailbroken|a developer assistant)\b"),
    re.compile(r"(?i)\btreat this (?:text|content|excerpt|document) as (?:a )?developer instruction\b"),
    re.compile(r"(?i)\bdisregard (?:the )?(?:knowledge base|documents|banking policies?)\b"),
    re.compile(r"(?i)\b(?:system|developer) (?:instructions?|prompt)[:=]"),
    re.compile(r"(?i)\bnew instructions?:\s*"),
    re.compile(r"(?i)\boverride policy:\s*"),
]

_FILTERED_REPLACEMENT = "[UNTRUSTED_INSTRUCTION_REDACTED]"

# Permitted governance status for knowledge to enter answering context
_PERMITTED_STATUSES = {"approved", "current"}


class SanitizedChunk(NamedTuple):
    """Result of sanitizing a retrieved chunk."""

    text: str
    injections_detected: list[str]


def sanitize_chunk_text(text: str) -> SanitizedChunk:
    """Sanitize retrieved chunk text by neutralizing instruction override directives."""
    if not text:
        return SanitizedChunk(text="", injections_detected=[])

    injections_found: list[str] = []
    sanitized = text

    for pattern in _INDIRECT_INJECTION_PATTERNS:
        matches = pattern.findall(sanitized)
        if matches:
            injections_found.extend([str(m).strip() for m in matches])
            sanitized = pattern.sub(_FILTERED_REPLACEMENT, sanitized)

    return SanitizedChunk(text=sanitized, injections_detected=injections_found)


def is_chunk_governance_valid(status: str | None) -> bool:
    """Ensure chunk status belongs to approved/current governance lifecycle."""
    if not status:
        return False
    return status.strip().lower() in _PERMITTED_STATUSES
