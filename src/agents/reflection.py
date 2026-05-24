"""
Reflection agent node.

Synthesises the day's scored observations and generates targeted reflection prompts
for the leader — surfacing gaps, wins, and patterns relative to VP Engineering expectations.

Also handles the inverse flow: accepting the leader's manual reflection text from the
daily form and incorporating it into the overall daily context.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class ReflectionOutput(BaseModel):
    summary: str  # 2-3 sentence summary of the day's leadership signals
  strengths: list[str] = Field(default_factory=list)  # dimensions where score >= 4
  growth_areas: list[str] = Field(default_factory=list)  # dimensions where score <= 2
  prompts: list[str] = Field(default_factory=list)  # questions for the leader to reflect on
    leader_response: str = ""  # verbatim from daily form, if provided


async def reflect(state: dict) -> dict:
    """
    LangGraph node: reflection.

    Input state keys:
      - dimension_aggregates: dict[str, DimensionAggregate]
      - reflection_text: str  (optional manual input from leader)

    Output state keys (added):
      - reflection: ReflectionOutput

    TODO:
    - Build a compact summary of dimension averages.
    - Call Anthropic to generate a narrative summary + personalised reflection prompts.
    - Identify top strength and top growth area for the day.
    - If reflection_text is provided, incorporate the leader's own framing into the summary.
    """
    reflection_text = state.get("reflection_text", "")

    # TODO: implement LLM-driven reflection synthesis
    output = ReflectionOutput(
        summary="Reflection not yet generated.",
        prompts=["What was your highest-leverage action today?"],
        leader_response=reflection_text,
    )

    return {**state, "reflection": output}
