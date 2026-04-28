import type { ReactNode } from "react";

type LandingSectionProps = {
  label: string;
  title: string;
  description: string;
  children: ReactNode;
};

export default function LandingSection({
  label,
  title,
  description,
  children,
}: LandingSectionProps) {
  return (
    <section style={styles.section}>
      <div style={styles.header}>
        <p style={styles.label}>{label}</p>
        <h2 style={styles.title}>{title}</h2>
        <p style={styles.description}>{description}</p>
      </div>

      <div>{children}</div>
    </section>
  );
}

const styles: Record<string, React.CSSProperties> = {
  section: {
    maxWidth: "1120px",
    width: "100%",
    margin: "0 auto",
    display: "flex",
    flexDirection: "column",
    gap: "22px",
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
    fontSize: "2.1rem",
    lineHeight: 1.2,
  },
  description: {
    margin: 0,
    color: "#c7d2e6",
    lineHeight: 1.8,
    maxWidth: "820px",
  },
};