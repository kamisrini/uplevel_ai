"""
Calendar ingestion: fetches events from Google Calendar or Microsoft Graph (Outlook).

Normalises raw calendar data into CalendarEvent objects that the observation agent
can reason over — meeting types, attendee counts, duration, and whether the leader
owned/facilitated the meeting.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

import httpx
from pydantic import BaseModel, Field


class MeetingType(StrEnum):
    ONE_ON_ONE = "one_on_one"
    TEAM = "team"
    CROSS_FUNCTIONAL = "cross_functional"
    EXECUTIVE = "executive"
    EXTERNAL = "external"
    UNKNOWN = "unknown"


class CalendarEvent(BaseModel):
    event_id: str
    title: str
    start: datetime
    end: datetime
    attendees: list[str] = Field(default_factory=list)
    organiser: str = ""
    meeting_type: MeetingType = MeetingType.UNKNOWN
    description: str = ""

    @property
    def duration_minutes(self) -> int:
        return int((self.end - self.start).total_seconds() / 60)

    @property
    def is_owned_by_leader(self) -> bool:
        """True when the leader organised (and therefore led) the meeting."""
        # TODO: inject leader email from config
        return False


class CalendarIngester:
    """
    TODO:
    - Authenticate with Google Calendar API (OAuth2) or Microsoft Graph.
    - Fetch events for a given date range.
    - Classify meeting type based on attendee list and title heuristics.
    - Return list[CalendarEvent] sorted by start time.
    """

    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        self._client = client or httpx.AsyncClient()

    async def fetch(self, date: datetime) -> list[CalendarEvent]:
        """Return all calendar events for the given day."""
        # TODO: implement Google Calendar / Microsoft Graph fetch
        raise NotImplementedError

    async def close(self) -> None:
        await self._client.aclose()
