from app.ml.scam_detection.synthetic_dataset import get_training_texts_and_labels
from app.schemas.scam_detection import (
    ScamCheckRequest,
    ScamPredictionResponse,
    WarningSignal,
)
from app.services.scam_signal_rules import extract_warning_signals


def test_scam_check_request_accepts_valid_text() -> None:
    request = ScamCheckRequest(text="This is an investment message with enough text.")

    assert request.text.startswith("This is")


def test_warning_signal_extraction_detects_guaranteed_returns() -> None:
    signals = extract_warning_signals(
        "This project offers guaranteed profit with no risk."
    )

    signal_types = [signal.signal_type for signal in signals]

    assert "guaranteed_return" in signal_types


def test_warning_signal_extraction_detects_urgency() -> None:
    signals = extract_warning_signals(
        "Act now because this is a limited time opportunity."
    )

    signal_types = [signal.signal_type for signal in signals]

    assert "urgency_pressure" in signal_types


def test_synthetic_dataset_has_multiple_labels() -> None:
    texts, labels = get_training_texts_and_labels()

    assert len(texts) == len(labels)
    assert len(texts) >= 40
    assert "safe" in labels
    assert "suspicious" in labels
    assert "scam" in labels


def test_prediction_response_schema() -> None:
    response = ScamPredictionResponse(
        input_text="Guaranteed profit if you invest today.",
        predicted_label="scam",
        scam_probability=0.91,
        risk_level="high",
        warning_signals=[
            WarningSignal(
                signal_type="guaranteed_return",
                matched_text="guaranteed profit",
                severity="high",
                explanation="Guaranteed returns are a common scam warning sign.",
            )
        ],
        investment_checklist=[
            {
                "check": "Check whether the message promises guaranteed returns.",
                "reason": "Guaranteed returns are a common warning sign in misleading investment promotions.",
            }
        ],
        explanation="The message contains high-risk promotional language.",
        educational_message="Treat guaranteed return claims with caution and research before making decisions.",
    )

    assert response.predicted_label == "scam"
    assert response.risk_level == "high"
    assert response.scam_probability > 0.9
    assert len(response.warning_signals) == 1
    assert len(response.investment_checklist) == 1