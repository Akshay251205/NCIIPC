import { useMemo, useState } from "react";
import {
  ClipboardList,
  CheckCircle2,
  XCircle,
  Activity,
  Search,
  Eye,
  X,
  User,
  Database,
  ShieldCheck,
  BrainCircuit,
  Settings,
  Clock3,
  FileText,
} from "lucide-react";

interface AuditLog {
  id: string;
  timestamp: string;
  user: string;
  role: string;
  action: string;
  module: string;
  details: string;
  source: string;
  status: "Success" | "Failed";
}

const auditLogs: AuditLog[] = [
  {
    id: "AUD-00001",
    timestamp: "14 Sep 2026, 14:32",
    user: "Admin",
    role: "Administrator",
    action: "Dataset Uploaded",
    module: "Data Management",
    details: "Uploaded alerts.csv containing 125,400 records.",
    source: "Admin Portal",
    status: "Success",
  },
  {
    id: "AUD-00002",
    timestamp: "14 Sep 2026, 13:45",
    user: "Admin",
    role: "Administrator",
    action: "Analyst Created",
    module: "Users & Analysts",
    details: "Created analyst account AN00328.",
    source: "Admin Portal",
    status: "Success",
  },
  {
    id: "AUD-00003",
    timestamp: "14 Sep 2026, 12:18",
    user: "System",
    role: "System",
    action: "AI Model Loaded",
    module: "Rules & AI",
    details: "Loaded Analyst Anomaly Detection model.",
    source: "System",
    status: "Success",
  },
  {
    id: "AUD-00004",
    timestamp: "14 Sep 2026, 11:03",
    user: "Admin",
    role: "Administrator",
    action: "Rule Configuration Viewed",
    module: "Rules & AI",
    details: "Viewed configuration for Speed Demon Detector.",
    source: "Admin Portal",
    status: "Success",
  },
  {
    id: "AUD-00005",
    timestamp: "14 Sep 2026, 10:27",
    user: "Admin",
    role: "Administrator",
    action: "Organization Viewed",
    module: "Organizations",
    details: "Viewed organization details for ORG00052.",
    source: "Admin Portal",
    status: "Success",
  },
  {
    id: "AUD-00006",
    timestamp: "14 Sep 2026, 09:54",
    user: "Admin",
    role: "Administrator",
    action: "Dataset Validation",
    module: "Data Management",
    details: "Validation completed successfully for analysts.csv.",
    source: "Admin Portal",
    status: "Success",
  },
  {
    id: "AUD-00007",
    timestamp: "14 Sep 2026, 09:21",
    user: "Admin",
    role: "Administrator",
    action: "Login",
    module: "Security",
    details: "Administrator successfully authenticated.",
    source: "Authentication",
    status: "Success",
  },
  {
    id: "AUD-00008",
    timestamp: "13 Sep 2026, 18:42",
    user: "Admin",
    role: "Administrator",
    action: "Dataset Upload Failed",
    module: "Data Management",
    details: "Uploaded file failed CSV schema validation.",
    source: "Admin Portal",
    status: "Failed",
  },
  {
    id: "AUD-00009",
    timestamp: "13 Sep 2026, 17:15",
    user: "System",
    role: "System",
    action: "Detection Run",
    module: "Rules & AI",
    details: "Analyst behavioral detection evaluation completed.",
    source: "Detection Engine",
    status: "Success",
  },
  {
    id: "AUD-00010",
    timestamp: "13 Sep 2026, 16:03",
    user: "Admin",
    role: "Administrator",
    action: "User Viewed",
    module: "Users & Analysts",
    details: "Viewed user details for USR00241.",
    source: "Admin Portal",
    status: "Success",
  },
];

