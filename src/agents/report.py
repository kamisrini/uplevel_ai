"""
Report agent node.

Assembles scored observations, dimension aggregates, and reflection output into
a structured DailyReport that can be persisted to Postgres and served via the API.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from src.agents.observation import Observation
from src.agents.reflection import ReflectionOutput
from src.agents.scoring import DimensionAggregate, ScoredObservation


@dataclass
class DailyReport:
    report_date: date
    observations: list[Observation] = field(default_factory=list)
    scored_observations: list[ScoredObservation] = field(default_factory=list)
    dimension_scores: dict[str, float] = field(default_factory=dict)  # dimension → average
    overall_score: float = 0.0  # average across all dimensions
    reflection: ReflectionOutput | None = None

    def to_dict(self) -> dict:
        """Serialise to JSON-safe dict for API responses."""
        return {
            "report_date": self.report_date.isoformat(),
            "dimension_scores": self.dimension_scores,
            "overall_score": round(self.overall_score, 2),
            "summary": self.reflection.summary if self.reflection else "",
            "strengths": self.reflection.strengths if self.reflection else [],
            "growth_areas": self.reflection.growth_areas if self.reflection else [],
            "prompts": self.reflection.prompts if self.reflection else [],
        }


async def build_report(state: dict) -> dict:
    """
    LangGraph node: report.

    Input state keys:
      - observations, scored_observations, dimension_aggregates, reflection, report_date

    Output state keys (added):
      - daily_report: DailyReport

    TODO:
    - Compute overall_score as weighted average across dimension_aggregates.
    - Populate DailyReport dataclass from state.
    - Persist report to Postgres via memory.postgres module.
    - Update Neo4j relationship graph with any new stakeholder/influence edges detected.
    """
    from datetime import date as _date

    aggregates: dict[str, DimensionAggregate] = state.get("dimension_aggregates", {})
    dimension_scores = {name: agg.average for name, agg in aggregates.items()}
    overall = sum(dimension_scores.values()) / len(dimension_scores) if dimension_scores else 0.0

    report = DailyReport(
        report_date=state.get("report_date", _date.today()),
        observations=state.get("observations", []),
        scored_observations=state.get("scored_observations", []),
        dimension_scores=dimension_scores,
        overall_score=overall,
        reflection=state.get("reflection"),
    )

    return {**state, "daily_report": report}
