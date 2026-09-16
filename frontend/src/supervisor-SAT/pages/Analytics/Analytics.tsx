import {
  Activity,
  AlertTriangle,
  BarChart3,
  CheckCircle,
  Clock,
  ShieldAlert,
  TrendingDown,
  TrendingUp,
} from "lucide-react";
import "./Analytics.css";

const organizationPerformance = [
  {
    name: "Organization Alpha",
    riskScore: 86,
    investigationQuality: 82,
    evidenceCoverage: 64,
    closureRate: 58,
  },
  {
    name: "Organization Beta",
    riskScore: 68,
    investigationQuality: 76,
    evidenceCoverage: 72,
    closureRate: 71,
  },
  {
    name: "Organization Gamma",
    riskScore: 74,
    investigationQuality: 69,
    evidenceCoverage: 61,
    closureRate: 63,
  },
  {
    name: "Organization Delta",
    riskScore: 52,
    investigationQuality: 81,
    evidenceCoverage: 79,
    closureRate: 84,
  },
];

const analystPerformance = [
  {
    name: "Aarav Sharma",
    organization: "Alpha",
    performance: 88,
    closure: 91,
    evidence: 88,
  },
  {
    name: "Priya Singh",
    organization: "Alpha",
    performance: 68,
    closure: 68,
    evidence: 61,
  },
  {
    name: "Rahul Verma",
    organization: "Beta",
    performance: 86,
    closure: 87,
    evidence: 82,
  },
  {
    name: "Ananya Gupta",
    organization: "Gamma",
    performance: 55,
    closure: 54,
    evidence: 48,
  },
  {
    name: "Vikram Mehta",
    organization: "Beta",
    performance: 84,
    closure: 84,
    evidence: 79,
  },
];

const monthlyAlerts = [
  { month: "Apr", alerts: 112 },
  { month: "May", alerts: 128 },
  { month: "Jun", alerts: 141 },
  { month: "Jul", alerts: 136 },
  { month: "Aug", alerts: 154 },
  { month: "Sep", alerts: 148 },
];

