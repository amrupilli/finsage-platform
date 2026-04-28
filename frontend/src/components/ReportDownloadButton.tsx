import { useState } from "react";
import { downloadSessionReport } from "../lib/api";
import { getOnboardingSessionId } from "../lib/onboardingSession";

export default function ReportDownloadButton() {
  const [isDownloading, setIsDownloading] = useState(false);
  const [error, setError] = useState("");

  async function handleDownloadReport() {
    setError("");

    const sessionId = getOnboardingSessionId();

    if (!sessionId) {
      setError(
        "No onboarding session was found. Complete onboarding before downloading your report."
      );
      return;
    }

    const numericSessionId = Number(sessionId);

    if (Number.isNaN(numericSessionId)) {
      setError("Invalid onboarding session ID. Please complete onboarding again.");
      return;
    }

    try {
      setIsDownloading(true);

      const reportBlob = await downloadSessionReport(numericSessionId);

      const downloadUrl = window.URL.createObjectURL(reportBlob);
      const link = document.createElement("a");

      link.href = downloadUrl;
      link.download = `finsage-report-session-${numericSessionId}.pdf`;

      document.body.appendChild(link);
      link.click();
      link.remove();

      window.URL.revokeObjectURL(downloadUrl);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to download report."
      );
    } finally {
      setIsDownloading(false);
    }
  }

  return (
    <div style={styles.wrapper}>
      <button
        type="button"
        onClick={handleDownloadReport}
        disabled={isDownloading}
        style={{
          ...styles.button,
          opacity: isDownloading ? 0.7 : 1,
          cursor: isDownloading ? "not-allowed" : "pointer",
        }}
      >
        {isDownloading ? "Preparing report..." : "Download PDF report"}
      </button>

      {error && <p style={styles.error}>{error}</p>}
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  wrapper: {
    display: "flex",
    flexDirection: "column",
    gap: "8px",
    alignItems: "flex-start",
  },
  button: {
    border: "none",
    borderRadius: "999px",
    background: "#6c8cff",
    color: "#ffffff",
    padding: "12px 18px",
    fontWeight: 800,
  },
  error: {
    margin: 0,
    color: "#ff8e8e",
    lineHeight: 1.6,
  },
};