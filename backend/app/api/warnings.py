from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.scam_detection import ScamCheckRequest, ScamPredictionResponse
from app.services.investment_check_service import (
    InvestmentCheckResponse,
    assess_investment_question,
)
from app.services.scam_detection_service import predict_scam_risk


router = APIRouter(prefix="/warnings", tags=["warnings"])


class InvestmentCheckRequest(BaseModel):
    input_text: str


@router.post("/scam-check", response_model=ScamPredictionResponse)
def check_investment_message_for_scam_risk(
    request: ScamCheckRequest,
    current_user: User = Depends(get_current_user),
) -> ScamPredictionResponse:
    return predict_scam_risk(request.text)


@router.post("/investment-check", response_model=InvestmentCheckResponse)
def run_investment_check(
    request: InvestmentCheckRequest,
    current_user: User = Depends(get_current_user),
) -> InvestmentCheckResponse:
    return assess_investment_question(request.input_text)