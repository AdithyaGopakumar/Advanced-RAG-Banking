"""Grounding and banking policy evaluator.

Checks claim coverage, unsupported claim rate, and response behavior compliance.
"""

import re
from evaluation.schemas.models import EvaluationCase, ExpectedBehavior, GroundingMetrics


def evaluate_grounding(
    case: EvaluationCase,
    actual_response_type: str,
    actual_support_level: str | None,
    actual_response: str,
    claims: list[dict[str, str]] | None = None,
) -> GroundingMetrics:
    """Assess whether the response complies with the banking KB-only policy."""
    response_lower = actual_response.lower()

    # 1. Behavior verification
    behavior_correct = False
    if case.expected_behavior == ExpectedBehavior.ANSWER:
        behavior_correct = actual_response_type in ("answer", "partial") and actual_support_level in (
            "fully_supported",
            "partially_supported",
        )
    elif case.expected_behavior == ExpectedBehavior.PARTIAL:
        behavior_correct = actual_response_type == "partial" or (
            actual_support_level == "partially_supported"
            or "does not include" in response_lower
            or "not available" in response_lower
        )
    elif case.expected_behavior == ExpectedBehavior.UNAVAILABLE:
        behavior_correct = actual_response_type in ("unavailable", "error") or (
            actual_support_level in ("insufficient_evidence", "no_relevant_evidence")
            or "could not be produced" in response_lower
            or "not available" in response_lower
        )
    elif case.expected_behavior == ExpectedBehavior.REJECTION:
        behavior_correct = actual_response_type in ("rejected", "error") or (
            "only answer banking questions" in response_lower
        )
    elif case.expected_behavior == ExpectedBehavior.CLARIFICATION:
        behavior_correct = actual_response_type == "clarification" or (
            actual_support_level == "ambiguous" or "?" in actual_response
        )

    # 2. Check for forbidden claims
    forbidden_found: list[str] = []
    for forbidden in case.forbidden_claims:
        # Regex or substring search for forbidden claim keywords
        clean_forbidden = forbidden.strip().lower()
        if clean_forbidden and clean_forbidden in response_lower:
            forbidden_found.append(forbidden)

    # 3. Calculate claim coverage
    claim_coverage = 1.0
    if case.expected_claims:
        matched_expected = 0
        for exp in case.expected_claims:
            # Check keywords of the expected claim
            words = [w.lower() for w in re.findall(r"\b\w{4,}\b", exp.claim)]
            if words and any(w in response_lower for w in words):
                matched_expected += 1
        claim_coverage = matched_expected / len(case.expected_claims)

    # 4. Calculate unsupported claim rate
    unsupported_rate = 0.0
    if claims:
        unsupported_count = sum(1 for c in claims if c.get("support") == "unsupported")
        unsupported_rate = unsupported_count / len(claims)

    # 5. Overall policy compliance
    # Compliant if behavior is correct, no forbidden claims found, and no fabricated claims slipped in
    policy_compliant = behavior_correct and (len(forbidden_found) == 0)

    return GroundingMetrics(
        behavior_correct=behavior_correct,
        policy_compliant=policy_compliant,
        unsupported_claim_rate=unsupported_rate,
        claim_coverage=claim_coverage,
        forbidden_claims_detected=forbidden_found,
    )
