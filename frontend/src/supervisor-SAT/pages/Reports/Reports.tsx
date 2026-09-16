import {
  BarChart3,
  CalendarDays,
  Download,
  FileText,
  Eye,
  ShieldAlert,
  TrendingUp,
} from "lucide-react";
import { useState } from "react";
import { useFeedback } from "../../../components/feedback";
import "./Reports.css";

const reports = [
  {
    id: "RPT-001",
    name: "Monthly SOC Assessment Report",
    type: "SOC Assessment",
    organization: "Organization Alpha",
    period: "September 2026",
    status: "Ready",
    generated: "Today, 10:42 AM",
  },
  {
    id: "RPT-002",
    name: "Organization Risk Summary",
    type: "Risk Analysis",
    organization: "Organization Beta",
    period: "September 2026",
    status: "Ready",
    generated: "Today, 09:18 AM",
  },
  {
    id: "RPT-003",
    name: "Analyst Performance Report",
    type: "Analyst Analytics",
    organization: "All Organizations",
    period: "August 2026",
    status: "Ready",
    generated: "Yesterday, 04:35 PM",
  },
  {
    id: "RPT-004",
    name: "Priority Findings Report",
    type: "Findings Analysis",
    organization: "Organization Gamma",
    period: "August 2026",
    status: "Ready",
    generated: "Yesterday, 02:11 PM",
  },
  {
    id: "RPT-005",
    name: "Peer Benchmark Report",
    type: "Benchmark Analysis",
    organization: "Organization Alpha",
    period: "Q3 2026",
    status: "Ready",
    generated: "2 days ago",
  },
];

