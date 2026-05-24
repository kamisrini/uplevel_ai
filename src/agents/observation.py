"""
Observation agent node.

Receives raw ingestion data (calendar events, transcripts, work items, GitHub events)
and produces structured Observation objects — each representing a discrete leadership
behaviour signal that can be scored against the VP Engineering rubric.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum


class SignalSource(StrEnum):
    CALENDAR = "calendar"
    TRANSCRIPT = "transcript"
    ADO_JIRA = "ado_jira"
    GITHUB = "github"
    MANUAL = "manual"  # from daily reflection form


@dataclass
class Observation:
    source: SignalSource
    timestamp: datetime
    summary: str  # one-sentence description of the behaviour
    raw_text: str  # original text or event title for traceability
    metadata: dict = field(default_factory=dict)


async def observe(state: dict) -> dict:
    """
    LangGraph node: observation.

    Input state keys:
      - calendar_events: list[CalendarEvent]
      - transcript_chunks: list[TranscriptChunk]
      - work_items: list[WorkItem]
      - github_events: list[GitHubEvent]
      - reflection_text: str  (from daily form, may be empty)

    Output state keys (added):
      - observations: list[Observation]

    TODO:
    - For each calendar event, infer whether it signals a VP-level behaviour
      (e.g., executive alignment meeting, cross-org facilitation) and emit an Observation.
    - For each transcript chunk, extract decisions/action items and emit Observations.
    - For each work item / GitHub event, emit Observations around delegation and leverage.
    - Optionally call Anthropic to synthesise noisy signals into clean observation summaries.
    """
    observations: list[Observation] = []

    # TODO: implement per-source observation extraction logic

    return {**state, "observations": observations}
