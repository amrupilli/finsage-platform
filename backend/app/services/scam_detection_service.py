from pathlib import Path
from typing import Any
from app.services.warning_explanation_service import build_warning_from_scam_prediction
import joblib

from app.ml.scam_detection.train_model import MODEL_PATH, train_and_save_model
from app.schemas.scam_detection import (
    InvestmentChecklistItem,
    ScamPredictionResponse,
    WarningSignal,
)
from app.services.scam_signal_rules import extract_warning_signals


def load_scam_detection_model() -> Any:
    if not Path(MODEL_PATH).exists():
        train_and_save_model()

    return joblib.load(MODEL_PATH)


def map_probability_to_risk_level(scam_probability: float) -> str:
    if scam_probability >= 0.7:
        return "high"

    if scam_probability >= 0.4:
        return "medium"

    return "low"


def build_investment_checklist() -> list[InvestmentChecklistItem]:
    return [
        InvestmentChecklistItem(
            check="Check whether the message promises guaranteed returns.",
            reason="Genuine investment opportunities cannot guarantee profits because market values can rise or fall.",
        ),
        InvestmentChecklistItem(
            check="Check whether the message pressures you to act quickly.",
            reason="Urgency tactics can push users into decisions before they have time to research properly.",
        ),
        InvestmentChecklistItem(
            check="Check whether the project explains risks clearly.",
            reason="Transparent projects should explain volatility, fees, uncertainty, and possible loss.",
        ),
        InvestmentChecklistItem(
            check="Check whether independent sources support the claim.",
            reason="Users should compare claims against reliable sources rather than relying on one advert or message.",
        ),
        InvestmentChecklistItem(
            check="Check whether private payment or private messaging is requested.",
            reason="Requests to move into private channels can reduce transparency and accountability.",
        ),
    ]


def build_prediction_explanation(
    predicted_label: str,
    scam_probability: float,
    warning_signals: list[WarningSignal],
) -> str:
    if warning_signals:
        signal_names = ", ".join(signal.signal_type for signal in warning_signals)
        return (
            f"The message was classified as {predicted_label} with a scam probability "
            f"of {scam_probability:.2f}. The system detected warning signals including: "
            f"{signal_names}."
        )

    return (
        f"The message was classified as {predicted_label} with a scam probability "
        f"of {scam_probability:.2f}. No major rule-based warning signals were detected, "
        "but users should still research investment claims independently."
    )


def build_educational_message(predicted_label: str, risk_level: str) -> str:
    if predicted_label == "scam" or risk_level == "high":
        return (
            "This message contains high-risk indicators. Treat the claim with caution, "
            "avoid sending money or wallet details, and verify the opportunity using independent sources."
        )

    if predicted_label == "suspicious" or risk_level == "medium":
        return (
            "This message contains some risk indicators. It may not be a confirmed scam, "
            "but you should slow down, compare sources, and check whether the claims are realistic."
        )

    return (
        "This message appears lower risk based on the current model, but this does not mean it is safe to invest. "
        "Always research independently and remember that this platform is educational, not financial advice."
    )


def predict_scam_risk(text: str) -> ScamPredictionResponse:
    model = load_scam_detection_model()

    predicted_label = model.predict([text])[0]
    class_probabilities = model.predict_proba([text])[0]
    class_labels = list(model.classes_)

    if "scam" in class_labels:
        scam_class_index = class_labels.index("scam")
        scam_probability = float(class_probabilities[scam_class_index])
    else:
        scam_probability = 0.0

    warning_signals = extract_warning_signals(text)

    if warning_signals and scam_probability < 0.4:
        scam_probability = 0.4

    risk_level = map_probability_to_risk_level(scam_probability)

    prediction = ScamPredictionResponse(
        input_text=text,
        predicted_label=predicted_label,
        scam_probability=scam_probability,
        risk_level=risk_level,
        warning_signals=warning_signals,
        investment_checklist=build_investment_checklist(),
        explanation=build_prediction_explanation(
            predicted_label=predicted_label,
            scam_probability=scam_probability,
            warning_signals=warning_signals,
        ),
        educational_message=build_educational_message(
            predicted_label=predicted_label,
            risk_level=risk_level,
        ),
    )

    prediction.warning_summary = build_warning_from_scam_prediction(prediction)

    return prediction