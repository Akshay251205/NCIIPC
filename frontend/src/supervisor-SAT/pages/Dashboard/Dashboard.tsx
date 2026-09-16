import {
  Building2,
  Bell,
  AlertTriangle,
  ShieldAlert,
  TrendingUp,
  TrendingDown,
  Clock,
  Eye,
  RefreshCw,
} from "lucide-react";

import "./Dashboard.css";
import { useNavigate } from "react-router-dom";
import { useDashboardData } from "../../../hooks/useDashboardData";

const organizations = [
  {
    name: "Organization Alpha",
    score: 86,
    level: "Critical",
  },
  {
    name: "Organization Beta",
    score: 74,
    level: "High",
  },
  {
    name: "Organization Gamma",
    score: 68,
    level: "High",
  },
  {
    name: "Organization Delta",
    score: 52,
    level: "Medium",
  },
  {
    name: "Organization Epsilon",
    score: 34,
    level: "Low",
  },
];

const findings = [
  {
    title: "Low Evidence Investigation",
    organization: "Organization Alpha",
    severity: "Critical",
    time: "18 min ago",
  },
  {
    title: "Unusual Analyst Behavior",
    organization: "Organization Beta",
    severity: "High",
    time: "42 min ago",
  },
  {
    title: "Fast Alert Closure",
    organization: "Organization Gamma",
    severity: "High",
    time: "1 hr ago",
  },
  {
    title: "Peer Benchmark Outlier",
    organization: "Organization Delta",
    severity: "Medium",
    time: "2 hrs ago",
  },
];

function getSeverityClass(level: string) {
  return level.toLowerCase();
}

