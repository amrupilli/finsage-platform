import { Route, Routes } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";
import AppShell from "./layouts/AppShell";
import LandingPage from "./pages/LandingPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import OnboardingPage from "./pages/OnboardingPage";
import DashboardPage from "./pages/DashboardPage";
import PortfolioPage from "./pages/PortfolioPage";
import SimulationPage from "./pages/SimulationPage";
import WarningsPage from "./pages/WarningsPage";
import SettingsPage from "./pages/SettingsPage";
import OnboardingReviewPage from "./pages/OnboardingReviewPage";
import ScamDetectionPage from "./pages/ScamDetectionPage";
import InvestmentCheckPage from "./pages/InvestmentCheckPage";
export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      <Route element={<ProtectedRoute />}>
        <Route element={<AppShell />}>
          <Route path="/onboarding" element={<OnboardingPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/portfolio" element={<PortfolioPage />} />
          <Route path="/simulation" element={<SimulationPage />} />
          <Route path="/warnings" element={<WarningsPage />} />
          <Route path="/onboarding/review" element={<OnboardingReviewPage />} />
          <Route path="/investment-check" element={<InvestmentCheckPage />} />
          <Route path="/scam-check" element={<ScamDetectionPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Route>
      </Route>
    </Routes>
  );
}