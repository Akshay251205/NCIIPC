import { useEffect, useMemo, useState } from "react";
import {
  Users as UsersIcon,
  Search,
  Eye,
  Pencil,
  MoreVertical,
  UserCheck,
  ShieldCheck,
} from "lucide-react";

interface User {
  id: string;
  name: string;
  email: string;
  organization: string;
  role: "Admin" | "Supervisor" | "Analyst";
  status: "Active" | "Inactive";
  lastActive: string;
}

interface Analyst {
  id: string;
  name: string;
  organization: string;
  team: string;
  experience: string;
  shift: string;
  assignedAlerts: number;
  investigations: number;
  status: string;
}

const usersData: User[] = [
  {
    id: "USR-001",
    name: "Administrator",
    email: "admin@sat-sa.gov",
    organization: "SAT-SA",
    role: "Admin",
    status: "Active",
    lastActive: "2 min ago",
  },
  {
    id: "USR-002",
    name: "Rahul Sharma",
    email: "rahul@sat-sa.gov",
    organization: "NBC-001",
    role: "Supervisor",
    status: "Active",
    lastActive: "15 min ago",
  },
  {
    id: "USR-003",
    name: "Amit Kumar",
    email: "amit@sat-sa.gov",
    organization: "PGC-014",
    role: "Analyst",
    status: "Active",
    lastActive: "32 min ago",
  },
  {
    id: "USR-004",
    name: "Priya Singh",
    email: "priya@sat-sa.gov",
    organization: "NTS-021",
    role: "Analyst",
    status: "Active",
    lastActive: "1 hour ago",
  },
  {
    id: "USR-005",
    name: "Vikram Patel",
    email: "vikram@sat-sa.gov",
    organization: "IES-008",
    role: "Supervisor",
    status: "Inactive",
    lastActive: "2 days ago",
  },
];

const analystsData: Analyst[] = [
  {
    id: "AN-001",
    name: "Amit Kumar",
    organization: "NBC-001",
    team: "Threat Analysis",
    experience: "5 Years",
    shift: "Morning",
    assignedAlerts: 142,
    investigations: 38,
    status: "Active",
  },
  {
    id: "AN-002",
    name: "Priya Singh",
    organization: "PGC-014",
    team: "Incident Response",
    experience: "4 Years",
    shift: "Evening",
    assignedAlerts: 126,
    investigations: 31,
    status: "Active",
  },
  {
    id: "AN-003",
    name: "Arjun Mehta",
    organization: "NTS-021",
    team: "Threat Analysis",
    experience: "3 Years",
    shift: "Night",
    assignedAlerts: 98,
    investigations: 24,
    status: "Active",
  },
  {
    id: "AN-004",
    name: "Neha Verma",
    organization: "IES-008",
    team: "Incident Response",
    experience: "6 Years",
    shift: "Morning",
    assignedAlerts: 115,
    investigations: 42,
    status: "Inactive",
  },
  {
    id: "AN-005",
    name: "Rohan Gupta",
    organization: "NHN-032",
    team: "Monitoring",
    experience: "2 Years",
    shift: "Evening",
    assignedAlerts: 87,
    investigations: 19,
    status: "Active",
  },
];

