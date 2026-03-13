from app.services.onboarding_interpreter import clean_user_message, extract_field_value


def test_clean_user_message() -> None:
    cleaned = clean_user_message("  I want   to learn more   about crypto  ")
    assert cleaned == "I want to learn more about crypto"


def test_extract_field_value_for_goal_stage() -> None:
    field_name, value = extract_field_value(
        "goal",
        "I want to learn safely before investing anything serious.",
    )

    assert field_name == "goal"
    assert value == "I want to learn safely before investing anything serious."


def test_extract_field_value_for_intro_stage_returns_none() -> None:
    field_name, value = extract_field_value(
        "intro",
        "I heard a lot about crypto online.",
    )

    assert field_name is None
    assert value is None