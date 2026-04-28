export type ConversationStage =
  | "intro"
  | "goal"
  | "experience"
  | "budget"
  | "time_horizon"
  | "risk_attitude"
  | "complete";

export type OnboardingStartResponse = {
  session_id: number;
  assistant_message: string;
  current_stage: ConversationStage;
  missing_fields: string[];
  is_completed: boolean;
};

export type OnboardingMessageResponse = {
  session_id: number;
  assistant_message: string;
  current_stage: ConversationStage;
  missing_fields: string[];
  is_completed: boolean;
};

export type ChatMessage = {
  id: string;
  sender: "assistant" | "user";
  text: string;
};

export type OnboardingCompletionState = "in_progress" | "complete";