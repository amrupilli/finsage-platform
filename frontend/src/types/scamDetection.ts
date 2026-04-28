export type ScamLabel = "safe" | "suspicious" | "scam";

export type ScamRiskLevel = "low" | "medium" | "high";

export type SignalSeverity = "low" | "medium" | "high";

export type WarningCategory =
  | "scam_risk"
  | "portfolio_risk"
  | "simulation_risk"
  | "educational_guidance";

export interface WarningSignal {
  signal_type: string;
  matched_text: string;
  severity: SignalSeverity;
  explanation: string;
}

export interface InvestmentChecklistItem {
  check: string;
  reason: string;
}

export interface WarningSummary {
  category: WarningCategory;
  severity: SignalSeverity;
  title: string;
  message: string;
  recommended_action: string;
}

export interface ScamPredictionResponse {
  input_text: string;
  predicted_label: ScamLabel;
  scam_probability: number;
  risk_level: ScamRiskLevel;
  warning_signals: WarningSignal[];
  investment_checklist: InvestmentChecklistItem[];
  explanation: string;
  educational_message: string;
  warning_summary: WarningSummary | null;
}