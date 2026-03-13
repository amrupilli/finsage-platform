from app.schemas.onboarding import ConversationStage, OnboardingNextMessageResponse
from app.services.onboarding_interpreter import extract_field_value
from app.services.onboarding_prompts import ONBOARDING_PROMPTS
from app.services.onboarding_state import (
    get_initial_collected_fields,
    get_missing_fields,
    get_next_stage,
)


def start_onboarding_conversation(session_id: int) -> OnboardingNextMessageResponse:
    collected_fields = get_initial_collected_fields()

    return OnboardingNextMessageResponse(
        session_id=session_id,
        assistant_message=ONBOARDING_PROMPTS["intro"],
        current_stage="intro",
        missing_fields=get_missing_fields(collected_fields),
        is_completed=False,
    )


def process_onboarding_message(
    session_id: int,
    current_stage: ConversationStage,
    message_text: str,
    collected_fields: dict[str, str | None],
) -> tuple[OnboardingNextMessageResponse, dict[str, str | None]]:
    updated_fields = collected_fields.copy()

    field_name, extracted_value = extract_field_value(current_stage, message_text)

    if field_name and extracted_value:
        updated_fields[field_name] = extracted_value

    next_stage = get_next_stage(current_stage)
    missing_fields = get_missing_fields(updated_fields)

    if next_stage == "complete":
        return (
            OnboardingNextMessageResponse(
                session_id=session_id,
                assistant_message=ONBOARDING_PROMPTS["complete"],
                current_stage="complete",
                missing_fields=missing_fields,
                is_completed=True,
            ),
            updated_fields,
        )

    return (
        OnboardingNextMessageResponse(
            session_id=session_id,
            assistant_message=ONBOARDING_PROMPTS[next_stage],
            current_stage=next_stage,
            missing_fields=missing_fields,
            is_completed=False,
        ),
        updated_fields,
    )