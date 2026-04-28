import { Link } from "react-router-dom";
import HighlightPill from "../components/HighlightPill";
import LandingFeatureCard from "../components/LandingFeatureCard";
import LandingSection from "../components/LandingSection";

const featureCards = [
  {
    title: "Explainable risk profiling",
    description:
      "Users answer conversational onboarding questions and receive a transparent risk classification with reasoning across multiple dimensions.",
  },
  {
    title: "Educational portfolio scenarios",
    description:
      "The platform generates illustrative portfolio allocations to demonstrate diversification and different risk-return trade-offs.",
  },
  {
    title: "Monte Carlo simulation",
    description:
      "Repeated simulations show possible future portfolio outcomes, percentile ranges, downside risk, and uncertainty over time.",
  },
  {
    title: "Scam detection and warnings",
    description:
      "The platform will highlight suspicious digital asset projects and surface warning signals to improve risk awareness.",
  },
];

const workflowSteps = [
  {
    step: "01",
    title: "Answer onboarding questions",
    description:
      "Users complete a chatbot-style onboarding flow covering goals, budget, experience, time horizon, and risk attitude.",
  },
  {
    step: "02",
    title: "Receive a risk profile",
    description:
      "The backend interprets the onboarding responses and produces an explainable profile such as Conservative, Moderate, or Aggressive.",
  },
  {
    step: "03",
    title: "Explore portfolio and simulation outputs",
    description:
      "Users view educational portfolio scenarios and simulation metrics that explain risk exposure and potential uncertainty.",
  },
];

const highlights = [
  "Explainable outputs",
  "Educational only",
  "Backend-driven intelligence",
  "Risk-awareness focused",
];

