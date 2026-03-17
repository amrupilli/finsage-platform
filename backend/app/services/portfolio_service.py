from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.services.portfolio_persistence import save_portfolio_scenario_snapshot
from app.models.risk_profile import RiskProfileSnapshot
from app.schemas.portfolio import PortfolioScenarioResult
from app.services.budget_parser import extract_budget_amount
from app.services.onboarding_service import (
    get_onboarding_session_by_id,
    get_onboarding_state_snapshot,
    get_session_answers,
)
from app.services.portfolio_structure import build_portfolio_scenario


def generate_portfolio_for_session(
    db: Session,
    session_id: int,
    user_id: int,
) -> PortfolioScenarioResult:
    session = get_onboarding_session_by_id(db, session_id, user_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Onboarding session not found.",
        )

    answers = get_session_answers(db, session.id)
    _, collected_fields, _, is_completed = get_onboarding_state_snapshot(answers)

    if not is_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Portfolio scenario can only be generated after onboarding is complete.",
        )

    risk_snapshot = (
        db.query(RiskProfileSnapshot)
        .filter(RiskProfileSnapshot.session_id == session.id)
        .first()
    )

    if not risk_snapshot:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Risk profile must be generated before portfolio scenario generation.",
        )

    budget_text = collected_fields.get("budget", "")
    try:
        budget_amount = extract_budget_amount(budget_text)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid budget value: {str(exc)}",
        ) from exc

    portfolio_result = build_portfolio_scenario(
    profile=risk_snapshot.profile_label,
    budget=budget_amount,
)

    save_portfolio_scenario_snapshot(db, session.id, portfolio_result)

    return portfolio_result