from app.schemas.portfolio import PortfolioAllocation, PortfolioScenarioResult
from app.services.portfolio_config import (
    PORTFOLIO_CATEGORY_LABELS,
    PROFILE_ALLOCATIONS,
    PROFILE_TO_PORTFOLIO_TYPE,
)


def build_portfolio_summary(portfolio_type: str, profile: str) -> str:
    return (
        f"This educational portfolio scenario was generated for a {profile} user profile. "
        f"It follows a {portfolio_type.lower()} approach to illustrate how budget allocation "
        f"may differ depending on risk tolerance."
    )


def build_portfolio_scenario(profile: str, budget: float) -> PortfolioScenarioResult:
    if profile not in PROFILE_ALLOCATIONS:
        raise ValueError(f"Unsupported risk profile: {profile}")

    if budget <= 0:
        raise ValueError("Budget must be greater than zero.")

    allocation_rules = PROFILE_ALLOCATIONS[profile]
    portfolio_type = PROFILE_TO_PORTFOLIO_TYPE[profile]

    total_percentage = sum(allocation_rules.values())
    if total_percentage != 100:
        raise ValueError("Portfolio allocation rules must sum to 100.")

    allocations: list[PortfolioAllocation] = []

    category_items = list(allocation_rules.items())

    running_total = 0.0
    for index, (category_key, percentage) in enumerate(category_items):
        if category_key not in PORTFOLIO_CATEGORY_LABELS:
            raise ValueError(f"Unsupported portfolio category: {category_key}")

        if index < len(category_items) - 1:
            amount = round((percentage / 100) * budget, 2)
            running_total += amount
        else:
            amount = round(budget - running_total, 2)

        if category_key == "stable":
            rationale = "This allocation prioritises lower-volatility educational exposure."
        elif category_key == "balanced":
            rationale = "This allocation supports moderate growth while retaining balance."
        else:
            rationale = "This allocation demonstrates higher-risk, higher-volatility exposure."

        allocations.append(
            PortfolioAllocation(
                category=PORTFOLIO_CATEGORY_LABELS[category_key],
                percentage=float(percentage),
                amount=amount,
                rationale=rationale,
            )
        )

    return PortfolioScenarioResult(
        portfolio_type=portfolio_type,
        total_budget=budget,
        allocations=allocations,
        summary=build_portfolio_summary(portfolio_type, profile),
    )