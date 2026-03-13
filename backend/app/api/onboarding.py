from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.onboarding import (
    OnboardingMessageCreate,
    OnboardingNextMessageResponse,
    OnboardingStartResponse,
)
from app.services.onboarding_chat import (
    process_onboarding_message,
    start_onboarding_conversation,
)
from app.services.onboarding_service import (
    build_collected_fields_from_answers,
    create_onboarding_session,
    get_onboarding_session_by_id,
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
    collected_fields = build_collected_fields_from_answers(answers)

    current_stage = "goal" if not answers else answers[-1].question_key

    if current_stage != "goal" or answers:
        save_onboarding_answer(
            db=db,
            session_id=session.id,
            question_key=current_stage,
            answer_text=message_in.message_text,
        )

        answers = get_session_answers(db, session.id)
        collected_fields = build_collected_fields_from_answers(answers)

    response, updated_fields = process_onboarding_message(
        session_id=session.id,
        current_stage=current_stage,
        message_text=message_in.message_text,
        collected_fields=collected_fields,
    )

    if response.is_completed:
        mark_onboarding_session_completed(db, session)

    return response