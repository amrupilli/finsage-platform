import random
from dataclasses import dataclass

from app.services.simulation_structure import get_simulation_assumptions


@dataclass
class RawSimulationResult:
    final_values: list[float]
    sample_path: list[float]
    all_paths: list[list[float]]


def run_monte_carlo_simulation(
    profile: str,
    initial_budget: float,
    num_simulations: int,
    time_horizon_months: int,
) -> RawSimulationResult:
    if initial_budget <= 0:
        raise ValueError("Initial budget must be greater than zero.")

    if num_simulations <= 0:
        raise ValueError("Number of simulations must be greater than zero.")

    if time_horizon_months <= 0:
        raise ValueError("Time horizon must be greater than zero.")

    assumptions = get_simulation_assumptions(profile)

    annual_return = assumptions["expected_annual_return"]
    annual_volatility = assumptions["annual_volatility"]

    monthly_mean = annual_return / 12
    monthly_volatility = annual_volatility / (12 ** 0.5)

    final_values: list[float] = []
    sample_path: list[float] = []
    all_paths: list[list[float]] = []

    for simulation_index in range(num_simulations):
        portfolio_value = initial_budget
        current_path = [round(initial_budget, 2)]

        for _ in range(time_horizon_months):
            monthly_return = random.gauss(monthly_mean, monthly_volatility)
            portfolio_value *= (1 + monthly_return)

            if portfolio_value < 0:
                portfolio_value = 0

            current_path.append(round(portfolio_value, 2))

        final_values.append(round(portfolio_value, 2))
        all_paths.append(current_path)

        if simulation_index == 0:
            sample_path = current_path

    return RawSimulationResult(
        final_values=final_values,
        sample_path=sample_path,
        all_paths=all_paths,
    )