"""
Leadership signal classifier.

Uses the Anthropic SDK to map a free-text observation (derived from calendar,
transcripts, or work-item data) to one or more rubric dimensions and assign a
1-5 score for each.

The rubric text is passed as a cached system prompt (cache_control: ephemeral)
so repeated daily calls hit the prompt cache and reduce cost significantly.
"""

from __future__ import annotations

import anthropic

from src.config import settings
from src.scoring.rubric import DIMENSION_NAMES, rubric_as_text


class ClassificationResult:
    def __init__(self, dimension: str, score: int, rationale: str) -> None:
        self.dimension = dimension
        self.score = score
        self.rationale = rationale

    def __repr__(self) -> str:
        return f"ClassificationResult(dimension={self.dimension!r}, score={self.score}, rationale={self.rationale!r})"


class LeadershipClassifier:
    """
    Classifies a free-text observation against the VP Engineering rubric.

    TODO:
    - Call client.messages.create with the rubric as a cached system prompt.
    - Parse structured JSON response containing dimension, score, and rationale.
    - Handle multi-dimension observations (one observation can score on several dimensions).
    - Add retry logic for API errors (tenacity).
    """

    _SYSTEM_PROMPT_SUFFIX = """
You are an expert leadership coach calibrated to VP Engineering behavioural expectations.

Given an observation about an engineering leader's behaviour, identify which leadership
dimensions it demonstrates and assign a score from 1 (early EM) to 5 (VP-level behaviour).

Respond with a JSON array:
[
  {
    "dimension": "<one of the dimension names>",
    "score": <1-5>,
    "rationale": "<one sentence explaining the score>"
  }
]

Valid dimension names: """ + ", ".join(DIMENSION_NAMES)

    def __init__(self) -> None:
        self._client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self._rubric_text = rubric_as_text()

    def classify(self, observation_text: str) -> list[ClassificationResult]:
        """
        Classify `observation_text` against the rubric.
        Uses prompt caching on the system + rubric block to reduce cost.
        """
        # TODO: implement full Anthropic SDK call with cache_control blocks
        # Example structure (not yet wired):
        #
        # response = self._client.messages.create(
        #     model=settings.anthropic_model,
        #     max_tokens=1024,
        #     system=[
        #         {
        #             "type": "text",
        #             "text": self._rubric_text,
        #             "cache_control": {"type": "ephemeral"},
        #         },
        #         {
        #             "type": "text",
        #             "text": self._SYSTEM_PROMPT_SUFFIX,
        #         },
        #     ],
        #     messages=[{"role": "user", "content": observation_text}],
        # )
        # raw = json.loads(response.content[0].text)
        # return [ClassificationResult(**item) for item in raw]
        raise NotImplementedError
