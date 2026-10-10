"""CLI entrypoint to run banking RAG evaluation benchmarks."""

import argparse
import sys
from pathlib import Path

# Ensure Backend/ is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.modules.chat.dependencies import get_agent_resources
from evaluation.datasets import load_dataset
from evaluation.runners import EvaluationRunner, render_markdown_report, save_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Banking RAG evaluation benchmarks.")
    parser.add_argument(
        "--category",
        choices=["fully_supported", "partially_supported", "unsupported", "ambiguous", "adversarial"],
        help="Filter to run a specific evaluation category",
    )
    parser.add_argument(
        "--output-dir",
        default="evaluation/reports",
        help="Directory to save JSON and Markdown reports",
    )
    args = parser.parse_args()

    cases = load_dataset(category=args.category)
    if not cases:
        print(f"No evaluation cases found for category: {args.category or 'all'}")
        return 1

    print(f"Loaded {len(cases)} evaluation case(s). Initializing pipeline resources...")
    resources = get_agent_resources()
    runner = EvaluationRunner(resources)

    print("Running evaluation suite...")
    report = runner.run_suite(cases)

    json_path, md_path = save_report(report, output_dir=args.output_dir)

    print("\n" + render_markdown_report(report) + "\n")
    print(f"Saved JSON report: {json_path}")
    print(f"Saved Markdown report: {md_path}")

    # Return 0 if pass rate is acceptable, or exit code
    return 0


if __name__ == "__main__":
    sys.exit(main())
