from app.services.onboarding_state import (
    get_initial_collected_fields,
    get_missing_fields,
    get_next_stage,
)


def test_get_initial_collected_fields() -> None:
    fields = get_initial_collected_fields()

    assert fields["goal"] is None
    assert fields["experience_level"] is None
    assert fields["budget"] is None
    assert fields["time_horizon"] is None
    assert fields["risk_attitude"] is None


def test_get_missing_fields() -> None:
    fields = {
        "goal": "learn safely",
        "experience_level": None,
        "budget": "100",
        "time_horizon": None,
        "risk_attitude": "cautious",
    }

    missing = get_missing_fields(fields)

    assert missing == ["experience_level", "time_horizon"]


def test_get_next_stage() -> None:
    assert get_next_stage("intro") == "goal"
    assert get_next_stage("goal") == "experience"
    assert get_next_stage("risk_attitude") == "complete"