export default function Dashboard() {
  const navigate = useNavigate();
  const { overview, intelligence, loading, error, refresh } = useDashboardData();
  const dashboardKpis = [
    { title: "Organizations", value: overview?.total_organizations.toLocaleString() ?? "—", change: "Live data", trend: "up", icon: Building2 },
    { title: "Open Alerts", value: overview?.open_alerts.toLocaleString() ?? "—", change: "Live data", trend: "down", icon: Bell },
    { title: "Priority Findings", value: intelligence?.analysts_requiring_attention.toLocaleString() ?? "—", change: "Needs review", trend: "up", icon: AlertTriangle },
    { title: "Critical Alerts", value: overview?.critical_alerts.toLocaleString() ?? "—", change: "Live data", trend: "down", icon: ShieldAlert },
  ];
  const severityItems = ["CRITICAL", "HIGH", "MEDIUM", "LOW"].map((level) => {
    const value = intelligence?.risk_distribution[level as keyof NonNullable<typeof intelligence>["risk_distribution"]] ?? 0;
    const total = intelligence?.analysts_analyzed ?? 0;
    return { label: `${level[0]}${level.slice(1).toLowerCase()}`, value, percentage: total ? Math.round((value / total) * 100) : 0 };
  });
  const riskScore = intelligence?.average_risk_score ?? 0;
  return (
    <div className="dashboard">
      {/* Page Header */}
      <div className="dashboard-header">
        <div>
          <h1>Supervisor Dashboard</h1>

          <p>
            Overview of security operations and assessment health.
          </p>
        </div>

        <div className="dashboard-date">
          <span>Assessment Overview</span>
          <strong>Current Period</strong>
        </div>
        <button className="dashboard-refresh" onClick={() => void refresh()} disabled={loading}>
          <RefreshCw size={15} className={loading ? "spinning" : ""} /> {loading ? "Refreshing" : "Refresh live data"}
        </button>
      </div>

      {error && <div className="dashboard-data-message" role="status">{error}</div>}

      {/* KPI Cards */}
      <section className="kpi-grid">
        {dashboardKpis.map((item) => {
          const Icon = item.icon;

          return (
            <div className="kpi-card" key={item.title}>
              <div className="kpi-top">
                <div className="kpi-icon">
                  <Icon size={21} />
                </div>

                <span
                  className={`kpi-trend ${item.trend}`}
                >
                  {item.trend === "up" ? (
                    <TrendingUp size={14} />
                  ) : (
                    <TrendingDown size={14} />
                  )}

                  {item.change}
                </span>
              </div>

              <p className="kpi-title">{item.title}</p>

              <h2>{item.value}</h2>

              <p className="kpi-description">
                Compared with previous period
              </p>
            </div>
          );
        })}
      </section>

      {/* Main Analytics Row */}
      <section className="analytics-grid">
        {/* Risk Overview */}
        <div className="dashboard-card risk-card">
          <div className="card-header">
            <div>
              <h3>Risk Overview</h3>
              <p>Overall assessment health</p>
            </div>

            <span className="status-pill">
              Monitoring
            </span>
          </div>

          <div className="risk-content">
            <div className="risk-score">
              <div
                className="risk-circle"
                style={{
                  background: `conic-gradient(#2563eb ${riskScore}%, #e5e7eb ${riskScore}% 100%)`,
                }}
              >
                <div>
                  <strong>{Math.round(riskScore)}</strong>
                  <span>/100</span>
                </div>
              </div>

              <div>
                <p className="risk-label">Overall Risk Score</p>

                <h4>{riskScore >= 80 ? "Critical Risk" : riskScore >= 60 ? "High Risk" : riskScore >= 40 ? "Moderate Risk" : "Low Risk"}</h4>

                <p className="risk-description">
                  Security operations require continued
                  supervisor attention.
                </p>
              </div>
            </div>

            <div className="risk-metrics">
              <div>
                <span>Investigation Quality</span>
                <strong>82%</strong>
              </div>

              <div>
                <span>Evidence Coverage</span>
                <strong>76%</strong>
              </div>

              <div>
                <span>Escalation Rate</span>
                <strong>64%</strong>
              </div>
            </div>
          </div>
        </div>

        {/* Alert Severity */}
        <div className="dashboard-card">
          <div className="card-header">
            <div>
              <h3>Alert Severity</h3>
              <p>Current alert distribution</p>
            </div>

            <Bell size={19} className="card-icon" />
          </div>

          <div className="severity-list">
            {severityItems.map((item) => (
              <div
                className="severity-row"
                key={item.label}
              >
                <div className="severity-info">
                  <span
                    className={`severity-dot ${getSeverityClass(
                      item.label
                    )}`}
                  ></span>

                  <span>{item.label}</span>

                  <strong>{item.value}</strong>
                </div>

                <div className="severity-bar">
                  <div
                    className={`severity-fill ${getSeverityClass(
                      item.label
                    )}`}
                    style={{
                      width: `${item.percentage}%`,
                    }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Bottom Analytics */}
      <section className="bottom-grid">
        {/* Top Risk Organizations */}
        <div className="dashboard-card">
          <div className="card-header">
            <div>
              <h3>Top Risk Organizations</h3>
              <p>Organizations requiring attention</p>
            </div>

            <button className="view-button" onClick={() => navigate("/supervisor/organizations")}>
              View all
            </button>
          </div>

          <div className="organization-list">
            {organizations.map((organization, index) => (
              <div
                className="organization-row"
                key={organization.name}
              >
                <div className="organization-rank">
                  {index + 1}
                </div>

                <div className="organization-info">
                  <strong>{organization.name}</strong>

                  <span
                    className={`risk-badge ${getSeverityClass(
                      organization.level
                    )}`}
                  >
                    {organization.level}
                  </span>
                </div>

                <div className="organization-score">
                  <strong>{organization.score}</strong>
                  <span>/100</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Findings */}
        <div className="dashboard-card">
          <div className="card-header">
            <div>
              <h3>Recent Priority Findings</h3>
              <p>Issues requiring supervisor review</p>
            </div>

            <button className="view-button" onClick={() => navigate("/supervisor/findings")}>
              View all
            </button>
          </div>

          <div className="findings-list">
            {findings.map((finding) => (
              <div
                className="finding-row"
                key={finding.title}
              >
                <div className="finding-icon">
                  <AlertTriangle size={17} />
                </div>

                <div className="finding-info">
                  <strong>{finding.title}</strong>

                  <span>{finding.organization}</span>
                </div>

                <div className="finding-meta">
                  <span
                    className={`risk-badge ${getSeverityClass(
                      finding.severity
                    )}`}
                  >
                    {finding.severity}
                  </span>

                  <small>
                    <Clock size={12} />
                    {finding.time}
                  </small>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Assessment Attention */}
      <section className="attention-banner">
        <div className="attention-icon">
          <Eye size={21} />
        </div>

        <div>
          <strong>Supervisor Attention Required</strong>

          <p>
            12 critical alerts and 23 priority findings
            currently require review.
          </p>
        </div>

        <button onClick={() => navigate("/supervisor/findings")}>
          Review Findings
        </button>
      </section>
    </div>
  );
}
