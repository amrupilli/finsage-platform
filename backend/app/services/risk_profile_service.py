from app.schemas.risk_profile import RiskDimensionScore, RiskProfileResult
from app.services.risk_profile_structure import build_risk_summary, determine_risk_label


def score_goal(goal: str | None) -> RiskDimensionScore:
    if not goal:
        return RiskDimensionScore(
            dimension="goal",
            score=0,
            rationale="No clear investment goal was collected.",
        )

    goal_lower = goal.lower()

    if "learn" in goal_lower or "understand" in goal_lower or "safe" in goal_lower:
        return RiskDimensionScore(
            dimension="goal",
            score=1,
            rationale="The user appears learning-focused and cautious in their goals.",
        )

    if "grow" in goal_lower or "money" in goal_lower:
        return RiskDimensionScore(
            dimension="goal",
            score=2,
            rationale="The user appears interested in financial growth, suggesting moderate risk interest.",
        )

    if "experiment" in goal_lower or "high return" in goal_lower or "aggressive" in goal_lower:
        return RiskDimensionScore(
            dimension="goal",
            score=3,
            rationale="The user’s goal suggests a higher tolerance for experimentation or upside seeking.",
        )

    return RiskDimensionScore(
        dimension="goal",
        score=1,
        rationale="The user’s goal suggests a generally cautious or exploratory mindset.",
    )


def score_experience(experience: str | None) -> RiskDimensionScore:
    if not experience:
        return RiskDimensionScore(
            dimension="experience_level",
            score=0,
            rationale="No experience level was collected.",
        )

    experience_lower = experience.lower()

    if "beginner" in experience_lower or "new" in experience_lower or "no experience" in experience_lower:
        return RiskDimensionScore(
            dimension="experience_level",
            score=1,
            rationale="The user described themselves as a beginner or inexperienced investor.",
        )

    if "some" in experience_lower or "little" in experience_lower:
        return RiskDimensionScore(
            dimension="experience_level",
            score=2,
            rationale="The user appears to have limited but developing investment experience.",
        )

    if "comfortable" in experience_lower or "experienced" in experience_lower:
        return RiskDimensionScore(
            dimension="experience_level",
            score=3,
            rationale="The user appears more comfortable with investing concepts and risk exposure.",
        )

    return RiskDimensionScore(
        dimension="experience_level",
        score=1,
        rationale="The user’s experience description suggests a cautious experience level.",
    )


def score_budget(budget: str | None) -> RiskDimensionScore:
    if not budget:
        return RiskDimensionScore(
            dimension="budget",
            score=0,
            rationale="No budget information was collected.",
        )

    budget_lower = budget.lower()

    if "small" in budget_lower or "low" in budget_lower or "100" in budget_lower:
        return RiskDimensionScore(
            dimension="budget",
            score=1,
            rationale="The user described a relatively limited investment scenario budget.",
        )

    if "200" in budget_lower or "500" in budget_lower or "moderate" in budget_lower:
        return RiskDimensionScore(
            dimension="budget",
            score=2,
            rationale="The user appears comfortable modelling a moderate investment amount.",
        )

    if "1000" in budget_lower or "large" in budget_lower or "more" in budget_lower:
        return RiskDimensionScore(
            dimension="budget",
            score=3,
            rationale="The user appears comfortable discussing a relatively larger investment scenario.",
        )

    return RiskDimensionScore(
        dimension="budget",
        score=1,
        rationale="The user’s budget description suggests a cautious financial comfort level.",
    )


def score_time_horizon(time_horizon: str | None) -> RiskDimensionScore:
    if not time_horizon:
        return RiskDimensionScore(
            dimension="time_horizon",
            score=0,
            rationale="No time horizon was collected.",
        )

    horizon_lower = time_horizon.lower()

    if "short" in horizon_lower or "less than" in horizon_lower or "6 months" in horizon_lower:
        return RiskDimensionScore(
            dimension="time_horizon",
            score=1,
            rationale="The user described a shorter investment time horizon.",
        )

    if "1 year" in horizon_lower or "medium" in horizon_lower or "1 to 3 years" in horizon_lower:
        return RiskDimensionScore(
            dimension="time_horizon",
            score=2,
            rationale="The user described a medium-term investment outlook.",
        )

    if "long" in horizon_lower or "more than 3 years" in horizon_lower:
        return RiskDimensionScore(
            dimension="time_horizon",
            score=3,
            rationale="The user described a longer-term investment outlook, which can support greater risk capacity.",
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

    if "sell" in attitude_lower or "panic" in attitude_lower or "worried" in attitude_lower:
        return RiskDimensionScore(
            dimension="risk_attitude",
            score=1,
            rationale="The user’s response suggests discomfort with sharp portfolio losses.",
        )

    if "wait" in attitude_lower or "monitor" in attitude_lower or "hold" in attitude_lower:
        return RiskDimensionScore(
            dimension="risk_attitude",
            score=2,
            rationale="The user appears able to tolerate some volatility without immediate exit.",
        )

    if "buy" in attitude_lower or "opportunity" in attitude_lower or "comfortable" in attitude_lower:
        return RiskDimensionScore(
            dimension="risk_attitude",
            score=3,
            rationale="The user’s reaction suggests a stronger tolerance for volatility and downside movement.",
        )

    return RiskDimensionScore(
        dimension="risk_attitude",
        score=1,
        rationale="The user’s answer suggests a relatively cautious attitude toward losses.",
    )


def generate_risk_profile(collected_fields: dict[str, str | None]) -> RiskProfileResult:
    dimension_scores = [
        score_goal(collected_fields.get("goal")),
        score_experience(collected_fields.get("experience_level")),
        score_budget(collected_fields.get("budget")),
        score_time_horizon(collected_fields.get("time_horizon")),
        score_risk_attitude(collected_fields.get("risk_attitude")),
    ]

    total_score = sum(item.score for item in dimension_scores)
    profile = determine_risk_label(total_score)
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