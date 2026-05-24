"""
GitHub ingestion: pulls PR reviews, code comments, and repository activity.

VP-level signal comes not from volume of commits but from quality of review feedback,
architectural guidance in PR comments, and breadth of repositories the leader touches
(cross-team leverage vs. deep individual contribution).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

import httpx


class GitHubActivityType(StrEnum):
    PR_REVIEW = "pr_review"
    PR_COMMENT = "pr_comment"
    ISSUE_COMMENT = "issue_comment"
    COMMIT = "commit"
    REPO_CREATION = "repo_creation"


@dataclass
class GitHubEvent:
    event_id: str
    activity_type: GitHubActivityType
    repo: str
    actor: str
    timestamp: datetime
    body: str = ""
    url: str = ""
    metadata: dict = field(default_factory=dict)


class GitHubIngester:
    """
    TODO:
    - Authenticate with GitHub REST API (personal access token).
    - Fetch events for the authenticated user across all relevant repos.
    - Separate signal types: architectural PR reviews score higher than small fixes.
    - Return list[GitHubEvent] sorted by timestamp.
    """

    _BASE = "https://api.github.com"

    def __init__(self, token: str) -> None:
        self._client = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
        )

    async def fetch(self, username: str, since: datetime) -> list[GitHubEvent]:
        """Return GitHub events for `username` since `since`."""
        raise NotImplementedError

    async def close(self) -> None:
        await self._client.aclose()
