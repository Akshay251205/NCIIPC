import { useEffect, useMemo, useState } from "react";
import {
  Users,
  AlertTriangle,
  Clock,
  CheckCircle,
  Search,
  Filter,
  ChevronRight,
  ShieldAlert,
} from "lucide-react";
import "./Analysts.css";
import { useNavigate } from "react-router-dom";

const fallbackAnalysts = [
  {
    id: "AN-001",
    name: "Aarav Sharma",
    organization: "Organization Alpha",
    status: "Healthy",
    closureRate: 91,
    evidenceReview: 88,
    escalationAccuracy: 94,
    investigationCompletion: 92,
    avgClosureTime: "3.2 hrs",
  },
  {
    id: "AN-002",
    name: "Priya Singh",
    organization: "Organization Alpha",
    status: "Needs Attention",
    closureRate: 68,
    evidenceReview: 61,
    escalationAccuracy: 73,
    investigationCompletion: 70,
    avgClosureTime: "6.8 hrs",
  },
  {
    id: "AN-003",
    name: "Rahul Verma",
    organization: "Organization Beta",
    status: "Healthy",
    closureRate: 87,
    evidenceReview: 82,
    escalationAccuracy: 90,
    investigationCompletion: 89,
    avgClosureTime: "4.1 hrs",
  },
  {
    id: "AN-004",
    name: "Ananya Gupta",
    organization: "Organization Gamma",
    status: "High Risk",
    closureRate: 54,
    evidenceReview: 48,
    escalationAccuracy: 59,
    investigationCompletion: 57,
    avgClosureTime: "9.4 hrs",
  },
  {
    id: "AN-005",
    name: "Vikram Mehta",
    organization: "Organization Beta",
    status: "Healthy",
    closureRate: 84,
    evidenceReview: 79,
    escalationAccuracy: 86,
    investigationCompletion: 85,
    avgClosureTime: "4.6 hrs",
  },
  {
    id: "AN-006",
    name: "Neha Kapoor",
    organization: "Organization Delta",
    status: "Needs Attention",
    closureRate: 71,
    evidenceReview: 67,
    escalationAccuracy: 76,
    investigationCompletion: 73,
    avgClosureTime: "6.1 hrs",
  },
];