function Reports() {
  const notify = useFeedback();
  const [reportType, setReportType] = useState("SOC Assessment");
  const [organization, setOrganization] = useState("All Organizations");
  const [startDate, setStartDate] = useState("2026-09-01");
  const [endDate, setEndDate] = useState("2026-09-13");
  const [generatedReports, setGeneratedReports] = useState(reports);
  const generateReport = () => {
    const report = { id: `RPT-${String(generatedReports.length + 1).padStart(3, "0")}`, name: `${organization} ${reportType} Report`, type: reportType, organization, period: `${startDate} to ${endDate}`, status: "Ready", generated: "Just now" };
    setGeneratedReports((current) => [report, ...current]);
    notify("Report generated", `${report.name} is ready to review or download.`);
  };
  const downloadReport = (report: (typeof reports)[number]) => {
    const file = new Blob([`SAT-SA ${report.name}\n\nOrganization: ${report.organization}\nPeriod: ${report.period}\nStatus: ${report.status}\n`], { type: "text/plain" });
    const url = URL.createObjectURL(file);
    const link = document.createElement("a");
    link.href = url; link.download = `${report.id}.txt`; link.click(); URL.revokeObjectURL(url);
    notify("Download started", `${report.name} has been exported as a text report.`);
  };
  return (
    <div className="reports-page">
      <div className="reports-header">
        <div>
          <h1>Reports</h1>
          <p>
            Generate, review, and manage supervisor assessment reports.
          </p>
        </div>

        <button className="generate-report-button" onClick={generateReport}>
          <FileText size={17} />
          Generate Report
        </button>
      </div>

      {/* Summary Cards */}
      <div className="reports-summary-grid">
        <div className="report-summary-card">
          <div className="report-summary-icon blue">
            <FileText size={21} />
          </div>

          <div>
            <span>Total Reports</span>
            <strong>24</strong>
            <small>Generated reports</small>
          </div>
        </div>

        <div className="report-summary-card">
          <div className="report-summary-icon green">
            <TrendingUp size={21} />
          </div>

          <div>
            <span>This Month</span>
            <strong>8</strong>
            <small>Reports generated</small>
          </div>
        </div>

        <div className="report-summary-card">
          <div className="report-summary-icon orange">
            <ShieldAlert size={21} />
          </div>

          <div>
            <span>Priority Reports</span>
            <strong>5</strong>
            <small>Require supervisor review</small>
          </div>
        </div>

        <div className="report-summary-card">
          <div className="report-summary-icon purple">
            <BarChart3 size={21} />
          </div>

          <div>
            <span>Organizations</span>
            <strong>4</strong>
            <small>Covered by reports</small>
          </div>
        </div>
      </div>

      {/* Report Generator */}
      <div className="reports-card report-generator">
        <div className="reports-card-header">
          <div>
            <h2>Quick Report Generator</h2>
            <p>Select the information you want included in the report.</p>
          </div>
        </div>

        <div className="report-form-grid">
          <div className="report-form-group">
            <label>Report Type</label>
            <select value={reportType} onChange={(event) => setReportType(event.target.value)}>
              <option>SOC Assessment</option>
              <option>Risk Analysis</option>
              <option>Analyst Analytics</option>
              <option>Findings Analysis</option>
              <option>Benchmark Analysis</option>
            </select>
          </div>

          <div className="report-form-group">
            <label>Organization</label>
            <select value={organization} onChange={(event) => setOrganization(event.target.value)}>
              <option>All Organizations</option>
              <option>Organization Alpha</option>
              <option>Organization Beta</option>
              <option>Organization Gamma</option>
              <option>Organization Delta</option>
            </select>
          </div>

          <div className="report-form-group">
            <label>Start Date</label>

            <div className="date-input">
              <CalendarDays size={16} />
              <input type="date" value={startDate} onChange={(event) => setStartDate(event.target.value)} />
            </div>
          </div>

          <div className="report-form-group">
            <label>End Date</label>

            <div className="date-input">
              <CalendarDays size={16} />
              <input type="date" value={endDate} onChange={(event) => setEndDate(event.target.value)} />
            </div>
          </div>
        </div>

        <div className="report-options">
          <label>
            <input type="checkbox" defaultChecked />
            Include risk analysis
          </label>

          <label>
            <input type="checkbox" defaultChecked />
            Include analyst performance
          </label>

          <label>
            <input type="checkbox" defaultChecked />
            Include priority findings
          </label>

          <label>
            <input type="checkbox" />
            Include peer benchmark
          </label>
        </div>

        <button className="generate-report-secondary" onClick={generateReport}>
          <FileText size={16} />
          Generate Report
        </button>
      </div>

      {/* Reports List */}
      <div className="reports-card">
        <div className="reports-card-header">
          <div>
            <h2>Recent Reports</h2>
            <p>Previously generated supervisor reports.</p>
          </div>

          <button className="view-all-button" onClick={() => notify("Showing all reports", `${generatedReports.length} reports are available in this session.`)}>View All</button>
        </div>

        <div className="reports-table-wrapper">
          <table className="reports-table">
            <thead>
              <tr>
                <th>Report</th>
                <th>Type</th>
                <th>Organization</th>
                <th>Period</th>
                <th>Status</th>
                <th>Generated</th>
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>
              {generatedReports.map((report) => (
                <tr key={report.id}>
                  <td>
                    <div className="report-name-cell">
                      <div className="report-file-icon">
                        <FileText size={17} />
                      </div>

                      <div>
                        <strong>{report.name}</strong>
                        <span>{report.id}</span>
                      </div>
                    </div>
                  </td>

                  <td>{report.type}</td>

                  <td>{report.organization}</td>

                  <td>{report.period}</td>

                  <td>
                    <span className="report-status">
                      {report.status}
                    </span>
                  </td>

                  <td>{report.generated}</td>

                  <td>
                    <div className="report-actions">
                      <button title="View Report" onClick={() => notify(report.name, `Generated ${report.generated}. ${report.period}.`)}>
                        <Eye size={16} />
                      </button>

                      <button title="Download Report" onClick={() => downloadReport(report)}>
                        <Download size={16} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Report Insight */}
      <div className="report-insight">
        <div className="report-insight-icon">
          <BarChart3 size={20} />
        </div>

        <div>
          <strong>Reporting Insight</strong>

          <p>
            Organization Alpha has the highest current risk score. Consider
            including risk analysis, priority findings, and peer benchmark
            information in the next assessment report.
          </p>
        </div>
      </div>
    </div>
  );
}

export default Reports;
