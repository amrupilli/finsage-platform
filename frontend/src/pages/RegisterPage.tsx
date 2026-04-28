import { useState } from "react";
import { Link } from "react-router-dom";
import AuthCard from "../components/AuthCard";
import { apiRequest } from "../lib/api";

type RegisterResponse = {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  created_at: string;
};

export default function RegisterPage() {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setSuccessMessage("");
    setErrorMessage("");
    setIsSubmitting(true);

    try {
      const response = await apiRequest<RegisterResponse>("/auth/register", {
        method: "POST",
        body: JSON.stringify({
          email,
          full_name: fullName,
          password,
        }),
      });

      setSuccessMessage(
        `Account created successfully for ${response.email}. You can now log in.`
      );

      setFullName("");
      setEmail("");
      setPassword("");
    } catch (error) {
      if (error instanceof Error) {
        setErrorMessage(error.message);
      } else {
        setErrorMessage("Registration failed.");
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <AuthCard
      title="Create your account"
      description="Register to access the FinSage platform and begin the onboarding process."
    >
      <form onSubmit={handleSubmit} style={styles.form}>
        <label style={styles.label}>
          Full name
          <input
            type="text"
            value={fullName}
            onChange={(event) => setFullName(event.target.value)}
            placeholder="Amrutha Nair"
            required
            style={styles.input}
          />
        </label>

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
            placeholder="Enter a secure password"
            required
            style={styles.input}
          />
        </label>

        <button type="submit" disabled={isSubmitting} style={styles.button}>
          {isSubmitting ? "Creating account..." : "Register"}
        </button>

        {successMessage && <p style={styles.success}>{successMessage}</p>}
        {errorMessage && <p style={styles.error}>{errorMessage}</p>}
      </form>

      <p style={styles.footerText}>
        Already have an account?{" "}
        <Link to="/login" style={styles.link}>
          Go to login
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
  success: {
    margin: 0,
    color: "#2ecc71",
    lineHeight: 1.6,
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