function Analysts() {
  const navigate = useNavigate();
  const [analysts, setAnalysts] = useState(fallbackAnalysts);
  const [total, setTotal] = useState(fallbackAnalysts.length);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    let active = true;
    fetch("/api/v1/analysts/performance?limit=100").then((response) => {
      if (!response.ok) throw new Error("Unable to load analysts");
      return response.json() as Promise<{ total: number; data: Array<{ analyst_id: string; name: string; organization_id: string; status: string | null; closure_rate: number; evidence_review_rate: number; escalation_rate: number; investigation_completion: number; avg_closure_time_minutes: number | null }> }>;
    }).then((result) => {
      if (!active) return;
      setTotal(result.total);
      setAnalysts(result.data.map((analyst) => ({
        id: analyst.analyst_id,
        name: analyst.name,
        organization: analyst.organization_id,
        status: analyst.status ?? "Unknown",
        closureRate: Math.round(analyst.closure_rate),
        evidenceReview: Math.round(analyst.evidence_review_rate),
        escalationAccuracy: Math.round(analyst.escalation_rate),
        investigationCompletion: analyst.investigation_completion,
        avgClosureTime: analyst.avg_closure_time_minutes == null ? "—" : `${Math.round(analyst.avg_closure_time_minutes)} min`,
      })));
    }).catch(() => undefined).finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, []);
  const filteredAnalysts = useMemo(() => analysts.filter((analyst) => `${analyst.name} ${analyst.id} ${analyst.organization}`.toLowerCase().includes(search.toLowerCase())), [analysts, search]);
  return (
    <div className="analysts-page">
      {/* Page Header */}
      <div className="analysts-header">
        <div>
          <h1>Analysts</h1>
          <p>
            Monitor analyst performance, investigation quality, and behavioral
            indicators.
          </p>
        </div>

        <button className="filter-button">
          <Filter size={17} />
          Filters
        </button>
      </div>

      {/* KPI Cards */}
      <div className="analyst-kpi-grid">
        <div className="analyst-kpi-card">
          <div className="analyst-kpi-icon">
            <Users size={21} />
          </div>

          <div>
            <span>Total Analysts</span>
            <strong>{total.toLocaleString()}</strong>
            <small>Across all organizations</small>
          </div>
        </div>

        <div className="analyst-kpi-card">
          <div className="analyst-kpi-icon warning">
            <AlertTriangle size={21} />
          </div>

          <div>
            <span>Need Attention</span>
            <strong>5</strong>
            <small>Require supervisor review</small>
          </div>
        </div>

        <div className="analyst-kpi-card">
          <div className="analyst-kpi-icon">
            <Clock size={21} />
          </div>

          <div>
            <span>Avg Closure Time</span>
            <strong>5.2 hrs</strong>
            <small>Across active investigations</small>
          </div>
        </div>

        <div className="analyst-kpi-card">
          <div className="analyst-kpi-icon success">
            <CheckCircle size={21} />
          </div>

          <div>
            <span>Avg Completion</span>
            <strong>81%</strong>
            <small>Investigation completion</small>
          </div>
        </div>
      </div>

      {/* Attention Banner */}
      <div className="analyst-attention-banner">
        <div className="attention-icon">
          <ShieldAlert size={20} />
        </div>

        <div>
          <strong>5 analysts require attention</strong>
          <p>
            Some analysts show lower investigation quality or unusual
            behavioral indicators.
          </p>
        </div>

        <button>Review Analysts</button>
      </div>

      {/* Analyst Table */}
      <section className="analyst-section">
        <div className="section-header">
          <div>
            <h2>Analyst Performance</h2>
            <p>Performance indicators across monitored analysts.</p>
          </div>

          <div className="analyst-search">
            <Search size={17} />
            <input placeholder="Search analysts..." value={search} onChange={(event) => setSearch(event.target.value)} />
          </div>
        </div>

        <div className="analyst-table-wrapper">
          <table className="analyst-table">
            <thead>
              <tr>
                <th>Analyst</th>
                <th>Organization</th>
                <th>Status</th>
                <th>Closure Rate</th>
                <th>Evidence Review</th>
                <th>Escalation Accuracy</th>
                <th>Completion</th>
                <th>Avg Closure</th>
                <th></th>
              </tr>
            </thead>

            <tbody>
              {filteredAnalysts.map((analyst) => (
                <tr key={analyst.id}>
                  <td>
                    <div className="analyst-name-cell">
                      <div className="analyst-avatar">
                        {analyst.name.charAt(0)}
                      </div>

                      <div>
                        <strong>{analyst.name}</strong>
                        <span>{analyst.id}</span>
                      </div>
                    </div>
                  </td>

                  <td>{analyst.organization}</td>

                  <td>
                    <span
                      className={`analyst-status ${analyst.status
                        .toLowerCase()
                        .replace(" ", "-")}`}
                    >
                      {analyst.status}
                    </span>
                  </td>

                  <td>
                    <div className="metric-cell">
                      <strong>{analyst.closureRate}%</strong>
                      <div className="metric-bar">
                        <div
                          className="metric-fill"
                          style={{
                            width: `${analyst.closureRate}%`,
                          }}
                        />
                      </div>
                    </div>
                  </td>

                  <td>
                    <span className="percentage">
                      {analyst.evidenceReview}%
                    </span>
                  </td>

                  <td>
                    <span className="percentage">
                      {analyst.escalationAccuracy}%
                    </span>
                  </td>

                  <td>
                    <span className="percentage">
                      {analyst.investigationCompletion}%
                    </span>
                  </td>

                  <td>{analyst.avgClosureTime}</td>

                  <td>
                    <button
                    className="analyst-details-button"
                    onClick={() =>
                        navigate(`/supervisor/analysts/${analyst.id}`)
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
        <div className="analyst-pagination">
          <span>{loading ? "Loading analysts…" : `Showing ${filteredAnalysts.length} of ${total.toLocaleString()} analysts`}</span>

          <div>
            <button disabled>Previous</button>
            <button className="active-page">1</button>
            <button>2</button>
            <button>3</button>
            <button>4</button>
            <button>Next</button>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Analysts;
