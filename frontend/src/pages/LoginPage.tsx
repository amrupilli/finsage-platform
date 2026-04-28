import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import AuthCard from "../components/AuthCard";
import { useAuth } from "../context/AuthContext";
import { apiRequest } from "../lib/api";

type LoginResponse = {
  access_token: string;
  token_type: string;
};

export default function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setErrorMessage("");
    setIsSubmitting(true);

    try {
      const response = await apiRequest<LoginResponse>("/auth/login", {
        method: "POST",
        body: JSON.stringify({
          email,
          password,
        }),
      });

      login(response.access_token);

      navigate("/dashboard");
    } catch (error) {
      if (error instanceof Error) {
        setErrorMessage(error.message);
      } else {
        setErrorMessage("Login failed.");
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <AuthCard
      title="Welcome back"
      description="Log in to access your account, continue onboarding, and view your risk and portfolio outputs."
    >
      <form onSubmit={handleSubmit} style={styles.form}>
        <label style={styles.label}>
          Email
          <input
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="you@example.com"
            required
            style={styles.input}
          />
        </label>

        <label style={styles.label}>
          Password
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="Enter your password"
            required
            style={styles.input}
          />
        </label>

        <button type="submit" disabled={isSubmitting} style={styles.button}>
          {isSubmitting ? "Logging in..." : "Login"}
        </button>

        {errorMessage && <p style={styles.error}>{errorMessage}</p>}
      </form>

      <p style={styles.footerText}>
        Don&apos;t have an account?{" "}
        <Link to="/register" style={styles.link}>
          Create one
        </Link>
      </p>
    </AuthCard>
  );
}

const styles: Record<string, React.CSSProperties> = {
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "16px",
  },
  label: {
    display: "flex",
    flexDirection: "column",
    gap: "8px",
    fontWeight: 500,
    color: "#f5f7fb",
  },
  input: {
    background: "#18213b",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "12px",
    padding: "12px 14px",
    color: "#f5f7fb",
    outline: "none",
  },
  button: {
    marginTop: "8px",
    background: "#5c7bfa",
    color: "#ffffff",
    border: "none",
    borderRadius: "12px",
    padding: "13px 16px",
    fontWeight: 700,
    cursor: "pointer",
  },
  error: {
    margin: 0,
    color: "#ff6b6b",
    lineHeight: 1.6,
  },
  footerText: {
    margin: 0,
    color: "#c7d2e6",
  },
  link: {
    color: "#8fb3ff",
    fontWeight: 600,
  },
};