import math
from statistics import mean

from app.schemas.simulation import (
    PortfolioSimulationResult,
    SimulationBandPoint,
    SimulationMetrics,
    SimulationPathPoint,
    SimulationPercentiles,
)
from app.services.simulation_engine import RawSimulationResult
from app.services.simulation_structure import build_simulation_summary


def calculate_percentile(values: list[float], percentile: float) -> float:
    if not values:
        raise ValueError("Values list cannot be empty.")

    if not 0 <= percentile <= 100:
        raise ValueError("Percentile must be between 0 and 100.")

    sorted_values = sorted(values)

    if len(sorted_values) == 1:
        return round(sorted_values[0], 2)

    index = (percentile / 100) * (len(sorted_values) - 1)
    lower_index = int(index)
    upper_index = min(lower_index + 1, len(sorted_values) - 1)
    weight = index - lower_index

    interpolated = (
        sorted_values[lower_index] * (1 - weight)
        + sorted_values[upper_index] * weight
    )

    return round(interpolated, 2)


def calculate_probability_of_loss(
    final_values: list[float],
    initial_budget: float,
) -> float:
    if not final_values:
        raise ValueError("Final values list cannot be empty.")

    losses = sum(1 for value in final_values if value < initial_budget)
    probability = losses / len(final_values)
    return round(probability, 4)


def calculate_estimated_volatility(final_values: list[float]) -> float:
    if not final_values:
        raise ValueError("Final values list cannot be empty.")

    if len(final_values) == 1:
        return 0.0

    average_value = mean(final_values)
    variance = sum((value - average_value) ** 2 for value in final_values) / len(final_values)
    std_dev = math.sqrt(variance)

    return round(std_dev, 2)


def calculate_max_drawdown(path_values: list[float]) -> float:
    if not path_values:
        raise ValueError("Path values cannot be empty.")

    peak = path_values[0]
    max_drawdown = 0.0

    for value in path_values:
        if value > peak:
            peak = value

        if peak > 0:
            drawdown = (peak - value) / peak
            if drawdown > max_drawdown:
                max_drawdown = drawdown

    return round(max_drawdown, 4)


def build_percentile_band(all_paths: list[list[float]]) -> list[SimulationBandPoint]:
    if not all_paths:
        raise ValueError("All paths cannot be empty.")

    num_steps = len(all_paths[0])

    band: list[SimulationBandPoint] = []

    for step_index in range(num_steps):
        step_values = [path[step_index] for path in all_paths]

        band.append(
            SimulationBandPoint(
                step=step_index,
                p10=calculate_percentile(step_values, 10),
                p50=calculate_percentile(step_values, 50),
                p90=calculate_percentile(step_values, 90),
            )
        )

    return band


def build_simulation_result(
    profile: str,
    initial_budget: float,
    num_simulations: int,
    time_horizon_months: int,
    raw_result: RawSimulationResult,
) -> PortfolioSimulationResult:
    final_values = raw_result.final_values
    sample_path = raw_result.sample_path
    all_paths = raw_result.all_paths

    expected_final_value = round(mean(final_values), 2)
    probability_of_loss = calculate_probability_of_loss(final_values, initial_budget)
    estimated_volatility = calculate_estimated_volatility(final_values)
    max_drawdown = calculate_max_drawdown(sample_path)

    percentiles = SimulationPercentiles(
        p10=calculate_percentile(final_values, 10),
        p50=calculate_percentile(final_values, 50),
        p90=calculate_percentile(final_values, 90),
    )

    metrics = SimulationMetrics(
        expected_final_value=expected_final_value,
        probability_of_loss=probability_of_loss,
        estimated_volatility=estimated_volatility,
        max_drawdown=max_drawdown,
        percentiles=percentiles,
    )

    sample_path_points = [
        SimulationPathPoint(step=index, portfolio_value=value)
        for index, value in enumerate(sample_path)
    ]

    percentile_band = build_percentile_band(all_paths)

    return PortfolioSimulationResult(
        initial_budget=initial_budget,
        num_simulations=num_simulations,
        time_horizon_months=time_horizon_months,
        metrics=metrics,
        sample_path=sample_path_points,
        percentile_band=percentile_band,
        summary=build_simulation_summary(profile, time_horizon_months),
    )