const ONBOARDING_SESSION_ID_KEY = "finsage_onboarding_session_id";

export function saveOnboardingSessionId(sessionId: number): void {
  localStorage.setItem(ONBOARDING_SESSION_ID_KEY, String(sessionId));
}

export function getOnboardingSessionId(): number | null {
  const rawValue = localStorage.getItem(ONBOARDING_SESSION_ID_KEY);

  if (!rawValue) {
    return null;
  }

  const parsedValue = Number(rawValue);

  if (Number.isNaN(parsedValue)) {
    return null;
  }

  return parsedValue;
}

export function clearOnboardingSessionId(): void {
  localStorage.removeItem(ONBOARDING_SESSION_ID_KEY);
}