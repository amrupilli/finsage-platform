from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.portfolio import PortfolioScenarioSnapshot
from app.models.risk_profile import RiskProfileSnapshot
from app.schemas.simulation import PortfolioSimulationResult
from app.services.onboarding_service import get_onboarding_session_by_id
from app.services.simulation_config import (
    DEFAULT_NUM_SIMULATIONS,
    DEFAULT_TIME_HORIZON_MONTHS,
)
from app.services.simulation_engine import run_monte_carlo_simulation
from app.services.simulation_metrics import build_simulation_result


def generate_simulation_for_session(
    db: Session,
    session_id: int,
    user_id: int,
) -> PortfolioSimulationResult:
    session = get_onboarding_session_by_id(db, session_id, user_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Onboarding session not found.",
        )

    risk_snapshot = (
        db.query(RiskProfileSnapshot)
        .filter(RiskProfileSnapshot.session_id == session.id)
        .first()
    )

    if not risk_snapshot:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Risk profile must be generated before simulation.",
        )

    portfolio_snapshot = (
        db.query(PortfolioScenarioSnapshot)
        .filter(PortfolioScenarioSnapshot.session_id == session.id)
        .first()
    )

    if not portfolio_snapshot:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Portfolio scenario must be generated before simulation.",
        )

    raw_result = run_monte_carlo_simulation(
        profile=risk_snapshot.profile_label,
        initial_budget=portfolio_snapshot.total_budget,
        num_simulations=DEFAULT_NUM_SIMULATIONS,
        time_horizon_months=DEFAULT_TIME_HORIZON_MONTHS,
    )

    return build_simulation_result(
        profile=risk_snapshot.profile_label,
        initial_budget=portfolio_snapshot.total_budget,
        num_simulations=DEFAULT_NUM_SIMULATIONS,
        time_horizon_months=DEFAULT_TIME_HORIZON_MONTHS,
        raw_result=raw_result,
    )