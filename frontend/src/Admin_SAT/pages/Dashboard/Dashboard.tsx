import {
  Building2,
  Users,
  UserRoundCheck,
  ShieldAlert,
  ClipboardCheck,
  Server,
  Database,
  Code2,
  BrainCircuit,
  Settings,
  UploadCloud,
  Plus,
  ArrowUpRight,
  Activity,
} from "lucide-react";

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  PieChart,
  Pie,
  Cell,
} from "recharts";

import {
  alertTrendData,
  sectorData,
  recentActivity,
} from "../../data/mockData";
import { useNavigate } from "react-router-dom";
import { useDashboardData } from "../../../hooks/useDashboardData";

const statIcons = {
  organization: Building2,
  users: Users,
  analysts: UserRoundCheck,
  alerts: ShieldAlert,
  investigations: ClipboardCheck,
  assets: Server,
};

function Dashboard() {
  const navigate = useNavigate();
  const { overview, risk, loading, error, refresh } = useDashboardData();
  const dashboardStats = [
    { title: "Organizations", value: overview?.total_organizations.toLocaleString() ?? "—", change: "Live", description: "registered organizations", type: "organization" as const },
    { title: "Analysts", value: overview?.total_analysts.toLocaleString() ?? "—", change: "Live", description: "active analyst records", type: "analysts" as const },
    { title: "Total Alerts", value: overview?.total_alerts.toLocaleString() ?? "—", change: "Live", description: "security alerts", type: "alerts" as const },
    { title: "Investigations", value: overview?.total_investigations.toLocaleString() ?? "—", change: "Live", description: "tracked investigations", type: "investigations" as const },
    { title: "Assets", value: overview?.total_assets.toLocaleString() ?? "—", change: "Live", description: "monitored assets", type: "assets" as const },
  ];
  const severityData = [
    { name: "Critical", value: risk?.critical_alerts ?? 0 },
    { name: "High", value: risk?.high_alerts ?? 0 },
    { name: "Medium", value: risk?.medium_alerts ?? 0 },
    { name: "Low", value: risk?.low_alerts ?? 0 },
  ];
  return (
    <div className="dashboard-page">

      {/* PAGE HEADER */}

      <div className="page-heading">
        <div>
          <h2>Welcome, Admin</h2>
          <p>
            Here's an overview of your SAT-SA system.
          </p>
        </div>

        <div className="dashboard-date">
          <span>System Overview</span>
          <strong>{loading ? "Loading live data…" : "Live backend data"}</strong>
        </div>
        <button className="view-link" onClick={() => void refresh()} disabled={loading}>
          {loading ? "Refreshing…" : "Refresh"}
        </button>
      </div>

      {error && <div className="admin-data-message" role="status">{error}</div>}

      {/* KPI CARDS */}

      <section className="stats-grid">
        {dashboardStats.map((stat) => {
          const Icon = statIcons[stat.type];

          return (
            <div className="stat-card" key={stat.title}>
              <div className="stat-card-top">
                <div className={`stat-icon ${stat.type}`}>
                  <Icon size={21} />
                </div>

                <button className="stat-more" onClick={() => navigate(stat.type === "organization" ? "/admin/organizations" : stat.type === "analysts" ? "/admin/users" : "/admin/data")}>
                  <ArrowUpRight size={17} />
                </button>
              </div>

              <div className="stat-value">
                {stat.value}
              </div>

              <div className="stat-title">
                {stat.title}
              </div>

              <div className="stat-change">
                <span>{stat.change}</span>
                {stat.description}
              </div>
            </div>
          );
        })}
      </section>

      {/* SYSTEM HEALTH */}

      <section className="dashboard-grid-two">

        <div className="dashboard-card system-health-card">
          <div className="card-header">
            <div>
              <h3>System Health</h3>
              <p>Current status of SAT-SA services</p>
            </div>

            <button className="view-link" onClick={() => navigate("/admin/settings")}>
              View details
              <ArrowUpRight size={15} />
            </button>
          </div>

          <div className="health-grid">

            <HealthItem
              icon={<Database size={19} />}
              name="Database"
              status="Healthy"
            />

            <HealthItem
              icon={<Code2 size={19} />}
              name="API Services"
              status="Operational"
            />

            <HealthItem
              icon={<Settings size={19} />}
              name="Rule Engine"
              status="Running"
            />

            <HealthItem
              icon={<BrainCircuit size={19} />}
              name="AI Models"
              status="Loaded"
            />

          </div>
        </div>

        {/* DATA INGESTION */}

        <div className="dashboard-card ingestion-card">

          <div className="card-header">
            <div>
              <h3>Data Ingestion</h3>
              <p>Dataset processing status</p>
            </div>

            <button className="view-link" onClick={() => navigate("/admin/data")}>
              View all
              <ArrowUpRight size={15} />
            </button>
          </div>

          <div className="ingestion-content">

            <div className="progress-ring">
              <div>
                <strong>78%</strong>
                <span>Processed</span>
              </div>
            </div>

            <div className="ingestion-stats">

              <div>
                <span>Total Records</span>
                <strong>{overview?.total_alerts.toLocaleString() ?? "—"}</strong>
              </div>

              <div>
                <span>Processed</span>
                <strong>{overview?.open_alerts.toLocaleString() ?? "—"}</strong>
              </div>

              <div>
                <span>Pending</span>
                <strong>{overview?.total_investigations.toLocaleString() ?? "—"}</strong>
              </div>

              <div>
                <span>Failed</span>
                <strong className="danger-text">
                  {overview?.critical_alerts.toLocaleString() ?? "—"}
                </strong>
              </div>

            </div>

          </div>
        </div>

      </section>

      {/* CHARTS */}

      <section className="dashboard-grid-main">

        {/* ALERT TREND */}

        <div className="dashboard-card trend-card">

          <div className="card-header">

            <div>
              <h3>Alerts Trend</h3>
              <p>Alert volume over the last 8 days</p>
            </div>

            <select className="chart-select">
              <option>Last 8 days</option>
              <option>Last 30 days</option>
              <option>Last 90 days</option>
            </select>

          </div>

          <div className="chart-container">

            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={alertTrendData}>

                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                  stroke="#e9eef4"
                />

                <XAxis
                  dataKey="day"
                  axisLine={false}
                  tickLine={false}
                  tick={{
                    fill: "#7b8798",
                    fontSize: 11,
                  }}
                />

                <YAxis
                  axisLine={false}
                  tickLine={false}
                  tick={{
                    fill: "#7b8798",
                    fontSize: 11,
                  }}
                  tickFormatter={(value) =>
                    `${value / 1000}K`
                  }
                />

                <Tooltip />

                <Line
                  type="monotone"
                  dataKey="alerts"
                  stroke="#2468b1"
                  strokeWidth={2.5}
                  dot={{
                    r: 4,
                    fill: "#2468b1",
                  }}
                  activeDot={{
                    r: 6,
                  }}
                />

              </LineChart>
            </ResponsiveContainer>

          </div>
        </div>

        {/* SEVERITY */}

        <div className="dashboard-card severity-card">

          <div className="card-header">

            <div>
              <h3>Alerts by Severity</h3>
              <p>Current alert distribution</p>
            </div>

          </div>

          <div className="severity-content">

            <div className="severity-chart">

              <ResponsiveContainer
                width="100%"
                height="100%"
              >
                <PieChart>

                  <Pie
                    data={severityData}
                    dataKey="value"
                    nameKey="name"
                    innerRadius={58}
                    outerRadius={82}
                    paddingAngle={2}
                  >
                    <Cell fill="#dc3545" />
                    <Cell fill="#e98235" />
                    <Cell fill="#e8b83e" />
                    <Cell fill="#35a86b" />
                  </Pie>

                </PieChart>
              </ResponsiveContainer>

              <div className="donut-center">
                <strong>{overview?.total_alerts.toLocaleString() ?? "—"}</strong>
                <span>Total Alerts</span>
              </div>

            </div>

            <div className="severity-list">

              {severityData.map((item, index) => (
                <div
                  className="severity-item"
                  key={item.name}
                >
                  <div>
                    <i
                      className={`severity-dot severity-${index}`}
                    />

                    <span>{item.name}</span>
                  </div>

                  <strong>
                    {item.value.toLocaleString()}
                  </strong>
                </div>
              ))}

            </div>

          </div>
        </div>

      </section>

      {/* SECTOR + ACTIVITY */}

      <section className="dashboard-grid-two">

        {/* ORGANIZATIONS BY SECTOR */}

        <div className="dashboard-card sector-card">

          <div className="card-header">

            <div>
              <h3>Organizations by Sector</h3>
              <p>Registered organizations</p>
            </div>

            <button className="view-link" onClick={() => navigate("/admin/organizations")}>
              View all
              <ArrowUpRight size={15} />
            </button>

          </div>

          <div className="sector-list">

            {sectorData.map((item) => (
              <div
                className="sector-row"
                key={item.sector}
              >
                <div className="sector-label">
                  <span>{item.sector}</span>
                  <strong>
                    {item.organizations}
                  </strong>
                </div>

                <div className="sector-bar">
                  <span
                    style={{
                      width: `${(item.organizations / 12) * 100}%`,
                    }}
                  />
                </div>
              </div>
            ))}

          </div>
        </div>

        {/* RECENT ACTIVITY */}

        <div className="dashboard-card activity-card">

          <div className="card-header">

            <div>
              <h3>Recent System Activity</h3>
              <p>Latest administrative actions</p>
            </div>

            <button className="view-link" onClick={() => navigate("/admin/audit")}>
              View all
              <ArrowUpRight size={15} />
            </button>

          </div>

          <div className="activity-list">

            {recentActivity.map((item) => (
              <div
                className="activity-row"
                key={`${item.time}-${item.action}`}
              >

                <div className="activity-icon">
                  <Activity size={16} />
                </div>

                <div className="activity-info">
                  <strong>{item.action}</strong>

                  <span>
                    {item.user} · {item.detail}
                  </span>
                </div>

                <div className="activity-right">
                  <span>{item.time}</span>
                  <small>{item.status}</small>
                </div>

              </div>
            ))}

          </div>
        </div>

      </section>

      {/* QUICK ACTIONS */}

      <section className="quick-actions-section">

        <div className="section-title">
          <div>
            <h3>Quick Actions</h3>
            <p>Common administrative operations</p>
          </div>
        </div>

        <div className="quick-actions-grid">

          <QuickAction
            icon={<Building2 size={21} />}
            title="Add Organization"
            description="Register a new CSE"
            onClick={() => navigate("/admin/organizations")}
          />

          <QuickAction
            icon={<Users size={21} />}
            title="Add User"
            description="Create an administrator or analyst"
            onClick={() => navigate("/admin/users")}
          />

          <QuickAction
            icon={<UploadCloud size={21} />}
            title="Upload Dataset"
            description="Import SOC data"
            onClick={() => navigate("/admin/data")}
          />

          <QuickAction
            icon={<Settings size={21} />}
            title="Configure Rules"
            description="Manage detection rules"
            onClick={() => navigate("/admin/rules")}
          />

        </div>

      </section>

    </div>
  );
}


/* =========================
   HEALTH ITEM
========================= */

interface HealthItemProps {
  icon: React.ReactNode;
  name: string;
  status: string;
}

function HealthItem({
  icon,
  name,
  status,
}: HealthItemProps) {
  return (
    <div className="health-item">

      <div className="health-icon">
        {icon}
      </div>

      <div>
        <strong>{name}</strong>

        <span>
          <i />
          {status}
        </span>
      </div>

    </div>
  );
}


/* =========================
   QUICK ACTION
========================= */

interface QuickActionProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  onClick: () => void;
}

function QuickAction({
  icon,
  title,
  description,
  onClick,
}: QuickActionProps) {
  return (
    <button className="quick-action" onClick={onClick}>

      <div className="quick-action-icon">
        {icon}
      </div>

      <div>
        <strong>{title}</strong>
        <span>{description}</span>
      </div>

      <Plus size={17} />

    </button>
  );
}

export default Dashboard;
