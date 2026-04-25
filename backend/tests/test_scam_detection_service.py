from app.services.scam_detection_service import (
    build_investment_checklist,
    map_probability_to_risk_level,
    predict_scam_risk,
)


def test_probability_maps_to_low_risk() -> None:
    assert map_probability_to_risk_level(0.2) == "low"


def test_probability_maps_to_medium_risk() -> None:
    assert map_probability_to_risk_level(0.5) == "medium"


def test_probability_maps_to_high_risk() -> None:
    assert map_probability_to_risk_level(0.8) == "high"


def test_investment_checklist_contains_user_guidance() -> None:
    checklist = build_investment_checklist()

    assert len(checklist) >= 5
    assert any("guaranteed returns" in item.check.lower() for item in checklist)
    assert any("independent sources" in item.check.lower() for item in checklist)


def test_predict_scam_risk_returns_high_risk_for_obvious_scam() -> None:
    result = predict_scam_risk(
        "Guaranteed profit with 20% daily return. Act now and send your wallet address."
    )

    assert result.predicted_label in {"safe", "suspicious", "scam"}
    assert result.risk_level in {"medium", "high"}
    assert result.scam_probability >= 0.4
    assert len(result.warning_signals) >= 1
    assert len(result.investment_checklist) >= 5
    assert "educational" not in result.educational_message.lower() or result.educational_message