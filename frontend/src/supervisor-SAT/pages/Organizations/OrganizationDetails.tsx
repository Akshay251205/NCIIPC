import {
  ArrowLeft,
  AlertTriangle,
  ShieldAlert,
  Users,
  FileWarning,
  TrendingUp,
  TrendingDown,
  Clock,
  CheckCircle2,
} from "lucide-react";

import "./OrganizationDetails.css";

export default function OrganizationDetails() {
  return (
    <div className="organization-details">

      {/* Back Button */}
      <button className="back-button">
        <ArrowLeft size={16} />
        Back to Organizations
      </button>

      {/* Organization Header */}
      <div className="details-header">

        <div className="details-title">

          <div className="details-avatar">
            A
          </div>

          <div>
            <span className="details-code">
              ORG-001
            </span>

            <h1>Organization Alpha</h1>

            <p>
              Security assessment and operational health overview
            </p>
          </div>

        </div>

        <div className="assessment-status">
          <span>Assessment Status</span>
          <strong>
            <CheckCircle2 size={14} />
            Monitoring
          </strong>
        </div>

      </div>

      {/* Risk Summary */}
      <section className="risk-summary-grid">

        <div className="large-risk-card">

          <div className="large-risk-header">
            <div>
              <span>Overall Risk Score</span>
              <h2>86<span>/100</span></h2>
            </div>

            <div className="critical-badge">
              Critical Risk
            </div>
          </div>

          <div className="risk-progress">
            <div
              className="risk-progress-value"
              style={{ width: "86%" }}
            />
          </div>

          <p className="risk-note">
            Risk score is significantly above the recommended
            assessment threshold.
          </p>

        </div>

        <div className="detail-stat-card">

          <div className="detail-stat-icon alerts">
            <AlertTriangle size={20} />
          </div>

          <span>Active Alerts</span>

          <strong>38</strong>

          <small>
            <TrendingUp size={12} />
            8.4% from previous period
          </small>

        </div>

        <div className="detail-stat-card">

          <div className="detail-stat-icon findings">
            <FileWarning size={20} />
          </div>

          <span>Priority Findings</span>

          <strong>12</strong>

          <small>
            Requires supervisor review
          </small>

        </div>

        <div className="detail-stat-card">

          <div className="detail-stat-icon analysts">
            <Users size={20} />
          </div>

          <span>Assigned Analysts</span>

          <strong>8</strong>

          <small>
            6 currently active
          </small>

        </div>

      </section>

      {/* Assessment Metrics */}
      <section className="details-card">

        <div className="details-card-header">
          <div>
            <h3>Assessment Quality</h3>
            <p>
              Key indicators used to evaluate security operations.
            </p>
          </div>
        </div>

        <div className="quality-grid">

          <div className="quality-item">

            <div className="quality-top">
              <span>Investigation Quality</span>
              <strong>82%</strong>
            </div>

            <div className="quality-bar">
              <div
                className="quality-fill good"
                style={{ width: "82%" }}
              />
            </div>

            <small>
              Good investigation coverage
            </small>

          </div>

          <div className="quality-item">

            <div className="quality-top">
              <span>Evidence Coverage</span>
              <strong>64%</strong>
            </div>

            <div className="quality-bar">
              <div
                className="quality-fill warning"
                style={{ width: "64%" }}
              />
            </div>

            <small>
              Below recommended coverage
            </small>

          </div>

          <div className="quality-item">

            <div className="quality-top">
              <span>Escalation Rate</span>
              <strong>71%</strong>
            </div>

            <div className="quality-bar">
              <div
                className="quality-fill good"
                style={{ width: "71%" }}
              />
            </div>

            <small>
              Healthy escalation behavior
            </small>

          </div>

          <div className="quality-item">

            <div className="quality-top">
              <span>Alert Closure Rate</span>
              <strong>58%</strong>
            </div>

            <div className="quality-bar">
              <div
                className="quality-fill warning"
                style={{ width: "58%" }}
              />
            </div>

            <small>
              Requires attention
            </small>

          </div>

        </div>

      </section>

      {/* Two Column Section */}
      <section className="details-two-column">

        {/* Alert Distribution */}
        <div className="details-card">

          <div className="details-card-header">
            <div>
              <h3>Alert Distribution</h3>
              <p>
                Current alert severity breakdown.
              </p>
            </div>

            <ShieldAlert size={18} />
          </div>

          <div className="alert-distribution">

            <div className="alert-row">
              <div className="alert-label">
                <span className="alert-dot critical" />
                Critical
              </div>

              <strong>12</strong>

              <div className="alert-bar">
                <div
                  className="critical-bar"
                  style={{ width: "80%" }}
                />
              </div>
            </div>

            <div className="alert-row">
              <div className="alert-label">
                <span className="alert-dot high" />
                High
              </div>

              <strong>14</strong>

              <div className="alert-bar">
                <div
                  className="high-bar"
                  style={{ width: "65%" }}
                />
              </div>
            </div>

            <div className="alert-row">
              <div className="alert-label">
                <span className="alert-dot medium" />
                Medium
              </div>

              <strong>8</strong>

              <div className="alert-bar">
                <div
                  className="medium-bar"
                  style={{ width: "45%" }}
                />
              </div>
            </div>

            <div className="alert-row">
              <div className="alert-label">
                <span className="alert-dot low" />
                Low
              </div>

              <strong>4</strong>

              <div className="alert-bar">
                <div
                  className="low-bar"
                  style={{ width: "25%" }}
                />
              </div>
            </div>

          </div>

        </div>

        {/* Analyst Performance */}
        <div className="details-card">

          <div className="details-card-header">
            <div>
              <h3>Analyst Performance</h3>
              <p>
                Current organization analyst metrics.
              </p>
            </div>

            <Users size={18} />
          </div>

          <div className="analyst-metrics">

            <div>
              <span>Average Closure Time</span>
              <strong>4.8 hrs</strong>
            </div>

            <div>
              <span>Evidence Review</span>
              <strong>76%</strong>
            </div>

            <div>
              <span>Escalation Accuracy</span>
              <strong>89%</strong>
            </div>

            <div>
              <span>Investigation Completion</span>
              <strong>81%</strong>
            </div>

          </div>

        </div>

      </section>

      {/* Benchmark */}
      <section className="details-card">

        <div className="details-card-header">

          <div>
            <h3>Peer Benchmark</h3>

            <p>
              Comparison with organizations of similar size
              and operational profile.
            </p>
          </div>

          <TrendingDown size={18} />

        </div>

        <div className="benchmark-grid">

          <div className="benchmark-item">
            <span>Organization Risk</span>
            <strong>86</strong>
            <small>Higher than peer average</small>
          </div>

          <div className="benchmark-item">
            <span>Peer Average</span>
            <strong>61</strong>
            <small>Current peer baseline</small>
          </div>

          <div className="benchmark-item">
            <span>Investigation Quality</span>
            <strong>82%</strong>
            <small>+7% above peers</small>
          </div>

          <div className="benchmark-item">
            <span>Evidence Coverage</span>
            <strong>64%</strong>
            <small>-9% below peers</small>
          </div>

        </div>

      </section>

      {/* Recent Findings */}
      <section className="details-card">

        <div className="details-card-header">

          <div>
            <h3>Recent Priority Findings</h3>

            <p>
              Findings that require supervisor attention.
            </p>
          </div>

        </div>

        <div className="detail-findings">

          <div className="detail-finding">

            <div className="finding-warning">
              <AlertTriangle size={16} />
            </div>

            <div>
              <strong>
                Low Evidence Investigation
              </strong>

              <span>
                Investigation contains insufficient supporting evidence.
              </span>
            </div>

            <div className="finding-right">
              <span className="finding-critical">
                Critical
              </span>

              <small>
                <Clock size={11} />
                18 min ago
              </small>
            </div>

          </div>

          <div className="detail-finding">

            <div className="finding-warning">
              <TrendingUp size={16} />
            </div>

            <div>
              <strong>
                Unusual Analyst Behavior
              </strong>

              <span>
                Analyst activity differs significantly from peers.
              </span>
            </div>

            <div className="finding-right">
              <span className="finding-high">
                High
              </span>

              <small>
                <Clock size={11} />
                42 min ago
              </small>
            </div>

          </div>

          <div className="detail-finding">

            <div className="finding-warning">
              <AlertTriangle size={16} />
            </div>

            <div>
              <strong>
                Fast Alert Closure
              </strong>

              <span>
                Multiple alerts were closed significantly faster than expected.
              </span>
            </div>

            <div className="finding-right">
              <span className="finding-high">
                High
              </span>

              <small>
                <Clock size={11} />
                1 hr ago
              </small>
            </div>

          </div>

        </div>

      </section>

    </div>
  );
}
