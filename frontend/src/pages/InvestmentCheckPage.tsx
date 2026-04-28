import { useState } from "react";
import PageSection from "../components/PageSection";
import {
  runInvestmentCheck,
  type InvestmentCheckResponse,
} from "../lib/api";

export default function InvestmentCheckPage() {
  const [inputText, setInputText] = useState("");
  const [result, setResult] = useState<InvestmentCheckResponse | null>(null);
  const [isChecking, setIsChecking] = useState(false);
  const [error, setError] = useState("");

  async function handleCheck() {
    setError("");
    setResult(null);

    if (inputText.trim().length < 5) {
      setError("Please enter a short description of the investment opportunity.");
      return;
    }

    try {
      setIsChecking(true);
      const response = await runInvestmentCheck(inputText);
      setResult(response);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to run investment check."
      );
    } finally {
      setIsChecking(false);
    }
  }

  return (
    <PageSection
      title="Investment Check Assistant"
      description="Ask what you should check before considering an investment opportunity. This tool gives an educational checklist, not financial advice."
    >
      <div style={styles.wrapper}>
        <section style={styles.heroCard}>
          <p style={styles.label}>Optional advanced feature</p>
          <h2 style={styles.heroTitle}>
            What should I check before investing in this?
          </h2>
          <p style={styles.heroText}>
            Paste a short description of an asset, platform, opportunity, or
            investment claim. FinSage will return a structured checklist covering
            transparency, credibility, risk, return claims, liquidity, and scam
            signals.
          </p>
        </section>

        <section style={styles.card}>
          <label style={styles.inputLabel}>Investment description</label>
          <textarea
            value={inputText}
            onChange={(event) => setInputText(event.target.value)}
            placeholder="Example: Someone on Telegram said this crypto coin will double my money in one week with no risk."
            rows={5}
            style={styles.textarea}
          />

          <button
            type="button"
            onClick={handleCheck}
            disabled={isChecking}
            style={{
              ...styles.primaryButton,
              opacity: isChecking ? 0.65 : 1,
            }}
          >
            {isChecking ? "Checking..." : "Run investment check"}
          </button>
        </section>

        {error && (
          <div style={styles.errorBox}>
            <p style={styles.errorText}>{error}</p>
          </div>
        )}

        {result && (
          <>
            <section style={styles.resultCard}>
              <p style={styles.label}>Risk signal</p>
              <h2 style={styles.resultTitle}>{result.risk_level}</h2>
              <p style={styles.summary}>{result.summary}</p>
              <p style={styles.disclaimer}>{result.educational_message}</p>
            </section>

            <section style={styles.card}>
              <p style={styles.label}>Checklist</p>
              <h2 style={styles.cardTitle}>Before investing, check these areas</h2>

              <div style={styles.checklistGrid}>
                {result.checklist.map((item) => (
                  <div key={item.title} style={styles.checkItem}>
                    <div style={styles.checkHeader}>
                      <h3 style={styles.checkTitle}>{item.title}</h3>
                      <span style={styles.statusBadge}>{item.status}</span>
                    </div>
                    <p style={styles.checkText}>{item.explanation}</p>
                  </div>
                ))}
              </div>
            </section>
          </>
        )}
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
    background:
      "linear-gradient(135deg, rgba(47,190,150,0.18), rgba(18,26,48,1))",
    border: "1px solid rgba(47,190,150,0.25)",
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
  card: {
    background: "#121a30",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "24px",
    padding: "24px",
    boxShadow: "0 20px 60px rgba(0,0,0,0.25)",
  },
  inputLabel: {
    display: "block",
    marginBottom: "10px",
    color: "#c7d2e6",
    fontWeight: 800,
  },
  textarea: {
    width: "100%",
    minHeight: "140px",
    resize: "vertical",
    borderRadius: "16px",
    border: "1px solid rgba(255,255,255,0.12)",
    background: "#0b1020",
    color: "#ffffff",
    padding: "14px",
    font: "inherit",
    lineHeight: 1.7,
    boxSizing: "border-box",
  },
  primaryButton: {
    marginTop: "16px",
    border: "1px solid rgba(47, 190, 150, 0.45)",
    borderRadius: "14px",
    background: "rgba(47, 190, 150, 0.18)",
    color: "#d7fff2",
    fontWeight: 900,
    padding: "12px 16px",
    cursor: "pointer",
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
  resultCard: {
    background: "rgba(108, 140, 255, 0.14)",
    border: "1px solid rgba(108, 140, 255, 0.28)",
    borderRadius: "24px",
    padding: "24px",
  },
  resultTitle: {
    margin: "8px 0 0 0",
    fontSize: "1.8rem",
  },
  summary: {
    margin: "14px 0 0 0",
    color: "#e5ecff",
    lineHeight: 1.8,
  },
  disclaimer: {
    margin: "14px 0 0 0",
    color: "#ffd27d",
    lineHeight: 1.7,
    fontWeight: 700,
  },
  cardTitle: {
    margin: "8px 0 0 0",
    fontSize: "1.45rem",
  },
  checklistGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
    gap: "16px",
    marginTop: "18px",
  },
  checkItem: {
    background: "#18213b",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "18px",
    padding: "18px",
  },
  checkHeader: {
    display: "flex",
    justifyContent: "space-between",
    gap: "12px",
    alignItems: "center",
  },
  checkTitle: {
    margin: 0,
    fontSize: "1.05rem",
  },
  statusBadge: {
    border: "1px solid rgba(47,190,150,0.35)",
    background: "rgba(47,190,150,0.14)",
    color: "#d7fff2",
    borderRadius: "999px",
    padding: "6px 10px",
    fontSize: "0.8rem",
    fontWeight: 900,
    whiteSpace: "nowrap",
  },
  checkText: {
    margin: "12px 0 0 0",
    color: "#c7d2e6",
    lineHeight: 1.7,
  },
};