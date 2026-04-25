from pydantic import BaseModel

from app.schemas.warning import UserWarning


class RiskProfileSummary(BaseModel):
    profile: str
    summary: str


class PortfolioSummary(BaseModel):
    description: str
    allocations: dict[str, float]


class SimulationSummary(BaseModel):
    expected_return: float
    probability_of_loss: float
    summary: str


class ReportResponse(BaseModel):
    user_email: str
    risk_profile: RiskProfileSummary
    portfolio: PortfolioSummary
    simulation: SimulationSummary
    warnings: list[UserWarning]
    disclaimer: str