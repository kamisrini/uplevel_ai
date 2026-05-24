"""
Postgres event log.

Stores time-series leadership observations and daily reports using SQLAlchemy
async ORM. Provides an append-only event log that powers trend analysis in
the weekly report generator.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from datetime import date, datetime

from sqlalchemy import JSON, Date, DateTime, Float, Integer, String, Text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.config import settings


class Base(DeclarativeBase):
    pass


class EventLog(Base):
    """Append-only log of raw leadership signals ingested each day."""

    __tablename__ = "event_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    event_date: Mapped[date] = mapped_column(Date, index=True)
    source: Mapped[str] = mapped_column(String(32))  # calendar | transcript | ado_jira | github
    summary: Mapped[str] = mapped_column(Text)
    raw_text: Mapped[str] = mapped_column(Text, default="")
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, default=dict)


class DailyReportRecord(Base):
    """Persisted daily report — one row per leader per day."""

    __tablename__ = "daily_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    report_date: Mapped[date] = mapped_column(Date, index=True, unique=True)
    overall_score: Mapped[float] = mapped_column(Float)
    dimension_scores: Mapped[dict] = mapped_column(JSON, default=dict)
    summary: Mapped[str] = mapped_column(Text, default="")
    full_report: Mapped[dict] = mapped_column(JSON, default=dict)


_engine = create_async_engine(settings.postgres_dsn, echo=settings.debug)
AsyncSessionLocal = async_sessionmaker(_engine, expire_on_commit=False)


async def init_db() -> None:
    """Create all tables if they don't exist (use Alembic for migrations in production)."""
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields a database session."""
    async with AsyncSessionLocal() as session:
        yield session