function Users() {
  const [activeTab, setActiveTab] = useState<"users" | "analysts">(
    "users"
  );

  const [search, setSearch] = useState("");
  const [organization, setOrganization] =
    useState("All Organizations");
  const [status, setStatus] = useState("All Status");

  // Selected records for View Details modal
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [selectedAnalyst, setSelectedAnalyst] =
    useState<Analyst | null>(null);
  const [apiAnalysts, setApiAnalysts] = useState<Analyst[] | null>(null);
  const [analystTotal, setAnalystTotal] = useState(analystsData.length);
  const [analystLoadError, setAnalystLoadError] = useState(false);

  useEffect(() => {
    let active = true;
    fetch("/api/v1/analysts?limit=100")
      .then((response) => {
        if (!response.ok) throw new Error("Unable to load analysts");
        return response.json() as Promise<{ total: number; data: Array<{ analyst_id: string; name: string; organization_id: string; team: string | null; experience_years: number | null; shift: string | null; status: string | null }> }>;
      })
      .then((result) => {
        if (!active) return;
        setApiAnalysts(result.data.map((analyst) => ({
          id: analyst.analyst_id,
          name: analyst.name,
          organization: analyst.organization_id,
          team: analyst.team ?? "Unassigned",
          experience: analyst.experience_years == null ? "—" : `${analyst.experience_years} years`,
          shift: analyst.shift ?? "—",
          assignedAlerts: 0,
          investigations: 0,
          status: analyst.status ?? "Unknown",
        })));
        setAnalystTotal(result.total);
      })
      .catch(() => { if (active) setAnalystLoadError(true); });
    return () => { active = false; };
  }, []);

  // =========================
  // FILTER USERS
  // =========================

  const filteredUsers = useMemo(() => {
    return usersData.filter((user) => {
      const searchValue = search.toLowerCase().trim();

      const matchesSearch =
        user.name.toLowerCase().includes(searchValue) ||
        user.email.toLowerCase().includes(searchValue) ||
        user.organization.toLowerCase().includes(searchValue);

      const matchesOrganization =
        organization === "All Organizations" ||
        user.organization === organization;

      const matchesStatus =
        status === "All Status" || user.status === status;

      return (
        matchesSearch &&
        matchesOrganization &&
        matchesStatus
      );
    });
  }, [search, organization, status]);

  // =========================
  // FILTER ANALYSTS
  // =========================

  const filteredAnalysts = useMemo(() => {
    return (apiAnalysts ?? analystsData).filter((analyst) => {
      const searchValue = search.toLowerCase().trim();

      const matchesSearch =
        analyst.name.toLowerCase().includes(searchValue) ||
        analyst.organization
          .toLowerCase()
          .includes(searchValue) ||
        analyst.team.toLowerCase().includes(searchValue);

      const matchesOrganization =
        organization === "All Organizations" ||
        analyst.organization === organization;

      const matchesStatus =
        status === "All Status" ||
        analyst.status === status;

      return (
        matchesSearch &&
        matchesOrganization &&
        matchesStatus
      );
    });
  }, [apiAnalysts, search, organization, status]);

  // =========================
  // TAB CHANGE
  // =========================

  const handleTabChange = (
    tab: "users" | "analysts"
  ) => {
    setActiveTab(tab);

    // Reset filters when changing tab
    setSearch("");
    setOrganization("All Organizations");
    setStatus("All Status");

    // Close any open modal
    setSelectedUser(null);
    setSelectedAnalyst(null);
  };

  // =========================
  // CLEAR FILTERS
  // =========================

  const clearFilters = () => {
    setSearch("");
    setOrganization("All Organizations");
    setStatus("All Status");
  };

  return (
    <div className="users-page">

      {/* =========================
          PAGE HEADER
      ========================= */}

      <div className="page-heading">
        <div>
          <h2>Users & Analysts</h2>

          <p>
            Manage system users, supervisors and security analysts.
          </p>
        </div>
      </div>

      {/* =========================
          SUMMARY CARDS
      ========================= */}

      <div className="user-summary">

        <div className="summary-card">
          <div className="summary-icon">
            <UsersIcon size={21} />
          </div>

          <div>
            <span>Total Users</span>
            <strong>438</strong>
          </div>
        </div>

        <div className="summary-card">
          <div className="summary-icon">
            <UserCheck size={21} />
          </div>

          <div>
            <span>Active Users</span>
            <strong>421</strong>
          </div>
        </div>

        <div className="summary-card">
          <div className="summary-icon">
            <ShieldCheck size={21} />
          </div>

          <div>
            <span>Analysts</span>
            <strong>326</strong>
          </div>
        </div>

        <div className="summary-card">
          <div className="summary-icon">
            <UsersIcon size={21} />
          </div>

          <div>
            <span>Supervisors</span>
            <strong>84</strong>
          </div>
        </div>

      </div>

      {/* =========================
          USERS PANEL
      ========================= */}

      <div className="users-panel">

        {activeTab === "analysts" && analystLoadError && (
          <div className="admin-data-message" role="status">The backend analyst list is unavailable; displaying the local demo list.</div>
        )}

        {/* =========================
            TABS
        ========================= */}

        <div className="users-tabs">

          <button
            className={
              activeTab === "users"
                ? "active"
                : ""
            }
            onClick={() => handleTabChange("users")}
          >
            <UsersIcon size={17} />
            Users
          </button>

          <button
            className={
              activeTab === "analysts"
                ? "active"
                : ""
            }
            onClick={() =>
              handleTabChange("analysts")
            }
          >
            <ShieldCheck size={17} />
            Analysts
          </button>

        </div>

        {/* =========================
            TOOLBAR
        ========================= */}

        <div className="users-toolbar">

          <div className="users-search">
            <Search size={18} />

            <input
              type="text"
              placeholder={
                activeTab === "users"
                  ? "Search users..."
                  : "Search analysts..."
              }
              value={search}
              onChange={(event) =>
                setSearch(event.target.value)
              }
            />
          </div>

          <select
            value={organization}
            onChange={(event) =>
              setOrganization(event.target.value)
            }
          >
            <option>All Organizations</option>
            <option>NBC-001</option>
            <option>PGC-014</option>
            <option>NTS-021</option>
            <option>IES-008</option>
            <option>NHN-032</option>
          </select>

          <select
            value={status}
            onChange={(event) =>
              setStatus(event.target.value)
            }
          >
            <option>All Status</option>
            <option>Active</option>
            <option>Inactive</option>
          </select>

          {(search ||
            organization !== "All Organizations" ||
            status !== "All Status") && (
            <button
              className="clear-filter-button"
              onClick={clearFilters}
            >
              Clear
            </button>
          )}

        </div>

        {/* =========================
            TABLE
        ========================= */}

        <div className="table-container">

          {/* =========================
              USERS TABLE
          ========================= */}

          {activeTab === "users" ? (

            <table className="organizations-table">

              <thead>
                <tr>
                  <th>User</th>
                  <th>Organization</th>
                  <th>Role</th>
                  <th>Status</th>
                  <th>Last Active</th>
                  <th>Actions</th>
                </tr>
              </thead>

              <tbody>

                {filteredUsers.length > 0 ? (

                  filteredUsers.map((user) => (

                    <tr key={user.id}>

                      <td>
                        <div className="organization-name">

                          <div className="organization-logo">
                            <UsersIcon size={18} />
                          </div>

                          <div>
                            <strong>
                              {user.name}
                            </strong>

                            <span>
                              {user.email}
                            </span>
                          </div>

                        </div>
                      </td>

                      <td>
                        {user.organization}
                      </td>

                      <td>
                        <span className="role-badge">
                          {user.role}
                        </span>
                      </td>

                      <td>
                        <span
                          className={`status-badge ${user.status.toLowerCase()}`}
                        >
                          {user.status}
                        </span>
                      </td>

                      <td>
                        {user.lastActive}
                      </td>

                      <td>
                        <div className="table-actions">

                          {/* VIEW */}
                          <button
                            title="View"
                            onClick={() =>
                              setSelectedUser(user)
                            }
                          >
                            <Eye size={17} />
                          </button>

                          {/* EDIT - Reserved for later */}
                          <button title="Edit">
                            <Pencil size={17} />
                          </button>

                          {/* MORE - Reserved for later */}
                          <button title="More">
                            <MoreVertical size={17} />
                          </button>

                        </div>
                      </td>

                    </tr>

                  ))

                ) : (

                  <tr>
                    <td
                      colSpan={6}
                      className="empty-table"
                    >
                      No users found.
                    </td>
                  </tr>

                )}

              </tbody>

            </table>

          ) : (

            /* =========================
               ANALYSTS TABLE
            ========================= */

            <table className="organizations-table">

              <thead>
                <tr>
                  <th>Analyst</th>
                  <th>Organization</th>
                  <th>Team</th>
                  <th>Experience</th>
                  <th>Shift</th>
                  <th>Alerts</th>
                  <th>Investigations</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>

              <tbody>

                {filteredAnalysts.length > 0 ? (

                  filteredAnalysts.map((analyst) => (

                    <tr key={analyst.id}>

                      <td>
                        <div className="organization-name">

                          <div className="organization-logo">
                            <ShieldCheck size={18} />
                          </div>

                          <div>
                            <strong>
                              {analyst.name}
                            </strong>

                            <span>
                              {analyst.id}
                            </span>
                          </div>

                        </div>
                      </td>

                      <td>
                        {analyst.organization}
                      </td>

                      <td>
                        {analyst.team}
                      </td>

                      <td>
                        {analyst.experience}
                      </td>

                      <td>
                        {analyst.shift}
                      </td>

                      <td>
                        {analyst.assignedAlerts}
                      </td>

                      <td>
                        {analyst.investigations}
                      </td>

                      <td>
                        <span
                          className={`status-badge ${analyst.status.toLowerCase()}`}
                        >
                          {analyst.status}
                        </span>
                      </td>

                      <td>
                        <div className="table-actions">

                          {/* VIEW */}
                          <button
                            title="View"
                            onClick={() =>
                              setSelectedAnalyst(analyst)
                            }
                          >
                            <Eye size={17} />
                          </button>

                          {/* EDIT - Reserved for later */}
                          <button title="Edit">
                            <Pencil size={17} />
                          </button>

                          {/* MORE - Reserved for later */}
                          <button title="More">
                            <MoreVertical size={17} />
                          </button>

                        </div>
                      </td>

                    </tr>

                  ))

                ) : (

                  <tr>
                    <td
                      colSpan={9}
                      className="empty-table"
                    >
                      No analysts found.
                    </td>
                  </tr>

                )}

              </tbody>

            </table>

          )}

        </div>

        {/* =========================
            TABLE FOOTER
        ========================= */}

        <div className="table-footer">

          <span>
            {activeTab === "users"
              ? `Showing ${filteredUsers.length} of ${usersData.length} users`
              : `Showing ${filteredAnalysts.length} of ${analystTotal.toLocaleString()} analysts`}
          </span>

          <div className="pagination">

            <button disabled>
              Previous
            </button>

            <button className="current-page">
              1
            </button>

            <button>
              Next
            </button>

          </div>

        </div>

      </div>

      {/* =====================================================
          USER DETAILS MODAL
      ===================================================== */}

      {selectedUser && (

        <div
          className="details-modal-overlay"
          onClick={() =>
            setSelectedUser(null)
          }
        >

          <div
            className="details-modal"
            onClick={(event) =>
              event.stopPropagation()
            }
          >

            {/* MODAL HEADER */}

            <div className="details-modal-header">

              <div>
                <h3>
                  User Details
                </h3>

                <p>
                  System user information
                </p>
              </div>

              <button
                className="details-modal-close"
                onClick={() =>
                  setSelectedUser(null)
                }
                aria-label="Close"
              >
                ×
              </button>

            </div>

            {/* USER PROFILE */}

            <div className="details-profile">

              <div className="details-avatar">
                <UsersIcon size={25} />
              </div>

              <div>

                <h4>
                  {selectedUser.name}
                </h4>

                <span>
                  {selectedUser.id}
                </span>

              </div>

            </div>

            {/* USER DETAILS */}

            <div className="details-grid">

              <div className="details-item">
                <span>Email</span>
                <strong>
                  {selectedUser.email}
                </strong>
              </div>

              <div className="details-item">
                <span>Organization</span>
                <strong>
                  {selectedUser.organization}
                </strong>
              </div>

              <div className="details-item">
                <span>Role</span>
                <strong>
                  {selectedUser.role}
                </strong>
              </div>

              <div className="details-item">
                <span>Status</span>

                <strong>
                  <span
                    className={`status-badge ${selectedUser.status.toLowerCase()}`}
                  >
                    {selectedUser.status}
                  </span>
                </strong>

              </div>

              <div className="details-item">
                <span>Last Active</span>
                <strong>
                  {selectedUser.lastActive}
                </strong>
              </div>

            </div>

            {/* MODAL FOOTER */}

            <div className="details-modal-footer">

              <button
                className="secondary-button"
                onClick={() =>
                  setSelectedUser(null)
                }
              >
                Close
              </button>

            </div>

          </div>

        </div>

      )}

      {/* =====================================================
          ANALYST DETAILS MODAL
      ===================================================== */}

      {selectedAnalyst && (

        <div
          className="details-modal-overlay"
          onClick={() =>
            setSelectedAnalyst(null)
          }
        >

          <div
            className="details-modal"
            onClick={(event) =>
              event.stopPropagation()
            }
          >

            {/* MODAL HEADER */}

            <div className="details-modal-header">

              <div>
                <h3>
                  Analyst Details
                </h3>

                <p>
                  Security analyst information
                </p>
              </div>

              <button
                className="details-modal-close"
                onClick={() =>
                  setSelectedAnalyst(null)
                }
                aria-label="Close"
              >
                ×
              </button>

            </div>

            {/* ANALYST PROFILE */}

            <div className="details-profile">

              <div className="details-avatar">
                <ShieldCheck size={25} />
              </div>

              <div>

                <h4>
                  {selectedAnalyst.name}
                </h4>

                <span>
                  {selectedAnalyst.id}
                </span>

              </div>

            </div>

            {/* ANALYST DETAILS */}

            <div className="details-grid">

              <div className="details-item">
                <span>Organization</span>
                <strong>
                  {selectedAnalyst.organization}
                </strong>
              </div>

              <div className="details-item">
                <span>Team</span>
                <strong>
                  {selectedAnalyst.team}
                </strong>
              </div>

              <div className="details-item">
                <span>Experience</span>
                <strong>
                  {selectedAnalyst.experience}
                </strong>
              </div>

              <div className="details-item">
                <span>Shift</span>
                <strong>
                  {selectedAnalyst.shift}
                </strong>
              </div>

              <div className="details-item">
                <span>Assigned Alerts</span>
                <strong>
                  {selectedAnalyst.assignedAlerts}
                </strong>
              </div>

              <div className="details-item">
                <span>Investigations</span>
                <strong>
                  {selectedAnalyst.investigations}
                </strong>
              </div>

              <div className="details-item">
                <span>Status</span>

                <strong>
                  <span
                    className={`status-badge ${selectedAnalyst.status.toLowerCase()}`}
                  >
                    {selectedAnalyst.status}
                  </span>
                </strong>

              </div>

            </div>

            {/* MODAL FOOTER */}

            <div className="details-modal-footer">

              <button
                className="secondary-button"
                onClick={() =>
                  setSelectedAnalyst(null)
                }
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

export default Users;
