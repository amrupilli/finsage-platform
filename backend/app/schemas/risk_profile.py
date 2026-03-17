from typing import Literal

from pydantic import BaseModel


RiskLabel = Literal["Conservative", "Moderate", "Aggressive"]


class RiskDimensionScore(BaseModel):
    dimension: str
    score: int
    rationale: str


class RiskProfileResult(BaseModel):
    profile: RiskLabel
    total_score: int
    dimension_scores: list[RiskDimensionScore]
    summary: str