import { Link, Outlet, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const navItems = [
  { label: "Dashboard", path: "/dashboard" },
  { label: "Onboarding", path: "/onboarding" },
  { label: "Portfolio", path: "/portfolio" },
  { label: "Simulation", path: "/simulation" },
  { label: "Warnings", path: "/warnings" },
  { label: "Settings", path: "/settings" },
];

export default function AppShell() {
  const location = useLocation();
  const navigate = useNavigate();
  const { logout } = useAuth();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <div style={styles.app}>
      <aside style={styles.sidebar}>
        <div>
          <div style={styles.logo}>FinSage</div>
          <p style={styles.tagline}>Educational digital asset risk platform</p>
        </div>

        <nav style={styles.nav}>
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;

            return (
              <Link
                key={item.path}
                to={item.path}
                style={{
                  ...styles.navLink,
                  ...(isActive ? styles.navLinkActive : {}),
                }}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div style={styles.footerCard}>
          <p style={styles.footerTitle}>System status</p>
          <p style={styles.footerText}>
            Backend-connected educational workflow for profiling, portfolios,
            simulation, and warnings.
          </p>

          <button onClick={handleLogout} style={styles.logoutButton}>
            Logout
          </button>
        </div>
      </aside>

      <main style={styles.main}>
        <div style={styles.topBar}>
          <div>
            <p style={styles.topBarLabel}>Workspace</p>
            <h2 style={styles.topBarTitle}>FinSage Platform</h2>
          </div>
        </div>

        <div style={styles.pageContent}>
          <Outlet />
        </div>
      </main>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  app: {
    display: "flex",
    minHeight: "100vh",
    background: "transparent",
    color: "#f5f7fb",
  },
  sidebar: {
    width: "260px",
    background: "rgba(18, 26, 48, 0.94)",
    borderRight: "1px solid rgba(255,255,255,0.08)",
    padding: "24px 18px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
    gap: "28px",
    backdropFilter: "blur(8px)",
  },
  logo: {
    fontSize: "1.6rem",
    fontWeight: 800,
    letterSpacing: "0.4px",
    marginBottom: "8px",
  },
  tagline: {
    margin: 0,
    color: "#c7d2e6",
    fontSize: "0.95rem",
    lineHeight: 1.6,
  },
  nav: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  navLink: {
    color: "#c7d2e6",
    textDecoration: "none",
    padding: "12px 14px",
    borderRadius: "14px",
    transition: "0.2s ease",
    background: "transparent",
    border: "1px solid transparent",
    fontWeight: 500,
  },
  navLinkActive: {
    background: "rgba(92, 123, 250, 0.16)",
    color: "#ffffff",
    border: "1px solid rgba(92, 123, 250, 0.25)",
  },
  footerCard: {
    background: "#18213b",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "18px",
    padding: "16px",
  },
  footerTitle: {
    margin: "0 0 8px 0",
    fontWeight: 700,
  },
  footerText: {
    margin: "0 0 16px 0",
    color: "#c7d2e6",
    lineHeight: 1.6,
    fontSize: "0.92rem",
  },
  logoutButton: {
    width: "100%",
    background: "transparent",
    border: "1px solid rgba(255,255,255,0.12)",
    color: "#f5f7fb",
    borderRadius: "12px",
    padding: "10px 12px",
    cursor: "pointer",
    fontWeight: 600,
  },
  main: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    padding: "24px 28px",
    gap: "20px",
  },
  topBar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    paddingBottom: "8px",
  },
  topBarLabel: {
    margin: 0,
    color: "#8fa1c7",
    fontSize: "0.9rem",
  },
  topBarTitle: {
    margin: "4px 0 0 0",
    fontSize: "1.8rem",
  },
  pageContent: {
    flex: 1,
  },
};