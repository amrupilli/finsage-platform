import { getAccessToken } from "./auth";
import type { PortfolioScenarioResponse } from "../types/portfolio";
import type { PortfolioSimulationResponse } from "../types/simulation";
import type { ScamPredictionResponse } from "../types/scamDetection";
export const API_BASE_URL = "http://127.0.0.1:8000";

export async function apiRequest<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const mergedHeaders = {
    "Content-Type": "application/json",
    ...(options?.headers ?? {}),
  };

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: mergedHeaders,
  });

  if (!response.ok) {
    let errorMessage = "Something went wrong.";

    try {
      const errorData = await response.json();

      if (typeof errorData?.detail === "string") {
        errorMessage = errorData.detail;
      } else if (Array.isArray(errorData?.detail)) {
        errorMessage = errorData.detail
          .map((item: any) => item.msg || JSON.stringify(item))
          .join(", ");
      } else if (errorData?.detail) {
        errorMessage = JSON.stringify(errorData.detail);
      }
    } catch {
      // keep default message
    }

    throw new Error(errorMessage);
  }

  return response.json() as Promise<T>;
}

export async function authenticatedApiRequest<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const token = getAccessToken();

  if (!token) {
    throw new Error("No access token found. Please log in again.");
  }

  return apiRequest<T>(path, {
    ...options,
    headers: {
      ...(options?.headers ?? {}),
      Authorization: `Bearer ${token}`,
    },
  });
}

export type OnboardingAnswer = {
  answer_id: number;
  question_key: string;
  field_name: string | null;
  answer_text: string;
  created_at: string;
};

export type OnboardingAnswersReviewResponse = {
  session_id: number;
  is_completed: boolean;
  current_stage: string;
  missing_fields: string[];
  collected_fields: Record<string, string | null>;
  answers: OnboardingAnswer[];
};

export type OnboardingAnswerUpdateResponse = {
  session_id: number;
  answer: OnboardingAnswer;
  current_stage: string;
  missing_fields: string[];
  collected_fields: Record<string, string | null>;
  is_completed: boolean;
  message: string;
};

export async function getOnboardingAnswers(
  sessionId: number
): Promise<OnboardingAnswersReviewResponse> {
  return authenticatedApiRequest<OnboardingAnswersReviewResponse>(
    `/onboarding/${sessionId}/answers`,
    {
      method: "GET",
    }
  );
}

export async function updateOnboardingAnswer(
  sessionId: number,
  answerId: number,
  answerText: string
): Promise<OnboardingAnswerUpdateResponse> {
  return authenticatedApiRequest<OnboardingAnswerUpdateResponse>(
    `/onboarding/${sessionId}/answers/${answerId}`,
    {
      method: "PATCH",
      body: JSON.stringify({
        answer_text: answerText,
      }),
    }
  );
}

export async function regenerateOnboardingOutputs(
  sessionId: number
): Promise<any> {
  return authenticatedApiRequest<any>(
    `/onboarding/${sessionId}/regenerate`,
    {
      method: "POST",
    }
  );
}

export async function getPortfolioScenario(
  sessionId: number
): Promise<PortfolioScenarioResponse> {
  return authenticatedApiRequest<PortfolioScenarioResponse>(
    `/onboarding/${sessionId}/portfolio-scenario`,
    {
      method: "GET",
    }
  );
}

export async function getPortfolioSimulation(
  sessionId: number
): Promise<PortfolioSimulationResponse> {
  return authenticatedApiRequest<PortfolioSimulationResponse>(
    `/onboarding/${sessionId}/simulation`,
    {
      method: "GET",
    }
  );
}

export type LatestCompletedOnboardingResponse = {
  session_id: number;
  is_completed: boolean;
};

export async function getLatestCompletedOnboardingSession(): Promise<LatestCompletedOnboardingResponse> {
  return authenticatedApiRequest<LatestCompletedOnboardingResponse>(
    "/onboarding/latest-completed",
    {
      method: "GET",
    }
  );
}

export type InvestmentChecklistItem = {
  title: string;
  status: string;
  explanation: string;
};

export type InvestmentCheckResponse = {
  input_text: string;
  risk_level: string;
  summary: string;
  checklist: InvestmentChecklistItem[];
  educational_message: string;
};

export async function runInvestmentCheck(
  inputText: string
): Promise<InvestmentCheckResponse> {
  return authenticatedApiRequest<InvestmentCheckResponse>(
    "/warnings/investment-check",
    {
      method: "POST",
      body: JSON.stringify({
        input_text: inputText,
      }),
    }
  );
}

export type UserWarning = {
  category: "scam_risk" | "portfolio_risk" | "simulation_risk" | "educational_guidance";
  severity: "low" | "medium" | "high";
  title: string;
  message: string;
  recommended_action: string;
};

export type FullFlowResponse = {
  risk_profile: unknown;
  portfolio: unknown;
  simulation: unknown;
  warnings: UserWarning[];
};

export async function getFullFinancialFlow(
  sessionId: number
): Promise<FullFlowResponse> {
  return authenticatedApiRequest<FullFlowResponse>(`/flow/${sessionId}`, {
    method: "GET",
  });
}
export async function runScamDetection(
  inputText: string
): Promise<ScamPredictionResponse> {
  return authenticatedApiRequest<ScamPredictionResponse>(
    "/warnings/scam-check",
    {
      method: "POST",
      body: JSON.stringify({
        text: inputText,
      }),
    }
  );
}

export async function downloadSessionReport(sessionId: number): Promise<Blob> {
  const token = getAccessToken();

  if (!token) {
    throw new Error("No access token found. Please log in again.");
  }

  const response = await fetch(
    `${API_BASE_URL}/reports/${sessionId}/download`,
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    let errorMessage = "Failed to download report.";

    try {
      const errorData = await response.json();

      if (typeof errorData?.detail === "string") {
        errorMessage = errorData.detail;
      } else if (errorData?.detail) {
        errorMessage = JSON.stringify(errorData.detail);
      }
    } catch {
      // Keep default error message if backend does not return JSON
    }

    throw new Error(errorMessage);
  }

  return response.blob();
}