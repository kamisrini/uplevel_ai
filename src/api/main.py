"""FastAPI application entry point."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import reflection as reflection_router
from src.memory.postgres import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="uplevel_ai",
    description="Daily leadership impact agent for engineering leaders.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reflection_router.router, prefix="/api/v1")


@app.get("/")
async def health() -> dict:
    return {"status": "ok", "service": "uplevel_ai"}
