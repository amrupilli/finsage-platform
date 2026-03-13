from app.schemas.onboarding import ConversationStage
from app.services.onboarding_state import FIELD_BY_STAGE


def clean_user_message(message_text: str) -> str:
    return " ".join(message_text.strip().split())


def extract_field_value(
    stage: ConversationStage,
    message_text: str,
) -> tuple[str | None, str | None]:
    cleaned_message = clean_user_message(message_text)

    if stage == "intro":
        return None, None

    field_name = FIELD_BY_STAGE.get(stage)

    if not field_name:
        return None, None

    if not cleaned_message:
        return field_name, None

    return field_name, cleaned_message