"""Tests for the daily report renderer."""

from datetime import date

from src.agents.report import DailyReport
from src.agents.reflection import ReflectionOutput
from src.reports.daily import render_json, render_markdown


def _make_report() -> DailyReport:
    return DailyReport(
        report_date=date(2026, 5, 23),
        dimension_scores={"strategic_influence": 4.0, "delegation_effectiveness": 3.5},
        overall_score=3.75,
        reflection=ReflectionOutput(
            summary="Strong day for strategic influence.",
            strengths=["strategic_influence"],
            growth_areas=["org_leverage"],
            prompts=["What could you have delegated today?"],
        ),
    )


def test_render_markdown_contains_date():
    md = render_markdown(_make_report())
    assert "2026-05-23" in md


def test_render_markdown_contains_score():
    md = render_markdown(_make_report())
    assert "3.8" in md or "3.75" in md


def test_render_json_has_required_keys():
    data = render_json(_make_report())
    assert "report_date" in data
    assert "overall_score" in data
    assert "dimension_scores" in data
