from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.report import (
    PortfolioSummary,
    ReportResponse,
    RiskProfileSummary,
    SimulationSummary,
)
from app.schemas.warning import UserWarning
from app.services.portfolio_service import generate_portfolio_for_session
from app.services.risk_profile_service import generate_risk_profile
from app.services.simulation_service import generate_simulation_for_session
from app.services.warning_explanation_service import (
    build_portfolio_concentration_warning,
    build_simulation_warning,
)
from app.services.onboarding_service import (
    build_collected_fields_from_answers,
    get_onboarding_session_by_id,
    get_session_answers,
)


REPORT_DISCLAIMER = (
    "This report is generated for educational purposes only. It does not provide "
    "financial advice, investment recommendations, or a guarantee of future performance. "
    "Users should research independently and consider seeking regulated financial advice "
    "before making real investment decisions."
)


def build_report_for_session(
    db: Session,
    session_id: int,
    current_user: User,
) -> ReportResponse:
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

    return ReportResponse(
        user_email=current_user.email,
        risk_profile=RiskProfileSummary(
            profile=risk_profile.profile,
            summary=risk_profile.summary,
        ),
        portfolio=PortfolioSummary(
            description=portfolio.summary,
            allocations={
                allocation.category: allocation.percentage
                for allocation in portfolio.allocations
            },
        ),
        simulation=SimulationSummary(
            expected_return=simulation.metrics.expected_final_value,
            probability_of_loss=simulation.metrics.probability_of_loss,
            summary=simulation.summary,
        ),
        warnings=warnings,
        disclaimer=REPORT_DISCLAIMER,
    )