"""Evaluation runner executing test cases against the banking agent pipeline."""

import time
import uuid
from typing import Any
from app.ai.graphs.workflow import AgentResources, run_agent
from evaluation.evaluators.grounding import evaluate_grounding
from evaluation.evaluators.retrieval import compute_retrieval_metrics
from evaluation.schemas.models import (
    CaseEvaluationResult,
    EvaluationCase,
    EvaluationReport,
)


class EvaluationRunner:
    """Executes a suite of evaluation cases against the banking agent."""

    def __init__(self, resources: AgentResources) -> None:
        self.resources = resources

    def evaluate_case(self, case: EvaluationCase) -> CaseEvaluationResult:
        """Execute one test case and compute all evaluation metrics."""
        start_time = time.perf_counter()
        turn = run_agent(
            case.query,
            self.resources,
            full_trace=True,
            request_id=case.id,
            metadata={"evaluation_case_id": case.id, "evaluation_category": case.category.value},
        )
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        retrieved_chunk_ids = list(turn.chunk_ids)
        trace = turn.trace or {}

        # If turn.chunk_ids was empty, extract candidate chunk_ids from trace
        if not retrieved_chunk_ids:
            rerank_step = trace.get("reranking")
            if isinstance(rerank_step, dict):
                ranked = rerank_step.get("ranked_evidence") or []
                retrieved_chunk_ids = [
                    (
                        r["candidate"].get("chunk_id", "")
                        if isinstance(r.get("candidate"), dict)
                        else r.get("chunk_id", "")
                    )
                    for r in ranked
                    if isinstance(r, dict)
                ]
                retrieved_chunk_ids = [cid for cid in retrieved_chunk_ids if cid]


        # 1. Retrieval Metrics
        retrieval_metrics = None
        if case.required_chunk_ids:
            retrieval_metrics = compute_retrieval_metrics(retrieved_chunk_ids, case.required_chunk_ids)

        # 2. Grounding Metrics
        grounding_step = trace.get("grounding")
        claims: list[dict[str, str]] = []
        if isinstance(grounding_step, dict):
            claims = grounding_step.get("claims") or []

        grounding_metrics = evaluate_grounding(
            case=case,
            actual_response_type=turn.response_type,
            actual_support_level=turn.support_level,
            actual_response=turn.response,
            claims=claims,
        )

        # 3. Overall Case Pass/Fail Decision
        failure_reasons: list[str] = []
        if not grounding_metrics.behavior_correct:
            failure_reasons.append(
                f"Expected behavior '{case.expected_behavior.value}', got response_type='{turn.response_type}'"
            )
        if not grounding_metrics.policy_compliant:
            failure_reasons.append("Policy non-compliant")
        if grounding_metrics.forbidden_claims_detected:
            failure_reasons.append(
                f"Forbidden claims detected: {grounding_metrics.forbidden_claims_detected}"
            )
        if retrieval_metrics and retrieval_metrics.hit_rate < 1.0:
            failure_reasons.append(
                f"Required chunks not retrieved: {case.required_chunk_ids} vs {retrieved_chunk_ids}"
            )

        passed = len(failure_reasons) == 0

        return CaseEvaluationResult(
            case_id=case.id,
            category=case.category,
            query=case.query,
            expected_behavior=case.expected_behavior,
            actual_response_type=turn.response_type,
            actual_support_level=turn.support_level,
            actual_response=turn.response,
            retrieved_chunk_ids=retrieved_chunk_ids,
            retrieval_metrics=retrieval_metrics,
            grounding_metrics=grounding_metrics,
            passed=passed,
            failure_reasons=failure_reasons,
            latency_ms=round(elapsed_ms, 2),
        )

    def run_suite(self, cases: list[EvaluationCase]) -> EvaluationReport:
        """Run all test cases and produce an aggregated EvaluationReport."""
        results: list[CaseEvaluationResult] = []
        for case in cases:
            res = self.evaluate_case(case)
            results.append(res)

        total = len(results)
        passed = sum(1 for r in results if r.passed)
        pass_rate = round(passed / total, 4) if total > 0 else 0.0
        avg_latency = round(sum(r.latency_ms for r in results) / total, 2) if total > 0 else 0.0

        # Retrieval aggregates
        retrieval_cases = [r for r in results if r.retrieval_metrics is not None]
        retrieval_agg: dict[str, float] = {}
        if retrieval_cases:
            n_ret = len(retrieval_cases)
            retrieval_agg = {
                "mean_hit_rate": round(sum(r.retrieval_metrics.hit_rate for r in retrieval_cases) / n_ret, 4),
                "mean_recall_at_1": round(sum(r.retrieval_metrics.recall_at_1 for r in retrieval_cases) / n_ret, 4),
                "mean_recall_at_3": round(sum(r.retrieval_metrics.recall_at_3 for r in retrieval_cases) / n_ret, 4),
                "mean_recall_at_5": round(sum(r.retrieval_metrics.recall_at_5 for r in retrieval_cases) / n_ret, 4),
                "mean_recall_at_8": round(sum(r.retrieval_metrics.recall_at_8 for r in retrieval_cases) / n_ret, 4),
                "mean_precision_at_5": round(sum(r.retrieval_metrics.precision_at_5 for r in retrieval_cases) / n_ret, 4),
                "mean_mrr": round(sum(r.retrieval_metrics.mrr for r in retrieval_cases) / n_ret, 4),
                "mean_ndcg_at_5": round(sum(r.retrieval_metrics.ndcg_at_5 for r in retrieval_cases) / n_ret, 4),
            }

        # Grounding aggregates
        grounding_agg: dict[str, float] = {}
        if results:
            grounding_agg = {
                "mean_behavior_accuracy": round(sum(1 for r in results if r.grounding_metrics and r.grounding_metrics.behavior_correct) / total, 4),
                "mean_policy_compliance": round(sum(1 for r in results if r.grounding_metrics and r.grounding_metrics.policy_compliant) / total, 4),
                "mean_claim_coverage": round(sum(r.grounding_metrics.claim_coverage for r in results if r.grounding_metrics) / total, 4),
                "mean_unsupported_claim_rate": round(sum(r.grounding_metrics.unsupported_claim_rate for r in results if r.grounding_metrics) / total, 4),
            }

        # Category summaries
        cat_summary: dict[str, dict[str, Any]] = {}
        for r in results:
            cat_name = r.category.value
            if cat_name not in cat_summary:
                cat_summary[cat_name] = {"total": 0, "passed": 0, "pass_rate": 0.0}
            cat_summary[cat_name]["total"] += 1
            if r.passed:
                cat_summary[cat_name]["passed"] += 1

        for cdata in cat_summary.values():
            if cdata["total"] > 0:
                cdata["pass_rate"] = round(cdata["passed"] / cdata["total"], 4)

        return EvaluationReport(
            run_id=f"eval_run_{uuid.uuid4().hex[:8]}",
            total_cases=total,
            passed_cases=passed,
            pass_rate=pass_rate,
            average_latency_ms=avg_latency,
            retrieval_aggregates=retrieval_agg,
            grounding_aggregates=grounding_agg,
            category_summary=cat_summary,
            results=results,
        )
