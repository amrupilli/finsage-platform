export type RiskLevel = "Conservative" | "Moderate" | "Aggressive";

export type RiskDimensionScore = {
  dimension: string;
  score: number;
  rationale: string;
};

export type RiskProfileResponse = {
  profile: RiskLevel;
  total_score: number;
  dimension_scores: RiskDimensionScore[];
  summary: string;
};