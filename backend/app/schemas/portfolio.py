from pydantic import BaseModel


class PortfolioAllocation(BaseModel):
    category: str
    percentage: float
    amount: float
    rationale: str


class PortfolioScenarioResult(BaseModel):
    portfolio_type: str
    total_budget: float
    allocations: list[PortfolioAllocation]
    summary: str