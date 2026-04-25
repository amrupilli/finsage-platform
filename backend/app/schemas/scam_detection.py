from typing import Literal

from pydantic import BaseModel, Field


ScamLabel = Literal["safe", "suspicious", "scam"]
RiskLevel = Literal["low", "medium", "high"]
SignalSeverity = Literal["low", "medium", "high"]


class ScamCheckRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=10,
        max_length=3000,
        description="User-provided investment message, advert, project description, or claim to check.",
    )


class WarningSignal(BaseModel):
    signal_type: str
    matched_text: str
    severity: SignalSeverity
    explanation: str


class InvestmentChecklistItem(BaseModel):
    check: str
    reason: str


class ScamPredictionResponse(BaseModel):
    input_text: str
    predicted_label: ScamLabel
    scam_probability: float = Field(..., ge=0.0, le=1.0)
    risk_level: RiskLevel
    warning_signals: list[WarningSignal]
    investment_checklist: list[InvestmentChecklistItem]
    explanation: str
    educational_message: str


class ScamTrainingExample(BaseModel):
    text: str
    label: ScamLabel