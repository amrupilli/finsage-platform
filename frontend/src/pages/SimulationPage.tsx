import { useEffect, useState } from "react";
import PageSection from "../components/PageSection";
import {
  authenticatedApiRequest,
  getPortfolioScenario,
  getPortfolioSimulation,
} from "../lib/api";
import { getOnboardingSessionId } from "../lib/onboardingSession";
import type { PortfolioSimulationResponse } from "../types/simulation";
import type { RiskProfileResponse } from "../types/riskProfile";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend,
} from "recharts";

export default function SimulationPage() {
  const [simulation, setSimulation] =
    useState<PortfolioSimulationResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadSimulation() {
      setIsLoading(true);
      setError("");

      const sessionId = getOnboardingSessionId();

      if (!sessionId) {
        setError("No onboarding session found. Complete onboarding first.");
        setIsLoading(false);
        return;
      }

      try {
        await authenticatedApiRequest<RiskProfileResponse>(
          `/onboarding/${sessionId}/risk-profile`,
          { method: "GET" }
        );

        await getPortfolioScenario(sessionId);

        const response = await getPortfolioSimulation(sessionId);
        setSimulation(response);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to load simulation."
        );
      } finally {
        setIsLoading(false);
      }
    }

    loadSimulation();
  }, []);

  if (isLoading) {
    return (
      <PageSection
        title="Monte Carlo Simulation"
        description="Loading educational simulation outputs..."
      >
        <p style={styles.mutedText}>Loading Monte Carlo simulation...</p>
      </PageSection>
    );
  }

  if (error) {
    return (
      <PageSection
        title="Monte Carlo Simulation"
        description="There was a problem loading the simulation."
      >
        <div style={styles.errorBox}>
          <p style={styles.errorText}>{error}</p>
        </div>
      </PageSection>
    );
  }

  if (!simulation) {
    return null;
  }

  const worstCase = simulation.metrics.percentiles.p10;
  const averageCase = simulation.metrics.percentiles.p50;
  const bestCase = simulation.metrics.percentiles.p90;
  const expectedValue = simulation.metrics.expected_final_value;
  const probabilityOfLoss = simulation.metrics.probability_of_loss * 100;
  const volatility = simulation.metrics.estimated_volatility * 100;
  const drawdown = simulation.metrics.max_drawdown * 100;

  return (
    <PageSection
      title="Monte Carlo Simulation"
      description="Explore possible educational portfolio outcomes under uncertainty. These results are estimates for learning purposes only and are not financial advice."
    >
      <div style={styles.wrapper}>
        <section style={styles.heroCard}>
          <div>
            <p style={styles.label}>Simulation overview</p>
            <h2 style={styles.heroTitle}>
              {simulation.num_simulations} simulated outcomes over{" "}
              {simulation.time_horizon_months} months
            </h2>
            <p style={styles.heroText}>
              FinSage uses Monte Carlo simulation to model a range of possible
              outcomes for your educational portfolio scenario. Instead of
              showing one fixed result, it shows how the portfolio may perform
              under weaker, average, and stronger market conditions.
            </p>
          </div>

          <div style={styles.heroMetric}>
            <p style={styles.metricLabel}>Starting amount</p>
            <p style={styles.heroMetricValue}>
              £{simulation.initial_budget.toFixed(2)}
            </p>
          </div>
        </section>

        <section style={styles.caseGrid}>
          <div style={styles.caseCard}>
            <p style={styles.caseLabel}>Worst case</p>
            <h3 style={styles.caseValue}>£{worstCase.toFixed(2)}</h3>
            <p style={styles.caseText}>
              This represents a weaker outcome where returns are poor or market
              conditions move against the portfolio. It helps show downside
              risk.
            </p>
          </div>

          <div style={styles.caseCardHighlight}>
            <p style={styles.caseLabel}>Average case</p>
            <h3 style={styles.caseValue}>£{averageCase.toFixed(2)}</h3>
            <p style={styles.caseText}>
              This is the middle outcome from the simulation range. It is useful
              for understanding a typical projected scenario, not a guaranteed
              result.
            </p>
          </div>

          <div style={styles.caseCard}>
            <p style={styles.caseLabel}>Best case</p>
            <h3 style={styles.caseValue}>£{bestCase.toFixed(2)}</h3>
            <p style={styles.caseText}>
              This shows a stronger outcome where simulated conditions are more
              favourable. It should be viewed as possible upside, not a promise.
            </p>
          </div>
        </section>

        <section style={styles.card}>
          <p style={styles.label}>Projected value graph</p>
          <h2 style={styles.title}>Best, average, and worst outcome paths</h2>
          <p style={styles.summary}>
            The graph compares the downside path, median path, and upside path.
            A wider gap between the lines means greater uncertainty.
          </p>

          <div style={styles.chartBox}>
            <ResponsiveContainer width="100%" height={340}>
              <LineChart data={simulation.percentile_band}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="rgba(255,255,255,0.08)"
                />
                <XAxis dataKey="step" stroke="#8fa1c7" />
                <YAxis
                  stroke="#8fa1c7"
                  tickFormatter={(value) => `£${Math.round(Number(value))}`}
                />
                <Tooltip
                  formatter={(value) => `£${Number(value).toFixed(2)}`}
                  labelFormatter={(label) => `Month ${label}`}
                  contentStyle={{
                    background: "#121a30",
                    border: "1px solid rgba(255,255,255,0.12)",
                    borderRadius: "12px",
                    color: "#ffffff",
                  }}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="p10"
                  name="Worst case"
                  stroke="#ff8e8e"
                  strokeWidth={3}
                  dot={false}
                />
                <Line
                  type="monotone"
                  dataKey="p50"
                  name="Average case"
                  stroke="#6c8cff"
                  strokeWidth={3}
                  dot={false}
                />
                <Line
                  type="monotone"
                  dataKey="p90"
                  name="Best case"
                  stroke="#9fffd9"
                  strokeWidth={3}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section style={styles.metricGrid}>
          <div style={styles.metricBox}>
            <p style={styles.metricLabel}>Expected final value</p>
            <p style={styles.metricValue}>£{expectedValue.toFixed(2)}</p>
            <p style={styles.metricHint}>
              Average projected final value across simulations.
            </p>
          </div>

          <div style={styles.metricBox}>
            <p style={styles.metricLabel}>Probability of loss</p>
            <p style={styles.metricValue}>{probabilityOfLoss.toFixed(1)}%</p>
            <p style={styles.metricHint}>
              Estimated chance of ending below the starting amount.
            </p>
          </div>

          <div style={styles.metricBox}>
            <p style={styles.metricLabel}>Volatility</p>
            <p style={styles.metricValue}>{volatility.toFixed(1)}%</p>
            <p style={styles.metricHint}>
              Indicates how unstable the simulated outcomes are.
            </p>
          </div>

          <div style={styles.metricBox}>
            <p style={styles.metricLabel}>Max drawdown</p>
            <p style={styles.metricValue}>{drawdown.toFixed(1)}%</p>
            <p style={styles.metricHint}>
              Shows the largest simulated fall from a previous high.
            </p>
          </div>
        </section>

        <section style={styles.explanationCard}>
          <p style={styles.label}>How to read this</p>
          <h2 style={styles.title}>What the results mean</h2>
          <p style={styles.summary}>
            The simulation does not predict the future. It helps users
            understand uncertainty. If the worst-case value is much lower than
            the starting amount, the portfolio carries meaningful downside risk.
            If the best-case and worst-case values are far apart, the outcome is
            more volatile. This supports FinSage’s educational aim by showing
            that investment decisions involve a range of possible outcomes, not
            one guaranteed return.
          </p>
        </section>
      </div>
    </PageSection>
  );
}

