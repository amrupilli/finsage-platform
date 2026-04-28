type LandingFeatureCardProps = {
  title: string;
  description: string;
};

export default function LandingFeatureCard({
  title,
  description,
}: LandingFeatureCardProps) {
  return (
    <div style={styles.card}>
      <h3 style={styles.title}>{title}</h3>
      <p style={styles.description}>{description}</p>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  card: {
    background: "#121a30",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "20px",
    padding: "24px",
    boxShadow: "0 12px 30px rgba(0,0,0,0.18)",
  },
  title: {
    marginTop: 0,
    marginBottom: "12px",
    fontSize: "1.05rem",
  },
  description: {
    margin: 0,
    color: "#c7d2e6",
    lineHeight: 1.7,
    fontSize: "0.95rem",
  },
};