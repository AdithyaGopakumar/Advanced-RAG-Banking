"""Loads evaluation benchmark datasets."""

import json
from pathlib import Path
from evaluation.schemas.models import EvalCategory, EvaluationCase


def load_dataset(dataset_dir: str | Path | None = None, category: EvalCategory | str | None = None) -> list[EvaluationCase]:
    """Load evaluation cases from JSON files in dataset_dir."""
    if dataset_dir is None:
        base_dir = Path(__file__).parent
    else:
        base_dir = Path(dataset_dir)

    cases: list[EvaluationCase] = []
    category_filter = str(category.value if isinstance(category, EvalCategory) else category).lower() if category else None

    for file_path in base_dir.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            items = data if isinstance(data, list) else data.get("cases", [])
            for item in items:
                case = EvaluationCase.model_validate(item)
                if category_filter is None or case.category.value.lower() == category_filter:
                    cases.append(case)
        except Exception as exc:
            import logging
            logging.getLogger(__name__).warning("Failed to load evaluation dataset %s: %s", file_path, exc)

    return cases
