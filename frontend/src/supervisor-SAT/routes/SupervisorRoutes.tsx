import { Routes, Route, Navigate } from "react-router-dom";
import SupervisorLayout from "../components/layout/SupervisorLayout";
import Dashboard from "../pages/Dashboard/Dashboard";
import Organizations from "../pages/Organizations/Organizations";
import OrganizationDetails from "../pages/Organizations/OrganizationDetails";
import Analysts from "../pages/Analysts/Analysts";
import AnalystDetails from "../pages/Analysts/AnalystDetails";
import Alerts from "../pages/Alerts/Alerts";
import AlertDetails from "../pages/Alerts/AlertDetails";
import InvestigationDetails from "../pages/Investigations/InvestigationDetails";
import Findings from "../pages/Findings/Findings";
import FindingDetails from "../pages/Findings/FindingDetails";
import Analytics from "../pages/Analytics/Analytics";
import Reports from "../pages/Reports/Reports";


// function Analysts() {
//   return (
//     <div>
//       <h1>Analysts</h1>
//       <p>Analysts module will be built here.</p>
//     </div>
//   );
// }

// function Alerts() {
//   return (
//     <div>
//       <h1>Alerts</h1>
//       <p>Alerts module will be built here.</p>
//     </div>
//   );
// }

// function Findings() {
//   return (
//     <div>
//       <h1>Priority Findings</h1>
//       <p>Priority findings will be built here.</p>
//     </div>
//   );
// }

// function Analytics() {
//   return (
//     <div>
//       <h1>Analytics</h1>
//       <p>Analytics module will be built here.</p>
//     </div>
//   );
// }

// function Reports() {
//   return (
//     <div>
//       <h1>Reports</h1>
//       <p>Reports module will be built here.</p>
//     </div>
//   );
// }

export default function SupervisorRoutes() {
  return (
    <SupervisorLayout>
      <Routes>
      <Route
        path="/"
        element={
          <Navigate
            to="/supervisor/dashboard"
            replace
          />
        }
      />

      <Route
        path="/supervisor/dashboard"
        element={<Dashboard />}
      />

      <Route
        path="/supervisor/organizations"
        element={<Organizations />}
      />

      <Route
        path="/supervisor/organizations/:id"
        element={<OrganizationDetails />}
        />

      <Route
        path="/supervisor/analysts"
        element={<Analysts />}
      />

      <Route
        path="/supervisor/analysts/:id"
        element={<AnalystDetails />}
        />

      <Route
        path="/supervisor/alerts"
        element={<Alerts />}
      />

      <Route
        path="/supervisor/alerts/:id"
        element={<AlertDetails />}
        />

        <Route
        path="/supervisor/investigations/:id"
        element={<InvestigationDetails />}
        />

      <Route
        path="/supervisor/findings"
        element={<Findings />}
      />

      <Route
        path="/supervisor/findings/:id"
        element={<FindingDetails />}
        />

      <Route
        path="/supervisor/analytics"
        element={<Analytics />}
      />

      <Route
        path="/supervisor/reports"
        element={<Reports />}
      />

        <Route path="*" element={<Navigate to="/supervisor/dashboard" replace />} />
      </Routes>
    </SupervisorLayout>
  );
}
