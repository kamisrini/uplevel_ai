"""
Neo4j relationship graph.

Models the leader's influence network: who they interact with, which teams they
coordinate across, and how decision/information flows through the organisation.

Over time this graph reveals whether the leader is expanding their cross-team
reach (VP behaviour) or staying siloed within their immediate team.

Node types:  Person, Team, Project, Decision
Edge types:  INFLUENCED, COLLABORATED_WITH, OWNS, DEPENDS_ON, MADE_DECISION
"""

from __future__ import annotations

from neo4j import AsyncDriver, AsyncGraphDatabase

from src.config import settings


class Neo4jClient:
    """
    Thin wrapper around the Neo4j async driver.

    TODO:
    - Upsert Person nodes from calendar attendee lists and transcript speakers.
    - Create COLLABORATED_WITH edges weighted by interaction frequency.
    - Upsert Decision nodes from transcript/ADO items and link to Person (MADE_DECISION).
    - Expose query methods for the weekly report: degree centrality, team coverage ratio.
    """

    def __init__(self, driver: AsyncDriver | None = None) -> None:
        self._driver = driver or AsyncGraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
        )

    async def upsert_person(self, name: str, email: str = "", role: str = "") -> None:
        """Create or update a Person node."""
        async with self._driver.session() as session:
            await session.run(
                "MERGE (p:Person {email: $email}) "
                "SET p.name = $name, p.role = $role",
                email=email or name,
                name=name,
                role=role,
            )

    async def record_collaboration(self, from_email: str, to_email: str, date_str: str) -> None:
        """Create or increment a COLLABORATED_WITH edge between two people."""
        async with self._driver.session() as session:
            await session.run(
                """
                MATCH (a:Person {email: $from_email}), (b:Person {email: $to_email})
                MERGE (a)-[r:COLLABORATED_WITH {date: $date}]->(b)
                ON CREATE SET r.count = 1
                ON MATCH  SET r.count = r.count + 1
                """,
                from_email=from_email,
                to_email=to_email,
                date=date_str,
            )

    async def cross_team_reach(self, leader_email: str) -> list[str]:
        """Return distinct team names reachable from the leader within 2 hops."""
        async with self._driver.session() as session:
            result = await session.run(
                """
                MATCH (l:Person {email: $email})-[:COLLABORATED_WITH*1..2]->(p:Person)
                WHERE p.team IS NOT NULL
                RETURN DISTINCT p.team AS team
                """,
                email=leader_email,
            )
            return [record["team"] async for record in result]

    async def close(self) -> None:
        await self._driver.close()
