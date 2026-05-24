"""
Meeting transcript ingestion: parses output from Otter.ai, Microsoft Teams, or Zoom.

Extracts speaker turns, decisions made, action items assigned, and open questions
from meeting recordings so the observation agent can assess facilitation quality,
decision ownership, and clarity of outcomes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SpeakerTurn:
    speaker: str
    text: str
    timestamp_seconds: float


@dataclass
class TranscriptChunk:
    meeting_id: str
    meeting_title: str
    date: datetime
    turns: list[SpeakerTurn] = field(default_factory=list)
    decisions: list[str] = field(default_factory=list)
    action_items: list[str] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)

    @property
    def leader_talk_ratio(self) -> float:
        """Fraction of words spoken by the leader — high values may indicate under-delegation."""
        # TODO: inject leader name from config and compute ratio
        return 0.0


class TranscriptIngester:
    """
    TODO:
    - Accept raw transcript JSON (Otter, Teams, Zoom export formats).
    - Parse into SpeakerTurn list.
    - Use a lightweight Anthropic call to extract decisions / action items / open questions.
    - Return list[TranscriptChunk].
    """

    async def parse_otter(self, raw: dict) -> TranscriptChunk:
        """Parse Otter.ai transcript export."""
        raise NotImplementedError

    async def parse_teams(self, raw: dict) -> TranscriptChunk:
        """Parse Microsoft Teams VTT/JSON transcript export."""
        raise NotImplementedError

    async def parse_zoom(self, raw: dict) -> TranscriptChunk:
        """Parse Zoom transcript JSON export."""
        raise NotImplementedError
