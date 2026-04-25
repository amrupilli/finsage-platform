from typing import Literal

from pydantic import BaseModel


WarningCategory = Literal[
    "scam_risk",
    "portfolio_risk",
    "simulation_risk",
    "educational_guidance",
]

WarningSeverity = Literal["low", "medium", "high"]


class UserWarning(BaseModel):
    category: WarningCategory
    severity: WarningSeverity
    title: str
    message: str
    recommended_action: str