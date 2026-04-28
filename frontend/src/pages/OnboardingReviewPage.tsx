import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  getOnboardingAnswers,
  regenerateOnboardingOutputs,
  updateOnboardingAnswer,
  type OnboardingAnswer,
  type OnboardingAnswersReviewResponse,
} from "../lib/api";
import { getOnboardingSessionId } from "../lib/onboardingSession";

export default function OnboardingReviewPage() {
  const navigate = useNavigate();

  const [reviewData, setReviewData] =
    useState<OnboardingAnswersReviewResponse | null>(null);
  const [editedAnswers, setEditedAnswers] = useState<Record<number, string>>({});
  const [loading, setLoading] = useState(true);
  const [savingAnswerId, setSavingAnswerId] = useState<number | null>(null);
  const [regenerating, setRegenerating] = useState(false);
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const sessionId = getOnboardingSessionId();

  useEffect(() => {
    async function loadAnswers() {
      try {
        setLoading(true);
        setError("");

        if (sessionId === null) {
          throw new Error("No onboarding session found.");
        }

        const data = await getOnboardingAnswers(sessionId);
        setReviewData(data);

        const initialAnswers: Record<number, string> = {};
        data.answers.forEach((answer) => {
          initialAnswers[answer.answer_id] = answer.answer_text;
        });
        setEditedAnswers(initialAnswers);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load answers.");
      } finally {
        setLoading(false);
      }
    }

    loadAnswers();
  }, [sessionId]);

  function handleAnswerChange(answerId: number, value: string) {
    setEditedAnswers((previous) => ({
      ...previous,
      [answerId]: value,
    }));
  }

  async function handleSaveAnswer(answer: OnboardingAnswer) {
    try {
      setSavingAnswerId(answer.answer_id);
      setError("");
      setSuccessMessage("");

      const updatedText = editedAnswers[answer.answer_id];

      if (!updatedText || updatedText.trim().length === 0) {
        throw new Error("Answer cannot be empty.");
      }

      await updateOnboardingAnswer(sessionId!, answer.answer_id, updatedText);
      setSuccessMessage("Answer saved successfully.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save answer.");
    } finally {
      setSavingAnswerId(null);
    }
  }

  async function handleRegenerateOutputs() {
    try {
      setRegenerating(true);
      setError("");
      setSuccessMessage("");

      await regenerateOnboardingOutputs(sessionId!);

      setSuccessMessage("Outputs regenerated successfully.");
      navigate("/dashboard");
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to regenerate outputs."
      );
    } finally {
      setRegenerating(false);
    }
  }

  if (loading) {
    return <p style={styles.mutedText}>Loading your saved answers...</p>;
  }

  return (
    <div style={styles.page}>
      <div style={styles.header}>
        <p style={styles.label}>Phase B</p>
        <h1 style={styles.title}>Review & Edit Onboarding Answers</h1>
        <p style={styles.description}>
          Update your saved questionnaire responses. After editing, regenerate
          your dashboard so the risk profile, portfolio, and simulation match
          the new answers.
        </p>
      </div>

      {error && (
        <div style={styles.errorBox}>
          <p style={styles.errorText}>{error}</p>
        </div>
      )}

      {successMessage && (
        <div style={styles.successBox}>
          <p style={styles.successText}>{successMessage}</p>
        </div>
      )}

      <section style={styles.card}>
        <div style={styles.cardHeader}>
          <div>
            <p style={styles.cardLabel}>Saved answers</p>
            <h2 style={styles.cardTitle}>Questionnaire responses</h2>
          </div>
          <button
            type="button"
            onClick={() => navigate("/dashboard")}
            style={styles.secondaryButton}
          >
            Back to dashboard
          </button>
        </div>

        <div style={styles.answerGrid}>
          {reviewData?.answers.map((answer) => (
            <div key={answer.answer_id} style={styles.answerCard}>
              <p style={styles.answerLabel}>Question type</p>
              <h3 style={styles.answerTitle}>
                {(answer.field_name || answer.question_key).replace("_", " ")}
              </h3>

              <label style={styles.textareaLabel}>Your answer</label>
              <textarea
                value={editedAnswers[answer.answer_id] ?? ""}
                onChange={(event) =>
                  handleAnswerChange(answer.answer_id, event.target.value)
                }
                rows={4}
                style={styles.textarea}
              />

              <button
                type="button"
                onClick={() => handleSaveAnswer(answer)}
                disabled={savingAnswerId === answer.answer_id}
                style={{
                  ...styles.primaryButton,
                  opacity: savingAnswerId === answer.answer_id ? 0.65 : 1,
                }}
              >
                {savingAnswerId === answer.answer_id ? "Saving..." : "Save answer"}
              </button>
            </div>
          ))}
        </div>
      </section>

      <section style={styles.regenerateCard}>
        <p style={styles.cardLabel}>Regenerate outputs</p>
        <h2 style={styles.cardTitle}>Refresh your dashboard</h2>
        <p style={styles.description}>
          This reruns the risk profile, portfolio scenario, Monte Carlo
          simulation, and warning logic using your edited answers.
        </p>

        {reviewData?.missing_fields && reviewData.missing_fields.length > 0 && (
          <p style={styles.warningText}>
            Missing fields: {reviewData.missing_fields.join(", ")}
          </p>
        )}

        <button
          type="button"
          onClick={handleRegenerateOutputs}
          disabled={regenerating}
          style={{
            ...styles.greenButton,
            opacity: regenerating ? 0.65 : 1,
          }}
        >
          {regenerating ? "Regenerating..." : "Regenerate dashboard outputs"}
        </button>
      </section>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  page: {
    display: "flex",
    flexDirection: "column",
    gap: "24px",
  },
  header: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  label: {
    margin: 0,
    color: "#8fa1c7",
    fontSize: "0.9rem",
    fontWeight: 700,
    textTransform: "uppercase",
    letterSpacing: "0.5px",
  },
  title: {
    margin: 0,
    fontSize: "2rem",
  },
  description: {
    margin: 0,
    color: "#c7d2e6",
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
  cardHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "16px",
    marginBottom: "20px",
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
    margin: "6px 0 0 0",
    fontSize: "1.35rem",
  },
  answerGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
    gap: "18px",
  },
  answerCard: {
    background: "#18213b",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "18px",
    padding: "18px",
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  answerLabel: {
    margin: 0,
    color: "#8fa1c7",
    fontSize: "0.8rem",
    fontWeight: 800,
    textTransform: "uppercase",
  },
  answerTitle: {
    margin: 0,
    fontSize: "1.15rem",
    textTransform: "capitalize",
  },
  textareaLabel: {
    color: "#c7d2e6",
    fontWeight: 700,
    fontSize: "0.9rem",
  },
  textarea: {
    width: "100%",
    minHeight: "110px",
    resize: "vertical",
    borderRadius: "14px",
    border: "1px solid rgba(255,255,255,0.12)",
    background: "#0b1020",
    color: "#ffffff",
    padding: "12px",
    font: "inherit",
    lineHeight: 1.6,
    boxSizing: "border-box",
  },
  primaryButton: {
    alignSelf: "flex-start",
    border: "1px solid rgba(108, 140, 255, 0.45)",
    borderRadius: "12px",
    background: "rgba(108, 140, 255, 0.18)",
    color: "#dbe4ff",
    fontWeight: 800,
    padding: "10px 14px",
    cursor: "pointer",
  },
  secondaryButton: {
    border: "1px solid rgba(255,255,255,0.12)",
    borderRadius: "12px",
    background: "#18213b",
    color: "#dbe4ff",
    fontWeight: 800,
    padding: "10px 14px",
    cursor: "pointer",
  },
  regenerateCard: {
    background: "rgba(26, 83, 92, 0.22)",
    border: "1px solid rgba(47, 190, 150, 0.25)",
    borderRadius: "24px",
    padding: "24px",
  },
  greenButton: {
    marginTop: "18px",
    border: "1px solid rgba(47, 190, 150, 0.45)",
    borderRadius: "12px",
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
  successBox: {
    background: "rgba(47, 190, 150, 0.1)",
    border: "1px solid rgba(47, 190, 150, 0.25)",
    borderRadius: "16px",
    padding: "16px",
  },
  successText: {
    margin: 0,
    color: "#9fffd9",
  },
  warningText: {
    margin: "14px 0 0 0",
    color: "#ffd27d",
  },
  mutedText: {
    margin: 0,
    color: "#8fa1c7",
  },
};