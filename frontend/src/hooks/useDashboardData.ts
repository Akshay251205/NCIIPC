import { useCallback, useEffect, useState } from "react";
import { getDashboardData, type IntelligenceSummary, type Overview, type RiskSummary } from "../api/dashboard";

export function useDashboardData() {
  const [overview, setOverview] = useState<Overview | null>(null);
  const [intelligence, setIntelligence] = useState<IntelligenceSummary | null>(null);
  const [risk, setRisk] = useState<RiskSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getDashboardData();
      setOverview(data.overview);
      setIntelligence(data.intelligence);
      setRisk(data.risk);
      setError(null);
    } catch {
      setError("Live data is temporarily unavailable. Showing the last available dashboard state.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const timer = window.setTimeout(() => { void refresh(); }, 0);
    return () => window.clearTimeout(timer);
  }, [refresh]);
  return { overview, intelligence, risk, loading, error, refresh };
}
