"""Smoke tests for the LangGraph graph wiring."""

import pytest

from src.agents.graph import build_graph, run_daily


def test_graph_compiles():
    graph = build_graph()
    assert graph is not None


@pytest.mark.asyncio
async def test_run_daily_returns_state_with_report():
    state = await run_daily(reflection_text="Had a good executive alignment today.")
    assert "daily_report" in state
    report = state["daily_report"]
    assert report is not None
    assert report.report_date is not None


@pytest.mark.asyncio
async def test_run_daily_empty_inputs():
    """Graph should complete gracefully with no ingestion data."""
    state = await run_daily()
    assert "observations" in state
    assert isinstance(state["observations"], list)