function Analytics() {
  return (
    <div className="analytics-page">
      <div className="analytics-header">
        <div>
          <h1>Analytics</h1>
          <p>
            Monitor SOC performance, risk trends, and peer benchmark insights.
          </p>
        </div>

        <button className="analytics-period">
          Last 6 Months
        </button>
      </div>

      {/* KPI Cards */}
      <div className="analytics-kpi-grid">
        <div className="analytics-kpi-card">
          <div className="analytics-kpi-icon blue">
            <Activity size={21} />
          </div>

          <div>
            <span>Total Alerts</span>
            <strong>819</strong>
            <small className="positive">
              <TrendingDown size={13} />
              4.2% vs previous period
            </small>
          </div>
        </div>

        <div className="analytics-kpi-card">
          <div className="analytics-kpi-icon red">
            <ShieldAlert size={21} />
          </div>

          <div>
            <span>Average Risk Score</span>
            <strong>70</strong>
            <small className="negative">
              <TrendingUp size={13} />
              6.8% increase
            </small>
          </div>
        </div>

        <div className="analytics-kpi-card">
          <div className="analytics-kpi-icon green">
            <CheckCircle size={21} />
          </div>

          <div>
            <span>Investigation Completion</span>
            <strong>81%</strong>
            <small className="positive">
              <TrendingUp size={13} />
              3.4% improvement
            </small>
          </div>
        </div>

        <div className="analytics-kpi-card">
          <div className="analytics-kpi-icon orange">
            <Clock size={21} />
          </div>

          <div>
            <span>Avg Closure Time</span>
            <strong>5.2 hrs</strong>
            <small className="positive">
              <TrendingDown size={13} />
              8.1% faster
            </small>
          </div>
        </div>
      </div>

      {/* Main Analytics Grid */}
      <div className="analytics-main-grid">
        {/* Alert Trend */}
        <div className="analytics-card alert-trend-card">
          <div className="analytics-card-header">
            <div>
              <h2>Alert Volume Trend</h2>
              <p>Monthly alert activity across organizations</p>
            </div>

            <BarChart3 size={20} />
          </div>

          <div className="bar-chart">
            {monthlyAlerts.map((item) => {
              const height = (item.alerts / 160) * 100;

              return (
                <div className="bar-column" key={item.month}>
                  <span>{item.alerts}</span>

                  <div className="bar-wrapper">
                    <div
                      className="bar"
                      style={{ height: `${height}%` }}
                    />
                  </div>

                  <small>{item.month}</small>
                </div>
              );
            })}
          </div>
        </div>

        {/* Risk Distribution */}
        <div className="analytics-card">
          <div className="analytics-card-header">
            <div>
              <h2>Risk Distribution</h2>
              <p>Current organization risk levels</p>
            </div>

            <ShieldAlert size={20} />
          </div>

          <div className="risk-distribution">
            <div className="risk-row">
              <div className="risk-label">
                <span className="risk-dot critical" />
                Critical
                <strong>1</strong>
              </div>

              <div className="risk-progress">
                <div
                  className="risk-progress-fill critical-fill"
                  style={{ width: "25%" }}
                />
              </div>
            </div>

            <div className="risk-row">
              <div className="risk-label">
                <span className="risk-dot high" />
                High
                <strong>2</strong>
              </div>

              <div className="risk-progress">
                <div
                  className="risk-progress-fill high-fill"
                  style={{ width: "50%" }}
                />
              </div>
            </div>

            <div className="risk-row">
              <div className="risk-label">
                <span className="risk-dot medium" />
                Medium
                <strong>1</strong>
              </div>

              <div className="risk-progress">
                <div
                  className="risk-progress-fill medium-fill"
                  style={{ width: "25%" }}
                />
              </div>
            </div>

            <div className="risk-summary">
              <AlertTriangle size={18} />
              <div>
                <strong>3 organizations</strong>
                <span>require closer monitoring</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Organization Performance */}
      <div className="analytics-card">
        <div className="analytics-card-header">
          <div>
            <h2>Organization Performance</h2>
            <p>
              Compare investigation and evidence quality across organizations.
            </p>
          </div>
        </div>

        <div className="performance-table-wrapper">
          <table className="performance-table">
            <thead>
              <tr>
                <th>Organization</th>
                <th>Risk Score</th>
                <th>Investigation Quality</th>
                <th>Evidence Coverage</th>
                <th>Closure Rate</th>
              </tr>
            </thead>

            <tbody>
              {organizationPerformance.map((organization) => (
                <tr key={organization.name}>
                  <td>
                    <strong>{organization.name}</strong>
                  </td>

                  <td>
                    <span
                      className={`score-badge ${
                        organization.riskScore >= 80
                          ? "critical-score"
                          : organization.riskScore >= 70
                            ? "high-score"
                            : "normal-score"
                      }`}
                    >
                      {organization.riskScore}
                    </span>
                  </td>

                  <td>
                    <div className="metric-cell">
                      <span>{organization.investigationQuality}%</span>
                      <div className="metric-bar">
                        <div
                          style={{
                            width: `${organization.investigationQuality}%`,
                          }}
                        />
                      </div>
                    </div>
                  </td>

                  <td>
                    <div className="metric-cell">
                      <span>{organization.evidenceCoverage}%</span>
                      <div className="metric-bar">
                        <div
                          style={{
                            width: `${organization.evidenceCoverage}%`,
                          }}
                        />
                      </div>
                    </div>
                  </td>

                  <td>
                    <div className="metric-cell">
                      <span>{organization.closureRate}%</span>
                      <div className="metric-bar">
                        <div
                          style={{
                            width: `${organization.closureRate}%`,
                          }}
                        />
                      </div>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Analyst Performance + Peer Benchmark */}
      <div className="analytics-bottom-grid">
        <div className="analytics-card">
          <div className="analytics-card-header">
            <div>
              <h2>Analyst Performance</h2>
              <p>Top analysts by overall performance</p>
            </div>
          </div>

          <div className="analyst-performance-list">
            {analystPerformance.map((analyst) => (
              <div className="analyst-performance-item" key={analyst.name}>
                <div className="analyst-avatar">
                  {analyst.name
                    .split(" ")
                    .map((word) => word[0])
                    .join("")}
                </div>

                <div className="analyst-info">
                  <strong>{analyst.name}</strong>
                  <span>{analyst.organization}</span>
                </div>

                <div className="analyst-score">
                  <strong>{analyst.performance}</strong>
                  <span>Performance</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Peer Benchmark */}
        <div className="analytics-card benchmark-card">
          <div className="analytics-card-header">
            <div>
              <h2>Peer Benchmark</h2>
              <p>Organization Alpha vs peer average</p>
            </div>
          </div>

          <div className="benchmark-summary">
            <div className="benchmark-score">
              <span>Your Organization</span>
              <strong>86</strong>
              <small>Risk Score</small>
            </div>

            <div className="benchmark-vs">VS</div>

            <div className="benchmark-score peer">
              <span>Peer Average</span>
              <strong>61</strong>
              <small>Risk Score</small>
            </div>
          </div>

          <div className="benchmark-metrics">
            <div>
              <span>Investigation Quality</span>
              <strong>82% vs 74%</strong>
            </div>

            <div>
              <span>Evidence Coverage</span>
              <strong>64% vs 71%</strong>
            </div>

            <div>
              <span>Closure Rate</span>
              <strong>58% vs 69%</strong>
            </div>
          </div>

          <div className="benchmark-warning">
            <AlertTriangle size={18} />

            <div>
              <strong>Performance gap detected</strong>
              <span>
                Evidence coverage and closure rate are below the peer average.
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Insight */}
      <div className="analytics-insight">
        <div className="insight-icon">
          <Activity size={21} />
        </div>

        <div>
          <strong>Supervisor Insight</strong>
          <p>
            Organization Alpha currently has the highest risk score in the
            portfolio. Investigation quality remains strong, but evidence
            coverage and alert closure performance require improvement.
          </p>
        </div>
      </div>
    </div>
  );
}

export default Analytics;