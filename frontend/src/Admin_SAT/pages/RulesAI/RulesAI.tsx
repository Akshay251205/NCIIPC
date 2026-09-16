import { useMemo, useState } from "react";
import {
  ShieldCheck,
  BrainCircuit,
  Activity,
  SlidersHorizontal,
  CheckCircle2,
  AlertTriangle,
  Info,
  Eye,
  X,
  Clock3,
  Gauge,
  Database,
} from "lucide-react";

type Tab = "overview" | "rules" | "models" | "risk";

interface DetectionRule {
  id: string;
  name: string;
  description: string;
  condition: string;
  score: number;
  severity: "Medium" | "High" | "Informational";
  status: "Active";
}

interface ModelFeature {
  name: string;
  description: string;
}

const detectionRules: DetectionRule[] = [
  {
    id: "RULE-001",
    name: "Suspiciously Fast Closure",
    description:
      "Flags analysts who close alerts unusually quickly while having at least one closed alert.",
    condition: "Average closure time < 10 minutes",
    score: 30,
    severity: "High",
    status: "Active",
  },
  {
    id: "RULE-002",
    name: "Low Evidence Review",
    description:
      "Identifies analysts with a low percentage of alerts where evidence was reviewed.",
    condition: "Evidence review rate < 50%",
    score: 20,
    severity: "Medium",
    status: "Active",
  },
  {
    id: "RULE-003",
    name: "Low Escalation Rate",
    description:
      "Flags unusually low escalation behavior when the analyst has handled multiple alerts.",
    condition: "Escalation rate < 10%",
    score: 15,
    severity: "Medium",
    status: "Active",
  },
  {
    id: "RULE-004",
    name: "Shallow Investigation Activity",
    description:
      "Detects analysts performing very few investigation queries.",
    condition: "Average investigation queries < 2",
    score: 20,
    severity: "Medium",
    status: "Active",
  },
  {
    id: "RULE-005",
    name: "Very Short Investigations",
    description:
      "Flags investigations whose average duration is unusually short.",
    condition: "Average investigation time < 10 minutes",
    score: 15,
    severity: "Medium",
    status: "Active",
  },
  {
    id: "RULE-006",
    name: "High Alert Workload",
    description:
      "Provides workload context for analysts handling a large number of alerts. This indicator does not increase risk by itself.",
    condition: "Total alerts ≥ 100",
    score: 0,
    severity: "Informational",
    status: "Active",
  },
];

const modelFeatures: ModelFeature[] = [
  {
    name: "Total Alerts",
    description: "Total number of alerts handled by the analyst.",
  },
  {
    name: "Average Closure Time",
    description: "Average time required to close alerts, measured in minutes.",
  },
  {
    name: "Evidence Review Rate",
    description: "Percentage of alerts where evidence was reviewed.",
  },
  {
    name: "Escalation Rate",
    description: "Percentage of alerts escalated by the analyst.",
  },
  {
    name: "Total Investigations",
    description: "Total number of investigations performed.",
  },
  {
    name: "Average Queries",
    description: "Average number of queries executed during investigations.",
  },
  {
    name: "Average Investigation Time",
    description: "Average duration of investigations in minutes.",
  },
];

