from unittest.mock import Mock, patch
from app.schemas.warning import UserWarning
from app.services.report_service import REPORT_DISCLAIMER, build_report_for_session


def test_report_disclaimer_is_non_advisory() -> None:
    assert "educational purposes only" in REPORT_DISCLAIMER
    assert "does not provide financial advice" in REPORT_DISCLAIMER


@patch("app.services.report_service.build_portfolio_concentration_warning")
@patch("app.services.report_service.build_simulation_warning")
@patch("app.services.report_service.generate_simulation_for_session")
@patch("app.services.report_service.generate_portfolio_for_session")
@patch("app.services.report_service.generate_risk_profile")
@patch("app.services.report_service.build_collected_fields_from_answers")
@patch("app.services.report_service.get_session_answers")
@patch("app.services.report_service.get_onboarding_session_by_id")
def test_build_report_for_session_combines_outputs(
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
    user.email = "student@example.com"

    session = Mock()
    session.id = 10

    mock_get_session.return_value = session
    mock_get_answers.return_value = []
    mock_build_fields.return_value = {
        "goal": "learn safely",
        "experience_level": "beginner",
        "budget": "100",
        "time_horizon": "1 year",
        "risk_attitude": "wait",
    }

    risk_profile = Mock()
    risk_profile.profile = "Moderate"
    risk_profile.summary = "Moderate educational profile."
    mock_generate_risk.return_value = risk_profile

    allocation_one = Mock()
    allocation_one.category = "Stable Digital Assets"
    allocation_one.percentage = 60

    allocation_two = Mock()
    allocation_two.category = "Growth Digital Assets"
    allocation_two.percentage = 40

    portfolio = Mock()
    portfolio.summary = "Balanced portfolio scenario."
    portfolio.allocations = [allocation_one, allocation_two]
    mock_generate_portfolio.return_value = portfolio

    simulation_metrics = Mock()
    simulation_metrics.expected_final_value = 1250.0
    simulation_metrics.probability_of_loss = 0.28

    simulation = Mock()
    simulation.metrics = simulation_metrics
    simulation.summary = "Simulation shows moderate downside risk."
    mock_generate_simulation.return_value = simulation

    simulation_warning = UserWarning(
    category="simulation_risk",
    severity="medium",
    title="Moderate downside risk in simulation",
    message="The simulation shows a meaningful chance of loss.",
    recommended_action="Review downside outcomes before interpreting the result.",
    )

    portfolio_warning = UserWarning(
    category="portfolio_risk",
    severity="high",
    title="High portfolio concentration detected",
    message="A large share of the scenario is concentrated in one asset category.",
    recommended_action="Review diversification before interpreting the result.",
    )

    mock_sim_warning.return_value = simulation_warning
    mock_portfolio_warning.return_value = portfolio_warning

    report = build_report_for_session(
        db=db,
        session_id=10,
        current_user=user,
    )

    assert report.user_email == "student@example.com"
    assert report.risk_profile.profile == "Moderate"
    assert report.portfolio.allocations["Stable Digital Assets"] == 60
    assert report.simulation.expected_return == 1250.0
    assert len(report.warnings) == 2
    assert "financial advice" in report.disclaimer