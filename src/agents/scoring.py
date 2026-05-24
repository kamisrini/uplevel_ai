"""
Scoring agent node.

Takes the list of Observation objects from the observation node and scores
each one against the VP Engineering rubric using the LeadershipClassifier.

Produces a list of ScoredObservation objects and aggregated dimension scores.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.agents.observation import Observation
from src.scoring.classifier import ClassificationResult


@dataclass
class ScoredObservation:
    observation: Observation
    classifications: list[ClassificationResult] = field(default_factory=list)


@dataclass
class DimensionAggregate:
    dimension: str
    scores: list[int] = field(default_factory=list)

    @property
    def average(self) -> float:
        return sum(self.scores) / len(self.scores) if self.scores else 0.0

    @property
    def peak(self) -> int:
        return max(self.scores, default=0)


async def score(state: dict) -> dict:
    """
    LangGraph node: scoring.

    Input state keys:
      - observations: list[Observation]

    Output state keys (added):
      - scored_observations: list[ScoredObservation]
      - dimension_aggregates: dict[str, DimensionAggregate]

    TODO:
    - Instantiate LeadershipClassifier once per graph run (not per observation).
    - Call classifier.classify() for each observation.
    - Aggregate scores per rubric dimension.
    - Handle observations that don't map to any dimension (filter or mark as UNKNOWN).
    """
    observations: list[Observation] = state.get("observations", [])

    scored: list[ScoredObservation] = []
    aggregates: dict[str, DimensionAggregate] = {}

    for obs in observations:
        # TODO: uncomment when classifier is implemented
        # classifications = classifier.classify(obs.summary)
        classifications: list[ClassificationResult] = []
        scored.append(ScoredObservation(observation=obs, classifications=classifications))

        for cls in classifications:
            if cls.dimension not in aggregates:
                aggregates[cls.dimension] = DimensionAggregate(dimension=cls.dimension)
            aggregates[cls.dimension].scores.append(cls.score)

    return {**state, "scored_observations": scored, "dimension_aggregates": aggregates}
