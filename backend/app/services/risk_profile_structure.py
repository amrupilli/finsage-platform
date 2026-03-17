from app.schemas.risk_profile import RiskProfileResult
from app.services.risk_dimensions import PROFILE_THRESHOLDS


def determine_risk_label(total_score: int) -> str:
    for label, (min_score, max_score) in PROFILE_THRESHOLDS.items():
        if min_score <= total_score <= max_score:
            return label
    return "Moderate"


def build_risk_summary(profile: str, rationales: list[str]) -> str:
    joined_rationales = " ".join(rationales)
    return f"The user was classified as {profile} based on the collected onboarding signals. {joined_rationales}"