import re


MIN_USEFUL_LENGTH = 4


GENERIC_INVALID_RESPONSES = {
    "hi",
    "hello",
    "hey",
    "ok",
    "okay",
    "yes",
    "no",
    "idk",
    "dont know",
    "don't know",
    "not sure",
    "asdf",
    "asdfgh",
    "qwerty",
    "random",
    "blah",
    "test",
    "nothing",
}


def normalise_user_text(text: str) -> str:
    return text.strip().lower()


def looks_like_repeated_characters(text: str) -> bool:
    cleaned = re.sub(r"\s+", "", text.lower())

    if len(cleaned) < 4:
        return False

    return len(set(cleaned)) <= 2


def has_enough_signal(text: str) -> bool:
    cleaned = normalise_user_text(text)

    if len(cleaned) < MIN_USEFUL_LENGTH:
        return False

    if cleaned in GENERIC_INVALID_RESPONSES:
        return False

    if looks_like_repeated_characters(cleaned):
        return False

    return True


def validate_onboarding_answer(stage: str, answer: str) -> tuple[bool, str | None]:
    cleaned = normalise_user_text(answer)

    if not has_enough_signal(cleaned):
        return (
            False,
            "I need a little more detail before I can use that answer. Could you explain your answer in a short sentence?",
        )

    if stage == "goal":
        if len(cleaned.split()) < 3:
            return (
                False,
                "Could you describe your investing goal in a bit more detail? For example, are you trying to learn, grow money slowly, or explore higher-risk assets?",
            )

    if stage == "experience":
        experience_terms = [
            "beginner",
            "new",
            "little",
            "some",
            "intermediate",
            "experienced",
            "expert",
            "never",
            "started",
            "know",
            "learn",
        ]

        if not any(term in cleaned for term in experience_terms) and len(cleaned.split()) < 4:
            return (
                False,
                "Could you tell me more about your investing experience? For example, whether you are a beginner or have invested before.",
            )

    if stage == "budget":
        has_number = any(character.isdigit() for character in cleaned)
        budget_terms = ["small", "low", "medium", "high", "afford", "month", "pounds", "£"]

        if not has_number and not any(term in cleaned for term in budget_terms):
            return (
                False,
                "Could you give a rough idea of your budget or comfort level? For example, a monthly amount or whether it is low, medium, or high.",
            )

    if stage == "time_horizon":
        time_terms = [
            "month",
            "months",
            "year",
            "years",
            "short",
            "long",
            "term",
            "weeks",
            "future",
        ]

        if not any(term in cleaned for term in time_terms) and not any(character.isdigit() for character in cleaned):
            return (
                False,
                "Could you explain your time horizon? For example, a few months, one year, or several years.",
            )

    if stage == "risk_attitude":
        risk_terms = [
            "risk",
            "safe",
            "loss",
            "lose",
            "comfortable",
            "worried",
            "cautious",
            "aggressive",
            "stable",
            "volatile",
            "wait",
            "panic",
        ]

        if not any(term in cleaned for term in risk_terms) and len(cleaned.split()) < 4:
            return (
                False,
                "Could you explain how you would feel if your investment went down in value? This helps estimate your risk attitude.",
            )

    return True, None