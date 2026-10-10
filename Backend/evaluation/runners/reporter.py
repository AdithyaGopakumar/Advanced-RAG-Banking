"""Generates Markdown and JSON benchmark evaluation reports."""

import json
from pathlib import Path
from evaluation.schemas.models import EvaluationReport


def render_markdown_report(report: EvaluationReport) -> str:
    """Format an EvaluationReport into human-readable Markdown."""
    lines: list[str] = [
        f"# Benchmark Evaluation Report: `{report.run_id}`",
        "",
        f"- **Timestamp:** {report.timestamp}",
        f"- **Total Cases:** {report.total_cases}",
        f"- **Passed Cases:** {report.passed_cases} ({report.pass_rate * 100:.1f}%)",
        f"- **Average Latency:** {report.average_latency_ms:.1f} ms",
        "",
        "## Category Performance",
        "",
        "| Category | Total Cases | Passed | Pass Rate |",
        "|---|---|---|---|",
    ]

    for cat, data in report.category_summary.items():
        lines.append(f"| `{cat}` | {data['total']} | {data['passed']} | {data['pass_rate'] * 100:.1f}% |")

    lines.append("")
    lines.append("## Retrieval Metrics (Independent of Generation)")
    lines.append("")
    if report.retrieval_aggregates:
        lines.append("| Metric | Value |")
        lines.append("|---|---|")
        for k, v in report.retrieval_aggregates.items():
            lines.append(f"| `{k}` | {v} |")
    else:
        lines.append("*No retrieval-labeled cases evaluated in this run.*")

    lines.append("")
    lines.append("## Grounding & Policy Compliance Metrics")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---|")
    for k, v in report.grounding_aggregates.items():
        lines.append(f"| `{k}` | {v} |")

    lines.append("")
    lines.append("## Case Details")
    lines.append("")
    lines.append("| Case ID | Category | Expected Behavior | Actual Response Type | Result | Latency |")
    lines.append("|---|---|---|---|---|---|")
    for r in report.results:
        status_icon = "PASS" if r.passed else "FAIL"
        lines.append(
            f"| `{r.case_id}` | `{r.category.value}` | `{r.expected_behavior.value}` | `{r.actual_response_type}` | **{status_icon}** | {r.latency_ms:.1f}ms |"
        )

    return "\n".join(lines)


def save_report(report: EvaluationReport, output_dir: str | Path | None = None) -> tuple[Path, Path]:
    """Save report as both JSON and Markdown in output_dir."""
    if output_dir is None:
        target_dir = Path(__file__).resolve().parents[1] / "reports"
    else:
        target_dir = Path(output_dir)

    target_dir.mkdir(parents=True, exist_ok=True)

    json_path = target_dir / f"{report.run_id}.json"
    md_path = target_dir / f"{report.run_id}.md"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report.model_dump(), f, indent=2)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(render_markdown_report(report))

    return json_path, md_path
