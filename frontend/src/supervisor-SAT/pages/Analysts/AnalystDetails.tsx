import {
  ArrowLeft,
  ShieldAlert,
  Clock,
  CheckCircle2,
  AlertTriangle,
  TrendingUp,
  TrendingDown,
  Activity,
  FileWarning,
} from "lucide-react";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import "./AnalystDetails.css";
import { useFeedback } from "../../../components/feedback";

type AnalystProfile = { analyst_id: string; organization_id: string; name: string; role: string | null; team: string | null; experience_years: number | null; shift: string | null; status: string | null };
type AnalystIntelligence = { risk: { score: number; level: string; indicators: string[] }; evidence_context: { performance: { average_closure_time_minutes: number | null; closure_rate: number; evidence_review_rate: number; escalation_rate: number }; investigations: { total: number; average_duration_minutes: number | null } }; behavioral_anomaly: { observations: string[] }; recommendations: string[] };

export default function AnalystDetails() {
  const navigate = useNavigate();
  const { id } = useParams();
  const notify = useFeedback();
  const [analyst, setAnalyst] = useState<AnalystProfile | null>(null);
  const [draft, setDraft] = useState<AnalystProfile | null>(null);
  const [editing, setEditing] = useState(false);
  const [intelligence, setIntelligence] = useState<AnalystIntelligence | null>(null);

  useEffect(() => {
    if (!id) return;
    let active = true;
    fetch(`/api/v1/analysts/${id}`).then((response) => {
      if (!response.ok) throw new Error("Analyst not found");
      return response.json() as Promise<AnalystProfile>;
    }).then((profile) => { if (active) { setAnalyst(profile); setDraft(profile); } }).catch(() => { if (active) notify("Analyst unavailable", "The requested analyst could not be loaded from the API."); });
    return () => { active = false; };
  }, [id, notify]);

  useEffect(() => {
    if (!id) return;
    let active = true;
    fetch(`/intelligence/analysts/${id}/profile`).then((response) => {
      if (!response.ok) throw new Error("Intelligence unavailable");
      return response.json() as Promise<AnalystIntelligence>;
    }).then((data) => { if (active) setIntelligence(data); }).catch(() => { if (active) setIntelligence(null); });
    return () => { active = false; };
  }, [id]);

  const profile = analyst ?? { analyst_id: id ?? "—", organization_id: "Loading…", name: "Loading analyst…", role: "—", team: "—", experience_years: null, shift: "—", status: "Unknown" };
  const performance = intelligence?.evidence_context.performance;
  const investigation = intelligence?.evidence_context.investigations;
  const riskScore = intelligence?.risk.score ?? 0;
  const percentage = (value: number | undefined) => `${Math.round(value ?? 0)}%`;
  const saveProfile = async () => {
    if (!draft || !id) return;
    const response = await fetch(`/api/v1/analysts/${id}`, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name: draft.name, role: draft.role, team: draft.team, experience_years: draft.experience_years, shift: draft.shift, status: draft.status }) });
    if (!response.ok) { notify("Save failed", "The analyst profile could not be updated."); return; }
    const saved = await response.json() as AnalystProfile;
    setAnalyst(saved); setDraft(saved); setEditing(false); notify("Profile updated", `${saved.name}'s analyst record is saved to the backend.`);
  };

  return (
    <div className="analyst-details">

      {/* Back Button */}
      <button
        className="analyst-back-button"
        onClick={() => navigate("/supervisor/analysts")}
      >
        <ArrowLeft size={16} />
        Back to Analysts
      </button>

      {/* Analyst Header */}
      <div className="analyst-details-header">

        <div className="analyst-details-title">

          <div className="analyst-details-avatar">
            {profile.name.charAt(0)}
          </div>

          <div>
            <span className="analyst-details-code">
              {profile.analyst_id}
            </span>

            <h1>{profile.name}</h1>

            <p>
              {profile.organization_id} · {profile.role ?? "Security Operations Analyst"}
            </p>
          </div>

        </div>

        <div className="analyst-assessment-status">
          <span>Analyst Status</span>

          <strong>
            <CheckCircle2 size={14} />
            {profile.status ?? "Unknown"}
          </strong>
        </div>

      </div>

      <section className="analyst-details-card analyst-edit-card">
        <div className="analyst-card-header"><div><h3>Analyst Profile</h3><p>Profile fields are saved directly to the SAT-SA backend.</p></div><button className="profile-button" onClick={() => editing ? void saveProfile() : setEditing(true)}>{editing ? "Save profile" : "Edit profile"}</button></div>
        {editing && draft ? <div className="analyst-edit-grid">
          {(["name", "role", "team", "shift", "status"] as const).map((field) => <label key={field}>{field}<input value={draft[field] ?? ""} onChange={(event) => setDraft({ ...draft, [field]: event.target.value })} /></label>)}
          <label>Experience years<input type="number" min="0" value={draft.experience_years ?? ""} onChange={(event) => setDraft({ ...draft, experience_years: event.target.value === "" ? null : Number(event.target.value) })} /></label>
          <button className="secondary-button" onClick={() => { setDraft(analyst); setEditing(false); }}>Cancel</button>
        </div> : <div className="analyst-profile-summary"><span>Team: <strong>{profile.team ?? "—"}</strong></span><span>Shift: <strong>{profile.shift ?? "—"}</strong></span><span>Experience: <strong>{profile.experience_years ?? "—"} years</strong></span></div>}
      </section>

      {/* Performance Summary */}
      <section className="analyst-summary-grid">

        {/* Overall Performance */}
        <div className="analyst-performance-card">

          <div className="analyst-performance-header">

            <div>
              <span>Overall Performance</span>

              <h2>
                {Math.round(100 - riskScore)}<span>/100</span>
              </h2>
            </div>

            <div className="analyst-good-badge">
              Healthy
            </div>

          </div>

          <div className="analyst-performance-progress">
            <div
              className="analyst-performance-value"
              style={{ width: `${100 - riskScore}%` }}
            />
          </div>

          <p>
            Analyst performance is above the recommended operational
            benchmark.
          </p>

        </div>

        {/* Closure Time */}
        <div className="analyst-stat-card">

          <div className="analyst-stat-icon time">
            <Clock size={20} />
          </div>

          <span>Avg Closure Time</span>

          <strong>{performance?.average_closure_time_minutes == null ? "—" : `${performance.average_closure_time_minutes} min`}</strong>

          <small>
            <TrendingDown size={12} />
            18% faster than peers
          </small>

        </div>

        {/* Evidence Review */}
        <div className="analyst-stat-card">

          <div className="analyst-stat-icon evidence">
            <FileWarning size={20} />
          </div>

          <span>Evidence Review</span>

          <strong>{percentage(performance?.evidence_review_rate)}</strong>

          <small>
            Good evidence coverage
          </small>

        </div>

        {/* Escalation Accuracy */}
        <div className="analyst-stat-card">

          <div className="analyst-stat-icon accuracy">
            <ShieldAlert size={20} />
          </div>

          <span>Escalation Accuracy</span>

          <strong>{percentage(performance?.escalation_rate)}</strong>

          <small>
            <TrendingUp size={12} />
            6% above peer average
          </small>

        </div>

      </section>

      {/* Investigation Quality */}
      <section className="analyst-details-card">

        <div className="analyst-card-header">

          <div>
            <h3>Investigation Quality</h3>

            <p>
              Key indicators used to evaluate analyst investigation
              performance.
            </p>
          </div>

          <Activity size={18} />

        </div>

        <div className="analyst-quality-grid">

          <div className="analyst-quality-item">

            <div className="analyst-quality-top">
              <span>Alert Closure Rate</span>
              <strong>{percentage(performance?.closure_rate)}</strong>
            </div>

            <div className="analyst-quality-bar">
              <div
                className="analyst-quality-fill good"
                style={{ width: percentage(performance?.closure_rate) }}
              />
            </div>

            <small>
              Strong alert handling performance
            </small>

          </div>

          <div className="analyst-quality-item">

            <div className="analyst-quality-top">
              <span>Evidence Review</span>
              <strong>{percentage(performance?.evidence_review_rate)}</strong>
            </div>

            <div className="analyst-quality-bar">
              <div
                className="analyst-quality-fill good"
                style={{ width: percentage(performance?.evidence_review_rate) }}
              />
            </div>

            <small>
              Evidence coverage is healthy
            </small>

          </div>

          <div className="analyst-quality-item">

            <div className="analyst-quality-top">
              <span>Escalation Accuracy</span>
              <strong>{percentage(performance?.escalation_rate)}</strong>
            </div>

            <div className="analyst-quality-bar">
              <div
                className="analyst-quality-fill good"
                style={{ width: percentage(performance?.escalation_rate) }}
              />
            </div>

            <small>
              High-quality escalation decisions
            </small>

          </div>

          <div className="analyst-quality-item">

            <div className="analyst-quality-top">
              <span>Investigation Completion</span>
              <strong>{investigation?.total ?? 0}</strong>
            </div>

            <div className="analyst-quality-bar">
              <div
                className="analyst-quality-fill good"
                style={{ width: `${Math.min((investigation?.total ?? 0) * 20, 100)}%` }}
              />
            </div>

            <small>
              Investigations are completed consistently
            </small>

          </div>

        </div>

      </section>

      {/* Two Column Section */}
      <section className="analyst-two-column">

        {/* Behavioral Indicators */}
        <div className="analyst-details-card">

          <div className="analyst-card-header">

            <div>
              <h3>Behavioral Indicators</h3>

              <p>
                Activity patterns identified from analyst behavior.
              </p>
            </div>

            <ShieldAlert size={18} />

          </div>

          <div className="behavior-list">

            <div className="behavior-item">

              <div className="behavior-icon good">
                <CheckCircle2 size={16} />
              </div>

              <div>
                <strong>Normal Investigation Pace</strong>

                <span>
                  Investigation activity is consistent with peer behavior.
                </span>
              </div>

              <div className="behavior-status good-status">
                Normal
              </div>

            </div>

            <div className="behavior-item">

              <div className="behavior-icon good">
                <CheckCircle2 size={16} />
              </div>

              <div>
                <strong>Evidence Collection</strong>

                <span>
                  Evidence review patterns are within the expected range.
                </span>
              </div>

              <div className="behavior-status good-status">
                Normal
              </div>

            </div>

            <div className="behavior-item">

              <div className="behavior-icon warning">
                <AlertTriangle size={16} />
              </div>

              <div>
                <strong>After-hours Activity</strong>

                <span>
                  Slight increase in investigation activity outside normal
                  working hours.
                </span>
              </div>

              <div className="behavior-status warning-status">
                Monitor
              </div>

            </div>

          </div>

        </div>

        {/* Peer Benchmark */}
        <div className="analyst-details-card">

          <div className="analyst-card-header">

            <div>
              <h3>Peer Benchmark</h3>

              <p>
                Comparison with analysts of similar operational profile.
              </p>
            </div>

            <TrendingUp size={18} />

          </div>

          <div className="analyst-benchmark">

            <div className="analyst-benchmark-item">
              <span>Analyst Performance</span>
              <strong>88</strong>
              <small>+11 above peer average</small>
            </div>

            <div className="analyst-benchmark-item">
              <span>Peer Average</span>
              <strong>77</strong>
              <small>Current peer baseline</small>
            </div>

            <div className="analyst-benchmark-item">
              <span>Evidence Review</span>
              <strong>88%</strong>
              <small>+8% above peers</small>
            </div>

            <div className="analyst-benchmark-item">
              <span>Closure Rate</span>
              <strong>91%</strong>
              <small>+9% above peers</small>
            </div>

          </div>

        </div>

      </section>

      {/* Recent Investigations */}
      <section className="analyst-details-card">

        <div className="analyst-card-header">

          <div>
            <h3>Recent Investigations</h3>

            <p>
              Latest investigation activity handled by this analyst.
            </p>
          </div>

        </div>

        <div className="investigation-list">

          <div className="investigation-item">

            <div className="investigation-icon critical">
              <AlertTriangle size={16} />
            </div>

            <div>
              <strong>
                Suspicious Authentication Activity
              </strong>

              <span>
                High-severity authentication anomaly investigation.
              </span>
            </div>

            <div className="investigation-right">
              <span className="investigation-high">
                High
              </span>

              <small>
                <Clock size={11} />
                24 min ago
              </small>
            </div>

          </div>

          <div className="investigation-item">

            <div className="investigation-icon normal">
              <CheckCircle2 size={16} />
            </div>

            <div>
              <strong>
                Unusual Network Traffic
              </strong>

              <span>
                Investigation completed with supporting evidence.
              </span>
            </div>

            <div className="investigation-right">
              <span className="investigation-medium">
                Medium
              </span>

              <small>
                <Clock size={11} />
                1 hr ago
              </small>
            </div>

          </div>

          <div className="investigation-item">

            <div className="investigation-icon normal">
              <CheckCircle2 size={16} />
            </div>

            <div>
              <strong>
                Endpoint Security Alert
              </strong>

              <span>
                Alert reviewed and closed after evidence validation.
              </span>
            </div>

            <div className="investigation-right">
              <span className="investigation-low">
                Low
              </span>

              <small>
                <Clock size={11} />
                2 hrs ago
              </small>
            </div>

          </div>

        </div>

      </section>

    </div>
  );
}
