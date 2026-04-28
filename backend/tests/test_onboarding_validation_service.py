from app.services.onboarding_validation_service import validate_onboarding_answer


def test_rejects_nonsense_answer() -> None:
    is_valid, message = validate_onboarding_answer("goal", "asdfgh")

    assert is_valid is False
    assert message is not None


def test_rejects_too_short_goal() -> None:
    is_valid, message = validate_onboarding_answer("goal", "money")

    assert is_valid is False
    assert message is not None


def test_accepts_valid_goal_answer() -> None:
    is_valid, message = validate_onboarding_answer(
        "goal",
        "I want to learn how to invest safely.",
    )

    assert is_valid is True
    assert message is None


def test_accepts_valid_budget_answer() -> None:
    is_valid, message = validate_onboarding_answer(
        "budget",
        "I can put around 100 pounds per month.",
    )

    assert is_valid is True
    assert message is None


def test_rejects_invalid_time_horizon_answer() -> None:
    is_valid, message = validate_onboarding_answer("time_horizon", "maybe")

    assert is_valid is False
    assert message is not None


def test_accepts_valid_risk_attitude_answer() -> None:
    is_valid, message = validate_onboarding_answer(
        "risk_attitude",
        "I would be worried if I lost money, so I prefer safer options.",
    )

    assert is_valid is True
    assert message is None