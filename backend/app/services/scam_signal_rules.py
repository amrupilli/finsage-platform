from dataclasses import dataclass

from app.schemas.scam_detection import WarningSignal


@dataclass(frozen=True)
class ScamSignalRule:
    signal_type: str
    keywords: tuple[str, ...]
    severity: str
    explanation: str


SCAM_SIGNAL_RULES: tuple[ScamSignalRule, ...] = (
    ScamSignalRule(
        signal_type="guaranteed_return",
        keywords=(
            "guaranteed profit",
            "guaranteed return",
            "risk free profit",
            "no risk",
            "can't lose",
            "cannot lose",
        ),
        severity="high",
        explanation="Claims of guaranteed or risk-free returns are a common investment scam warning sign.",
    ),
    ScamSignalRule(
        signal_type="unrealistic_return",
        keywords=(
            "double your money",
            "100% return",
            "20% daily",
            "daily profit",
            "massive returns",
            "huge returns",
        ),
        severity="high",
        explanation="Very high or unrealistic return claims can indicate misleading or fraudulent promotion.",
    ),
    ScamSignalRule(
        signal_type="urgency_pressure",
        keywords=(
            "act now",
            "limited time",
            "only today",
            "don't miss out",
            "last chance",
            "join now",
        ),
        severity="medium",
        explanation="Urgency language can pressure users into decisions without proper research.",
    ),
    ScamSignalRule(
        signal_type="social_hype",
        keywords=(
            "everyone is buying",
            "viral token",
            "celebrity backed",
            "influencer approved",
            "next bitcoin",
        ),
        severity="medium",
        explanation="Hype-based promotion may encourage speculative behaviour without clear evidence.",
    ),
    ScamSignalRule(
        signal_type="private_contact",
        keywords=(
            "dm me",
            "message me privately",
            "send wallet",
            "whatsapp me",
            "telegram group",
        ),
        severity="medium",
        explanation="Moving investment discussions into private channels can reduce transparency and accountability.",
    ),
)


def extract_warning_signals(text: str) -> list[WarningSignal]:
    lowered_text = text.lower()
    detected_signals: list[WarningSignal] = []

    for rule in SCAM_SIGNAL_RULES:
        for keyword in rule.keywords:
            if keyword in lowered_text:
                detected_signals.append(
                    WarningSignal(
                        signal_type=rule.signal_type,
                        matched_text=keyword,
                        severity=rule.severity,
                        explanation=rule.explanation,
                    )
                )
                break

    return detected_signals