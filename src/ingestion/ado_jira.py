"""
ADO / Jira ingestion: pulls work-item activity to surface delegation patterns,
backlog ownership, and cross-team coordination signals.

Relevant VP-level signals: is the leader assigning/unblocking others, writing
acceptance criteria, shaping roadmap items, or still in the weeds of implementation?
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

import httpx
from pydantic import BaseModel, Field


class WorkItemActivity(StrEnum):
    CREATED = "created"
    ASSIGNED = "assigned"
    COMMENTED = "commented"
    RESOLVED = "resolved"
    ESCALATED = "escalated"


class WorkItem(BaseModel):
    item_id: str
    title: str
    source: str  # "ado" | "jira"
    activity: WorkItemActivity
    actor: str
    timestamp: datetime
    description: str = ""
    tags: list[str] = Field(default_factory=list)


class ADOIngester:
    """
    TODO:
    - Authenticate with Azure DevOps REST API (PAT).
    - Fetch work items updated/created by the leader in the last N days.
    - Map ADO fields to WorkItem dataclass.
    """

    def __init__(self, org: str, pat: str) -> None:
        self._org = org
        self._headers = {"Authorization": f"Basic {pat}"}
        self._client = httpx.AsyncClient(headers=self._headers)

    async def fetch(self, since: datetime) -> list[WorkItem]:
        """Return WorkItem activity since `since` for the configured org."""
        raise NotImplementedError


class JiraIngester:
    """
    TODO:
    - Authenticate with Jira Cloud REST v3 API (email + API token).
    - JQL query for issues updated by the leader since `since`.
    - Map Jira fields to WorkItem dataclass.
    """

    def __init__(self, base_url: str, email: str, token: str) -> None:
        self._base_url = base_url
        self._client = httpx.AsyncClient(auth=(email, token))

    async def fetch(self, since: datetime) -> list[WorkItem]:
        """Return WorkItem activity since `since`."""
        raise NotImplementedError
