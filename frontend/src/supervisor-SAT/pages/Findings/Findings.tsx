import {
  AlertTriangle,
  ShieldAlert,
  Search,
  Filter,
  ChevronRight,
  CheckCircle2,
  Clock,
  Building2,
  User,
  TrendingUp,
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import "./Findings.css";

const findings = [
  {
    id: "FND-001",
    title: "Potential Privileged Account Compromise",
    organization: "Organization Alpha",
    alertId: "ALT-1001",
    category: "Account Security",
    riskScore: 94,
    severity: "Critical",
    status: "Requires Action",
    analyst: "Aarav Sharma",
    detected: "12 min ago",
  },
  {
    id: "FND-002",
    title: "Unusual Network Communication Pattern",
    organization: "Organization Beta",
    alertId: "ALT-1002",
    category: "Network Security",
    riskScore: 87,
    severity: "High",
    status: "Under Review",
    analyst: "Rahul Verma",
    detected: "28 min ago",
  },
  {
    id: "FND-003",
    title: "Repeated Authentication Failures",
    organization: "Organization Alpha",
    alertId: "ALT-1003",
    category: "Authentication",
    riskScore: 82,
    severity: "High",
    status: "Requires Action",
    analyst: "Priya Singh",
    detected: "41 min ago",
  },
  {
    id: "FND-004",
    title: "Endpoint Security Control Degradation",
    organization: "Organization Gamma",
    alertId: "ALT-1004",
    category: "Endpoint Security",
    riskScore: 74,
    severity: "High",
    status: "Under Review",
    analyst: "Ananya Gupta",
    detected: "1 hr ago",
  },
  {
    id: "FND-005",
    title: "Abnormal DNS Request Activity",
    organization: "Organization Delta",
    alertId: "ALT-1005",
    category: "Network Security",
    riskScore: 69,
    severity: "Medium",
    status: "Monitoring",
    analyst: "Neha Kapoor",
    detected: "2 hrs ago",
  },
  {
    id: "FND-006",
    title: "Potential Policy Violation",
    organization: "Organization Beta",
    alertId: "ALT-1006",
    category: "Policy",
    riskScore: 61,
    severity: "Medium",
    status: "Monitoring",
    analyst: "Vikram Mehta",
    detected: "3 hrs ago",
  },
];

export default function Findings() {
  const navigate = useNavigate();

  return (
    <div className="findings-page">
      {/* Header */}
      <div className="findings-header">
        <div>
          <div className="page-label">SUPERVISOR</div>
          <h1>Priority Findings</h1>
          <p>
            Review the most important security findings requiring
            supervisor attention.
          </p>
        </div>

        <div className="findings-header-badge">
          <ShieldAlert size={18} />
          6 Priority Findings
        </div>
      </div>

      {/* KPI Cards */}
      <div className="findings-kpi-grid">
        <div className="finding-kpi-card critical-card">
          <div className="finding-kpi-icon">
            <ShieldAlert size={21} />
          </div>

          <div>
            <span>Critical Findings</span>
            <strong>1</strong>
            <small>Immediate action required</small>
          </div>
        </div>

        <div className="finding-kpi-card">
          <div className="finding-kpi-icon">
            <AlertTriangle size={21} />
          </div>

          <div>
            <span>High Risk Findings</span>
            <strong>3</strong>
            <small>Require supervisor review</small>
          </div>
        </div>

        <div className="finding-kpi-card">
          <div className="finding-kpi-icon">
            <Clock size={21} />
          </div>

          <div>
            <span>Requires Action</span>
            <strong>2</strong>
            <small>Waiting for decision</small>
          </div>
        </div>

        <div className="finding-kpi-card">
          <div className="finding-kpi-icon">
            <TrendingUp size={21} />
          </div>

          <div>
            <span>Average Risk Score</span>
            <strong>78</strong>
            <small>Across priority findings</small>
          </div>
        </div>
      </div>

      {/* Attention Banner */}
      <div className="findings-attention-banner">
        <div className="attention-icon">
          <ShieldAlert size={20} />
        </div>

        <div>
          <strong>Immediate supervisor attention required</strong>
          <p>
            1 critical finding has a risk score above 90 and requires
            immediate review.
          </p>
        </div>
      </div>

      {/* Findings Table */}
      <section className="findings-table-section">
        <div className="findings-table-header">
          <div>
            <h2>Priority Findings</h2>
            <p>Ranked by security risk and supervisor priority.</p>
          </div>

          <div className="findings-tools">
            <div className="findings-search">
              <Search size={17} />
              <input placeholder="Search findings..." />
            </div>

            <button className="findings-filter-button">
              <Filter size={17} />
              Filter
            </button>
          </div>
        </div>

        <div className="findings-table-wrapper">
          <table className="findings-table">
            <thead>
              <tr>
                <th>Finding</th>
                <th>Organization</th>
                <th>Risk Score</th>
                <th>Severity</th>
                <th>Status</th>
                <th>Analyst</th>
                <th>Detected</th>
                <th></th>
              </tr>
            </thead>

            <tbody>
              {findings.map((finding) => (
                <tr key={finding.id}>
                  <td>
                    <div className="finding-name">
                      <div className="finding-row-icon">
                        <AlertTriangle size={17} />
                      </div>

                      <div>
                        <strong>{finding.title}</strong>
                        <span>
                          {finding.id} • {finding.category}
                        </span>
                      </div>
                    </div>
                  </td>

                  <td>
                    <div className="organization-cell">
                      <Building2 size={15} />
                      {finding.organization}
                    </div>
                  </td>

                  <td>
                    <div
                      className={`risk-score ${
                        finding.riskScore >= 90
                          ? "risk-critical"
                          : finding.riskScore >= 80
                            ? "risk-high"
                            : "risk-medium"
                      }`}
                    >
                      {finding.riskScore}
                    </div>
                  </td>

                  <td>
                    <span
                      className={`severity-badge severity-${finding.severity.toLowerCase()}`}
                    >
                      {finding.severity}
                    </span>
                  </td>

                  <td>
                    <span
                      className={`finding-status status-${finding.status
                        .toLowerCase()
                        .replace(" ", "-")}`}
                    >
                      {finding.status === "Requires Action" ? (
                        <Clock size={13} />
                      ) : (
                        <CheckCircle2 size={13} />
                      )}

                      {finding.status}
                    </span>
                  </td>

                  <td>
                    <div className="analyst-cell">
                      <User size={14} />
                      {finding.analyst}
                    </div>
                  </td>

                  <td className="detected-cell">{finding.detected}</td>

                  <td>
                    <button
                      className="finding-details-button"
                      onClick={() =>
                        navigate(`/supervisor/findings/${finding.id}`)
                      }
                    >
                      <ChevronRight size={17} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="findings-pagination">
          <span>Showing 1–6 of 6 findings</span>

          <div>
            <button disabled>Previous</button>
            <button className="pagination-active">1</button>
            <button disabled>Next</button>
          </div>
        </div>
      </section>
    </div>
  );
}