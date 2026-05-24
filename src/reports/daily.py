"""
Daily assessment report generator.

Renders a DailyReport into human-readable markdown and a structured JSON payload
suitable for API consumers or email delivery.
"""

from __future__ import annotations

from src.agents.report import DailyReport
from src.scoring.rubric import RUBRIC_BY_NAME


def render_markdown(report: DailyReport) -> str:
    """
    Render a DailyReport as a markdown string for display or email.

    TODO:
    - Render dimension scores as a progress-bar style table.
    - Highlight dimensions that are at VP level (5/5) vs. gaps (<3).
    - Include reflection summary and growth prompts.
    - Append a "trend vs. yesterday" section using Postgres history.
    """
    lines = [
        f"# Uplevel Daily Report — {report.report_date.isoformat()}",
        "",
        f"**Overall Score:** {report.overall_score:.1f} / 5.0",
        "",
        "## Dimension Scores",
    ]

    for dim_name, avg in sorted(report.dimension_scores.items(), key=lambda x: -x[1]):
        rubric_dim = RUBRIC_BY_NAME.get(dim_name)
        label = dim_name.replace("_", " ").title() if not rubric_dim else rubric_dim.name.replace("_", " ").title()
        bar = "█" * round(avg) + "░" * (5 - round(avg))
        lines.append(f"- **{label}**: {bar} {avg:.1f}")

    if report.reflection:
        lines += [
            "",
            "## Summary",
            report.reflection.summary,
        ]
        if report.reflection.strengths:
            lines += ["", "## Strengths Today"]
            lines += [f"- {s}" for s in report.reflection.strengths]
        if report.reflection.growth_areas:
            lines += ["", "## Growth Areas"]
            lines += [f"- {g}" for g in report.reflection.growth_areas]
        if report.reflection.prompts:
            lines += ["", "## Reflection Prompts"]
            lines += [f"{i+1}. {p}" for i, p in enumerate(report.reflection.prompts)]

    return "\n".join(lines)


def render_json(report: DailyReport) -> dict:
    """Return a JSON-serialisable dict of the daily report."""
    return report.to_dict()
