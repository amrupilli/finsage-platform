import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  authenticatedApiRequest,
  getLatestCompletedOnboardingSession,
  getPortfolioScenario,
  getPortfolioSimulation,
} from "../lib/api";
import {
  getOnboardingSessionId,
  saveOnboardingSessionId,
} from "../lib/onboardingSession";
import type { RiskProfileResponse } from "../types/riskProfile";
import type { PortfolioScenarioResponse } from "../types/portfolio";
import type { PortfolioSimulationResponse } from "../types/simulation";
import ReportDownloadButton from "../components/ReportDownloadButton";

export default function DashboardPage() {
  const navigate = useNavigate();

  const [riskProfile, setRiskProfile] = useState<RiskProfileResponse | null>(
    null
  );
  const [portfolio, setPortfolio] = useState<PortfolioScenarioResponse | null>(
    null
  );
  const [simulation, setSimulation] =
    useState<PortfolioSimulationResponse | null>(null);

  const [isLoading, setIsLoading] = useState(true);
  const [dashboardError, setDashboardError] = useState("");

  useEffect(() => {
    async function fetchDashboardData() {
      setIsLoading(true);
      setDashboardError("");

      let sessionId = getOnboardingSessionId();

      if (!sessionId) {
        try {
          const latestSession = await getLatestCompletedOnboardingSession();
          sessionId = latestSession.session_id;
          saveOnboardingSessionId(sessionId);
        } catch {
          setDashboardError(
            "No completed onboarding was found. Please complete onboarding first."
          );
          setIsLoading(false);
          return;
        }
      }

      try {
        const riskResponse = await authenticatedApiRequest<RiskProfileResponse>(
          `/onboarding/${sessionId}/risk-profile`,
          { method: "GET" }
        );

        const portfolioResponse = await getPortfolioScenario(sessionId);
        const simulationResponse = await getPortfolioSimulation(sessionId);

        setRiskProfile(riskResponse);
        setPortfolio(portfolioResponse);
        setSimulation(simulationResponse);
      } catch (error) {
        localStorage.removeItem("finsage_onboarding_session_id");

        if (error instanceof Error) {
          setDashboardError(
            `${error.message} Please complete onboarding again.`
          );
        } else {
          setDashboardError(
            "Failed to load dashboard. Please complete onboarding again."
          );
        }
      } finally {
        setIsLoading(false);
      }
    }

    fetchDashboardData();
  }, []);

  const expectedFinalValue =
    simulation?.metrics.expected_final_value.toFixed(2) ?? "0.00";

  const probabilityOfLoss = simulation
    ? (simulation.metrics.probability_of_loss * 100).toFixed(1)
    : "0.0";

  return (
    <div style={styles.page}>
      <section style={styles.hero}>
        <div>
          <p style={styles.label}>Dashboard</p>
          <h1 style={styles.heroTitle}>Your FinSage overview</h1>
          <p style={styles.heroText}>
            A personalised educational summary of your risk profile, portfolio
            scenario, Monte Carlo outcomes, and warning insights.
          </p>

          <div style={styles.buttonRow}>
            <button
              type="button"
              onClick={() => navigate("/onboarding/review")}
              style={styles.primaryButton}
            >
              Review or edit answers
            </button>

            <button
              type="button"
              onClick={() => navigate("/portfolio")}
              style={styles.secondaryButton}
            >
              View portfolio
            </button>

            <button
              type="button"
              onClick={() => navigate("/simulation")}
              style={styles.secondaryButton}
            >
              View simulation
            </button>
            <button
  type="button"
  onClick={() => navigate("/investment-check")}
  style={styles.secondaryButton}
>
  Investment check
</button>
<button
  onClick={() => navigate("/scam-check")}
  style={styles.secondaryButton}
>
  Scam check
</button>
<ReportDownloadButton />
          </div>
        </div>

        <div style={styles.heroPanel}>
          <p style={styles.panelLabel}>Current profile</p>
          <h2 style={styles.profileLarge}>
            {riskProfile?.profile ?? "Loading..."}
          </h2>
          <p style={styles.panelText}>
            FinSage classifies this profile using your questionnaire answers,
            including goals, experience, budget, time horizon, and risk
            attitude.
          </p>
        </div>
      </section>

      {isLoading && (
        <section style={styles.card}>
          <p style={styles.mutedText}>Loading your dashboard...</p>
        </section>
      )}

      {!isLoading && dashboardError && (
        <section style={styles.errorBox}>
          <p style={styles.errorText}>{dashboardError}</p>
          <button
            type="button"
            onClick={() => navigate("/onboarding")}
            style={styles.primaryButton}
          >
            Go to onboarding
          </button>
        </section>
      )}

      {!isLoading && !dashboardError && riskProfile && (
        <>
          <section style={styles.quickGrid}>
            <div style={styles.statCard}>
              <p style={styles.statLabel}>Risk profile</p>
              <h2 style={styles.statValue}>{riskProfile.profile}</h2>
              <p style={styles.statHint}>Based on {riskProfile.dimension_scores.length} dimensions</p>
            </div>

            <div style={styles.statCard}>
              <p style={styles.statLabel}>Total score</p>
              <h2 style={styles.statValue}>{riskProfile.total_score}</h2>
              <p style={styles.statHint}>Higher score means higher tolerance</p>
            </div>

            <div style={styles.statCard}>
              <p style={styles.statLabel}>Portfolio type</p>
              <h2 style={styles.statValueSmall}>
                {portfolio?.portfolio_type ?? "Not generated"}
              </h2>
              <p style={styles.statHint}>Educational allocation scenario</p>
            </div>

            <div style={styles.statCard}>
              <p style={styles.statLabel}>Expected value</p>
              <h2 style={styles.statValue}>£{expectedFinalValue}</h2>
              <p style={styles.statHint}>Monte Carlo average outcome</p>
            </div>
          </section>

          <section style={styles.twoColumn}>
            <div style={styles.card}>
              <p style={styles.cardLabel}>Risk profile</p>
              <h2 style={styles.cardTitle}>Personalised risk summary</h2>

              <div style={styles.profileBadge}>{riskProfile.profile}</div>

              <p style={styles.summary}>{riskProfile.summary}</p>

              <div style={styles.dimensionList}>
                {riskProfile.dimension_scores.map((item) => (
                  <div key={item.dimension} style={styles.dimensionItem}>
                    <div>
                      <p style={styles.dimensionName}>
                        {item.dimension.replace("_", " ")}
                      </p>
                      <p style={styles.dimensionReason}>{item.rationale}</p>
                    </div>
                    <span style={styles.dimensionScore}>{item.score}/3</span>
                  </div>
                ))}
              </div>
            </div>

            <div style={styles.card}>
              <p style={styles.cardLabel}>Simulation snapshot</p>
              <h2 style={styles.cardTitle}>Outcome range</h2>

              <div style={styles.outcomeStack}>
                <div style={styles.outcomeBox}>
                  <p style={styles.statLabel}>Worst case</p>
                  <h3 style={styles.outcomeValue}>
                    £{simulation?.metrics.percentiles.p10.toFixed(2)}
                  </h3>
                </div>

                <div style={styles.outcomeBoxHighlight}>
                  <p style={styles.statLabel}>Average case</p>
                  <h3 style={styles.outcomeValue}>
                    £{simulation?.metrics.percentiles.p50.toFixed(2)}
                  </h3>
                </div>

                <div style={styles.outcomeBox}>
                  <p style={styles.statLabel}>Best case</p>
                  <h3 style={styles.outcomeValue}>
                    £{simulation?.metrics.percentiles.p90.toFixed(2)}
                  </h3>
                </div>
              </div>

              <p style={styles.summary}>
                Probability of loss: <strong>{probabilityOfLoss}%</strong>. This
                shows the chance of the simulated portfolio ending below the
                starting budget.
              </p>
            </div>
          </section>

          <section style={styles.card}>
            <div style={styles.cardHeader}>
              <div>
                <p style={styles.cardLabel}>Portfolio allocation</p>
                <h2 style={styles.cardTitle}>Educational scenario</h2>
              </div>

              <button
                type="button"
                onClick={() => navigate("/portfolio")}
                style={styles.secondaryButton}
              >
                Open full portfolio
              </button>
            </div>

            <p style={styles.summary}>{portfolio?.summary}</p>

            <div style={styles.allocationGrid}>
              {portfolio?.allocations.map((item) => (
                <div key={item.category} style={styles.allocationCard}>
                  <div style={styles.allocationTop}>
                    <h3 style={styles.allocationTitle}>{item.category}</h3>
                    <span style={styles.allocationPercent}>
                      {item.percentage}%
                    </span>
                  </div>

                  <div style={styles.barTrack}>
                    <div
                      style={{
                        ...styles.barFill,
                        width: `${item.percentage}%`,
                      }}
                    />
                  </div>

                  <p style={styles.allocationAmount}>
                    £{item.amount.toFixed(2)}
                  </p>
                  <p style={styles.allocationReason}>{item.rationale}</p>
                </div>
              ))}
            </div>
          </section>
        </>
      )}
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  page: {
    display: "flex",
    flexDirection: "column",
    gap: "24px",
  },
  hero: {
    display: "grid",
    gridTemplateColumns: "2fr 1fr",
    gap: "24px",
    background:
      "linear-gradient(135deg, rgba(108,140,255,0.22), rgba(18,26,48,0.95))",
    border: "1px solid rgba(108,140,255,0.22)",
    borderRadius: "30px",
    padding: "30px",
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
    fontSize: "2.4rem",
    lineHeight: 1.15,
  },
  heroText: {
    margin: "16px 0 0 0",
    color: "#dbe4ff",
    lineHeight: 1.8,
    maxWidth: "850px",
  },
  buttonRow: {
    display: "flex",
    flexWrap: "wrap",
    gap: "12px",
    marginTop: "22px",
  },
  primaryButton: {
    border: "1px solid rgba(108, 140, 255, 0.45)",
    borderRadius: "14px",
    background: "rgba(108, 140, 255, 0.22)",
    color: "#dbe4ff",
    fontWeight: 900,
    padding: "12px 16px",
    cursor: "pointer",
  },
  secondaryButton: {
    border: "1px solid rgba(255,255,255,0.12)",
    borderRadius: "14px",
    background: "#18213b",
    color: "#dbe4ff",
    fontWeight: 900,
    padding: "12px 16px",
    cursor: "pointer",
  },
  heroPanel: {
    background: "rgba(11,16,32,0.65)",
    border: "1px solid rgba(255,255,255,0.1)",
    borderRadius: "24px",
    padding: "22px",
  },
  panelLabel: {
    margin: 0,
    color: "#8fa1c7",
    fontWeight: 800,
    textTransform: "uppercase",
    fontSize: "0.8rem",
  },
  profileLarge: {
    margin: "10px 0 0 0",
    fontSize: "2rem",
  },
  panelText: {
    margin: "14px 0 0 0",
    color: "#c7d2e6",
    lineHeight: 1.7,
  },
  quickGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
    gap: "16px",
  },
  statCard: {
    background: "#121a30",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "22px",
    padding: "20px",
  },
  statLabel: {
    margin: 0,
    color: "#8fa1c7",
    fontWeight: 800,
    fontSize: "0.85rem",
  },
  statValue: {
    margin: "8px 0 0 0",
    fontSize: "1.9rem",
  },
  statValueSmall: {
    margin: "8px 0 0 0",
    fontSize: "1.25rem",
    lineHeight: 1.35,
  },
  statHint: {
    margin: "8px 0 0 0",
    color: "#c7d2e6",
    lineHeight: 1.5,
  },
  twoColumn: {
    display: "grid",
    gridTemplateColumns: "1.4fr 1fr",
    gap: "24px",
  },
  card: {
    background: "#121a30",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "24px",
    padding: "24px",
    boxShadow: "0 20px 60px rgba(0,0,0,0.25)",
  },
  cardHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "16px",
  },
  cardLabel: {
    margin: 0,
    color: "#8fa1c7",
    fontSize: "0.85rem",
    fontWeight: 800,
    textTransform: "uppercase",
    letterSpacing: "0.5px",
  },
  cardTitle: {
    margin: "8px 0 0 0",
    fontSize: "1.45rem",
  },
  profileBadge: {
    display: "inline-flex",
    marginTop: "18px",
    background: "rgba(108, 140, 255, 0.16)",
    border: "1px solid rgba(108, 140, 255, 0.28)",
    color: "#cdd7ff",
    borderRadius: "999px",
    padding: "8px 14px",
    fontWeight: 900,
  },
  summary: {
    margin: "16px 0 0 0",
    color: "#e5ecff",
    lineHeight: 1.8,
  },
  dimensionList: {
    display: "flex",
    flexDirection: "column",
    gap: "12px",
    marginTop: "18px",
  },
  dimensionItem: {
    display: "flex",
    justifyContent: "space-between",
    gap: "16px",
    background: "#18213b",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "16px",
    padding: "14px",
  },
  dimensionName: {
    margin: 0,
    color: "#ffffff",
    fontWeight: 900,
    textTransform: "capitalize",
  },
  dimensionReason: {
    margin: "6px 0 0 0",
    color: "#c7d2e6",
    lineHeight: 1.5,
  },
  dimensionScore: {
    color: "#cdd7ff",
    fontWeight: 900,
    whiteSpace: "nowrap",
  },
  outcomeStack: {
    display: "grid",
    gridTemplateColumns: "1fr",
    gap: "12px",
    marginTop: "18px",
  },
  outcomeBox: {
    background: "#18213b",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "18px",
    padding: "16px",
  },
  outcomeBoxHighlight: {
    background: "rgba(108, 140, 255, 0.18)",
    border: "1px solid rgba(108, 140, 255, 0.35)",
    borderRadius: "18px",
    padding: "16px",
  },
  outcomeValue: {
    margin: "8px 0 0 0",
    fontSize: "1.5rem",
  },
  allocationGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
    gap: "16px",
    marginTop: "18px",
  },
  allocationCard: {
    background: "#18213b",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "18px",
    padding: "18px",
  },
  allocationTop: {
    display: "flex",
    justifyContent: "space-between",
    gap: "12px",
  },
  allocationTitle: {
    margin: 0,
    fontSize: "1.05rem",
  },
  allocationPercent: {
    color: "#cdd7ff",
    fontWeight: 900,
  },
  barTrack: {
    marginTop: "14px",
    height: "10px",
    background: "#0b1020",
    borderRadius: "999px",
    overflow: "hidden",
  },
  barFill: {
    height: "100%",
    background: "#6c8cff",
    borderRadius: "999px",
  },
  allocationAmount: {
    margin: "12px 0 0 0",
    color: "#ffffff",
    fontWeight: 900,
  },
  allocationReason: {
    margin: "8px 0 0 0",
    color: "#c7d2e6",
    lineHeight: 1.6,
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
    lineHeight: 1.7,
  },
};