import type { ReactNode } from "react";

type AuthCardProps = {
  title: string;
  description: string;
  children: ReactNode;
};

export default function AuthCard({
  title,
  description,
  children,
}: AuthCardProps) {
  return (
    <div style={styles.wrapper}>
      <div style={styles.card}>
        <h1 style={styles.title}>{title}</h1>
        <p style={styles.description}>{description}</p>
        <div style={styles.content}>{children}</div>
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  wrapper: {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: "24px",
  },
  card: {
    width: "100%",
    maxWidth: "520px",
    background: "#121a30",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "24px",
    padding: "36px",
    boxShadow: "0 20px 60px rgba(0,0,0,0.35)",
  },
  title: {
    marginTop: 0,
    marginBottom: "10px",
    fontSize: "2rem",
  },
  description: {
    marginTop: 0,
    marginBottom: "24px",
    color: "#c7d2e6",
    lineHeight: 1.7,
  },
  content: {
    display: "flex",
    flexDirection: "column",
    gap: "16px",
  },
};