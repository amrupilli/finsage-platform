from app.services.simulation_engine import RawSimulationResult
from app.services.simulation_metrics import (
    build_percentile_band,
    build_simulation_result,
    calculate_estimated_volatility,
    calculate_max_drawdown,
    calculate_percentile,
    calculate_probability_of_loss,
)


def test_calculate_percentile() -> None:
    values = [80.0, 90.0, 100.0, 110.0, 120.0]

    assert calculate_percentile(values, 10) == 84.0
    assert calculate_percentile(values, 50) == 100.0
    assert calculate_percentile(values, 90) == 116.0


def test_calculate_probability_of_loss() -> None:
    final_values = [80.0, 95.0, 105.0, 120.0]
    result = calculate_probability_of_loss(final_values, 100.0)

    assert result == 0.5


def test_calculate_estimated_volatility() -> None:
    final_values = [100.0, 110.0, 90.0, 120.0, 80.0]
    result = calculate_estimated_volatility(final_values)

    assert result > 0


def test_calculate_max_drawdown() -> None:
    sample_path = [100.0, 120.0, 110.0, 90.0, 95.0]
    result = calculate_max_drawdown(sample_path)

    assert result == 0.25


def test_build_percentile_band() -> None:
    all_paths = [
        [100.0, 105.0, 110.0],
        [100.0, 100.0, 95.0],
        [100.0, 110.0, 120.0],
    ]

    band = build_percentile_band(all_paths)

    assert len(band) == 3
    assert band[0].step == 0
    assert band[0].p50 == 100.0


def test_build_simulation_result() -> None:
    raw_result = RawSimulationResult(
        final_values=[80.0, 95.0, 100.0, 110.0, 130.0],
        sample_path=[100.0, 105.0, 98.0, 115.0],
        all_paths=[
            [100.0, 102.0, 101.0, 103.0],
            [100.0, 104.0, 99.0, 95.0],
            [100.0, 106.0, 100.0, 100.0],
            [100.0, 108.0, 105.0, 110.0],
            [100.0, 110.0, 112.0, 130.0],
        ],
    )

    result = build_simulation_result(
        profile="Moderate",
        initial_budget=100.0,
        num_simulations=5,
        time_horizon_months=12,
        raw_result=raw_result,
    )

    assert result.initial_budget == 100.0
    assert result.num_simulations == 5
    assert result.time_horizon_months == 12
    assert result.metrics.expected_final_value == 103.0
    assert result.metrics.probability_of_loss == 0.4
    assert result.metrics.percentiles.p50 == 100.0
    assert len(result.sample_path) == 4
    assert len(result.percentile_band) == 4