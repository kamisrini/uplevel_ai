"""
Weekly impact narrative generator.

Aggregates 5-7 daily reports into a WeeklyNarrative that surfaces trends,
momentum, and the most impactful leadership moments of the week.

The narrative is designed to be shared with the leader's manager or used as
input for a weekly leadership check-in.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

import anthropic

from src.agents.report import DailyReport
from src.config import settings
from src.scoring.rubric import DIMENSION_NAMES


@dataclass
class WeeklyNarrative:
    week_start: date
    week_end: date
    dimension_trends: dict[str, list[float]] = field(default_factory=dict)  # dimension → [mon..fri]
    average_scores: dict[str, float] = field(default_factory=dict)
    overall_weekly_score: float = 0.0
    narrative: str = ""  # LLM-generated 2-3 paragraph impact narrative
    top_wins: list[str] = field(default_factory=list)
    key_growth_areas: list[str] = field(default_factory=list)
    recommended_focus: str = ""  # one dimension to prioritise next week


class WeeklyReportGenerator:
    """
    TODO:
    - Accept list[DailyReport] for the target week.
    - Compute dimension trends (daily score per dimension) and weekly averages.
    - Call Anthropic to generate a 2-3 paragraph narrative summarising the week.
    - Identify top win, biggest gap, and recommended focus for next week.
    - Persist WeeklyNarrative to Postgres.
    """

    def __init__(self) -> None:
        self._client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    def generate(self, daily_reports: list[DailyReport]) -> WeeklyNarrative:
        if not daily_reports:
            raise ValueError("Need at least one daily report to generate a weekly narrative.")

        sorted_reports = sorted(daily_reports, key=lambda r: r.report_date)
        week_start = sorted_reports[0].report_date
        week_end = sorted_reports[-1].report_date

        # Compute trends
        trends: dict[str, list[float]] = {dim: [] for dim in DIMENSION_NAMES}
        for report in sorted_reports:
            for dim in DIMENSION_NAMES:
                trends[dim].append(report.dimension_scores.get(dim, 0.0))

        averages = {
            dim: sum(scores) / len(scores) if scores else 0.0
            for dim, scores in trends.items()
        }
        overall = sum(averages.values()) / len(averages) if averages else 0.0

        # TODO: call Anthropic to generate narrative text

        return WeeklyNarrative(
            week_start=week_start,
            week_end=week_end,
            dimension_trends=trends,
            average_scores=averages,
            overall_weekly_score=round(overall, 2),
            narrative="Weekly narrative not yet generated.",
        )
