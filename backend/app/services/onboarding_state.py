from app.schemas.onboarding import ConversationStage

STAGE_ORDER: list[ConversationStage] = [
    "intro",
    "goal",
    "experience",
    "budget",
    "time_horizon",
    "risk_attitude",
    "complete",
]

FIELD_BY_STAGE = {
    "goal": "goal",
    "experience": "experience_level",
    "budget": "budget",
    "time_horizon": "time_horizon",
    "risk_attitude": "risk_attitude",
}


def get_initial_collected_fields() -> dict[str, str | None]:
    return {
        "goal": None,
        "experience_level": None,
        "budget": None,
        "time_horizon": None,
        "risk_attitude": None,
    }


def get_missing_fields(collected_fields: dict[str, str | None]) -> list[str]:
    return [key for key, value in collected_fields.items() if not value]


def get_next_stage(current_stage: ConversationStage) -> ConversationStage:
    current_index = STAGE_ORDER.index(current_stage)

    if current_index + 1 < len(STAGE_ORDER):
        return STAGE_ORDER[current_index + 1]

    return "complete"
