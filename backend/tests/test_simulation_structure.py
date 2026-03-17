import pytest

from app.services.simulation_structure import (
    build_simulation_summary,
    get_simulation_assumptions,
)


def test_get_simulation_assumptions_conservative() -> None:
    assumptions = get_simulation_assumptions("Conservative")
    assert assumptions["expected_annual_return"] == 0.04
    assert assumptions["annual_volatility"] == 0.08


def test_get_simulation_assumptions_moderate() -> None:
    assumptions = get_simulation_assumptions("Moderate")
    assert assumptions["expected_annual_return"] == 0.07
    assert assumptions["annual_volatility"] == 0.15


def test_get_simulation_assumptions_aggressive() -> None:
    assumptions = get_simulation_assumptions("Aggressive")
    assert assumptions["expected_annual_return"] == 0.11
    assert assumptions["annual_volatility"] == 0.25


def test_get_simulation_assumptions_rejects_invalid_profile() -> None:
    with pytest.raises(ValueError, match="Unsupported risk profile"):
        get_simulation_assumptions("Very Aggressive")


def test_build_simulation_summary() -> None:
    summary = build_simulation_summary("Moderate", 12)
    assert "12-month outlook" in summary
    assert "Moderate" in summary
    assert "educational" in summary