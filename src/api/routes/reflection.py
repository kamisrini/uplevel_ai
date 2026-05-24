"""
Reflection and report API routes.

POST /reflection   — submit the daily reflection form; triggers the full agent graph
GET  /report/daily — retrieve today's (or a specific date's) daily report
GET  /report/weekly — retrieve the weekly narrative for the current or specified week
"""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.graph import run_daily
from src.memory.postgres import get_session

router = APIRouter(tags=["reflection"])


# ---------- Request / response schemas ----------

class ReflectionInput(BaseModel):
    reflection_text: str
    report_date: date | None = None


class DailyReportResponse(BaseModel):
    report_date: str
    overall_score: float
    dimension_scores: dict[str, float]
    summary: str
    strengths: list[str]
    growth_areas: list[str]
    prompts: list[str]


# ---------- Routes ----------

@router.post("/reflection", response_model=DailyReportResponse)
async def submit_reflection(
    payload: ReflectionInput,
    db: AsyncSession = Depends(get_session),
) -> DailyReportResponse:
    """
    Accept the leader's daily reflection text, run the full agent graph,
    persist the report, and return the scored daily assessment.

    TODO:
    - Wire ingestion fetchers so calendar/GitHub/Jira data is pulled automatically.
    - Persist DailyReportRecord to Postgres.
    - Return 409 if a report for this date already exists (idempotency guard).
    """
    final_state = await run_daily(
        reflection_text=payload.reflection_text,
        report_date=payload.report_date,
    )
    report = final_state.get("daily_report")
    if report is None:
        raise HTTPException(status_code=500, detail="Agent graph did not produce a report.")

    return DailyReportResponse(**report.to_dict())


@router.get("/report/daily", response_model=DailyReportResponse)
async def get_daily_report(
    report_date: date | None = None,
    db: AsyncSession = Depends(get_session),
) -> DailyReportResponse:
    """
    Return the persisted daily report for `report_date` (defaults to today).

    TODO:
    - Query DailyReportRecord from Postgres by date.
    - Return 404 if no report exists for the requested date.
    """
    raise HTTPException(status_code=501, detail="Not yet implemented.")


@router.get("/report/weekly")
async def get_weekly_report(
    week_start: date | None = None,
    db: AsyncSession = Depends(get_session),
) -> dict:
    """
    Return the weekly narrative for the week beginning `week_start`.

    TODO:
    - Fetch 5-7 DailyReportRecords from Postgres for the target week.
    - Generate WeeklyNarrative via WeeklyReportGenerator.
    - Cache result; regenerate on demand.
    """
    raise HTTPException(status_code=501, detail="Not yet implemented.")
