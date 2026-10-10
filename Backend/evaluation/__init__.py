"""Evaluation subsystem package."""

from evaluation.datasets import load_dataset
from evaluation.evaluators import compute_retrieval_metrics, evaluate_grounding
from evaluation.runners import EvaluationRunner, render_markdown_report, save_report
from evaluation.schemas import (
    CaseEvaluationResult,
    EvalCategory,
    EvaluationCase,
    EvaluationReport,
    ExpectedBehavior,
    GroundingMetrics,
    RetrievalMetrics,
)

__all__ = [
    "CaseEvaluationResult",
    "EvalCategory",
    "EvaluationCase",
    "EvaluationReport",
    "EvaluationRunner",
    "ExpectedBehavior",
    "GroundingMetrics",
    "RetrievalMetrics",
    "compute_retrieval_metrics",
    "evaluate_grounding",
    "load_dataset",
    "render_markdown_report",
    "save_report",
]
