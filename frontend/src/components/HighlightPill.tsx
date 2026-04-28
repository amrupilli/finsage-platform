type HighlightPillProps = {
  text: string;
};

export default function HighlightPill({ text }: HighlightPillProps) {
  return <div style={styles.pill}>{text}</div>;
}

const styles: Record<string, React.CSSProperties> = {
  pill: {
    padding: "12px 16px",
    borderRadius: "999px",
    background: "rgba(255,255,255,0.04)",
    border: "1px solid rgba(255,255,255,0.08)",
    color: "#dce4ff",
    fontSize: "0.95rem",
    fontWeight: 600,
    textAlign: "center",
    boxShadow: "0 8px 24px rgba(0,0,0,0.12)",
  },
};