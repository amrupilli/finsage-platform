type ChatBubbleProps = {
  sender: "assistant" | "user";
  text: string;
};

export default function ChatBubble({ sender, text }: ChatBubbleProps) {
  const isAssistant = sender === "assistant";

  return (
    <div
      style={{
        ...styles.wrapper,
        justifyContent: isAssistant ? "flex-start" : "flex-end",
      }}
    >
      <div
        style={{
          ...styles.bubble,
          ...(isAssistant ? styles.assistantBubble : styles.userBubble),
        }}
      >
        <p style={styles.label}>{isAssistant ? "FinSage" : "You"}</p>
        <p style={styles.text}>{text}</p>
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  wrapper: {
    display: "flex",
    width: "100%",
  },
  bubble: {
    maxWidth: "75%",
    borderRadius: "18px",
    padding: "14px 16px",
    display: "flex",
    flexDirection: "column",
    gap: "8px",
    border: "1px solid rgba(255,255,255,0.08)",
  },
  assistantBubble: {
    background: "#18213b",
    color: "#f5f7fb",
  },
  userBubble: {
    background: "rgba(92, 123, 250, 0.18)",
    color: "#ffffff",
    border: "1px solid rgba(92, 123, 250, 0.24)",
  },
  label: {
    margin: 0,
    fontSize: "0.8rem",
    fontWeight: 700,
    color: "#8fa1c7",
    textTransform: "uppercase",
    letterSpacing: "0.4px",
  },
  text: {
    margin: 0,
    lineHeight: 1.7,
    whiteSpace: "pre-wrap",
  },
};