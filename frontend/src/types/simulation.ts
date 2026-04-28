export type SimulationPercentiles = {
  p10: number;
  p50: number;
  p90: number;
};

export type SimulationMetrics = {
  expected_final_value: number;
  probability_of_loss: number;
  estimated_volatility: number;
  max_drawdown: number;
  percentiles: SimulationPercentiles;
};

export type SimulationPathPoint = {
  step: number;
  portfolio_value: number;
};

export type SimulationBandPoint = {
  step: number;
  p10: number;
  p50: number;
  p90: number;
};

export type PortfolioSimulationResponse = {
  initial_budget: number;
  num_simulations: number;
  time_horizon_months: number;
  metrics: SimulationMetrics;
  sample_path: SimulationPathPoint[];
  percentile_band: SimulationBandPoint[];
  summary: string;
};