from pydantic import BaseModel


class SimulationPercentiles(BaseModel):
    p10: float
    p50: float
    p90: float


class SimulationMetrics(BaseModel):
    expected_final_value: float
    probability_of_loss: float
    estimated_volatility: float
    max_drawdown: float
    percentiles: SimulationPercentiles


class SimulationPathPoint(BaseModel):
    step: int
    portfolio_value: float


class PortfolioSimulationResult(BaseModel):
    initial_budget: float
    num_simulations: int
    time_horizon_months: int
    metrics: SimulationMetrics
    sample_path: list[SimulationPathPoint]
    summary: str