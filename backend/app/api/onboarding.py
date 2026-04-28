from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.onboarding import OnboardingSession
from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.onboarding import (
    OnboardingMessageCreate,
    OnboardingNextMessageResponse,
    OnboardingStartResponse,
    OnboardingState,
)
from app.schemas.portfolio import PortfolioScenarioResult
from app.schemas.risk_profile import RiskProfileResult
from app.schemas.simulation import PortfolioSimulationResult
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
    get_onboarding_answer_by_id,
    update_onboarding_answer,
)
from app.schemas.onboarding import (
    OnboardingAnswerResponse,
    OnboardingAnswersReviewResponse,
    OnboardingAnswerUpdateRequest,
    OnboardingAnswerUpdateResponse,
)
from app.services.onboarding_state import get_missing_fields
from app.services.onboarding_validation_service import validate_onboarding_answer
from app.services.portfolio_service import generate_portfolio_for_session
from app.services.risk_profile_persistence import save_risk_profile_snapshot
from app.services.risk_profile_service import generate_risk_profile
from app.services.simulation_service import generate_simulation_for_session
from app.services.full_flow_service import run_full_financial_flow
from app.services.onboarding_state import FIELD_BY_STAGE

router = APIRouter(prefix="/onboarding", tags=["onboarding"])

@router.get("/latest-completed")
def get_latest_completed_onboarding_session(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    sessions = (
        db.query(OnboardingSession)
        .filter(OnboardingSession.user_id == current_user.id)
        .order_by(OnboardingSession.created_at.desc())
        .all()
    )

    for session in sessions:
        answers = get_session_answers(db, session.id)
        _, _, missing_fields, is_completed = get_onboarding_state_snapshot(answers)

        if is_completed and not missing_fields:
            return {
                "session_id": session.id,
                "is_completed": True,
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No completed onboarding session found.",
    )

def _answer_to_response(answer) -> OnboardingAnswerResponse:
    return OnboardingAnswerResponse(
        answer_id=answer.id,
        question_key=answer.question_key,
        field_name=FIELD_BY_STAGE.get(answer.question_key),
        answer_text=answer.answer_text,
        created_at=answer.created_at,
    )

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

    is_valid_answer, validation_message = validate_onboarding_answer(
        stage=current_stage,
        answer=message_in.message_text,
    )

    if not is_valid_answer:
        return OnboardingNextMessageResponse(
            session_id=session.id,
            assistant_message=validation_message
            or "I need a little more detail before I can use that answer.",
            current_stage=current_stage,
            missing_fields=get_missing_fields(collected_fields),
            is_completed=False,
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
    _, collected_fields, missing_fields, is_completed = get_onboarding_state_snapshot(
        answers
    )

    if not is_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Onboarding is incomplete. Missing fields: {', '.join(missing_fields)}",
        )

    risk_profile = generate_risk_profile(collected_fields)
    save_risk_profile_snapshot(db, session.id, risk_profile)

    return risk_profile


@router.get("/{session_id}/portfolio-scenario", response_model=PortfolioScenarioResult)
def get_portfolio_scenario(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PortfolioScenarioResult:
    return generate_portfolio_for_session(db, session_id, current_user.id)


@router.get("/{session_id}/simulation", response_model=PortfolioSimulationResult)
def get_portfolio_simulation(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PortfolioSimulationResult:
    return generate_simulation_for_session(db, session_id, current_user.id)

@router.get("/{session_id}/answers", response_model=OnboardingAnswersReviewResponse)
def get_onboarding_answers_for_review(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = get_onboarding_session_by_id(db, session_id, current_user.id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    answers = get_session_answers(db, session.id)

    current_stage, collected_fields, missing_fields, is_completed = (
        get_onboarding_state_snapshot(answers)
    )

    return OnboardingAnswersReviewResponse(
        session_id=session.id,
        is_completed=session.is_completed or is_completed,
        current_stage=current_stage,
        missing_fields=missing_fields,
        collected_fields=collected_fields,
        answers=[_answer_to_response(a) for a in answers],
    )

@router.patch("/{session_id}/answers/{answer_id}", response_model=OnboardingAnswerUpdateResponse)
def update_onboarding_answer_for_review(
    session_id: int,
    answer_id: int,
    answer_in: OnboardingAnswerUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = get_onboarding_session_by_id(db, session_id, current_user.id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    answer = get_onboarding_answer_by_id(db, answer_id, session.id)

    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    updated = update_onboarding_answer(db, answer, answer_in.answer_text)

    answers = get_session_answers(db, session.id)
    current_stage, collected_fields, missing_fields, is_completed = (
        get_onboarding_state_snapshot(answers)
    )

    return OnboardingAnswerUpdateResponse(
        session_id=session.id,
        answer=_answer_to_response(updated),
        current_stage=current_stage,
        missing_fields=missing_fields,
        collected_fields=collected_fields,
        is_completed=is_completed,
        message="Answer updated. Regenerate to refresh outputs.",
    )

@router.post("/{session_id}/regenerate")
def regenerate_outputs_after_onboarding_edit(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = get_onboarding_session_by_id(db, session_id, current_user.id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    answers = get_session_answers(db, session.id)
    _, _, missing_fields, is_completed = get_onboarding_state_snapshot(answers)

    if not is_completed or missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Onboarding incomplete. Missing: {missing_fields}",
        )

    return run_full_financial_flow(
        db=db,
        session_id=session.id,
        current_user=current_user,
    )