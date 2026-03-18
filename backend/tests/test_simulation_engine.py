import random

import pytest

from app.services.simulation_engine import run_monte_carlo_simulation


def test_run_monte_carlo_simulation_returns_expected_lengths() -> None:
    random.seed(42)

    result = run_monte_carlo_simulation(
        profile="Moderate",
        initial_budget=100.0,
        num_simulations=100,
        time_horizon_months=12,
    )

    assert len(result.final_values) == 100
    assert len(result.sample_path) == 13
    assert len(result.all_paths) == 100
    assert len(result.all_paths[0]) == 13

def test_run_monte_carlo_simulation_sample_path_starts_with_initial_budget() -> None:
    random.seed(42)

    result = run_monte_carlo_simulation(
        profile="Conservative",
        initial_budget=250.0,
        num_simulations=50,
        time_horizon_months=6,
    )

    assert result.sample_path[0] == 250.0


def test_run_monte_carlo_simulation_rejects_invalid_budget() -> None:
    with pytest.raises(ValueError, match="Initial budget must be greater than zero"):
        run_monte_carlo_simulation(
            profile="Moderate",
            initial_budget=0,
            num_simulations=100,
            time_horizon_months=12,
        )


def test_run_monte_carlo_simulation_rejects_invalid_num_simulations() -> None:
    with pytest.raises(ValueError, match="Number of simulations must be greater than zero"):
        run_monte_carlo_simulation(
            profile="Moderate",
            initial_budget=100,
            num_simulations=0,
            time_horizon_months=12,
        )


def test_run_monte_carlo_simulation_rejects_invalid_time_horizon() -> None:
    with pytest.raises(ValueError, match="Time horizon must be greater than zero"):
        run_monte_carlo_simulation(
            profile="Moderate",
            initial_budget=100,
            num_simulations=100,
            time_horizon_months=0,
        )


def test_run_monte_carlo_simulation_rejects_invalid_profile() -> None:
    with pytest.raises(ValueError, match="Unsupported risk profile"):
        run_monte_carlo_simulation(
            profile="Very Aggressive",
            initial_budget=100,
            num_simulations=100,
            time_horizon_months=12,
        )