const styles: Record<string, React.CSSProperties> = {
  wrapper: {
    display: "flex",
    flexDirection: "column",
    gap: "24px",
  },
  heroCard: {
    display: "grid",
    gridTemplateColumns: "2fr 1fr",
    gap: "24px",
    background:
      "linear-gradient(135deg, rgba(108,140,255,0.22), rgba(18,26,48,1))",
    border: "1px solid rgba(108,140,255,0.25)",
    borderRadius: "28px",
    padding: "28px",
    boxShadow: "0 24px 70px rgba(0,0,0,0.28)",
  },
  label: {
    margin: 0,
    color: "#8fa1c7",
    fontSize: "0.85rem",
    fontWeight: 800,
    textTransform: "uppercase",
    letterSpacing: "0.5px",
  },
  heroTitle: {
    margin: "10px 0 0 0",
    fontSize: "2rem",
    lineHeight: 1.2,
  },
  heroText: {
    margin: "16px 0 0 0",
    color: "#dbe4ff",
    lineHeight: 1.8,
    maxWidth: "900px",
  },
  heroMetric: {
    background: "rgba(11,16,32,0.65)",
    border: "1px solid rgba(255,255,255,0.1)",
    borderRadius: "22px",
    padding: "22px",
    alignSelf: "stretch",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
  },
  heroMetricValue: {
    margin: "8px 0 0 0",
    fontSize: "2rem",
    fontWeight: 900,
  },
  caseGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
    gap: "18px",
  },
  caseCard: {
    background: "#121a30",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "24px",
    padding: "22px",
  },
  caseCardHighlight: {
    background: "rgba(108, 140, 255, 0.18)",
    border: "1px solid rgba(108, 140, 255, 0.35)",
    borderRadius: "24px",
    padding: "22px",
  },
  caseLabel: {
    margin: 0,
    color: "#8fa1c7",
    fontWeight: 800,
    textTransform: "uppercase",
    fontSize: "0.8rem",
  },
  caseValue: {
    margin: "10px 0 0 0",
    fontSize: "1.9rem",
  },
  caseText: {
    margin: "12px 0 0 0",
    color: "#c7d2e6",
    lineHeight: 1.7,
  },
  card: {
    background: "#121a30",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "24px",
    padding: "24px",
    boxShadow: "0 20px 60px rgba(0,0,0,0.25)",
  },
  title: {
    margin: "8px 0 0 0",
    fontSize: "1.5rem",
  },
  summary: {
    margin: "14px 0 0 0",
    color: "#e5ecff",
    lineHeight: 1.8,
  },
  chartBox: {
    marginTop: "22px",
    width: "100%",
    height: "370px",
    background: "#0b1020",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "20px",
    padding: "18px",
    boxSizing: "border-box",
  },
  metricGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
    gap: "16px",
  },
  metricBox: {
    background: "#121a30",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "20px",
    padding: "18px",
  },
  metricLabel: {
    margin: 0,
    color: "#8fa1c7",
    fontWeight: 800,
  },
  metricValue: {
    margin: "8px 0 0 0",
    color: "#ffffff",
    fontSize: "1.6rem",
    fontWeight: 900,
  },
  metricHint: {
    margin: "8px 0 0 0",
    color: "#c7d2e6",
    lineHeight: 1.6,
    fontSize: "0.95rem",
  },
  explanationCard: {
    background: "rgba(47, 190, 150, 0.1)",
    border: "1px solid rgba(47, 190, 150, 0.25)",
    borderRadius: "24px",
    padding: "24px",
  },
  mutedText: {
    margin: 0,
    color: "#8fa1c7",
  },
  errorBox: {
    background: "rgba(255, 107, 107, 0.08)",
    border: "1px solid rgba(255, 107, 107, 0.2)",
    borderRadius: "16px",
    padding: "16px",
  },
  errorText: {
    margin: 0,
    color: "#ff8e8e",
  },
};