function AuditLogs() {
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("All");
  const [moduleFilter, setModuleFilter] = useState("All");
  const [selectedLog, setSelectedLog] = useState<AuditLog | null>(null);

  const filteredLogs = useMemo(() => {
    const searchValue = search.toLowerCase().trim();

    return auditLogs.filter((log) => {
      const matchesSearch =
        !searchValue ||
        log.id.toLowerCase().includes(searchValue) ||
        log.user.toLowerCase().includes(searchValue) ||
        log.action.toLowerCase().includes(searchValue) ||
        log.module.toLowerCase().includes(searchValue) ||
        log.details.toLowerCase().includes(searchValue);

      const matchesStatus =
        statusFilter === "All" || log.status === statusFilter;

      const matchesModule =
        moduleFilter === "All" || log.module === moduleFilter;

      return matchesSearch && matchesStatus && matchesModule;
    });
  }, [search, statusFilter, moduleFilter]);

  const successCount = auditLogs.filter(
    (log) => log.status === "Success"
  ).length;

  const failedCount = auditLogs.filter(
    (log) => log.status === "Failed"
  ).length;

  const modules = [
    "All",
    ...Array.from(new Set(auditLogs.map((log) => log.module))),
  ];

  return (
    <div className="audit-logs-page">
      {/* Header */}
      <div className="page-header">
        <div>
          <h2>Audit Logs</h2>
          <p>
            Review administrative, system and security activities across
            the SAT-SA platform.
          </p>
        </div>

        <div className="audit-status">
          <span></span>
          Audit Logging Active
        </div>
      </div>

      {/* Summary */}
      <div className="audit-summary-grid">
        <SummaryCard
          icon={<ClipboardList size={21} />}
          title="Total Activities"
          value={String(auditLogs.length)}
          description="Recorded audit events"
        />

        <SummaryCard
          icon={<Activity size={21} />}
          title="Today's Activities"
          value="8"
          description="Activities recorded today"
        />

        <SummaryCard
          icon={<CheckCircle2 size={21} />}
          title="Successful"
          value={String(successCount)}
          description="Completed successfully"
        />

        <SummaryCard
          icon={<XCircle size={21} />}
          title="Failed"
          value={String(failedCount)}
          description="Actions requiring attention"
          warning={failedCount > 0}
        />
      </div>

      {/* Main panel */}
      <section className="audit-panel">
        <div className="audit-panel-header">
          <div>
            <h3>Activity History</h3>
            <p>
              Complete record of actions performed within the Admin Portal.
            </p>
          </div>
        </div>

        {/* Filters */}
        <div className="audit-filters">
          <div className="audit-search">
            <Search size={17} />
            <input
              type="text"
              placeholder="Search audit logs..."
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
          </div>

          <select
            value={moduleFilter}
            onChange={(event) => setModuleFilter(event.target.value)}
          >
            {modules.map((module) => (
              <option key={module} value={module}>
                {module === "All" ? "All Modules" : module}
              </option>
            ))}
          </select>

          <select
            value={statusFilter}
            onChange={(event) => setStatusFilter(event.target.value)}
          >
            <option value="All">All Status</option>
            <option value="Success">Success</option>
            <option value="Failed">Failed</option>
          </select>
        </div>

        {/* Table */}
        <div className="audit-table-wrapper">
          <table className="audit-table">
            <thead>
              <tr>
                <th>Timestamp</th>
                <th>User</th>
                <th>Action</th>
                <th>Module</th>
                <th>Source</th>
                <th>Status</th>
                <th></th>
              </tr>
            </thead>

            <tbody>
              {filteredLogs.length > 0 ? (
                filteredLogs.map((log) => (
                  <tr key={log.id}>
                    <td>
                      <div className="audit-time">
                        <Clock3 size={14} />
                        {log.timestamp}
                      </div>
                    </td>

                    <td>
                      <div className="audit-user">
                        <div className="audit-user-avatar">
                          {log.user === "System" ? (
                            <Activity size={15} />
                          ) : (
                            <User size={15} />
                          )}
                        </div>

                        <div>
                          <strong>{log.user}</strong>
                          <span>{log.role}</span>
                        </div>
                      </div>
                    </td>

                    <td>
                      <span className="audit-action">
                        {log.action}
                      </span>
                    </td>

                    <td>
                      <ModuleBadge module={log.module} />
                    </td>

                    <td>
                      <span className="audit-source">
                        {log.source}
                      </span>
                    </td>

                    <td>
                      <StatusBadge status={log.status} />
                    </td>

                    <td>
                      <button
                        className="audit-view-button"
                        onClick={() => setSelectedLog(log)}
                      >
                        <Eye size={15} />
                        View
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={7}>
                    <div className="audit-empty">
                      <ClipboardList size={30} />
                      <strong>No audit logs found</strong>
                      <span>
                        Try changing your search or filter criteria.
                      </span>
                    </div>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        <div className="audit-results">
          Showing <strong>{filteredLogs.length}</strong> of{" "}
          <strong>{auditLogs.length}</strong> activities
        </div>
      </section>

      {/* Security note */}
      <section className="audit-security-note">
        <div className="audit-security-icon">
          <ShieldCheck size={20} />
        </div>

        <div>
          <strong>Audit trail protection</strong>
          <p>
            Audit records provide traceability for administrative and
            system activities. In the production system, these records
            should be persisted by the backend and protected from
            unauthorized modification.
          </p>
        </div>
      </section>

      {/* Details Modal */}
      {selectedLog && (
        <div
          className="modal-overlay"
          onClick={() => setSelectedLog(null)}
        >
          <div
            className="audit-detail-modal"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="modal-header">
              <div className="audit-modal-title">
                <div className="audit-modal-icon">
                  <ClipboardList size={20} />
                </div>

                <div>
                  <h3>Audit Activity</h3>
                  <span>{selectedLog.id}</span>
                </div>
              </div>

              <button
                className="modal-close"
                onClick={() => setSelectedLog(null)}
              >
                <X size={20} />
              </button>
            </div>

            <div className="audit-detail-body">
              <div className="audit-detail-status-row">
                <StatusBadge status={selectedLog.status} />
                <span>{selectedLog.timestamp}</span>
              </div>

              <DetailItem
                icon={<User size={16} />}
                label="User"
                value={`${selectedLog.user} — ${selectedLog.role}`}
              />

              <DetailItem
                icon={<Activity size={16} />}
                label="Action"
                value={selectedLog.action}
              />

              <DetailItem
                icon={<Database size={16} />}
                label="Module"
                value={selectedLog.module}
              />

              <DetailItem
                icon={<FileText size={16} />}
                label="Details"
                value={selectedLog.details}
              />

              <DetailItem
                icon={<Settings size={16} />}
                label="Source"
                value={selectedLog.source}
              />
            </div>

            <div className="modal-footer">
              <button
                className="secondary-button"
                onClick={() => setSelectedLog(null)}
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

/* =========================================================
   COMPONENTS
========================================================= */

interface SummaryCardProps {
  icon: React.ReactNode;
  title: string;
  value: string;
  description: string;
  warning?: boolean;
}

function SummaryCard({
  icon,
  title,
  value,
  description,
  warning,
}: SummaryCardProps) {
  return (
    <div className="audit-summary-card">
      <div
        className={`audit-summary-icon ${
          warning ? "warning" : ""
        }`}
      >
        {icon}
      </div>

      <strong className="audit-summary-value">{value}</strong>

      <span className="audit-summary-title">{title}</span>

      <p>{description}</p>
    </div>
  );
}

function StatusBadge({
  status,
}: {
  status: AuditLog["status"];
}) {
  return (
    <span
      className={`audit-status-badge ${
        status === "Success" ? "success" : "failed"
      }`}
    >
      {status === "Success" ? (
        <CheckCircle2 size={14} />
      ) : (
        <XCircle size={14} />
      )}
      {status}
    </span>
  );
}

function ModuleBadge({ module }: { module: string }) {
  let icon = <Database size={13} />;

  if (module === "Rules & AI") {
    icon = <BrainCircuit size={13} />;
  } else if (module === "Security") {
    icon = <ShieldCheck size={13} />;
  } else if (module === "Users & Analysts") {
    icon = <User size={13} />;
  } else if (module === "Organizations") {
    icon = <Database size={13} />;
  }

  return (
    <span className="audit-module-badge">
      {icon}
      {module}
    </span>
  );
}

function DetailItem({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
}) {
  return (
    <div className="audit-detail-item">
      <div className="audit-detail-label">
        {icon}
        <span>{label}</span>
      </div>

      <strong>{value}</strong>
    </div>
  );
}

export default AuditLogs;