from app.services.risk_profile_service import generate_risk_profile


def test_generate_risk_profile_returns_summary_and_dimensions() -> None:
    collected_fields = {
        "goal": "I want to learn safely.",
        "experience_level": "I am a beginner.",
        "budget": "Around 100 pounds.",
        "time_horizon": "Short term.",
        "risk_attitude": "I would panic and sell.",
    }

    result = generate_risk_profile(collected_fields)

    assert result.profile == "Conservative"
    assert result.total_score >= 0
    assert len(result.dimension_scores) == 5
    assert result.summary != ""