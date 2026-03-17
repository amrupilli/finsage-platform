from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.risk_profile import RiskProfileResult
from app.services.risk_profile_service import generate_risk_profile
from app.services.risk_profile_persistence import save_risk_profile_snapshot
from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.onboarding import (
    OnboardingMessageCreate,
    OnboardingNextMessageResponse,
    OnboardingStartResponse,
    OnboardingState,
)
from app.services.onboarding_chat import (
    process_onboarding_message,
    start_onboarding_conversation,
)
from app.services.onboarding_service import (
    build_collected_fields_from_answers,
    create_onboarding_session,
    get_onboarding_session_by_id,
    get_onboarding_state_snapshot,
    get_session_answers,
    mark_onboarding_session_completed,
    save_onboarding_answer,
)

router = APIRouter(prefix="/onboarding", tags=["onboarding"])


@router.post("/start", response_model=OnboardingStartResponse)
def start_onboarding(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OnboardingStartResponse:
    session = create_onboarding_session(db, current_user.id)
    response = start_onboarding_conversation(session.id)

    return OnboardingStartResponse(
        session_id=response.session_id,
        assistant_message=response.assistant_message,
        current_stage=response.current_stage,
        missing_fields=response.missing_fields,
        is_completed=response.is_completed,
    )


@router.get("/{session_id}/state", response_model=OnboardingState)
def get_onboarding_state(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OnboardingState:
    session = get_onboarding_session_by_id(db, session_id, current_user.id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Onboarding session not found.",
        )

    answers = get_session_answers(db, session.id)
    current_stage, collected_fields, missing_fields, is_completed = (
        get_onboarding_state_snapshot(answers)
    )

    return OnboardingState(
        session_id=session.id,
        current_stage=current_stage,
        collected_fields=collected_fields,
        missing_fields=missing_fields,
        is_completed=is_completed,
    )


@router.post("/{session_id}/message", response_model=OnboardingNextMessageResponse)
def send_onboarding_message(
    session_id: int,
    message_in: OnboardingMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OnboardingNextMessageResponse:
    session = get_onboarding_session_by_id(db, session_id, current_user.id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Onboarding session not found.",
        )

    if session.is_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Onboarding session is already complete.",
        )

    answers = get_session_answers(db, session.id)
    current_stage, collected_fields, _, _ = get_onboarding_state_snapshot(answers)

    if current_stage == "complete":
        mark_onboarding_session_completed(db, session)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Onboarding session is already complete.",
        )

    save_onboarding_answer(
        db=db,
        session_id=session.id,
        question_key=current_stage,
        answer_text=message_in.message_text,
    )

    answers = get_session_answers(db, session.id)
    previous_stage = answers[-1].question_key
    _, collected_fields, _, _ = get_onboarding_state_snapshot(answers)

    response, _ = process_onboarding_message(
        session_id=session.id,
        current_stage=previous_stage,
        message_text=message_in.message_text,
        collected_fields=collected_fields,
    )

    if response.is_completed:
        mark_onboarding_session_completed(db, session)

    return response
@router.get("/{session_id}/risk-profile", response_model=RiskProfileResult)
def get_risk_profile(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> RiskProfileResult:
    session = get_onboarding_session_by_id(db, session_id, current_user.id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Onboarding session not found.",
        )

    answers = get_session_answers(db, session.id)
    current_stage, collected_fields, missing_fields, is_completed = (
        get_onboarding_state_snapshot(answers)
    )

    if not is_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Onboarding is incomplete. Missing fields: {', '.join(missing_fields)}",
        )

    risk_profile = generate_risk_profile(collected_fields)
    save_risk_profile_snapshot(db, session.id, risk_profile)

    return risk_profile