export default function LandingPage() {
  return (
    <div style={styles.wrapper}>
      <header style={styles.topBar}>
        <div style={styles.brand}>FinSage</div>

        <nav style={styles.topNav}>
          <Link to="/login" style={styles.topNavLink}>
            Login
          </Link>
          <Link to="/register" style={styles.topNavButton}>
            Register
          </Link>
        </nav>
      </header>

      <section style={styles.heroCard}>
        <div style={styles.badge}>Educational digital asset risk platform</div>

        <h1 style={styles.title}>Learn digital asset risk with clarity, not hype.</h1>

        <p style={styles.subtitle}>
          FinSage is a backend-driven educational platform designed to help novice
          investors understand digital asset risk, scam signals, portfolio
          construction, and simulation outcomes through transparent and
          explainable outputs.
        </p>

        <div style={styles.actions}>
          <Link to="/register" style={styles.primaryButton}>
            Get started
          </Link>
          <Link to="/login" style={styles.secondaryButton}>
            Login
          </Link>
        </div>
      </section>

      <section style={styles.highlightStrip}>
        {highlights.map((item) => (
          <HighlightPill key={item} text={item} />
        ))}
      </section>

      <LandingSection
        label="Core platform capabilities"
        title="What the platform helps users understand"
        description="The frontend is designed around the same core workflow as the backend: onboarding, profiling, portfolio generation, simulation, and warning awareness."
      >
        <div style={styles.featuresGrid}>
          {featureCards.map((feature) => (
            <LandingFeatureCard
              key={feature.title}
              title={feature.title}
              description={feature.description}
            />
          ))}
        </div>
      </LandingSection>

      <LandingSection
        label="How it works"
        title="A structured learning flow"
        description="The platform is not built to give financial advice or support real trading. It is designed to improve financial literacy and risk awareness using explainable backend intelligence."
      >
        <div style={styles.workflowGrid}>
          {workflowSteps.map((item) => (
            <div key={item.step} style={styles.workflowCard}>
              <div style={styles.workflowStep}>{item.step}</div>
              <h3 style={styles.workflowTitle}>{item.title}</h3>
              <p style={styles.workflowDescription}>{item.description}</p>
            </div>
          ))}
        </div>
      </LandingSection>

      <section style={styles.ctaCard}>
        <div style={styles.ctaTextBlock}>
          <p style={styles.ctaLabel}>Ready to explore the platform?</p>
          <h2 style={styles.ctaTitle}>Create an account and begin the guided flow.</h2>
          <p style={styles.ctaDescription}>
            Register to access onboarding, generate your educational risk profile,
            and explore portfolio and simulation outputs designed to improve risk
            awareness.
          </p>
        </div>

        <div style={styles.ctaActions}>
          <Link to="/register" style={styles.primaryButton}>
            Register now
          </Link>
          <Link to="/login" style={styles.secondaryButton}>
            Login
          </Link>
        </div>
      </section>

      <footer style={styles.footer}>
        <div style={styles.footerBrand}>FinSage</div>
        <p style={styles.footerText}>
          Educational decision-support platform for digital asset risk awareness.
          No financial advice. No real trading.
        </p>
      </footer>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  wrapper: {
    minHeight: "100vh",
    display: "flex",
    flexDirection: "column",
    gap: "40px",
    padding: "24px 32px 40px 32px",
    background: "transparent",
    color: "#f5f7fb",
  },
  topBar: {
    maxWidth: "1120px",
    width: "100%",
    margin: "0 auto",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "8px 0",
  },
  brand: {
    fontSize: "1.4rem",
    fontWeight: 800,
    letterSpacing: "0.4px",
  },
  topNav: {
    display: "flex",
    alignItems: "center",
    gap: "14px",
  },
  topNavLink: {
    color: "#d6def2",
    fontWeight: 500,
  },
  topNavButton: {
    textDecoration: "none",
    background: "rgba(92, 123, 250, 0.18)",
    color: "#fff",
    padding: "10px 16px",
    borderRadius: "12px",
    border: "1px solid rgba(92, 123, 250, 0.24)",
    fontWeight: 700,
  },
  heroCard: {
    maxWidth: "1120px",
    width: "100%",
    margin: "0 auto",
    textAlign: "center",
    background:
      "linear-gradient(180deg, rgba(18,26,48,0.96) 0%, rgba(16,24,44,0.96) 100%)",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "30px",
    padding: "72px 42px",
    boxShadow: "0 22px 70px rgba(0,0,0,0.34)",
  },
  badge: {
    display: "inline-block",
    marginBottom: "18px",
    padding: "8px 14px",
    borderRadius: "999px",
    background: "rgba(92, 123, 250, 0.16)",
    border: "1px solid rgba(92, 123, 250, 0.25)",
    color: "#dce4ff",
    fontSize: "0.9rem",
    fontWeight: 600,
  },
  title: {
    fontSize: "3.6rem",
    lineHeight: 1.12,
    margin: "0 0 16px 0",
    maxWidth: "920px",
    marginInline: "auto",
  },
  subtitle: {
    fontSize: "1.08rem",
    lineHeight: 1.85,
    color: "#c7d2e6",
    margin: "0 auto 30px auto",
    maxWidth: "780px",
  },
  actions: {
    display: "flex",
    gap: "16px",
    justifyContent: "center",
    flexWrap: "wrap",
  },
  primaryButton: {
    textDecoration: "none",
    background: "#5c7bfa",
    color: "#fff",
    padding: "13px 24px",
    borderRadius: "12px",
    fontWeight: 700,
  },
  secondaryButton: {
    textDecoration: "none",
    background: "transparent",
    color: "#fff",
    padding: "13px 24px",
    borderRadius: "12px",
    border: "1px solid rgba(255,255,255,0.15)",
    fontWeight: 700,
  },
  highlightStrip: {
    maxWidth: "1120px",
    width: "100%",
    margin: "0 auto",
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
    gap: "14px",
  },
  featuresGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
    gap: "18px",
  },
  workflowGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
    gap: "18px",
  },
  workflowCard: {
    background: "linear-gradient(180deg, #121a30 0%, #10182c 100%)",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "22px",
    padding: "24px",
    boxShadow: "0 12px 30px rgba(0,0,0,0.18)",
  },
  workflowStep: {
    width: "42px",
    height: "42px",
    borderRadius: "50%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "rgba(92, 123, 250, 0.18)",
    color: "#ffffff",
    fontWeight: 700,
    marginBottom: "16px",
  },
  workflowTitle: {
    marginTop: 0,
    marginBottom: "12px",
    fontSize: "1.05rem",
  },
  workflowDescription: {
    margin: 0,
    color: "#c7d2e6",
    lineHeight: 1.7,
    fontSize: "0.95rem",
  },
  ctaCard: {
    maxWidth: "1120px",
    width: "100%",
    margin: "0 auto 8px auto",
    background: "linear-gradient(180deg, #121a30 0%, #10182c 100%)",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "26px",
    padding: "34px",
    boxShadow: "0 20px 60px rgba(0,0,0,0.25)",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "20px",
    flexWrap: "wrap",
  },
  ctaTextBlock: {
    maxWidth: "760px",
  },
  ctaLabel: {
    margin: 0,
    color: "#8fa1c7",
    fontSize: "0.9rem",
    fontWeight: 600,
    textTransform: "uppercase",
    letterSpacing: "0.5px",
  },
  ctaTitle: {
    margin: "6px 0 10px 0",
    fontSize: "1.8rem",
  },
  ctaDescription: {
    margin: 0,
    color: "#c7d2e6",
    lineHeight: 1.7,
  },
  ctaActions: {
    display: "flex",
    alignItems: "center",
    gap: "14px",
    flexWrap: "wrap",
  },
  footer: {
    maxWidth: "1120px",
    width: "100%",
    margin: "0 auto",
    paddingTop: "8px",
    borderTop: "1px solid rgba(255,255,255,0.08)",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "16px",
    flexWrap: "wrap",
  },
  footerBrand: {
    fontSize: "1.05rem",
    fontWeight: 700,
  },
  footerText: {
    margin: 0,
    color: "#8fa1c7",
    lineHeight: 1.6,
  },
};