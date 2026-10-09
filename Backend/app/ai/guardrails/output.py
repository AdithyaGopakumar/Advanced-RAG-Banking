"""Deterministic checks on a drafted answer before it is returned."""

from app.ai.prompts.generation import GENERATION_SYSTEM_PROMPT, GROUNDING_SYSTEM_PROMPT

_LEAK_MARKERS = (
    GENERATION_SYSTEM_PROMPT[:48],
    GROUNDING_SYSTEM_PROMPT[:48],
    "<<<evidence>>>",
)

SAFE_FALLBACK = "The answer could not be shown because it did not pass the output check."


def output_is_safe(text: str) -> bool:
    """Reject an empty reply or one that echoes system instructions."""
    if not text.strip():
        return False
    folded = text.casefold()
    return not any(marker.casefold() in folded for marker in _LEAK_MARKERS)
