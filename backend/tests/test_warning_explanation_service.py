from app.schemas.scam_detection import ScamPredictionResponse
from app.services.warning_explanation_service import (
    build_portfolio_concentration_warning,
    build_simulation_warning,
    build_warning_from_scam_prediction,
)


def test_high_scam_prediction_builds_high_warning() -> None:
    prediction = ScamPredictionResponse(
        input_text="Guaranteed profit.",
        predicted_label="scam",
        scam_probability=0.9,
        risk_level="high",
        warning_signals=[],
        investment_checklist=[],
        explanation="High risk.",
        educational_message="Be careful.",
    )

    warning = build_warning_from_scam_prediction(prediction)

    assert warning.category == "scam_risk"
    assert warning.severity == "high"
    assert "scam-risk" in warning.title.lower()


def test_medium_scam_prediction_builds_medium_warning() -> None:
    prediction = ScamPredictionResponse(
        input_text="This looks hyped.",
        predicted_label="suspicious",
        scam_probability=0.5,
        risk_level="medium",
        warning_signals=[],
        investment_checklist=[],
        explanation="Medium risk.",
        educational_message="Check carefully.",
    )

    warning = build_warning_from_scam_prediction(prediction)

    assert warning.category == "scam_risk"
    assert warning.severity == "medium"
    assert "suspicious" in warning.title.lower()


def test_low_scam_prediction_builds_low_guidance() -> None:
    prediction = ScamPredictionResponse(
        input_text="This is educational.",
        predicted_label="safe",
        scam_probability=0.1,
        risk_level="low",
        warning_signals=[],
        investment_checklist=[],
        explanation="Low risk.",
        educational_message="Still research.",
    )

    warning = build_warning_from_scam_prediction(prediction)

    assert warning.category == "educational_guidance"
    assert warning.severity == "low"


def test_medium_simulation_loss_builds_medium_warning() -> None:
    warning = build_simulation_warning(probability_of_loss=0.3)

    assert warning.category == "simulation_risk"
    assert warning.severity == "medium"


def test_high_simulation_loss_builds_high_warning() -> None:
    warning = build_simulation_warning(probability_of_loss=0.6)

    assert warning.category == "simulation_risk"
    assert warning.severity == "high"


def test_low_simulation_loss_builds_low_guidance() -> None:
    warning = build_simulation_warning(probability_of_loss=0.1)

    assert warning.category == "educational_guidance"
    assert warning.severity == "low"


def test_high_concentration_builds_high_warning() -> None:
    warning = build_portfolio_concentration_warning(
        largest_allocation_percentage=70
    )

    assert warning.category == "portfolio_risk"
    assert warning.severity == "high"


def test_medium_concentration_builds_medium_warning() -> None:
    warning = build_portfolio_concentration_warning(
        largest_allocation_percentage=45
    )

    assert warning.category == "portfolio_risk"
    assert warning.severity == "medium"


def test_low_concentration_builds_low_guidance() -> None:
    warning = build_portfolio_concentration_warning(
        largest_allocation_percentage=25
    )

    assert warning.category == "educational_guidance"
    assert warning.severity == "low"