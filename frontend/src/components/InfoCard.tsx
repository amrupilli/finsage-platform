import type { ReactNode } from "react";

type InfoCardProps = {
  title: string;
  value: string;
  description: string;
  accent?: string;
  children?: ReactNode;
};

export default function InfoCard({
  title,
  value,
  description,
  accent = "#5c7bfa",
  children,
}: InfoCardProps) {
  return (
    <div
      style={{
        ...styles.card,
        borderTop: `3px solid ${accent}`,
      }}
    >
      <p style={styles.title}>{title}</p>
      <h3 style={styles.value}>{value}</h3>
      <p style={styles.description}>{description}</p>
      {children}
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  card: {
    background: "#121a30",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "18px",
    padding: "20px",
    boxShadow: "0 16px 40px rgba(0,0,0,0.22)",
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  title: {
    margin: 0,
    color: "#8fa1c7",
    fontSize: "0.9rem",
    fontWeight: 600,
    textTransform: "uppercase",
    letterSpacing: "0.5px",
  },
  value: {
    margin: 0,
    fontSize: "1.5rem",
    fontWeight: 700,
  },
  description: {
    margin: 0,
    color: "#c7d2e6",
    lineHeight: 1.6,
    fontSize: "0.95rem",
  },
};