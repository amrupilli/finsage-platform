from app.services.risk_profile_service import generate_risk_profile


def test_generate_conservative_risk_profile() -> None:
    collected_fields = {
        "goal": "I want to learn safely before risking money.",
        "experience_level": "I am a complete beginner.",
        "budget": "Probably around 100 pounds.",
        "time_horizon": "Short term, maybe a few months.",
        "risk_attitude": "I would probably panic and sell.",
    }

    result = generate_risk_profile(collected_fields)

    assert result.profile == "Conservative"
    assert result.total_score <= 6
    assert len(result.dimension_scores) == 5
    assert "Conservative" in result.summary


def test_generate_moderate_risk_profile() -> None:
    collected_fields = {
        "goal": "I want to grow money over time and understand risk better.",
        "experience_level": "I have some investing knowledge.",
        "budget": "Maybe around 500 pounds.",
        "time_horizon": "1 to 3 years.",
        "risk_attitude": "I would hold and monitor it.",
    }

    result = generate_risk_profile(collected_fields)

    assert result.profile == "Moderate"
    assert 7 <= result.total_score <= 10
    assert len(result.dimension_scores) == 5
    assert "Moderate" in result.summary


def test_generate_aggressive_risk_profile() -> None:
    collected_fields = {
        "goal": "I want to experiment aggressively for high returns.",
        "experience_level": "I am comfortable with investing concepts.",
        "budget": "I could model 1000 pounds or more.",
        "time_horizon": "More than 3 years.",
        "risk_attitude": "I would see a drop as a buying opportunity.",
    }

    result = generate_risk_profile(collected_fields)

    assert result.profile == "Aggressive"
    assert result.total_score >= 11
    assert len(result.dimension_scores) == 5
    assert "Aggressive" in result.summary