function RulesAI() {
  const [activeTab, setActiveTab] = useState<Tab>("overview");
  const [selectedRule, setSelectedRule] = useState<DetectionRule | null>(
    null
  );

  const activeRules = useMemo(
    () => detectionRules.filter((rule) => rule.status === "Active"),
    []
  );

  const riskRules = useMemo(
    () => detectionRules.filter((rule) => rule.score > 0),
    []
  );

  const tabs = [
    {
      id: "overview" as Tab,
      label: "Overview",
      icon: Activity,
    },
    {
      id: "rules" as Tab,
      label: "Detection Rules",
      icon: ShieldCheck,
    },
    {
      id: "models" as Tab,
      label: "AI Models",
      icon: BrainCircuit,
    },
    {
      id: "risk" as Tab,
      label: "Risk Configuration",
      icon: SlidersHorizontal,
    },
  ];

  return (
    <div className="rules-ai-page">
      {/* Header */}
      <div className="page-header">
        <div>
          <h2>Rules & AI</h2>
          <p>
            Configure and monitor the rule-based and AI-driven detection
            capabilities of SAT-SA.
          </p>
        </div>

        <div className="rules-system-status">
          <span className="status-dot"></span>
          Detection System Active
        </div>
      </div>

      {/* Tabs */}
      <div className="rules-tabs">
        {tabs.map((tab) => {
          const Icon = tab.icon;

          return (
            <button
              key={tab.id}
              className={`rules-tab ${
                activeTab === tab.id ? "active" : ""
              }`}
              onClick={() => setActiveTab(tab.id)}
            >
              <Icon size={18} />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Overview */}
      {activeTab === "overview" && (
        <div className="rules-content">
          <div className="rules-summary-grid">
            <SummaryCard
              icon={<ShieldCheck size={22} />}
              title="Active Rules"
              value={String(activeRules.length)}
              description="Currently enabled detection rules"
            />

            <SummaryCard
              icon={<BrainCircuit size={22} />}
              title="AI Models"
              value="1"
              description="Currently configured detection model"
            />

            <SummaryCard
              icon={<Gauge size={22} />}
              title="Risk Thresholds"
              value="3"
              description="Low, Medium and High"
            />

            <SummaryCard
              icon={<Activity size={22} />}
              title="Detection Status"
              value="Active"
              description="Rule and anomaly detection enabled"
              status
            />
          </div>

          <div className="rules-overview-grid">
            {/* Detection engine */}
            <section className="rules-panel">
              <div className="rules-panel-header">
                <div>
                  <h3>Detection Engine</h3>
                  <p>Current SAT-SA detection pipeline</p>
                </div>

                <div className="engine-status">
                  <CheckCircle2 size={17} />
                  Operational
                </div>
              </div>

              <div className="engine-flow">
                <EngineStep
                  icon={<Database size={20} />}
                  title="Data"
                  description="Analyst & investigation data"
                />

                <div className="engine-arrow">→</div>

                <EngineStep
                  icon={<ShieldCheck size={20} />}
                  title="Rules"
                  description="Deterministic checks"
                />

                <div className="engine-arrow">→</div>

                <EngineStep
                  icon={<BrainCircuit size={20} />}
                  title="AI"
                  description="Anomaly detection"
                />

                <div className="engine-arrow">→</div>

                <EngineStep
                  icon={<Gauge size={20} />}
                  title="Risk"
                  description="Risk assessment"
                />
              </div>
            </section>

            {/* Risk distribution */}
            <section className="rules-panel">
              <div className="rules-panel-header">
                <div>
                  <h3>Risk Configuration</h3>
                  <p>Current risk score thresholds</p>
                </div>

                <SlidersHorizontal size={20} />
              </div>

              <div className="risk-level-list">
                <RiskLevel
                  label="Low"
                  range="0 – 39"
                  description="Normal behavior"
                  className="risk-low"
                />

                <RiskLevel
                  label="Medium"
                  range="40 – 69"
                  description="Requires attention"
                  className="risk-medium"
                />

                <RiskLevel
                  label="High"
                  range="70 – 100"
                  description="Requires supervisory review"
                  className="risk-high"
                />
              </div>
            </section>
          </div>

          {/* Active rules preview */}
          <section className="rules-panel">
            <div className="rules-panel-header">
              <div>
                <h3>Active Detection Rules</h3>
                <p>Rules currently contributing to analyst risk evaluation</p>
              </div>

              <button
                className="text-button"
                onClick={() => setActiveTab("rules")}
              >
                View all
              </button>
            </div>

            <div className="mini-rule-list">
              {riskRules.slice(0, 5).map((rule) => (
                <div className="mini-rule" key={rule.id}>
                  <div className="mini-rule-icon">
                    <ShieldCheck size={18} />
                  </div>

                  <div className="mini-rule-info">
                    <strong>{rule.name}</strong>
                    <span>{rule.condition}</span>
                  </div>

                  <div className="mini-rule-score">
                    +{rule.score}
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Current implementation note */}
          <section className="implementation-note">
            <div className="implementation-note-icon">
              <Info size={20} />
            </div>

            <div>
              <strong>Current implementation</strong>
              <p>
                Rules are currently predefined and evaluated by the backend.
                This Admin interface provides visibility into their
                configuration. Rule editing will be connected to backend APIs
                when available.
              </p>
            </div>
          </section>
        </div>
      )}

      {/* Detection Rules */}
      {activeTab === "rules" && (
        <div className="rules-content">
          <section className="rules-panel">
            <div className="rules-panel-header">
              <div>
                <h3>Detection Rules</h3>
                <p>
                  Explainable rules used for analyst behavioral risk
                  assessment.
                </p>
              </div>

              <div className="rule-count">
                {activeRules.length} Active
              </div>
            </div>

            <div className="rules-table-wrapper">
              <table className="rules-table">
                <thead>
                  <tr>
                    <th>Rule</th>
                    <th>Condition</th>
                    <th>Risk Contribution</th>
                    <th>Severity</th>
                    <th>Status</th>
                    <th>Action</th>
                  </tr>
                </thead>

                <tbody>
                  {activeRules.map((rule) => (
                    <tr key={rule.id}>
                      <td>
                        <div className="rule-name-cell">
                          <div className="rule-icon">
                            <ShieldCheck size={17} />
                          </div>

                          <div>
                            <strong>{rule.name}</strong>
                            <span>{rule.id}</span>
                          </div>
                        </div>
                      </td>

                      <td>
                        <span className="condition-text">
                          {rule.condition}
                        </span>
                      </td>

                      <td>
                        {rule.score > 0 ? (
                          <span className="score-badge">
                            +{rule.score}
                          </span>
                        ) : (
                          <span className="informational-score">
                            Informational
                          </span>
                        )}
                      </td>

                      <td>
                        <SeverityBadge severity={rule.severity} />
                      </td>

                      <td>
                        <span className="active-status">
                          <CheckCircle2 size={15} />
                          Active
                        </span>
                      </td>

                      <td>
                        <button
                          className="view-rule-button"
                          onClick={() => setSelectedRule(rule)}
                        >
                          <Eye size={16} />
                          View
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <section className="implementation-note">
            <div className="implementation-note-icon">
              <Info size={20} />
            </div>

            <div>
              <strong>Rule configuration is backend-controlled</strong>
              <p>
                The current backend contains predefined analyst behavior
                rules. Editing, enabling or disabling rules should only be
                activated after the backend exposes the corresponding
                configuration endpoints.
              </p>
            </div>
          </section>
        </div>
      )}

      {/* AI Models */}
      {activeTab === "models" && (
        <div className="rules-content">
          <section className="ai-model-card">
            <div className="ai-model-header">
              <div className="ai-model-title">
                <div className="ai-model-icon">
                  <BrainCircuit size={26} />
                </div>

                <div>
                  <h3>Analyst Anomaly Detection</h3>
                  <p>Isolation Forest</p>
                </div>
              </div>

              <span className="model-active-badge">
                <CheckCircle2 size={15} />
                Active
              </span>
            </div>

            <div className="ai-model-description">
              <p>
                Detects unusual analyst behavior from multiple behavioral
                metrics. The model standardizes the feature set before
                applying Isolation Forest anomaly detection.
              </p>
            </div>

            <div className="model-information-grid">
              <ModelInfo
                label="Algorithm"
                value="Isolation Forest"
              />

              <ModelInfo
                label="Estimators"
                value="200"
              />

              <ModelInfo
                label="Contamination"
                value="5%"
              />

              <ModelInfo
                label="Random State"
                value="42"
              />
            </div>
          </section>

          <section className="rules-panel">
            <div className="rules-panel-header">
              <div>
                <h3>Model Features</h3>
                <p>
                  Behavioral features currently supplied to the anomaly
                  detector.
                </p>
              </div>

              <span className="feature-count">
                {modelFeatures.length} Features
              </span>
            </div>

            <div className="model-features-grid">
              {modelFeatures.map((feature, index) => (
                <div className="model-feature" key={feature.name}>
                  <div className="feature-number">
                    {String(index + 1).padStart(2, "0")}
                  </div>

                  <div>
                    <strong>{feature.name}</strong>
                    <p>{feature.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </section>

          <section className="ai-output-panel">
            <div className="ai-output-icon">
              <Activity size={22} />
            </div>

            <div>
              <h3>Model Output</h3>
              <p>
                The anomaly detector produces an <strong>anomaly score</strong>{" "}
                and an <strong>is_anomaly</strong> result for each analyst.
              </p>
            </div>
          </section>

          <section className="implementation-note">
            <div className="implementation-note-icon">
              <Info size={20} />
            </div>

            <div>
              <strong>AI model configuration</strong>
              <p>
                Model parameters are currently controlled by the backend
                implementation. The Admin UI displays the active model and
                its features but does not modify model parameters.
              </p>
            </div>
          </section>
        </div>
      )}

      {/* Risk Configuration */}
      {activeTab === "risk" && (
        <div className="rules-content">
          <section className="risk-config-panel">
            <div className="rules-panel-header">
              <div>
                <h3>Risk Score Configuration</h3>
                <p>
                  Risk levels used by the analyst behavior evaluation
                  engine.
                </p>
              </div>

              <Gauge size={22} />
            </div>

            <div className="risk-scale">
              <div className="risk-scale-track">
                <div className="risk-segment low"></div>
                <div className="risk-segment medium"></div>
                <div className="risk-segment high"></div>
              </div>

              <div className="risk-scale-labels">
                <span>0</span>
                <span>40</span>
                <span>70</span>
                <span>100</span>
              </div>
            </div>

            <div className="risk-config-grid">
              <RiskConfigCard
                title="Low Risk"
                range="0 – 39"
                description="Analyst behavior does not currently trigger medium or high risk conditions."
                className="low"
              />

              <RiskConfigCard
                title="Medium Risk"
                range="40 – 69"
                description="Behavior requires attention and may warrant supervisory review."
                className="medium"
              />

              <RiskConfigCard
                title="High Risk"
                range="70 – 100"
                description="Behavior reaches the high-risk threshold and should receive supervisory attention."
                className="high"
              />
            </div>
          </section>

          <section className="rules-panel">
            <div className="rules-panel-header">
              <div>
                <h3>Risk Score Contributions</h3>
                <p>
                  Maximum contribution of each behavior rule to the risk
                  score.
                </p>
              </div>
            </div>

            <div className="contribution-list">
              {riskRules.map((rule) => (
                <div className="contribution-row" key={rule.id}>
                  <div>
                    <strong>{rule.name}</strong>
                    <span>{rule.condition}</span>
                  </div>

                  <div className="contribution-bar-container">
                    <div
                      className="contribution-bar"
                      style={{
                        width: `${(rule.score / 30) * 100}%`,
                      }}
                    ></div>
                  </div>

                  <strong className="contribution-value">
                    +{rule.score}
                  </strong>
                </div>
              ))}
            </div>
          </section>

          <section className="implementation-note">
            <div className="implementation-note-icon">
              <AlertTriangle size={20} />
            </div>

            <div>
              <strong>Configuration is read-only for now</strong>
              <p>
                These values mirror the current backend rule engine. We will
                connect editable controls only after the backend API contract
                is available.
              </p>
            </div>
          </section>
        </div>
      )}

      {/* Rule Details Modal */}
      {selectedRule && (
        <div
          className="modal-overlay"
          onClick={() => setSelectedRule(null)}
        >
          <div
            className="rule-detail-modal"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="modal-header">
              <div>
                <div className="modal-title-row">
                  <div className="rule-modal-icon">
                    <ShieldCheck size={21} />
                  </div>

                  <div>
                    <h3>{selectedRule.name}</h3>
                    <span>{selectedRule.id}</span>
                  </div>
                </div>
              </div>

              <button
                className="modal-close"
                onClick={() => setSelectedRule(null)}
              >
                <X size={20} />
              </button>
            </div>

            <div className="rule-modal-body">
              <div className="rule-detail-status">
                <span>
                  <CheckCircle2 size={16} />
                  Active Rule
                </span>

                <SeverityBadge severity={selectedRule.severity} />
              </div>

              <div className="rule-detail-section">
                <label>Description</label>
                <p>{selectedRule.description}</p>
              </div>

              <div className="rule-detail-section">
                <label>Detection Condition</label>

                <div className="condition-box">
                  <Clock3 size={17} />
                  {selectedRule.condition}
                </div>
              </div>

              <div className="rule-detail-stats">
                <div>
                  <span>Risk Contribution</span>
                  <strong>
                    {selectedRule.score > 0
                      ? `+${selectedRule.score}`
                      : "None"}
                  </strong>
                </div>

                <div>
                  <span>Rule Status</span>
                  <strong>Active</strong>
                </div>
              </div>

              <div className="rule-explanation">
                <Info size={18} />

                <p>
                  This rule is deterministic and explainable. When its
                  condition is satisfied, the configured risk contribution
                  is added to the analyst's behavioral risk score.
                </p>
              </div>
            </div>

            <div className="modal-footer">
              <button
                className="secondary-button"
                onClick={() => setSelectedRule(null)}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

/* -------------------------------------------------------
   Components
------------------------------------------------------- */

interface SummaryCardProps {
  icon: React.ReactNode;
  title: string;
  value: string;
  description: string;
  status?: boolean;
}

function SummaryCard({
  icon,
  title,
  value,
  description,
  status,
}: SummaryCardProps) {
  return (
    <div className="rules-summary-card">
      <div className="summary-card-top">
        <div className="summary-card-icon">{icon}</div>

        {status && (
          <span className="summary-active">
            <span></span>
            Active
          </span>
        )}
      </div>

      <strong className="summary-card-value">{value}</strong>
      <span className="summary-card-title">{title}</span>
      <p>{description}</p>
    </div>
  );
}

interface EngineStepProps {
  icon: React.ReactNode;
  title: string;
  description: string;
}

function EngineStep({
  icon,
  title,
  description,
}: EngineStepProps) {
  return (
    <div className="engine-step">
      <div className="engine-step-icon">{icon}</div>

      <strong>{title}</strong>
      <span>{description}</span>
    </div>
  );
}

interface RiskLevelProps {
  label: string;
  range: string;
  description: string;
  className: string;
}

function RiskLevel({
  label,
  range,
  description,
  className,
}: RiskLevelProps) {
  return (
    <div className={`risk-level ${className}`}>
      <div className="risk-level-indicator"></div>

      <div>
        <strong>{label}</strong>
        <span>{range}</span>
      </div>

      <p>{description}</p>
    </div>
  );
}

function SeverityBadge({
  severity,
}: {
  severity: DetectionRule["severity"];
}) {
  return (
    <span
      className={`severity-badge severity-${severity.toLowerCase()}`}
    >
      {severity}
    </span>
  );
}

function ModelInfo({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="model-info">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

interface RiskConfigCardProps {
  title: string;
  range: string;
  description: string;
  className: string;
}

function RiskConfigCard({
  title,
  range,
  description,
  className,
}: RiskConfigCardProps) {
  return (
    <div className={`risk-config-card ${className}`}>
      <div className="risk-config-card-header">
        <strong>{title}</strong>
        <span>{range}</span>
      </div>

      <p>{description}</p>
    </div>
  );
}

export default RulesAI;
