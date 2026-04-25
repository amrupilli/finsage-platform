from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.warning import UserWarning
from app.services.onboarding_service import (
    build_collected_fields_from_answers,
    get_onboarding_session_by_id,
    get_session_answers,
)
from app.services.portfolio_service import generate_portfolio_for_session
from app.services.risk_profile_service import generate_risk_profile
from app.services.simulation_service import generate_simulation_for_session
from app.services.warning_explanation_service import (
    build_portfolio_concentration_warning,
    build_simulation_warning,
)


def run_full_financial_flow(
    db: Session,
    session_id: int,
    current_user: User,
) -> dict:
    session = get_onboarding_session_by_id(db, session_id, current_user.id)

    if not session:
        raise ValueError("Onboarding session not found.")

    answers = get_session_answers(db, session.id)
    collected_fields = build_collected_fields_from_answers(answers)

    risk_profile = generate_risk_profile(collected_fields)

    portfolio = generate_portfolio_for_session(
        db=db,
        session_id=session.id,
        user_id=current_user.id,
    )

    simulation = generate_simulation_for_session(
        db=db,
        session_id=session.id,
        user_id=current_user.id,
    )

    largest_allocation = max(
        allocation.percentage for allocation in portfolio.allocations
    )

    warnings: list[UserWarning] = [
        build_simulation_warning(
            probability_of_loss=simulation.metrics.probability_of_loss
        ),
        build_portfolio_concentration_warning(
            largest_allocation_percentage=largest_allocation
        ),
    ]

    return {
        "risk_profile": risk_profile,
        "portfolio": portfolio,
        "simulation": simulation,
        "warnings": warnings,
    }