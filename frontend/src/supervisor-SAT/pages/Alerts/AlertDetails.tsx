import {
  ArrowLeft,
  AlertTriangle,
  ShieldAlert,
  Server,
  User,
  Clock,
  CheckCircle2,
  FileWarning,
  Activity,
  MessageSquare,
} from "lucide-react";
import { useNavigate, useParams } from "react-router-dom";
import "./AlertDetails.css";

export default function AlertDetails() {
  const navigate = useNavigate();
  const { id } = useParams();

  // Temporary mock data.
  // This will later come from the FastAPI backend.
  const alert = {
    id: id || "ALT-1001",
    title: "Suspicious Authentication Activity",
    organization: "Organization Alpha",
    asset: "AD-SERVER-01",
    severity: "Critical",
    status: "Open",
    analyst: "Aarav Sharma",
    detected: "12 minutes ago",
    category: "Authentication",
    source: "Active Directory",
    description:
      "Multiple unusual authentication attempts were detected against a privileged account. The activity differs from the normal authentication pattern observed for this organization.",
  };

  const timeline = [
    {
      time: "10:42 AM",
      title: "Alert detected",
      description: "Security monitoring system generated the alert.",
      icon: AlertTriangle,
    },
    {
      time: "10:44 AM",
      title: "Alert assigned",
      description: "Alert assigned to Aarav Sharma for investigation.",
      icon: User,
    },
    {
      time: "10:47 AM",
      title: "Initial review started",
      description: "Analyst began reviewing authentication activity.",
      icon: Activity,
    },
    {
      time: "10:51 AM",
      title: "Supervisor review required",
      description:
        "Alert remains critical and requires supervisor attention.",
      icon: ShieldAlert,
    },
  ];

  return (
    <div className="alert-details-page">
      {/* Back Button */}
      <button
        className="alert-back-button"
        onClick={() => navigate("/supervisor/alerts")}
      >
        <ArrowLeft size={18} />
        Back to Alerts
      </button>

      {/* Header */}
      <div className="alert-details-header">
        <div>
          <div className="alert-id">{alert.id}</div>

          <h1>{alert.title}</h1>

          <p>
            {alert.organization} • Detected {alert.detected}
          </p>
        </div>

        <div className="alert-header-status">
          <span className="severity-critical">
            <ShieldAlert size={16} />
            {alert.severity}
          </span>

          <span className="status-open">
            <Clock size={16} />
            {alert.status}
          </span>
        </div>
      </div>

      {/* Alert Summary */}
      <div className="alert-summary-grid">
        <div className="alert-info-card">
          <div className="alert-info-icon">
            <ShieldAlert size={20} />
          </div>

          <div>
            <span>Severity</span>
            <strong className="critical-text">{alert.severity}</strong>
          </div>
        </div>

        <div className="alert-info-card">
          <div className="alert-info-icon">
            <Server size={20} />
          </div>

          <div>
            <span>Affected Asset</span>
            <strong>{alert.asset}</strong>
          </div>
        </div>

        <div className="alert-info-card">
          <div className="alert-info-icon">
            <User size={20} />
          </div>

          <div>
            <span>Assigned Analyst</span>
            <strong>{alert.analyst}</strong>
          </div>
        </div>

        <div className="alert-info-card">
          <div className="alert-info-icon">
            <Clock size={20} />
          </div>

          <div>
            <span>Detected</span>
            <strong>{alert.detected}</strong>
          </div>
        </div>
      </div>

      <div className="alert-details-layout">
        {/* Left Column */}
        <div className="alert-main-column">
          {/* Description */}
          <section className="alert-section">
            <div className="section-title">
              <FileWarning size={20} />
              <h2>Alert Description</h2>
            </div>

            <p className="alert-description">
              {alert.description}
            </p>

            <div className="alert-metadata">
              <div>
                <span>Category</span>
                <strong>{alert.category}</strong>
              </div>

              <div>
                <span>Source</span>
                <strong>{alert.source}</strong>
              </div>

              <div>
                <span>Organization</span>
                <strong>{alert.organization}</strong>
              </div>
            </div>
          </section>

          {/* Investigation Summary */}
          <section className="alert-section">
            <div className="section-title">
              <Activity size={20} />
              <h2>Investigation Summary</h2>
            </div>

            <div className="investigation-box">
              <div className="investigation-status">
                <span className="status-dot"></span>
                Investigation in progress
              </div>

              <p>
                The assigned analyst is reviewing authentication logs,
                affected accounts, and related activity to determine
                whether the alert represents a genuine security incident.
              </p>

              <div className="investigation-metrics">
                <div>
                  <span>Evidence Reviewed</span>
                  <strong>76%</strong>
                </div>

                <div>
                  <span>Investigation Progress</span>
                  <strong>64%</strong>
                </div>

                <div>
                  <span>Escalation Status</span>
                  <strong>Required</strong>
                </div>
              </div>
            </div>
          </section>

          {/* Evidence */}
          <section className="alert-section">
            <div className="section-title">
              <FileWarning size={20} />
              <h2>Evidence</h2>
            </div>

            <div className="evidence-list">
              <div className="evidence-item">
                <CheckCircle2 size={18} />
                <div>
                  <strong>Authentication logs</strong>
                  <span>Reviewed</span>
                </div>
              </div>

              <div className="evidence-item">
                <CheckCircle2 size={18} />
                <div>
                  <strong>Source IP activity</strong>
                  <span>Under review</span>
                </div>
              </div>

              <div className="evidence-item">
                <CheckCircle2 size={18} />
                <div>
                  <strong>Privileged account activity</strong>
                  <span>Requires verification</span>
                </div>
              </div>
            </div>
          </section>
        </div>

        {/* Right Column */}
        <div className="alert-side-column">
          {/* Supervisor Action */}
          <section className="action-card">
            <div className="section-title">
              <ShieldAlert size={20} />
              <h2>Supervisor Action</h2>
            </div>

            <p>
              This critical alert requires immediate supervisor review.
            </p>

            <button
            className="primary-action"
            onClick={() =>
                navigate(`/supervisor/investigations/INV-2001`)
            }
            >
            Review Investigation
            </button>

            <button className="secondary-action">
              Escalate Alert
            </button>
          </section>

          {/* Analyst */}
          <section className="side-card">
            <div className="section-title">
              <User size={20} />
              <h2>Assigned Analyst</h2>
            </div>

            <div className="analyst-box">
              <div className="analyst-avatar">AS</div>

              <div>
                <strong>{alert.analyst}</strong>
                <span>Security Analyst</span>
              </div>
            </div>

            <button
              className="view-analyst-button"
              onClick={() => navigate("/supervisor/analysts/AN-001")}
            >
              View Analyst Profile
            </button>
          </section>

          {/* Communication */}
          <section className="side-card">
            <div className="section-title">
              <MessageSquare size={20} />
              <h2>Supervisor Notes</h2>
            </div>

            <textarea
              className="supervisor-notes"
              placeholder="Add a supervisor note..."
            />

            <button className="save-note-button">
              Save Note
            </button>
          </section>
        </div>
      </div>

      {/* Timeline */}
      <section className="alert-section timeline-section">
        <div className="section-title">
          <Clock size={20} />
          <h2>Alert Timeline</h2>
        </div>

        <div className="timeline">
          {timeline.map((item, index) => {
            const Icon = item.icon;

            return (
              <div className="timeline-item" key={index}>
                <div className="timeline-icon">
                  <Icon size={17} />
                </div>

                <div className="timeline-content">
                  <div className="timeline-top">
                    <strong>{item.title}</strong>
                    <span>{item.time}</span>
                  </div>

                  <p>{item.description}</p>
                </div>
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
}