from app.schemas.risk_profile import RiskDimensionScore, RiskProfileResult
from app.services.risk_profile_structure import build_risk_summary, determine_risk_label


def contains_any(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def score_goal(goal: str | None) -> RiskDimensionScore:
    if not goal:
        return RiskDimensionScore(
            dimension="goal",
            score=0,
            rationale="No clear investment goal was collected.",
        )

    goal_lower = goal.lower()

    high_risk_terms = [
        "high risk",
        "higher risk",
        "risky",
        "riskier",
        "aggressive",
        "high return",
        "higher return",
        "big return",
        "maximum return",
        "crypto",
        "speculative",
        "volatile",
        "fast growth",
    ]

    cautious_terms = [
        "low risk",
        "lower risk",
        "safe",
        "safely",
        "avoid risk",
        "protect",
        "stable",
        "cautious",
        "conservative",
        "dont lose",
        "don't lose",
        "not lose",
        "preserve",
    ]

    moderate_terms = [
        "grow",
        "growth",
        "money",
        "returns",
        "balanced",
        "medium",
        "moderate",
    ]

    if contains_any(goal_lower, cautious_terms):
        return RiskDimensionScore(
            dimension="goal",
            score=1,
            rationale="The user’s goal clearly prioritises low-risk or safer investing, suggesting a conservative objective.",
        )

    if contains_any(goal_lower, high_risk_terms):
        return RiskDimensionScore(
            dimension="goal",
            score=3,
            rationale="The user’s goal explicitly mentions higher-risk or speculative investing, suggesting stronger willingness to explore volatile assets.",
        )

    if contains_any(goal_lower, moderate_terms):
        return RiskDimensionScore(
            dimension="goal",
            score=2,
            rationale="The user appears interested in growth while not explicitly requesting high-risk exposure.",
        )

    return RiskDimensionScore(
        dimension="goal",
        score=2,
        rationale="The user’s goal suggests general investment interest, but does not clearly indicate either strong caution or high-risk appetite.",
    )


def score_experience(experience: str | None) -> RiskDimensionScore:
    if not experience:
        return RiskDimensionScore(
            dimension="experience_level",
            score=0,
            rationale="No experience level was collected.",
        )

    experience_lower = experience.lower()

    if contains_any(experience_lower, ["beginner", "new", "no experience", "never invested"]):
        return RiskDimensionScore(
            dimension="experience_level",
            score=1,
            rationale="The user appears to be a beginner, so the system should avoid assuming strong risk knowledge.",
        )

    if contains_any(experience_lower, ["some", "little", "basic", "started", "limited"]):
        return RiskDimensionScore(
            dimension="experience_level",
            score=2,
            rationale="The user has some investment exposure, suggesting developing knowledge but not advanced expertise.",
        )

    if contains_any(experience_lower, ["experienced", "comfortable", "confident", "advanced"]):
        return RiskDimensionScore(
            dimension="experience_level",
            score=3,
            rationale="The user describes stronger investment experience, which can support a higher risk capacity.",
        )

    return RiskDimensionScore(
        dimension="experience_level",
        score=2,
        rationale="The user gave a general experience response, suggesting moderate familiarity.",
    )


def score_budget(budget: str | None) -> RiskDimensionScore:
    if not budget:
        return RiskDimensionScore(
            dimension="budget",
            score=0,
            rationale="No budget information was collected.",
        )

    budget_lower = budget.lower()

    if contains_any(budget_lower, ["small", "low", "limited", "50", "100"]):
        return RiskDimensionScore(
            dimension="budget",
            score=1,
            rationale="The user described a limited budget, which reduces financial capacity for higher-risk exposure.",
        )

    if contains_any(budget_lower, ["1000", "large", "high", "more", "thousand"]):
        return RiskDimensionScore(
            dimension="budget",
            score=2,
            rationale="The user described a larger educational budget, but budget alone does not imply higher risk appetite.",
        )

    if contains_any(budget_lower, ["200", "300", "500", "medium", "moderate"]):
        return RiskDimensionScore(
            dimension="budget",
            score=2,
            rationale="The user appears comfortable with a moderate educational investment amount.",
        )

    return RiskDimensionScore(
        dimension="budget",
        score=2,
        rationale="The user provided a budget response that suggests moderate financial capacity.",
    )


def score_time_horizon(time_horizon: str | None) -> RiskDimensionScore:
    if not time_horizon:
        return RiskDimensionScore(
            dimension="time_horizon",
            score=0,
            rationale="No time horizon was collected.",
        )

    horizon_lower = time_horizon.lower()

    if contains_any(horizon_lower, ["short", "weeks", "few months", "6 months", "less than"]):
        return RiskDimensionScore(
            dimension="time_horizon",
            score=1,
            rationale="The user has a short time horizon, which limits ability to absorb volatility.",
        )

    if contains_any(horizon_lower, ["long", "long term", "long-term", "more than 3", "5 years", "10 years"]):
        return RiskDimensionScore(
            dimension="time_horizon",
            score=2,
            rationale="The user described a longer-term outlook, but this is treated as capacity for patience rather than automatic high-risk appetite.",
        )

    if contains_any(horizon_lower, ["1 year", "2 years", "3 years", "medium"]):
        return RiskDimensionScore(
            dimension="time_horizon",
            score=2,
            rationale="The user has a medium-term outlook, supporting moderate risk capacity.",
        )

    return RiskDimensionScore(
        dimension="time_horizon",
        score=2,
        rationale="The user’s time horizon suggests a moderate investment outlook.",
    )


def score_risk_attitude(risk_attitude: str | None) -> RiskDimensionScore:
    if not risk_attitude:
        return RiskDimensionScore(
            dimension="risk_attitude",
            score=0,
            rationale="No risk-attitude response was collected.",
        )

    attitude_lower = risk_attitude.lower()

    cautious_terms = [
        "worried",
        "panic",
        "sell",
        "avoid loss",
        "hate losing",
        "not comfortable",
        "low risk",
        "safe",
        "dont want to lose",
        "don't want to lose",
        "do not want to lose",
        "lose much",
        "not lose much",
        "preserve money",
        "protect my money",
    ]

    aggressive_terms = [
        "comfortable",
        "buy more",
        "opportunity",
        "high risk",
        "higher risk",
        "risky",
        "riskier",
        "can lose",
        "accept losses",
        "volatile",
        "aggressive",
    ]

    moderate_terms = [
        "wait",
        "hold",
        "monitor",
        "some risk",
        "balanced",
        "depends",
    ]

    if contains_any(attitude_lower, cautious_terms):
        return RiskDimensionScore(
            dimension="risk_attitude",
            score=1,
            rationale="The user explicitly indicates discomfort with losses, suggesting a conservative risk attitude.",
        )

    if contains_any(attitude_lower, aggressive_terms):
        return RiskDimensionScore(
            dimension="risk_attitude",
            score=3,
            rationale="The user’s response suggests comfort with volatility and potential losses, indicating stronger risk tolerance.",
        )

    if contains_any(attitude_lower, moderate_terms):
        return RiskDimensionScore(
            dimension="risk_attitude",
            score=2,
            rationale="The user appears able to tolerate some volatility without immediately exiting.",
        )

    return RiskDimensionScore(
        dimension="risk_attitude",
        score=2,
        rationale="The user’s risk response suggests moderate tolerance, but does not clearly indicate extreme caution or high-risk appetite.",
    )


def apply_safety_override(
    collected_fields: dict[str, str | None],
    profile: str,
    total_score: int,
) -> tuple[str, int]:
    combined_text = " ".join(
        value.lower() for value in collected_fields.values() if value
    )

    strong_caution_terms = [
        "low risk",
        "lower risk",
        "safe",
        "safely",
        "conservative",
        "dont want to lose",
        "don't want to lose",
        "do not want to lose",
        "lose much",
        "not lose much",
        "protect my money",
        "preserve money",
    ]

    strong_high_risk_terms = [
        "high risk",
        "higher risk",
        "risky",
        "riskier",
        "aggressive",
        "high return",
        "higher return",
        "speculative",
        "volatile",
    ]

    if contains_any(combined_text, strong_caution_terms):
        if profile == "Aggressive":
            return "Moderate", min(total_score, 10)
        if total_score <= 9:
            return "Conservative", min(total_score, 7)

    if contains_any(combined_text, strong_high_risk_terms):
        if total_score >= 10:
            return "Aggressive", max(total_score, 11)

    return profile, total_score


def generate_risk_profile(collected_fields: dict[str, str | None]) -> RiskProfileResult:
    dimension_scores = [
        score_goal(collected_fields.get("goal")),
        score_experience(collected_fields.get("experience_level")),
        score_budget(collected_fields.get("budget")),
        score_time_horizon(collected_fields.get("time_horizon")),
        score_risk_attitude(collected_fields.get("risk_attitude")),
    ]

    raw_total_score = sum(item.score for item in dimension_scores)
    raw_profile = determine_risk_label(raw_total_score)

    profile, total_score = apply_safety_override(
        collected_fields=collected_fields,
        profile=raw_profile,
        total_score=raw_total_score,
    )

    summary = build_risk_summary(
        profile,
        [item.rationale for item in dimension_scores],
    )

    return RiskProfileResult(
        profile=profile,
        total_score=total_score,
        dimension_scores=dimension_scores,
        summary=summary,
    )