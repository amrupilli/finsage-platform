from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.services.full_flow_service import run_full_financial_flow

router = APIRouter(prefix="/flow", tags=["flow"])


@router.get("/{session_id}")
def get_full_financial_flow(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = run_full_financial_flow(
        db=db,
        session_id=session_id,
        current_user=current_user,
    )

    return result