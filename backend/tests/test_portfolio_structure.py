from app.services.portfolio_structure import build_portfolio_scenario
import pytest

def test_build_portfolio_scenario_conservative() -> None:
    result = build_portfolio_scenario("Conservative", 100.0)

    assert result.portfolio_type == "Conservative Learning Portfolio"
    assert result.total_budget == 100.0
    assert len(result.allocations) == 3

    stable = result.allocations[0]
    assert stable.category == "Stable / Low Risk"
    assert stable.percentage == 70.0
    assert stable.amount == 70.0


def test_build_portfolio_scenario_moderate() -> None:
    result = build_portfolio_scenario("Moderate", 200.0)

    assert result.portfolio_type == "Balanced Learning Portfolio"
    assert result.total_budget == 200.0
    assert len(result.allocations) == 3

    amounts = [allocation.amount for allocation in result.allocations]
    assert sum(amounts) == 200.0


def test_build_portfolio_scenario_aggressive() -> None:
    result = build_portfolio_scenario("Aggressive", 1000.0)

    assert result.portfolio_type == "Growth-Oriented Learning Portfolio"
    assert len(result.allocations) == 3

    speculative = result.allocations[2]
    assert speculative.category == "Speculative / High Risk"
    assert speculative.percentage == 45.0
    assert speculative.amount == 450.0

def test_build_portfolio_scenario_rejects_invalid_profile() -> None:
    with pytest.raises(ValueError, match="Unsupported risk profile"):
        build_portfolio_scenario("Very Aggressive", 100.0)


def test_build_portfolio_scenario_rejects_invalid_budget() -> None:
    with pytest.raises(ValueError, match="Budget must be greater than zero"):
        build_portfolio_scenario("Moderate", 0.0)