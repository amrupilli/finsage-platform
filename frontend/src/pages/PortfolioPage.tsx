import { useEffect, useState } from "react";
import PageSection from "../components/PageSection";
import {
  authenticatedApiRequest,
  getPortfolioScenario,
} from "../lib/api";
import { getOnboardingSessionId } from "../lib/onboardingSession";
import type { PortfolioScenarioResponse } from "../types/portfolio";
import type { RiskProfileResponse } from "../types/riskProfile";

export default function PortfolioPage() {
  const [portfolio, setPortfolio] = useState<PortfolioScenarioResponse | null>(
    null
  );
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadPortfolio() {
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

        const response = await getPortfolioScenario(sessionId);
        setPortfolio(response);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to load portfolio."
        );
      } finally {
        setIsLoading(false);
      }
    }

    loadPortfolio();
  }, []);

  return (
    <PageSection
      title="Portfolio"
      description="This page displays the educational portfolio scenario generated from your onboarding responses and risk profile."
    >
      {isLoading && <p style={styles.mutedText}>Loading portfolio scenario...</p>}

      {!isLoading && error && (
        <div style={styles.errorBox}>
          <p style={styles.errorText}>{error}</p>
        </div>
      )}

      {!isLoading && !error && portfolio && (
        <div style={styles.wrapper}>
          <section style={styles.card}>
            <p style={styles.label}>Portfolio type</p>
            <h2 style={styles.title}>{portfolio.portfolio_type}</h2>
            <p style={styles.summary}>{portfolio.summary}</p>

            <div style={styles.metricGrid}>
              <div style={styles.metricBox}>
                <p style={styles.metricLabel}>Total educational budget</p>
                <p style={styles.metricValue}>
                  £{portfolio.total_budget.toFixed(2)}
                </p>
              </div>

              <div style={styles.metricBox}>
                <p style={styles.metricLabel}>Allocation categories</p>
                <p style={styles.metricValue}>{portfolio.allocations.length}</p>
              </div>
            </div>
          </section>

          <section style={styles.card}>
            <p style={styles.label}>Suggested educational allocation</p>

            <div style={styles.allocationList}>
              {portfolio.allocations.map((allocation) => (
                <div key={allocation.category} style={styles.allocationCard}>
                  <div style={styles.allocationHeader}>
                    <h3 style={styles.allocationTitle}>
                      {allocation.category}
                    </h3>
                    <p style={styles.allocationPercentage}>
                      {allocation.percentage}%
                    </p>
                  </div>

                  <div style={styles.barTrack}>
                    <div
                      style={{
                        ...styles.barFill,
                        width: `${allocation.percentage}%`,
                      }}
                    />
                  </div>

                  <p style={styles.amount}>
                    Modelled amount: £{allocation.amount.toFixed(2)}
                  </p>

                  <p style={styles.rationale}>{allocation.rationale}</p>
                </div>
              ))}
            </div>
          </section>
        </div>
      )}
    </PageSection>
  );
}

const styles: Record<string, React.CSSProperties> = {
  wrapper: {
    display: "flex",
    flexDirection: "column",
    gap: "24px",
  },
  card: {
    background: "#121a30",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "24px",
    padding: "24px",
    boxShadow: "0 20px 60px rgba(0,0,0,0.25)",
  },
  label: {
    margin: 0,
    color: "#8fa1c7",
    fontSize: "0.85rem",
    fontWeight: 800,
    textTransform: "uppercase",
    letterSpacing: "0.5px",
  },
  title: {
    margin: "8px 0 0 0",
    fontSize: "1.6rem",
  },
  summary: {
    margin: "16px 0 0 0",
    color: "#e5ecff",
    lineHeight: 1.8,
  },
  metricGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
    gap: "16px",
    marginTop: "20px",
  },
  metricBox: {
    background: "#18213b",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "18px",
    padding: "16px",
  },
  metricLabel: {
    margin: 0,
    color: "#8fa1c7",
    fontWeight: 700,
  },
  metricValue: {
    margin: "8px 0 0 0",
    color: "#ffffff",
    fontSize: "1.5rem",
    fontWeight: 900,
  },
  allocationList: {
    display: "flex",
    flexDirection: "column",
    gap: "16px",
    marginTop: "18px",
  },
  allocationCard: {
    background: "#18213b",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "18px",
    padding: "18px",
  },
  allocationHeader: {
    display: "flex",
    justifyContent: "space-between",
    gap: "16px",
    alignItems: "center",
  },
  allocationTitle: {
    margin: 0,
    fontSize: "1.1rem",
  },
  allocationPercentage: {
    margin: 0,
    color: "#cdd7ff",
    fontWeight: 900,
  },
  barTrack: {
    marginTop: "12px",
    height: "10px",
    background: "#0d1326",
    borderRadius: "999px",
    overflow: "hidden",
  },
  barFill: {
    height: "100%",
    background: "#6c8cff",
    borderRadius: "999px",
  },
  amount: {
    margin: "12px 0 0 0",
    color: "#ffffff",
    fontWeight: 700,
  },
  rationale: {
    margin: "8px 0 0 0",
    color: "#c7d2e6",
    lineHeight: 1.7,
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