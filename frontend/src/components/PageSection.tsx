import type { ReactNode } from "react";

type PageSectionProps = {
  title: string;
  description: string;
  children?: ReactNode;
};

export default function PageSection({
  title,
  description,
  children,
}: PageSectionProps) {
  return (
    <section style={styles.wrapper}>
      <div style={styles.header}>
        <h1 style={styles.title}>{title}</h1>
        <p style={styles.description}>{description}</p>
      </div>

      <div style={styles.content}>{children}</div>
    </section>
  );
}

const styles: Record<string, React.CSSProperties> = {
  wrapper: {
    display: "flex",
    flexDirection: "column",
    gap: "24px",
  },
  header: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  title: {
    margin: 0,
    fontSize: "2rem",
    fontWeight: 700,
  },
  description: {
    margin: 0,
    color: "#c7d2e6",
    maxWidth: "760px",
    lineHeight: 1.7,
  },
  content: {
    background: "#121a30",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "20px",
    padding: "24px",
    boxShadow: "0 20px 60px rgba(0,0,0,0.25)",
  },
};