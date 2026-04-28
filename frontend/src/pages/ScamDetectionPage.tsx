import { useState } from "react";
import PageSection from "../components/PageSection";
import { runScamDetection } from "../lib/api";
import type { ScamPredictionResponse } from "../types/scamDetection";

export default function ScamDetectionPage() {
  const [inputText, setInputText] = useState("");
  const [result, setResult] = useState<ScamPredictionResponse | null>(null);
  const [isChecking, setIsChecking] = useState(false);
  const [error, setError] = useState("");

  async function handleCheck() {
    setError("");
    setResult(null);

    const trimmedInput = inputText.trim();

    if (trimmedInput.length < 10) {
      setError(
        "Enter a longer investment message or claim so FinSage has enough information to analyse."
      );
      return;
    }

    try {
      setIsChecking(true);
      const response = await runScamDetection(trimmedInput);
      setResult(response);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to analyse message."
      );
    } finally {
      setIsChecking(false);
    }
  }

  function formatPercent(value: number) {
    return `${Math.round(value * 100)}%`;
  }

  function formatSignalName(value: string) {
    return value
      .split("_")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  }

  return (
    <PageSection
      title="Scam Detection"
      description="Paste an investment message to check for misleading, manipulative, or suspicious warning signals."
    >
      <div style={styles.wrapper}>
        <section style={styles.card}>
          <p style={styles.helperText}>
            This tool is for educational risk awareness only. It does not prove
            that something is legally a scam and it should not be treated as
            financial or legal advice.
          </p>

          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Example: Invest today and receive guaranteed profit with zero risk. Only available for the next 24 hours!"
            style={styles.textarea}
          />

          <button
            onClick={handleCheck}
            disabled={isChecking}
            style={styles.button}
          >
            {isChecking ? "Checking..." : "Analyse message"}
          </button>
        </section>

        {error && <p style={styles.error}>{error}</p>}

        {result && (
          <section style={styles.resultCard}>
            <div style={styles.resultHeader}>
              <div>
                <p style={styles.label}>Risk result</p>
                <h2 style={styles.riskTitle}>
                  {result.risk_level.toUpperCase()} risk
                </h2>
                <p style={styles.subText}>
                  Model label: {result.predicted_label}
                </p>
              </div>

              <div style={styles.scoreBadge}>
                {formatPercent(result.scam_probability)}
              </div>
            </div>

            <p style={styles.explanation}>{result.explanation}</p>

            {result.warning_summary && (
              <div style={styles.warningSummary}>
                <p style={styles.label}>Warning summary</p>

                <h3 style={styles.sectionTitle}>
                  {result.warning_summary.title}
                </h3>

                <p style={styles.explanation}>
                  {result.warning_summary.message}
                </p>

                <div style={styles.actionBox}>
                  <strong>Recommended action:</strong>
                  <p style={styles.explanation}>
                    {result.warning_summary.recommended_action}
                  </p>
                </div>
              </div>
            )}

            <div style={styles.sectionBlock}>
              <p style={styles.label}>Detected warning signs</p>

              {result.warning_signals.length === 0 ? (
                <p style={styles.explanation}>
                  No strong scam-specific wording was detected. This does not
                  mean the opportunity is safe. You should still check source
                  credibility, transparency, risks, and fees before acting.
                </p>
              ) : (
                <div style={styles.signalList}>
                  {result.warning_signals.map((signal, index) => (
                    <div key={`${signal.signal_type}-${index}`} style={styles.signalCard}>
                      <div style={styles.signalHeader}>
                        <strong>{formatSignalName(signal.signal_type)}</strong>
                        <span style={styles.severityBadge}>
                          {signal.severity}
                        </span>
                      </div>

                      <p style={styles.matchedText}>
                        Matched text: “{signal.matched_text}”
                      </p>

                      <p style={styles.explanation}>{signal.explanation}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div style={styles.sectionBlock}>
              <p style={styles.label}>Investment evaluation checklist</p>

              <div style={styles.signalList}>
                {result.investment_checklist.map((item, index) => (
                  <div key={`${item.check}-${index}`} style={styles.signalCard}>
                    <strong>{item.check}</strong>
                    <p style={styles.explanation}>{item.reason}</p>
                  </div>
                ))}
              </div>
            </div>

            <p style={styles.disclaimer}>{result.educational_message}</p>
          </section>
        )}
      </div>
    </PageSection>
  );
}

const styles: Record<string, React.CSSProperties> = {
  wrapper: {
    display: "flex",
    flexDirection: "column",
    gap: "20px",
  },
  card: {
    background: "#121a30",
    padding: "20px",
    borderRadius: "20px",
    border: "1px solid rgba(255,255,255,0.08)",
  },
  helperText: {
    margin: "0 0 14px 0",
    color: "#ffd27d",
    lineHeight: 1.7,
  },
  textarea: {
    width: "100%",
    minHeight: "150px",
    background: "#0b1020",
    color: "white",
    padding: "12px",
    borderRadius: "10px",
    border: "1px solid rgba(255,255,255,0.1)",
    resize: "vertical",
    boxSizing: "border-box",
    lineHeight: 1.6,
  },
  button: {
    marginTop: "10px",
    padding: "10px 14px",
    background: "#6c8cff",
    color: "white",
    border: "none",
    borderRadius: "10px",
    cursor: "pointer",
    fontWeight: 700,
  },
  resultCard: {
    background: "#18213b",
    padding: "20px",
    borderRadius: "20px",
    border: "1px solid rgba(255,255,255,0.08)",
    display: "flex",
    flexDirection: "column",
    gap: "18px",
  },
  resultHeader: {
    display: "flex",
    justifyContent: "space-between",
    gap: "16px",
    alignItems: "flex-start",
  },
  label: {
    margin: 0,
    color: "#8fa1c7",
    fontSize: "0.82rem",
    fontWeight: 800,
    textTransform: "uppercase",
    letterSpacing: "0.5px",
  },
  riskTitle: {
    margin: "6px 0 0 0",
    color: "#ffffff",
  },
  subText: {
    margin: "6px 0 0 0",
    color: "#8fa1c7",
  },
  scoreBadge: {
    background: "rgba(108, 140, 255, 0.16)",
    border: "1px solid rgba(108, 140, 255, 0.28)",
    color: "#cdd7ff",
    borderRadius: "999px",
    padding: "10px 14px",
    fontWeight: 900,
    whiteSpace: "nowrap",
  },
  explanation: {
    margin: 0,
    color: "#c7d2e6",
    lineHeight: 1.7,
  },
  warningSummary: {
    background: "#0b1020",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "16px",
    padding: "14px",
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  sectionTitle: {
    margin: 0,
    color: "#ffffff",
  },
  actionBox: {
    background: "rgba(255,255,255,0.04)",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "12px",
    padding: "12px",
    color: "#ffffff",
  },
  sectionBlock: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  signalList: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  signalCard: {
    background: "#0b1020",
    padding: "12px",
    borderRadius: "12px",
    border: "1px solid rgba(255,255,255,0.08)",
    display: "flex",
    flexDirection: "column",
    gap: "8px",
  },
  signalHeader: {
    display: "flex",
    justifyContent: "space-between",
    gap: "12px",
    color: "#ffffff",
  },
  severityBadge: {
    background: "rgba(255,255,255,0.08)",
    borderRadius: "999px",
    padding: "4px 8px",
    fontSize: "0.75rem",
    textTransform: "uppercase",
  },
  matchedText: {
    margin: 0,
    color: "#ffd27d",
    lineHeight: 1.6,
  },
  disclaimer: {
    margin: 0,
    color: "#ffd27d",
    lineHeight: 1.7,
  },
  error: {
    color: "#ff8e8e",
    background: "rgba(255, 107, 107, 0.08)",
    border: "1px solid rgba(255, 107, 107, 0.2)",
    borderRadius: "12px",
    padding: "12px",
    margin: 0,
  },
};