from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.scam_detection import ScamCheckRequest, ScamPredictionResponse
from app.services.scam_detection_service import predict_scam_risk

router = APIRouter(prefix="/warnings", tags=["warnings"])


@router.post("/scam-check", response_model=ScamPredictionResponse)
def check_investment_message_for_scam_risk(
    request: ScamCheckRequest,
    current_user: User = Depends(get_current_user),
) -> ScamPredictionResponse:
    return predict_scam_risk(request.text)