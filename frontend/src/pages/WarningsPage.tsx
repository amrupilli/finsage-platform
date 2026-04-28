import { useEffect, useState } from "react";
import PageSection from "../components/PageSection";
import { getFullFinancialFlow, type UserWarning } from "../lib/api";
import { getOnboardingSessionId } from "../lib/onboardingSession";

export default function WarningsPage() {
  const [warnings, setWarnings] = useState<UserWarning[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchWarnings() {
      setIsLoading(true);
      setError("");

      const sessionId = getOnboardingSessionId();

      if (!sessionId) {
        setError(
          "No onboarding session was found. Complete onboarding before viewing warning insights."
        );
        setIsLoading(false);
        return;
      }

      try {
        const response = await getFullFinancialFlow(Number(sessionId));
        setWarnings(response.warnings ?? []);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to load warnings."
        );
      } finally {
        setIsLoading(false);
      }
    }

    fetchWarnings();
  }, []);

  return (
    <PageSection
      title="Warning Insights"
      description="Review educational warnings generated from your risk profile, portfolio scenario, simulation output, and scam-awareness checks."
    >
      <div style={styles.wrapper}>
        {isLoading && (
          <section style={styles.card}>
            <p style={styles.mutedText}>Loading warning insights...</p>
          </section>
        )}

        {!isLoading && error && (
          <section style={styles.errorBox}>
            <p style={styles.errorText}>{error}</p>
          </section>
        )}

        {!isLoading && !error && warnings.length === 0 && (
          <section style={styles.card}>
            <p style={styles.mutedText}>
              No major warning insights were generated for this session. This
              does not mean there is no risk. It only means FinSage did not find
              strong warning conditions in the current outputs.
            </p>
          </section>
        )}

        {!isLoading && !error && warnings.length > 0 && (
          <div style={styles.warningGrid}>
            {warnings.map((warning, index) => (
              <article key={`${warning.category}-${index}`} style={styles.card}>
                <div style={styles.cardHeader}>
                  <div>
                    <p style={styles.category}>
                      {formatCategory(warning.category)}
                    </p>

                    <h2 style={styles.title}>{warning.title}</h2>
                  </div>

                  <span style={getSeverityStyle(warning.severity)}>
                    {warning.severity}
                  </span>
                </div>

                <p style={styles.message}>{warning.message}</p>

                <div style={styles.actionBox}>
                  <p style={styles.actionLabel}>Recommended action</p>
                  <p style={styles.actionText}>
                    {warning.recommended_action}
                  </p>
                </div>
              </article>
            ))}
          </div>
        )}
      </div>
    </PageSection>
  );
}

function formatCategory(category: UserWarning["category"]) {
  return category
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

function getSeverityStyle(severity: UserWarning["severity"]): React.CSSProperties {
  const baseStyle: React.CSSProperties = {
    borderRadius: "999px",
    padding: "6px 10px",
    fontSize: "0.78rem",
    fontWeight: 800,
    textTransform: "uppercase",
    whiteSpace: "nowrap",
    border: "1px solid rgba(255,255,255,0.12)",
  };

  if (severity === "high") {
    return {
      ...baseStyle,
      background: "rgba(255, 107, 107, 0.16)",
      color: "#ffb3b3",
    };
  }

  if (severity === "medium") {
    return {
      ...baseStyle,
      background: "rgba(255, 193, 7, 0.14)",
      color: "#ffe3a3",
    };
  }

  return {
    ...baseStyle,
    background: "rgba(88, 214, 141, 0.14)",
    color: "#b7f7cc",
  };
}

const styles: Record<string, React.CSSProperties> = {
  wrapper: {
    display: "flex",
    flexDirection: "column",
    gap: "20px",
  },
  warningGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
    gap: "18px",
  },
  card: {
    background: "#121a30",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "20px",
    padding: "20px",
    display: "flex",
    flexDirection: "column",
    gap: "14px",
    boxShadow: "0 20px 60px rgba(0,0,0,0.2)",
  },
  cardHeader: {
    display: "flex",
    justifyContent: "space-between",
    gap: "14px",
    alignItems: "flex-start",
  },
  category: {
    margin: 0,
    color: "#8fa1c7",
    fontSize: "0.82rem",
    fontWeight: 800,
    textTransform: "uppercase",
    letterSpacing: "0.5px",
  },
  title: {
    margin: "6px 0 0 0",
    color: "#ffffff",
    fontSize: "1.2rem",
    lineHeight: 1.4,
  },
  message: {
    margin: 0,
    color: "#c7d2e6",
    lineHeight: 1.7,
  },
  actionBox: {
    background: "#0b1020",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "14px",
    padding: "14px",
  },
  actionLabel: {
    margin: 0,
    color: "#8fa1c7",
    fontSize: "0.78rem",
    fontWeight: 800,
    textTransform: "uppercase",
    letterSpacing: "0.5px",
  },
  actionText: {
    margin: "8px 0 0 0",
    color: "#ffffff",
    lineHeight: 1.7,
  },
  mutedText: {
    margin: 0,
    color: "#8fa1c7",
    lineHeight: 1.7,
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