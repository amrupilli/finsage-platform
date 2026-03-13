from app.services.onboarding_prompts import ONBOARDING_PROMPTS


def test_onboarding_prompts_include_expected_stages() -> None:
    assert "intro" in ONBOARDING_PROMPTS
    assert "goal" in ONBOARDING_PROMPTS
    assert "experience" in ONBOARDING_PROMPTS
    assert "budget" in ONBOARDING_PROMPTS
    assert "time_horizon" in ONBOARDING_PROMPTS
    assert "risk_attitude" in ONBOARDING_PROMPTS
    assert "complete" in ONBOARDING_PROMPTS
