from sqlalchemy.orm import Session

from app.models.onboarding import OnboardingAnswer, OnboardingSession
from app.schemas.onboarding import ConversationStage
from app.services.onboarding_state import (
    FIELD_BY_STAGE,
    get_current_question_stage,
    get_initial_collected_fields,
    get_missing_fields,
)


def create_onboarding_session(db: Session, user_id: int) -> OnboardingSession:
    session = OnboardingSession(
        user_id=user_id,
        is_completed=False,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_onboarding_session_by_id(
    db: Session,
    session_id: int,
    user_id: int,
) -> OnboardingSession | None:
    return (
        db.query(OnboardingSession)
        .filter(
            OnboardingSession.id == session_id,
            OnboardingSession.user_id == user_id,
        )
        .first()
    )


def save_onboarding_answer(
    db: Session,
    session_id: int,
    question_key: str,
    answer_text: str,
) -> OnboardingAnswer:
    answer = OnboardingAnswer(
        session_id=session_id,
        question_key=question_key,
        answer_text=answer_text,
    )
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer


def get_session_answers(
    db: Session,
    session_id: int,
) -> list[OnboardingAnswer]:
    return (
        db.query(OnboardingAnswer)
        .filter(OnboardingAnswer.session_id == session_id)
        .order_by(OnboardingAnswer.created_at.asc(), OnboardingAnswer.id.asc())
        .all()
    )


def build_collected_fields_from_answers(
    answers: list[OnboardingAnswer],
) -> dict[str, str | None]:
    collected_fields = get_initial_collected_fields()

    for answer in answers:
        field_name = FIELD_BY_STAGE.get(answer.question_key)
        if field_name:
            collected_fields[field_name] = answer.answer_text

    return collected_fields


def get_onboarding_state_snapshot(
    answers: list[OnboardingAnswer],
) -> tuple[ConversationStage, dict[str, str | None], list[str], bool]:
    collected_fields = build_collected_fields_from_answers(answers)
    missing_fields = get_missing_fields(collected_fields)

    current_stage = get_current_question_stage(len(answers))
    is_completed = current_stage == "complete"

    return current_stage, collected_fields, missing_fields, is_completed


def mark_onboarding_session_completed(
    db: Session,
    session: OnboardingSession,
) -> OnboardingSession:
    session.is_completed = True
    db.add(session)
    db.commit()
    db.refresh(session)
    return session