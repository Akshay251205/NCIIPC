import { useMemo, useState } from "react";
import {
  Building2,
  Plus,
  Search,
  Eye,
  Pencil,
  MoreVertical,
  ShieldCheck,
} from "lucide-react";

interface Organization {
  id: string;
  name: string;
  code: string;
  sector: string;
  location: string;
  analysts: number;
  assets: number;
  alerts: string;
  risk: "Critical" | "High" | "Medium" | "Low";
  status: "Active" | "Inactive";
}

const organizations: Organization[] = [
  {
    id: "ORG-001",
    name: "National Banking Corporation",
    code: "NBC-001",
    sector: "Banking",
    location: "New Delhi",
    analysts: 28,
    assets: 1240,
    alerts: "18.4K",
    risk: "High",
    status: "Active",
  },
  {
    id: "ORG-002",
    name: "Power Grid Corporation",
    code: "PGC-014",
    sector: "Power",
    location: "Mumbai",
    analysts: 21,
    assets: 980,
    alerts: "12.7K",
    risk: "Critical",
    status: "Active",
  },
  {
    id: "ORG-003",
    name: "National Telecom Services",
    code: "NTS-021",
    sector: "Telecom",
    location: "Bengaluru",
    analysts: 19,
    assets: 1560,
    alerts: "9.8K",
    risk: "Medium",
    status: "Active",
  },
  {
    id: "ORG-004",
    name: "Indian Energy Systems",
    code: "IES-008",
    sector: "Oil & Gas",
    location: "Pune",
    analysts: 16,
    assets: 740,
    alerts: "7.2K",
    risk: "High",
    status: "Active",
  },
  {
    id: "ORG-005",
    name: "National Healthcare Network",
    code: "NHN-032",
    sector: "Healthcare",
    location: "Hyderabad",
    analysts: 12,
    assets: 520,
    alerts: "4.6K",
    risk: "Low",
    status: "Inactive",
  },
];

function Organizations() {
  const [search, setSearch] = useState("");
  const [sector, setSector] = useState("All Sectors");
  const [status, setStatus] = useState("All Status");

  const filteredOrganizations = useMemo(() => {
    return organizations.filter((organization) => {
      const searchValue = search.toLowerCase().trim();

      const matchesSearch =
        organization.name.toLowerCase().includes(searchValue) ||
        organization.code.toLowerCase().includes(searchValue) ||
        organization.location.toLowerCase().includes(searchValue);

      const matchesSector =
        sector === "All Sectors" || organization.sector === sector;

      const matchesStatus =
        status === "All Status" || organization.status === status;

      return matchesSearch && matchesSector && matchesStatus;
    });
  }, [search, sector, status]);

  return (
    <div className="organizations-page">

      {/* PAGE HEADER */}
      <div className="page-heading">
        <div>
          <h2>Organizations</h2>

          <p>
            Manage registered organizations and their security operations.
          </p>
        </div>

        <button className="primary-button">
          <Plus size={18} />
          Add Organization
        </button>
      </div>

      {/* SUMMARY CARDS */}
      <div className="organization-summary">

        <div className="summary-card">
          <div className="summary-icon">
            <Building2 size={21} />
          </div>

          <div>
            <span>Total Organizations</span>
            <strong>52</strong>
          </div>
        </div>

        <div className="summary-card">
          <div className="summary-icon">
            <ShieldCheck size={21} />
          </div>

          <div>
            <span>Active Organizations</span>
            <strong>48</strong>
          </div>
        </div>

        <div className="summary-card">
          <div className="summary-icon">
            <ShieldCheck size={21} />
          </div>

          <div>
            <span>High Risk</span>
            <strong>9</strong>
          </div>
        </div>

        <div className="summary-card">
          <div className="summary-icon">
            <Building2 size={21} />
          </div>

          <div>
            <span>Sectors Covered</span>
            <strong>7</strong>
          </div>
        </div>

      </div>

      {/* ORGANIZATION TABLE */}
      <div className="organization-panel">

        {/* TOOLBAR */}
        <div className="organization-toolbar">

          {/* SEARCH */}
          <div className="organization-search">

            <Search size={18} />

            <input
              type="text"
              placeholder="Search organizations..."
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />

          </div>

          {/* SECTOR */}
          <select
            value={sector}
            onChange={(event) => setSector(event.target.value)}
          >
            <option>All Sectors</option>
            <option>Banking</option>
            <option>Power</option>
            <option>Telecom</option>
            <option>Oil & Gas</option>
            <option>Healthcare</option>
          </select>

          {/* STATUS */}
          <select
            value={status}
            onChange={(event) => setStatus(event.target.value)}
          >
            <option>All Status</option>
            <option>Active</option>
            <option>Inactive</option>
          </select>

        </div>

        {/* TABLE */}
        <div className="table-container">

          <table className="organizations-table">

            <thead>
              <tr>
                <th>Organization</th>
                <th>Sector</th>
                <th>Location</th>
                <th>Analysts</th>
                <th>Assets</th>
                <th>Alerts</th>
                <th>Risk</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>

              {filteredOrganizations.length > 0 ? (

                filteredOrganizations.map((organization) => (

                  <tr key={organization.id}>

                    <td>
                      <div className="organization-name">

                        <div className="organization-logo">
                          <Building2 size={19} />
                        </div>

                        <div>
                          <strong>{organization.name}</strong>
                          <span>{organization.code}</span>
                        </div>

                      </div>
                    </td>

                    <td>{organization.sector}</td>

                    <td>{organization.location}</td>

                    <td>{organization.analysts}</td>

                    <td>{organization.assets.toLocaleString()}</td>

                    <td>{organization.alerts}</td>

                    <td>
                      <span
                        className={`risk-badge ${organization.risk.toLowerCase()}`}
                      >
                        {organization.risk}
                      </span>
                    </td>

                    <td>
                      <span
                        className={`status-badge ${organization.status.toLowerCase()}`}
                      >
                        {organization.status}
                      </span>
                    </td>

                    <td>

                      <div className="table-actions">

                        <button title="View">
                          <Eye size={17} />
                        </button>

                        <button title="Edit">
                          <Pencil size={17} />
                        </button>

                        <button title="More">
                          <MoreVertical size={17} />
                        </button>

                      </div>

                    </td>

                  </tr>

                ))

              ) : (

                <tr>
                  <td colSpan={9} className="empty-table">
                    No organizations found.
                  </td>
                </tr>

              )}

            </tbody>

          </table>

        </div>

        {/* FOOTER */}
        <div className="table-footer">

          <span>
            Showing {filteredOrganizations.length} of{" "}
            {organizations.length} organizations
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

    </div>
  );
}

export default Organizations;