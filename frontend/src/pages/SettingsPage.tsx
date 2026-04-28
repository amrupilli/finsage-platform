import PageSection from "../components/PageSection";
import { getAccessToken } from "../lib/auth";

export default function SettingsPage() {
  const token = getAccessToken();

  return (
    <PageSection
      title="Settings"
      description="This page will contain user profile actions, preferences, and future access points for reports and downloadable outputs."
    >
      <div style={styles.card}>
        <p style={styles.label}>Stored access token status</p>
        <p style={styles.value}>{token ? "Present" : "Missing"}</p>
        <p style={styles.description}>
          This confirms whether an access token is currently stored in the browser.
          Future profile controls and report actions will be added here.
        </p>
      </div>
    </PageSection>
  );
}

const styles: Record<string, React.CSSProperties> = {
  card: {
    background: "#121a30",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "18px",
    padding: "20px",
    boxShadow: "0 16px 40px rgba(0,0,0,0.22)",
  },
  label: {
    margin: "0 0 8px 0",
    color: "#8fa1c7",
    fontSize: "0.9rem",
    fontWeight: 600,
    textTransform: "uppercase",
    letterSpacing: "0.5px",
  },
  value: {
    margin: "0 0 10px 0",
    fontSize: "1.5rem",
    fontWeight: 700,
  },
  description: {
    margin: 0,
    color: "#c7d2e6",
    lineHeight: 1.6,
  },
};