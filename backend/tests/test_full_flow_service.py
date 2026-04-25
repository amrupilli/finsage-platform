from unittest.mock import Mock, patch

from app.services.full_flow_service import run_full_financial_flow


@patch("app.services.full_flow_service.build_portfolio_concentration_warning")
@patch("app.services.full_flow_service.build_simulation_warning")
@patch("app.services.full_flow_service.generate_simulation_for_session")
@patch("app.services.full_flow_service.generate_portfolio_for_session")
@patch("app.services.full_flow_service.generate_risk_profile")
@patch("app.services.full_flow_service.build_collected_fields_from_answers")
@patch("app.services.full_flow_service.get_session_answers")
@patch("app.services.full_flow_service.get_onboarding_session_by_id")
def test_full_flow_runs_all_steps(
    mock_get_session,
    mock_get_answers,
    mock_build_fields,
    mock_generate_risk,
    mock_generate_portfolio,
    mock_generate_simulation,
    mock_sim_warning,
    mock_portfolio_warning,
) -> None:
    db = Mock()

    user = Mock()
    user.id = 1

    session = Mock()
    session.id = 10

    mock_get_session.return_value = session
    mock_get_answers.return_value = []
    mock_build_fields.return_value = {}

    mock_generate_risk.return_value = Mock()
    mock_generate_portfolio.return_value = Mock(allocations=[Mock(percentage=50)])
    mock_generate_simulation.return_value = Mock(
        metrics=Mock(probability_of_loss=0.3)
    )

    mock_sim_warning.return_value = Mock()
    mock_portfolio_warning.return_value = Mock()

    result = run_full_financial_flow(
        db=db,
        session_id=10,
        current_user=user,
    )

    assert "risk_profile" in result
    assert "portfolio" in result
    assert "simulation" in result
    assert "warnings" in result