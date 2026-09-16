export type Overview = {
  total_organizations: number;
  total_analysts: number;
  total_assets: number;
  total_alerts: number;
  total_incidents: number;
  total_investigations: number;
  open_alerts: number;
  critical_alerts: number;
};

export type IntelligenceSummary = {
  analysts_analyzed: number;
  alerts_analyzed: number;
  investigations_analyzed: number;
  analysts_requiring_attention: number;
  average_risk_score: number;
  risk_distribution: Record<"LOW" | "MEDIUM" | "HIGH" | "CRITICAL", number>;
};

export type RiskSummary = {
  overall_risk_score: number;
  severity: string;
  critical_alerts: number;
  high_alerts: number;
  medium_alerts: number;
  low_alerts: number;
};

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`Request failed (${response.status})`);
  return response.json() as Promise<T>;
}

export async function getDashboardData() {
  const [overviewResponse, intelligenceResponse, riskResponse] = await Promise.all([
    getJson<{ success: boolean; data: Overview }>("/api/v1/dashboard/overview"),
    getJson<{ summary: IntelligenceSummary }>("/intelligence/summary"),
    getJson<{ success: boolean; data: RiskSummary }>("/api/v1/dashboard/risk-summary"),
  ]);
  return { overview: overviewResponse.data, intelligence: intelligenceResponse.summary, risk: riskResponse.data };
}
