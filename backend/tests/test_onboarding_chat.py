from app.services.onboarding_chat import (
    process_onboarding_message,
    start_onboarding_conversation,
)
from app.services.onboarding_state import get_initial_collected_fields


def test_start_onboarding_conversation() -> None:
    response = start_onboarding_conversation(session_id=1)

    assert response.session_id == 1
    assert response.current_stage == "intro"
    assert response.is_completed is False
    assert "interested in digital investing or crypto" in response.assistant_message


def test_process_onboarding_message_moves_to_next_stage() -> None:
    collected_fields = get_initial_collected_fields()

    response, updated_fields = process_onboarding_message(
        session_id=1,
        current_stage="goal",
        message_text="I want to understand risk before investing.",
        collected_fields=collected_fields,
    )

    assert updated_fields["goal"] == "I want to understand risk before investing."
    assert response.current_stage == "experience"
    assert response.is_completed is False


def test_process_onboarding_message_completes_flow() -> None:
    collected_fields = {
        "goal": "learn safely",
        "experience_level": "beginner",
        "budget": "100 pounds",
        "time_horizon": "1 to 3 years",
        "risk_attitude": None,
    }

    response, updated_fields = process_onboarding_message(
        session_id=1,
        current_stage="risk_attitude",
        message_text="I would probably stay calm and wait.",
        collected_fields=collected_fields,
    )

    assert updated_fields["risk_attitude"] == "I would probably stay calm and wait."
    assert response.current_stage == "complete"
    assert response.is_completed is True