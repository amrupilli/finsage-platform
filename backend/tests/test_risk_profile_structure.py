from app.services.risk_profile_structure import build_risk_summary, determine_risk_label


def test_determine_risk_label_conservative() -> None:
    assert determine_risk_label(5) == "Conservative"


def test_determine_risk_label_moderate() -> None:
    assert determine_risk_label(8) == "Moderate"


def test_determine_risk_label_aggressive() -> None:
    assert determine_risk_label(12) == "Aggressive"


def test_build_risk_summary() -> None:
    summary = build_risk_summary(
        "Moderate",
        [
            "The user showed some caution.",
            "The user described a medium-term investment mindset.",
        ],
    )

    assert "Moderate" in summary
    assert "some caution" in summary
    assert "medium-term investment mindset" in summary