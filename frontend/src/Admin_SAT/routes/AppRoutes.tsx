import { Routes, Route, Navigate } from "react-router-dom";

import AdminLayout from "../components/layout/AdminLayout";

import Dashboard from "../pages/Dashboard/Dashboard";
import Organizations from "../pages/Organizations/Organizations";
import Users from "../pages/Users/Users";
import DataManagement from "../pages/DataManagement/DataManagement";
import RulesAI from "../pages/RulesAI/RulesAI";
import AuditLogs from "../pages/AuditLogs/AuditLogs";
import Settings from "../pages/Settings/Settings";

function AppRoutes() {
  return (
    <Routes>

      {/* Admin default route */}
      <Route
        path="/admin"
        element={<Navigate to="/admin/dashboard" replace />}
      />

      {/* Admin Dashboard */}
      <Route
        path="/admin/dashboard"
        element={
          <AdminLayout>
            <Dashboard />
          </AdminLayout>
        }
      />

      {/* Organizations */}
      <Route
        path="/admin/organizations"
        element={
          <AdminLayout>
            <Organizations />
          </AdminLayout>
        }
      />

      {/* Users */}
      <Route
        path="/admin/users"
        element={
          <AdminLayout>
            <Users />
          </AdminLayout>
        }
      />

      {/* Data Management */}
      <Route
        path="/admin/data"
        element={
          <AdminLayout>
            <DataManagement />
          </AdminLayout>
        }
      />

      {/* Rules & AI */}
      <Route
        path="/admin/rules"
        element={
          <AdminLayout>
            <RulesAI />
          </AdminLayout>
        }
      />

      {/* Audit Logs */}
      <Route
        path="/admin/audit"
        element={
          <AdminLayout>
            <AuditLogs />
          </AdminLayout>
        }
      />

      {/* Settings */}
      <Route
        path="/admin/settings"
        element={
          <AdminLayout>
            <Settings />
          </AdminLayout>
        }
      />

      <Route path="*" element={<Navigate to="/admin/dashboard" replace />} />

    </Routes>
  );
}

export default AppRoutes;







// import { Routes, Route } from "react-router-dom";

// import AdminLayout from "../components/layout/AdminLayout";

// import Dashboard from "../pages/Dashboard/Dashboard";
// import Organizations from "../pages/Organizations/Organizations";
// import Users from "../pages/Users/Users";
// import DataManagement from "../pages/DataManagement/DataManagement";
// import RulesAI from "../pages/RulesAI/RulesAI";
// import AuditLogs from "../pages/AuditLogs/AuditLogs";
// import Settings from "../pages/Settings/Settings";

// function AppRoutes() {
//   return (
//     <Routes>
//       <Route path="/" element={<AdminLayout><Dashboard /></AdminLayout>} />

//       <Route
//         path="/organizations"
//         element={
//           <AdminLayout>
//             <Organizations />
//           </AdminLayout>
//         }
//       />

//       <Route
//         path="/users"
//         element={
//           <AdminLayout>
//             <Users />
//           </AdminLayout>
//         }
//       />

//       <Route
//         path="/data"
//         element={
//           <AdminLayout>
//             <DataManagement />
//           </AdminLayout>
//         }
//       />

//       <Route
//         path="/rules"
//         element={
//           <AdminLayout>
//             <RulesAI />
//           </AdminLayout>
//         }
//       />

//       <Route
//         path="/audit"
//         element={
//           <AdminLayout>
//             <AuditLogs />
//           </AdminLayout>
//         }
//       />

//       <Route
//         path="/settings"
//         element={
//           <AdminLayout>
//             <Settings />
//           </AdminLayout>
//         }
//       />
//     </Routes>
//   );
// }

// export default AppRoutes;
