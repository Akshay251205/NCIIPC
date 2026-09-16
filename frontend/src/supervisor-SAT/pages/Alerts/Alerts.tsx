import {
  AlertTriangle,
  Bell,
  CheckCircle2,
  Clock,
  Search,
  Filter,
  ChevronRight,
  ShieldAlert,
  XCircle,
} from "lucide-react";
import "./Alerts.css";
import { useNavigate } from "react-router-dom";


const alerts = [
  {
    id: "ALT-1001",
    title: "Suspicious Authentication Activity",
    organization: "Organization Alpha",
    asset: "AD-SERVER-01",
    severity: "Critical",
    status: "Open",
    analyst: "Aarav Sharma",
    time: "12 min ago",
  },
  {
    id: "ALT-1002",
    title: "Unusual Network Traffic",
    organization: "Organization Beta",
    asset: "WEB-SERVER-03",
    severity: "High",
    status: "Investigating",
    analyst: "Rahul Verma",
    time: "28 min ago",
  },
  {
    id: "ALT-1003",
    title: "Multiple Failed Login Attempts",
    organization: "Organization Alpha",
    asset: "VPN-GATEWAY",
    severity: "High",
    status: "Open",
    analyst: "Priya Singh",
    time: "41 min ago",
  },
  {
    id: "ALT-1004",
    title: "Endpoint Security Detection",
    organization: "Organization Gamma",
    asset: "LAPTOP-042",
    severity: "Medium",
    status: "Resolved",
    analyst: "Ananya Gupta",
    time: "1 hr ago",
  },
  {
    id: "ALT-1005",
    title: "Abnormal DNS Request",
    organization: "Organization Delta",
    asset: "DNS-SERVER-02",
    severity: "Medium",
    status: "Investigating",
    analyst: "Neha Kapoor",
    time: "2 hrs ago",
  },
  {
    id: "ALT-1006",
    title: "Policy Violation Detected",
    organization: "Organization Beta",
    asset: "WORKSTATION-118",
    severity: "Low",
    status: "Resolved",
    analyst: "Vikram Mehta",
    time: "3 hrs ago",
  },
  {
    id: "ALT-1007",
    title: "Privileged Account Activity",
    organization: "Organization Gamma",
    asset: "ADMIN-SERVER",
    severity: "Critical",
    status: "Open",
    analyst: "Ananya Gupta",
    time: "4 hrs ago",
  },
];

