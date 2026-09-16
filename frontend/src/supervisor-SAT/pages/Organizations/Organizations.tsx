import { useNavigate } from "react-router-dom";
import {
  Search,
  Filter,
  Building2,
  AlertTriangle,
  ShieldCheck,
  ChevronRight,
} from "lucide-react";

import "./Organizations.css";


interface Organization {
  name: string;
  code: string;
  riskScore: number;
  riskLevel: "Critical" | "High" | "Medium" | "Low";
  activeAlerts: number;
  priorityFindings: number;
  analysts: number;
  lastAssessment: string;
}

const organizations: Organization[] = [
  {
    name: "Organization Alpha",
    code: "ORG-001",
    riskScore: 86,
    riskLevel: "Critical",
    activeAlerts: 38,
    priorityFindings: 12,
    analysts: 8,
    lastAssessment: "Today",
  },
  {
    name: "Organization Beta",
    code: "ORG-002",
    riskScore: 74,
    riskLevel: "High",
    activeAlerts: 29,
    priorityFindings: 8,
    analysts: 6,
    lastAssessment: "Yesterday",
  },
  {
    name: "Organization Gamma",
    code: "ORG-003",
    riskScore: 68,
    riskLevel: "High",
    activeAlerts: 21,
    priorityFindings: 7,
    analysts: 5,
    lastAssessment: "2 days ago",
  },
  {
    name: "Organization Delta",
    code: "ORG-004",
    riskScore: 52,
    riskLevel: "Medium",
    activeAlerts: 16,
    priorityFindings: 4,
    analysts: 7,
    lastAssessment: "3 days ago",
  },
  {
    name: "Organization Epsilon",
    code: "ORG-005",
    riskScore: 34,
    riskLevel: "Low",
    activeAlerts: 8,
    priorityFindings: 2,
    analysts: 4,
    lastAssessment: "4 days ago",
  },
  {
    name: "Organization Zeta",
    code: "ORG-006",
    riskScore: 61,
    riskLevel: "Medium",
    activeAlerts: 14,
    priorityFindings: 5,
    analysts: 5,
    lastAssessment: "5 days ago",
  },
];

function getRiskClass(level: Organization["riskLevel"]) {
  return level.toLowerCase();
}

export default function Organizations() {
    const navigate = useNavigate();
  return (
    <div className="organizations-page">

      {/* Page Header */}
      <div className="organizations-header">
        <div>
          <h1>Organizations</h1>

          <p>
            Monitor organization security posture and assessment health.
          </p>
        </div>

        <div className="organization-summary">
          <Building2 size={18} />

          <div>
            <strong>{organizations.length}</strong>
            <span>Monitored Organizations</span>
          </div>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="organization-stats">

        <div className="organization-stat-card">
          <div className="stat-icon total">
            <Building2 size={20} />
          </div>

          <div>
            <span>Total Organizations</span>
            <strong>24</strong>
          </div>
        </div>

        <div className="organization-stat-card">
          <div className="stat-icon critical">
            <AlertTriangle size={20} />
          </div>

          <div>
            <span>High Risk</span>
            <strong>7</strong>
          </div>
        </div>

        <div className="organization-stat-card">
          <div className="stat-icon healthy">
            <ShieldCheck size={20} />
          </div>

          <div>
            <span>Low Risk</span>
            <strong>9</strong>
          </div>
        </div>

        <div className="organization-stat-card">
          <div className="stat-icon findings">
            <AlertTriangle size={20} />
          </div>

          <div>
            <span>Priority Findings</span>
            <strong>87</strong>
          </div>
        </div>

      </div>

      {/* Organization Table Card */}
      <div className="organization-table-card">

        {/* Table Header */}
        <div className="table-toolbar">

          <div>
            <h3>Organization Risk Overview</h3>
            <p>
              Ranked according to current assessment risk.
            </p>
          </div>

          <div className="table-actions">

            <div className="organization-search">
              <Search size={17} />

              <input
                type="text"
                placeholder="Search organizations..."
              />
            </div>

            <button className="filter-button">
              <Filter size={16} />
              Filter
            </button>

          </div>

        </div>

        {/* Table */}
        <div className="table-wrapper">

          <table className="organization-table">

            <thead>
              <tr>
                <th>Organization</th>
                <th>Risk Score</th>
                <th>Risk Level</th>
                <th>Active Alerts</th>
                <th>Priority Findings</th>
                <th>Analysts</th>
                <th>Last Assessment</th>
                <th></th>
              </tr>
            </thead>

            <tbody>

              {organizations.map((organization) => (

                <tr key={organization.code}>

                  {/* Organization */}
                  <td>
                    <div className="organization-name">

                      <div className="organization-avatar">
                        {organization.name.charAt(13)}
                      </div>

                      <div>
                        <strong>
                          {organization.name}
                        </strong>

                        <span>
                          {organization.code}
                        </span>
                      </div>

                    </div>
                  </td>

                  {/* Risk Score */}
                  <td>

                    <div className="risk-score-cell">

                      <strong>
                        {organization.riskScore}
                      </strong>

                      <div className="mini-progress">
                        <div
                          className={`mini-progress-fill ${getRiskClass(
                            organization.riskLevel
                          )}`}
                          style={{
                            width: `${organization.riskScore}%`,
                          }}
                        />
                      </div>

                    </div>

                  </td>

                  {/* Risk Level */}
                  <td>

                    <span
                      className={`organization-risk-badge ${getRiskClass(
                        organization.riskLevel
                      )}`}
                    >
                      {organization.riskLevel}
                    </span>

                  </td>

                  {/* Alerts */}
                  <td>

                    <div className="table-number">
                      <AlertTriangle size={14} />
                      {organization.activeAlerts}
                    </div>

                  </td>

                  {/* Findings */}
                  <td>
                    <span className="finding-number">
                      {organization.priorityFindings}
                    </span>
                  </td>

                  {/* Analysts */}
                  <td>
                    <span className="analyst-number">
                      {organization.analysts}
                    </span>
                  </td>

                  {/* Assessment */}
                  <td>
                    <span className="assessment-time">
                      {organization.lastAssessment}
                    </span>
                  </td>

                  {/* Details */}
                  <td>

                    <button
                    className="details-button"
                    onClick={() =>
                        navigate(
                        `/supervisor/organizations/${organization.code}`
                        )
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

        {/* Table Footer */}
        <div className="table-footer">

          <span>
            Showing {organizations.length} of 24 organizations
          </span>

          <div className="pagination">

            <button disabled>
              Previous
            </button>

            <button className="page-active">
              1
            </button>

            <button>
              2
            </button>

            <button>
              3
            </button>

            <button>
              Next
            </button>

          </div>

        </div>

      </div>

    </div>
  );
}