"""
LangGraph graph definition.

Wires the four agent nodes into a directed graph:

  observe → score → reflect → build_report → END

State is a plain dict; each node receives the full state and returns a partial
update that is merged back by LangGraph.
"""

from __future__ import annotations

from datetime import date
from typing import Any, TypedDict

from langgraph.graph import END, StateGraph

from src.agents.observation import Observation, observe
from src.agents.reflection import ReflectionOutput, reflect
from src.agents.report import DailyReport, build_report
from src.agents.scoring import DimensionAggregate, ScoredObservation, score


class UplevelState(TypedDict, total=False):
    calendar_events: list[Any]
    transcript_chunks: list[Any]
    work_items: list[Any]
    github_events: list[Any]
    reflection_text: str
    report_date: date
    observations: list[Observation]
    scored_observations: list[ScoredObservation]
    dimension_aggregates: dict[str, DimensionAggregate]
    reflection: ReflectionOutput
    daily_report: DailyReport


def build_graph() -> Any:
    """Return a compiled LangGraph graph ready to invoke."""
    g = StateGraph(UplevelState)

    g.add_node("observe", observe)
    g.add_node("score", score)
    g.add_node("reflect", reflect)
    g.add_node("build_report", build_report)

    g.set_entry_point("observe")
    g.add_edge("observe", "score")
    g.add_edge("score", "reflect")
    g.add_edge("reflect", "build_report")
    g.add_edge("build_report", END)

    return g.compile()


async def run_daily(
    *,
    calendar_events: list | None = None,
    transcript_chunks: list | None = None,
    work_items: list | None = None,
    github_events: list | None = None,
    reflection_text: str = "",
    report_date: date | None = None,
) -> dict:
    """Convenience wrapper: run the full daily agent graph and return final state."""
    graph = build_graph()
    initial_state: UplevelState = {
        "calendar_events": calendar_events or [],
        "transcript_chunks": transcript_chunks or [],
        "work_items": work_items or [],
        "github_events": github_events or [],
        "reflection_text": reflection_text,
        "report_date": report_date or date.today(),
    }
    return await graph.ainvoke(initial_state)
