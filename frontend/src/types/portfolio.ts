export type PortfolioAllocation = {
  category: string;
  percentage: number;
  amount: number;
  rationale: string;
};

export type PortfolioScenarioResponse = {
  portfolio_type: string;
  total_budget: number;
  allocations: PortfolioAllocation[];
  summary: string;
};