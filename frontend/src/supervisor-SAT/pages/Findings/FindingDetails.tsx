import {
  ArrowLeft,
  AlertTriangle,
  ShieldAlert,
  Building2,
  Server,
  User,
  Clock,
  FileSearch,
  CheckCircle2,
  Brain,
  TrendingUp,
  ExternalLink,
  MessageSquare,
} from "lucide-react";
import { useNavigate, useParams } from "react-router-dom";
import "./FindingDetails.css";

export default function FindingDetails() {
  const navigate = useNavigate();
  const { id } = useParams();

  const finding = {
    id: id || "FND-001",
    title: "Potential Privileged Account Compromise",
    organization: "Organization Alpha",
    alertId: "ALT-1001",
    investigationId: "INV-2001",
    asset: "AD-SERVER-01",
    analyst: "Aarav Sharma",
    category: "Account Security",
    severity: "Critical",
    riskScore: 94,
    status: "Requires Action",
    detected: "12 minutes ago",
  };

  const riskFactors = [
    {
      title: "Unusual authentication pattern",
      score: "+32",
      description:
        "Authentication activity differs significantly from the normal organizational baseline.",
    },
    {
      title: "Privileged account involved",
      score: "+28",
      description:
        "The affected account has elevated privileges within the organization's environment.",
    },
    {
      title: "Repeated authentication attempts",
      score: "+21",
      description:
        "Multiple authentication attempts were observed within a short period.",
    },
    {
      title: "Source activity requires verification",
      score: "+13",
      description:
        "The originating source has not yet been fully validated by the analyst.",
    },
  ];

  const evidence = [
    {
      name: "Authentication logs",
      description: "Multiple unusual login events detected.",
      status: "Verified",
    },
    {
      name: "Privileged account activity",
      description: "Elevated account privileges confirmed.",
      status: "Verified",
    },
    {
      name: "Source IP activity",
      description: "Source requires additional investigation.",
      status: "Under Review",
    },
    {
      name: "Related security alerts",
      description: "Related authentication alerts identified.",
      status: "Verified",
    },
  ];

  return (
    <div className="finding-details-page">
      {/* Back */}
      <button
        className="finding-back-button"
        onClick={() => navigate("/supervisor/findings")}
      >
        <ArrowLeft size={18} />
        Back to Priority Findings
      </button>

      {/* Header */}
      <div className="finding-details-header">
        <div>
          <div className="finding-detail-id">{finding.id}</div>

          <h1>{finding.title}</h1>

          <p>
            {finding.organization} • Detected {finding.detected}
          </p>
        </div>

        <div className="finding-header-status">
          <span className="finding-critical-badge">
            <ShieldAlert size={16} />
            {finding.severity}
          </span>

          <span className="finding-action-badge">
            <Clock size={16} />
            {finding.status}
          </span>
        </div>
      </div>

      {/* Risk Summary */}
      <div className="finding-risk-summary">
        <div className="risk-score-large">
          <span>Risk Score</span>
          <strong>{finding.riskScore}</strong>
          <small>Critical Risk</small>
        </div>

        <div className="risk-summary-content">
          <div className="risk-summary-heading">
            <div>
              <span>Supervisor Assessment</span>
              <h2>Immediate attention recommended</h2>
            </div>

            <ShieldAlert size={30} />
          </div>

          <p>
            This finding combines several high-risk indicators involving a
            privileged account. The current evidence suggests that the
            activity should be investigated further before the alert can
            be safely closed.
          </p>

          <div className="risk-progress">
            <div className="risk-progress-header">
              <span>Risk level</span>
              <strong>{finding.riskScore}/100</strong>
            </div>

            <div className="risk-progress-track">
              <div
                className="risk-progress-fill"
                style={{ width: `${finding.riskScore}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      <div className="finding-details-layout">
        {/* Main Column */}
        <div className="finding-main-column">
          {/* Finding Explanation */}
          <section className="finding-section">
            <div className="finding-section-title">
              <AlertTriangle size={20} />
              <h2>Finding Explanation</h2>
            </div>

            <p className="finding-explanation">
              A potential compromise of a privileged account has been
              identified. The observed authentication behavior is
              inconsistent with the organization's normal activity and
              requires additional verification.
            </p>

            <div className="finding-metadata-grid">
              <div>
                <span>Category</span>
                <strong>{finding.category}</strong>
              </div>

              <div>
                <span>Severity</span>
                <strong className="critical-text">
                  {finding.severity}
                </strong>
              </div>

              <div>
                <span>Organization</span>
                <strong>{finding.organization}</strong>
              </div>

              <div>
                <span>Affected Asset</span>
                <strong>{finding.asset}</strong>
              </div>
            </div>
          </section>

          {/* AI Reasoning */}
          <section className="finding-section ai-section">
            <div className="finding-section-title">
              <Brain size={20} />
              <h2>AI / Analytics Reasoning</h2>
            </div>

            <div className="ai-summary">
              <strong>Why this finding is prioritized</strong>

              <p>
                The analytics layer identified a significant deviation from
                the expected authentication behavior for this organization.
                The combination of privileged access, repeated attempts,
                and unusual source activity increases the overall risk.
              </p>
            </div>

            <div className="ai-indicators">
              <div>
                <span>Behavioral Deviation</span>
                <strong>High</strong>
              </div>

              <div>
                <span>Privilege Exposure</span>
                <strong>High</strong>
              </div>

              <div>
                <span>Evidence Confidence</span>
                <strong>76%</strong>
              </div>

              <div>
                <span>Priority</span>
                <strong>Immediate</strong>
              </div>
            </div>
          </section>

          {/* Risk Factors */}
          <section className="finding-section">
            <div className="finding-section-title">
              <TrendingUp size={20} />
              <h2>Risk Factors</h2>
            </div>

            <div className="risk-factor-list">
              {riskFactors.map((factor) => (
                <div className="risk-factor" key={factor.title}>
                  <div className="risk-factor-icon">
                    <AlertTriangle size={16} />
                  </div>

                  <div className="risk-factor-content">
                    <div>
                      <strong>{factor.title}</strong>
                      <span>{factor.score}</span>
                    </div>

                    <p>{factor.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Evidence */}
          <section className="finding-section">
            <div className="finding-section-title">
              <FileSearch size={20} />
              <h2>Supporting Evidence</h2>
            </div>

            <div className="finding-evidence-list">
              {evidence.map((item) => (
                <div className="finding-evidence-item" key={item.name}>
                  <div className="evidence-check">
                    <CheckCircle2 size={18} />
                  </div>

                  <div>
                    <strong>{item.name}</strong>
                    <p>{item.description}</p>
                  </div>

                  <span
                    className={
                      item.status === "Verified"
                        ? "evidence-verified"
                        : "evidence-review"
                    }
                  >
                    {item.status}
                  </span>
                </div>
              ))}
            </div>
          </section>
        </div>

        {/* Side Column */}
        <aside className="finding-side-column">
          {/* Recommended Action */}
          <section className="recommended-action-card">
            <div className="finding-section-title">
              <ShieldAlert size={20} />
              <h2>Recommended Action</h2>
            </div>

            <p>
              Continue investigation and verify the source of the
              authentication activity before closing the finding.
            </p>

            <button
              className="action-primary"
              onClick={() =>
                navigate(
                  `/supervisor/investigations/${finding.investigationId}`
                )
              }
            >
              Review Investigation
            </button>

            <button className="action-danger">
              Escalate to Incident
            </button>

            <button className="action-secondary">
              Mark as Reviewed
            </button>
          </section>

          {/* Related Alert */}
          <section className="finding-side-card">
            <div className="finding-section-title">
              <AlertTriangle size={20} />
              <h2>Related Alert</h2>
            </div>

            <div className="related-item">
              <strong>{finding.alertId}</strong>
              <span>Suspicious Authentication Activity</span>
            </div>

            <button
              className="related-button"
              onClick={() =>
                navigate(`/supervisor/alerts/${finding.alertId}`)
              }
            >
              View Alert
              <ExternalLink size={14} />
            </button>
          </section>

          {/* Organization */}
          <section className="finding-side-card">
            <div className="finding-section-title">
              <Building2 size={20} />
              <h2>Organization</h2>
            </div>

            <div className="organization-detail">
              <strong>{finding.organization}</strong>
              <span>Risk Score: 86/100</span>
            </div>

            <button
              className="related-button"
              onClick={() =>
                navigate("/supervisor/organizations/ORG-001")
              }
            >
              View Organization
              <ExternalLink size={14} />
            </button>
          </section>

          {/* Analyst */}
          <section className="finding-side-card">
            <div className="finding-section-title">
              <User size={20} />
              <h2>Assigned Analyst</h2>
            </div>

            <div className="finding-analyst">
              <div className="finding-analyst-avatar">AS</div>

              <div>
                <strong>{finding.analyst}</strong>
                <span>Security Analyst</span>
              </div>
            </div>

            <button
              className="related-button"
              onClick={() =>
                navigate("/supervisor/analysts/AN-001")
              }
            >
              View Analyst
              <ExternalLink size={14} />
            </button>
          </section>

          {/* Asset */}
          <section className="finding-side-card">
            <div className="finding-section-title">
              <Server size={20} />
              <h2>Affected Asset</h2>
            </div>

            <div className="asset-detail">
              <strong>{finding.asset}</strong>
              <span>Active Directory Server</span>
            </div>
          </section>

          {/* Notes */}
          <section className="finding-side-card">
            <div className="finding-section-title">
              <MessageSquare size={20} />
              <h2>Supervisor Notes</h2>
            </div>

            <textarea
              className="finding-notes"
              placeholder="Add a supervisor note..."
            />

            <button className="save-finding-note">
              Save Note
            </button>
          </section>
        </aside>
      </div>
    </div>
  );
}