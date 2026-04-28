import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import ChatBubble from "../components/ChatBubble";
import {
  authenticatedApiRequest,
  getLatestCompletedOnboardingSession,
} from "../lib/api";
import {
  getOnboardingSessionId,
  saveOnboardingSessionId,
} from "../lib/onboardingSession";
import type {
  ChatMessage,
  OnboardingCompletionState,
  OnboardingMessageResponse,
  OnboardingStartResponse,
} from "../types/onboarding";

function extractAssistantText(response: OnboardingMessageResponse): string {
  return response.assistant_message.trim();
}

function isCompletionMessage(text: string): boolean {
  const lowered = text.toLowerCase();

  return (
    lowered.includes("i have enough to build your initial profile") ||
    lowered.includes("next i’ll turn this into a structured risk assessment") ||
    lowered.includes("next i'll turn this into a structured risk assessment") ||
    lowered.includes("onboarding is complete") ||
    lowered.includes("you can continue to the dashboard")
  );
}

function detectCompletion(response: OnboardingMessageResponse): boolean {
  const assistantText = extractAssistantText(response);

  return (
    response.is_completed ||
    response.current_stage === "complete" ||
    isCompletionMessage(assistantText)
  );
}

export default function OnboardingPage() {
  const navigate = useNavigate();
  const chatBodyRef = useRef<HTMLDivElement | null>(null);
  const hasStartedRef = useRef(false);

  const [sessionId, setSessionId] = useState<number | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState("");
  const [isStarting, setIsStarting] = useState(true);
  const [isSending, setIsSending] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [completionState, setCompletionState] =
    useState<OnboardingCompletionState>("in_progress");

  useEffect(() => {
    if (hasStartedRef.current) {
      return;
    }

    hasStartedRef.current = true;

    async function startOnboardingSession() {
      setIsStarting(true);
      setErrorMessage("");

      try {
  const existingSessionId = getOnboardingSessionId();

  if (existingSessionId) {
    setSessionId(existingSessionId);
    setCompletionState("complete");
    setMessages([
      {
        id: crypto.randomUUID(),
        sender: "assistant",
        text: "Onboarding is already complete. You can continue to your dashboard or edit your saved answers.",
      },
    ]);
    return;
  }

  try {
    const latestSession = await getLatestCompletedOnboardingSession();

    saveOnboardingSessionId(latestSession.session_id);
    setSessionId(latestSession.session_id);
    setCompletionState("complete");
    setMessages([
      {
        id: crypto.randomUUID(),
        sender: "assistant",
        text: "Onboarding is already complete. You can continue to your dashboard or edit your saved answers.",
      },
    ]);
    return;
  } catch {
    // No completed onboarding exists yet, so start a new one.
  }

  const response = await authenticatedApiRequest<OnboardingStartResponse>(
    "/onboarding/start",
    {
      method: "POST",
    }
  );

        setSessionId(response.session_id);
        saveOnboardingSessionId(response.session_id);

        setMessages([
          {
            id: crypto.randomUUID(),
            sender: "assistant",
            text: response.assistant_message,
          },
        ]);

        if (detectCompletion(response)) {
          setCompletionState("complete");
        }
      } catch (error) {
        if (error instanceof Error) {
          setErrorMessage(error.message);
        } else {
          setErrorMessage("Failed to start onboarding.");
        }
      } finally {
        setIsStarting(false);
      }
    }

    startOnboardingSession();
  }, []);

  useEffect(() => {
    if (chatBodyRef.current) {
      chatBodyRef.current.scrollTop = chatBodyRef.current.scrollHeight;
    }
  }, [messages, errorMessage, completionState]);

useEffect(() => {
  if (completionState === "complete") {
    return;
  }

  const lastAssistantMessage = [...messages]
    .reverse()
    .find((message) => message.sender === "assistant");

  if (lastAssistantMessage && isCompletionMessage(lastAssistantMessage.text)) {
    setCompletionState("complete");
    setErrorMessage("");
  }
}, [messages, completionState]);

  async function handleSendMessage(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (
      !sessionId ||
      !inputText.trim() ||
      isSending ||
      completionState === "complete"
    ) {
      return;
    }

    const trimmedMessage = inputText.trim();

    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      sender: "user",
      text: trimmedMessage,
    };

    setMessages((previous) => [...previous, userMessage]);
    setInputText("");
    setIsSending(true);
    setErrorMessage("");

    try {
      const response = await authenticatedApiRequest<OnboardingMessageResponse>(
        `/onboarding/${sessionId}/message`,
        {
          method: "POST",
          body: JSON.stringify({
            message_text: trimmedMessage,
          }),
        }
      );

      const assistantText = extractAssistantText(response);

      if (assistantText) {
        const assistantMessage: ChatMessage = {
          id: crypto.randomUUID(),
          sender: "assistant",
          text: assistantText,
        };

        setMessages((previous) => [...previous, assistantMessage]);
      }

      if (detectCompletion(response)) {
        setCompletionState("complete");
        setErrorMessage("");
      }
    } catch (error) {
      if (error instanceof Error) {
        const loweredMessage = error.message.toLowerCase();

        if (
          loweredMessage.includes("already complete") ||
          loweredMessage.includes("session is already complete")
        ) {
          setCompletionState("complete");
          setErrorMessage("");

          setMessages((previous) => {
            const alreadyExists = previous.some(
              (message) =>
                message.sender === "assistant" &&
                message.text ===
                  "Onboarding is complete. You can continue to the dashboard."
            );

            if (alreadyExists) {
              return previous;
            }

            return [
              ...previous,
              {
                id: crypto.randomUUID(),
                sender: "assistant",
                text: "Onboarding is complete. You can continue to the dashboard.",
              },
            ];
          });
        } else {
          setErrorMessage(error.message);
        }
      } else {
        setErrorMessage("Failed to send onboarding message.");
      }
    } finally {
      setIsSending(false);
    }
  }

  function handleInputKeyDown(event: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      const form = event.currentTarget.form;
      if (form) {
        form.requestSubmit();
      }
    }
  }

  return (
    <div style={styles.page}>
      <div style={styles.header}>
        <p style={styles.label}>Conversational onboarding</p>
        <h1 style={styles.title}>Tell FinSage about your goals</h1>
        <p style={styles.description}>
          This onboarding flow is designed to feel conversational while still
          collecting structured backend signals for risk profiling and portfolio
          generation.
        </p>
      </div>

      <div style={styles.chatCard}>
        <div style={styles.chatHeader}>
          <div>
            <p style={styles.chatLabel}>Session</p>
            <h2 style={styles.chatTitle}>
              {sessionId ? `Session #${sessionId}` : "Starting..."}
            </h2>
          </div>

          {completionState === "complete" && (
            <div style={styles.completeBadge}>Completed</div>
          )}
        </div>

        <div ref={chatBodyRef} style={styles.chatBody}>
          {isStarting && (
            <div style={styles.stateBox}>
              <p style={styles.stateText}>Starting onboarding session...</p>
            </div>
          )}

          {!isStarting &&
            messages.map((message) => (
              <ChatBubble
                key={message.id}
                sender={message.sender}
                text={message.text}
              />
            ))}

          {!isStarting && errorMessage && (
            <div style={styles.errorBox}>
              <p style={styles.errorText}>{errorMessage}</p>
            </div>
          )}

          {completionState === "complete" && (
            <div style={styles.successBox}>
              <p style={styles.successText}>
                Onboarding is complete. You can now continue to the dashboard.
              </p>

              <button
  type="button"
  onClick={() => navigate("/onboarding/review")}
  style={styles.editButton}
>
  Edit saved answers
</button>
            </div>
          )}
        </div>

        <form onSubmit={handleSendMessage} style={styles.chatFooter}>
          <textarea
            value={inputText}
            onChange={(event) => setInputText(event.target.value)}
            onKeyDown={handleInputKeyDown}
            placeholder={
              completionState === "complete"
                ? "Onboarding complete"
                : "Type your answer..."
            }
            style={styles.input}
            disabled={
              isStarting ||
              isSending ||
              !sessionId ||
              completionState === "complete"
            }
            rows={1}
          />

          <button
            type="submit"
            style={{
              ...styles.sendButton,
              opacity:
                isStarting ||
                isSending ||
                !sessionId ||
                completionState === "complete" ||
                !inputText.trim()
                  ? 0.6
                  : 1,
              cursor:
                isStarting ||
                isSending ||
                !sessionId ||
                completionState === "complete" ||
                !inputText.trim()
                  ? "not-allowed"
                  : "pointer",
            }}
            disabled={
              isStarting ||
              isSending ||
              !sessionId ||
              completionState === "complete" ||
              !inputText.trim()
            }
          >
            {isSending ? "Sending..." : "Send"}
          </button>
        </form>
      </div>
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
    fontWeight: 600,
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
    maxWidth: "840px",
  },
  chatCard: {
    background: "#121a30",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "24px",
    boxShadow: "0 20px 60px rgba(0,0,0,0.25)",
    display: "flex",
    flexDirection: "column",
    minHeight: "560px",
    overflow: "hidden",
  },
  chatHeader: {
    padding: "20px 24px",
    borderBottom: "1px solid rgba(255,255,255,0.08)",
    background: "#18213b",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    gap: "16px",
  },
  chatLabel: {
    margin: 0,
    color: "#8fa1c7",
    fontSize: "0.85rem",
    fontWeight: 600,
    textTransform: "uppercase",
    letterSpacing: "0.5px",
  },
  chatTitle: {
    margin: "6px 0 0 0",
    fontSize: "1.2rem",
  },
  completeBadge: {
    background: "rgba(77, 208, 122, 0.16)",
    color: "#8ff0a4",
    border: "1px solid rgba(77, 208, 122, 0.28)",
    borderRadius: "999px",
    padding: "8px 14px",
    fontSize: "0.85rem",
    fontWeight: 700,
  },
  chatBody: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    gap: "16px",
    padding: "24px",
    overflowY: "auto",
  },
  chatFooter: {
    padding: "18px 24px",
    borderTop: "1px solid rgba(255,255,255,0.08)",
    background: "#10182c",
    display: "flex",
    gap: "12px",
    alignItems: "flex-end",
  },
  input: {
    flex: 1,
    resize: "none",
    minHeight: "56px",
    maxHeight: "160px",
    background: "#18213b",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "16px",
    padding: "16px",
    color: "#ffffff",
    fontSize: "1rem",
    lineHeight: 1.5,
    outline: "none",
    fontFamily: "inherit",
  },
  sendButton: {
    height: "56px",
    minWidth: "112px",
    borderRadius: "16px",
    border: "none",
    background: "#6c8cff",
    color: "#ffffff",
    fontWeight: 700,
    fontSize: "1rem",
    padding: "0 20px",
    transition: "0.2s ease",
  },
  stateBox: {
    background: "#18213b",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "16px",
    padding: "16px",
  },
  stateText: {
    margin: 0,
    color: "#c7d2e6",
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
  successBox: {
    background: "rgba(77, 208, 122, 0.08)",
    border: "1px solid rgba(77, 208, 122, 0.2)",
    borderRadius: "18px",
    padding: "18px",
    display: "flex",
    flexDirection: "column",
    gap: "14px",
  },
  successText: {
    margin: 0,
    color: "#d7ffe1",
    lineHeight: 1.7,
  },
  continueButton: {
    alignSelf: "flex-start",
    border: "none",
    borderRadius: "14px",
    background: "#4dd07a",
    color: "#08111f",
    fontWeight: 700,
    padding: "12px 18px",
    cursor: "pointer",
  },
  editButton: {
  alignSelf: "flex-start",
  border: "1px solid rgba(108, 140, 255, 0.4)",
  borderRadius: "14px",
  background: "rgba(108, 140, 255, 0.16)",
  color: "#dbe4ff",
  fontWeight: 700,
  padding: "12px 18px",
  cursor: "pointer",
},
};

