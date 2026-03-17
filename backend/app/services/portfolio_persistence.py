from sqlalchemy.orm import Session

from app.models.portfolio import PortfolioScenarioSnapshot
from app.schemas.portfolio import PortfolioScenarioResult


def save_portfolio_scenario_snapshot(
    db: Session,
    session_id: int,
    portfolio_result: PortfolioScenarioResult,
) -> PortfolioScenarioSnapshot:
    allocations_payload = [
        {
            "category": item.category,
            "percentage": item.percentage,
            "amount": item.amount,
            "rationale": item.rationale,
        }
        for item in portfolio_result.allocations
    ]

    existing_snapshot = (
        db.query(PortfolioScenarioSnapshot)
        .filter(PortfolioScenarioSnapshot.session_id == session_id)
        .first()
    )

    if existing_snapshot:
        existing_snapshot.portfolio_type = portfolio_result.portfolio_type
        existing_snapshot.total_budget = portfolio_result.total_budget
        existing_snapshot.summary = portfolio_result.summary
        existing_snapshot.allocations = allocations_payload

        db.commit()
        db.refresh(existing_snapshot)
        return existing_snapshot

    new_snapshot = PortfolioScenarioSnapshot(
        session_id=session_id,
        portfolio_type=portfolio_result.portfolio_type,
        total_budget=portfolio_result.total_budget,
        summary=portfolio_result.summary,
        allocations=allocations_payload,
    )

    db.add(new_snapshot)
    db.commit()
    db.refresh(new_snapshot)
    return new_snapshot