function Alerts() {
    const navigate = useNavigate();
  return (
    <div className="alerts-page">

      {/* Page Header */}
      <div className="alerts-header">

        <div>
          <h1>Alerts</h1>

          <p>
            Monitor security alerts and track investigation activity across
            organizations.
          </p>
        </div>

        <button className="alerts-filter-button">
          <Filter size={17} />
          Filters
        </button>

      </div>

      {/* KPI Cards */}
      <div className="alerts-kpi-grid">

        <div className="alerts-kpi-card">

          <div className="alerts-kpi-icon total">
            <Bell size={21} />
          </div>

          <div>
            <span>Total Alerts</span>
            <strong>148</strong>
            <small>Current monitoring period</small>
          </div>

        </div>

        <div className="alerts-kpi-card">

          <div className="alerts-kpi-icon critical">
            <ShieldAlert size={21} />
          </div>

          <div>
            <span>Critical Alerts</span>
            <strong>18</strong>
            <small>Requires immediate attention</small>
          </div>

        </div>

        <div className="alerts-kpi-card">

          <div className="alerts-kpi-icon open">
            <AlertTriangle size={21} />
          </div>

          <div>
            <span>Open Alerts</span>
            <strong>42</strong>
            <small>Awaiting investigation</small>
          </div>

        </div>

        <div className="alerts-kpi-card">

          <div className="alerts-kpi-icon resolved">
            <CheckCircle2 size={21} />
          </div>

          <div>
            <span>Resolved</span>
            <strong>106</strong>
            <small>71.6% resolution rate</small>
          </div>

        </div>

      </div>

      {/* Alert Summary */}
      <div className="alert-summary-grid">

        <div className="alert-summary-card">

          <div className="alert-summary-header">
            <div>
              <h3>Alert Severity</h3>
              <p>Current distribution by severity.</p>
            </div>

            <ShieldAlert size={18} />
          </div>

          <div className="severity-summary">

            <div className="severity-summary-item">
              <div>
                <span className="severity-dot critical-dot" />
                Critical
              </div>

              <strong>18</strong>
            </div>

            <div className="severity-summary-item">
              <div>
                <span className="severity-dot high-dot" />
                High
              </div>

              <strong>46</strong>
            </div>

            <div className="severity-summary-item">
              <div>
                <span className="severity-dot medium-dot" />
                Medium
              </div>

              <strong>57</strong>
            </div>

            <div className="severity-summary-item">
              <div>
                <span className="severity-dot low-dot" />
                Low
              </div>

              <strong>27</strong>
            </div>

          </div>

        </div>

        <div className="alert-summary-card">

          <div className="alert-summary-header">
            <div>
              <h3>Investigation Status</h3>
              <p>Current alert investigation state.</p>
            </div>

            <Clock size={18} />
          </div>

          <div className="investigation-summary">

            <div>
              <span>Open</span>
              <strong>42</strong>
            </div>

            <div>
              <span>Investigating</span>
              <strong>31</strong>
            </div>

            <div>
              <span>Resolved</span>
              <strong>106</strong>
            </div>

          </div>

        </div>

      </div>

      {/* Alerts Table */}
      <section className="alerts-table-card">

        <div className="alerts-table-header">

          <div>
            <h2>Recent Alerts</h2>

            <p>
              Latest alerts requiring monitoring or investigation.
            </p>
          </div>

          <div className="alerts-search">
            <Search size={17} />
            <input placeholder="Search alerts..." />
          </div>

        </div>

        <div className="alerts-table-wrapper">

          <table className="alerts-table">

            <thead>
              <tr>
                <th>Alert</th>
                <th>Organization</th>
                <th>Asset</th>
                <th>Severity</th>
                <th>Status</th>
                <th>Analyst</th>
                <th>Detected</th>
                <th></th>
              </tr>
            </thead>

            <tbody>

              {alerts.map((alert) => (
                <tr key={alert.id}>

                  {/* Alert */}
                  <td>

                    <div className="alert-name-cell">

                      <div
                        className={`alert-row-icon ${alert.severity.toLowerCase()}`}
                      >
                        <AlertTriangle size={16} />
                      </div>

                      <div>
                        <strong>{alert.title}</strong>
                        <span>{alert.id}</span>
                      </div>

                    </div>

                  </td>

                  {/* Organization */}
                  <td>
                    {alert.organization}
                  </td>

                  {/* Asset */}
                  <td>
                    <span className="asset-name">
                      {alert.asset}
                    </span>
                  </td>

                  {/* Severity */}
                  <td>

                    <span
                      className={`severity-badge ${alert.severity.toLowerCase()}`}
                    >
                      {alert.severity}
                    </span>

                  </td>

                  {/* Status */}
                  <td>

                    <span
                      className={`alert-status ${alert.status
                        .toLowerCase()
                        .replace(" ", "-")}`}
                    >
                      {alert.status}
                    </span>

                  </td>

                  {/* Analyst */}
                  <td>
                    {alert.analyst}
                  </td>

                  {/* Time */}
                  <td>

                    <span className="alert-time">
                      <Clock size={12} />
                      {alert.time}
                    </span>

                  </td>

                  {/* Details */}
                  <td>

                    <button
                    className="alert-details-button"
                    onClick={() =>
                        navigate(`/supervisor/alerts/${alert.id}`)
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
        <div className="alerts-pagination">

          <span>
            Showing 1–7 of 148 alerts
          </span>

          <div>

            <button disabled>
              Previous
            </button>

            <button className="active-page">
              1
            </button>

            <button>
              2
            </button>

            <button>
              3
            </button>

            <button>
              4
            </button>

            <button>
              Next
            </button>

          </div>

        </div>

      </section>

      {/* Attention Banner */}
      <div className="alerts-attention-banner">

        <div className="alerts-attention-icon">
          <XCircle size={20} />
        </div>

        <div>
          <strong>
            18 critical alerts require immediate review
          </strong>

          <p>
            Supervisors should prioritize alerts that remain open or have
            exceeded expected investigation time.
          </p>
        </div>

        <button>
          Review Critical Alerts
        </button>

      </div>

    </div>
  );
}

export default Alerts;