from app.models.onboarding import OnboardingAnswer, OnboardingSession


def test_onboarding_session_tablename() -> None:
    assert OnboardingSession.__tablename__ == "onboarding_sessions"


def test_onboarding_answer_tablename() -> None:
    assert OnboardingAnswer.__tablename__ == "onboarding_answers"