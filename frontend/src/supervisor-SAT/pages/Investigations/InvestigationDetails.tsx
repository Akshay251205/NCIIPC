import {
  ArrowLeft,
  ShieldAlert,
  User,
  Clock,
  FileSearch,
  CheckCircle2,
  AlertTriangle,
  Activity,
  MessageSquare,
  TrendingUp,
} from "lucide-react";
import { useNavigate, useParams } from "react-router-dom";
import "./InvestigationDetails.css";

export default function InvestigationDetails() {
  const navigate = useNavigate();
  const { id } = useParams();

  const investigation = {
    id: id || "INV-2001",
    alertId: "ALT-1001",
    title: "Suspicious Authentication Activity",
    organization: "Organization Alpha",
    asset: "AD-SERVER-01",
    analyst: "Aarav Sharma",
    severity: "Critical",
    status: "In Progress",
    progress: 64,
    evidenceReviewed: 76,
    riskScore: 86,
  };

  const timeline = [
    {
      time: "10:42 AM",
      title: "Investigation created",
      description: "Investigation automatically created from critical alert.",
      icon: ShieldAlert,
    },
    {
      time: "10:44 AM",
      title: "Analyst assigned",
      description: "Aarav Sharma was assigned to investigate the alert.",
      icon: User,
    },
    {
      time: "10:47 AM",
      title: "Authentication logs reviewed",
      description: "Initial authentication events were reviewed.",
      icon: FileSearch,
    },
    {
      time: "10:51 AM",
      title: "Suspicious activity identified",
      description:
        "Activity pattern differs from the organization's normal baseline.",
      icon: AlertTriangle,
    },
  ];

  return (
    <div className="investigation-page">
      {/* Back */}
      <button
        className="investigation-back-button"
        onClick={() => navigate(`/supervisor/alerts/${investigation.alertId}`)}
      >
        <ArrowLeft size={18} />
        Back to Alert
      </button>

      {/* Header */}
      <div className="investigation-header">
        <div>
          <div className="investigation-id">{investigation.id}</div>

          <h1>{investigation.title}</h1>

          <p>
            {investigation.organization} • Alert {investigation.alertId}
          </p>
        </div>

        <div className="investigation-status-group">
          <span className="critical-badge">
            <ShieldAlert size={15} />
            {investigation.severity}
          </span>

          <span className="progress-badge">
            <Activity size={15} />
            {investigation.status}
          </span>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="investigation-summary-grid">
        <div className="investigation-summary-card">
          <div className="summary-card-icon">
            <TrendingUp size={20} />
          </div>

          <div>
            <span>Risk Score</span>
            <strong>{investigation.riskScore}/100</strong>
          </div>
        </div>

        <div className="investigation-summary-card">
          <div className="summary-card-icon">
            <Activity size={20} />
          </div>

          <div>
            <span>Investigation Progress</span>
            <strong>{investigation.progress}%</strong>
          </div>
        </div>

        <div className="investigation-summary-card">
          <div className="summary-card-icon">
            <FileSearch size={20} />
          </div>

          <div>
            <span>Evidence Reviewed</span>
            <strong>{investigation.evidenceReviewed}%</strong>
          </div>
        </div>

        <div className="investigation-summary-card">
          <div className="summary-card-icon">
            <User size={20} />
          </div>

          <div>
            <span>Assigned Analyst</span>
            <strong>{investigation.analyst}</strong>
          </div>
        </div>
      </div>

      <div className="investigation-layout">
        {/* Main */}
        <div className="investigation-main">
          {/* Progress */}
          <section className="investigation-section">
            <div className="section-heading">
              <Activity size={20} />
              <h2>Investigation Progress</h2>
            </div>

            <div className="progress-header">
              <span>Overall completion</span>
              <strong>{investigation.progress}%</strong>
            </div>

            <div className="progress-track">
              <div
                className="progress-fill"
                style={{ width: `${investigation.progress}%` }}
              />
            </div>

            <div className="progress-stages">
              <div className="stage completed">
                <CheckCircle2 size={17} />
                <span>Alert Review</span>
              </div>

              <div className="stage completed">
                <CheckCircle2 size={17} />
                <span>Evidence Collection</span>
              </div>

              <div className="stage active">
                <Activity size={17} />
                <span>Analysis</span>
              </div>

              <div className="stage">
                <Clock size={17} />
                <span>Final Decision</span>
              </div>
            </div>
          </section>

          {/* Findings */}
          <section className="investigation-section">
            <div className="section-heading">
              <AlertTriangle size={20} />
              <h2>Investigation Findings</h2>
            </div>

            <div className="finding-box critical-finding">
              <div className="finding-icon">
                <AlertTriangle size={18} />
              </div>

              <div>
                <strong>Unusual authentication pattern</strong>
                <p>
                  Multiple authentication attempts were detected outside
                  the normal activity pattern for the affected account.
                </p>
              </div>
            </div>

            <div className="finding-box">
              <div className="finding-icon">
                <Activity size={18} />
              </div>

              <div>
                <strong>Source activity requires verification</strong>
                <p>
                  The source of the authentication attempts should be
                  verified against known organizational assets.
                </p>
              </div>
            </div>

            <div className="finding-box">
              <div className="finding-icon">
                <ShieldAlert size={18} />
              </div>

              <div>
                <strong>Potential privileged account risk</strong>
                <p>
                  The affected account has elevated privileges, increasing
                  the potential impact if the activity is malicious.
                </p>
              </div>
            </div>
          </section>

          {/* Evidence */}
          <section className="investigation-section">
            <div className="section-heading">
              <FileSearch size={20} />
              <h2>Evidence Review</h2>
            </div>

            <div className="evidence-table">
              <div className="evidence-row evidence-header">
                <span>Evidence</span>
                <span>Analyst Review</span>
                <span>Status</span>
              </div>

              <div className="evidence-row">
                <span>Authentication logs</span>
                <span>Completed</span>
                <strong className="reviewed">Reviewed</strong>
              </div>

              <div className="evidence-row">
                <span>Source IP activity</span>
                <span>In progress</span>
                <strong className="reviewing">Reviewing</strong>
              </div>

              <div className="evidence-row">
                <span>Privileged account activity</span>
                <span>Pending verification</span>
                <strong className="pending">Pending</strong>
              </div>

              <div className="evidence-row">
                <span>Related alerts</span>
                <span>Completed</span>
                <strong className="reviewed">Reviewed</strong>
              </div>
            </div>
          </section>

          {/* Timeline */}
          <section className="investigation-section">
            <div className="section-heading">
              <Clock size={20} />
              <h2>Investigation Timeline</h2>
            </div>

            <div className="investigation-timeline">
              {timeline.map((item, index) => {
                const Icon = item.icon;

                return (
                  <div className="investigation-timeline-item" key={index}>
                    <div className="investigation-timeline-icon">
                      <Icon size={16} />
                    </div>

                    <div className="investigation-timeline-content">
                      <div className="timeline-title-row">
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

        {/* Sidebar */}
        <aside className="investigation-sidebar">
          {/* Supervisor Decision */}
          <section className="decision-card">
            <div className="section-heading">
              <ShieldAlert size={20} />
              <h2>Supervisor Decision</h2>
            </div>

            <p>
              Based on the current evidence, this investigation requires
              continued review before closure.
            </p>

            <button className="decision-primary">
              Continue Investigation
            </button>

            <button className="decision-danger">
              Escalate to Incident
            </button>

            <button className="decision-secondary">
              Mark for Review
            </button>
          </section>

          {/* Analyst */}
          <section className="investigation-side-card">
            <div className="section-heading">
              <User size={20} />
              <h2>Analyst</h2>
            </div>

            <div className="investigation-analyst">
              <div className="analyst-circle">AS</div>

              <div>
                <strong>{investigation.analyst}</strong>
                <span>Security Analyst</span>
              </div>
            </div>

            <button
              className="profile-button"
              onClick={() => navigate("/supervisor/analysts/AN-001")}
            >
              View Analyst Performance
            </button>
          </section>

          {/* Asset */}
          <section className="investigation-side-card">
            <div className="section-heading">
              <Activity size={20} />
              <h2>Affected Asset</h2>
            </div>

            <div className="asset-info">
              <strong>{investigation.asset}</strong>
              <span>Active Directory Server</span>
            </div>
          </section>

          {/* Notes */}
          <section className="investigation-side-card">
            <div className="section-heading">
              <MessageSquare size={20} />
              <h2>Supervisor Notes</h2>
            </div>

            <textarea
              className="investigation-notes"
              placeholder="Add investigation notes..."
            />

            <button className="save-investigation-note">
              Save Note
            </button>
          </section>
        </aside>
      </div>
    </div>
  );
}