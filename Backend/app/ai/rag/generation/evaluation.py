"""Curated claim patterns used to check the support policy.

These cases do not call a model. They check that claim labels map to the
response status the product requires.
"""

from app.ai.rag.generation.models import GroundingStatus

GROUNDING_CASES: list[tuple[str, bool, list[tuple[str, str]], GroundingStatus]] = [
    ("no evidence", False, [], "no_relevant_evidence"),
    ("eligibility and fees", True, [("eligibility", "supported"), ("fees", "unsupported")], "partially_supported"),
    ("all supported", True, [("minimum balance", "supported")], "fully_supported"),
    ("all unsupported", True, [("interest rate", "unsupported")], "insufficient_evidence"),
    ("needs a product", True, [("account type", "ambiguous")], "ambiguous"),
    ("supported but ambiguous product", True, [("minimum balance", "supported"), ("which account", "ambiguous")], "ambiguous"),
    ("conflicting limits", True, [("daily limit", "contradictory"), ("daily limit", "supported")], "contradictory_evidence"),
    ("empty assessment", True, [], "insufficient_evidence"),
]
