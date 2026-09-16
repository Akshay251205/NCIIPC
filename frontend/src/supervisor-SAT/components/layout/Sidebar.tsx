import {
  LayoutDashboard,
  Building2,
  Users,
  Bell,
  AlertTriangle,
  BarChart3,
  FileText,
  Settings,
  LogOut,
} from "lucide-react";

import { NavLink } from "react-router-dom";
import { useFeedback } from "../../../components/feedback";

const menuItems = [
  {
    name: "Dashboard",
    icon: LayoutDashboard,
    path: "/supervisor/dashboard",
  },
  {
    name: "Organizations",
    icon: Building2,
    path: "/supervisor/organizations",
  },
  {
    name: "Analysts",
    icon: Users,
    path: "/supervisor/analysts",
  },
  {
    name: "Alerts",
    icon: Bell,
    path: "/supervisor/alerts",
  },
  {
    name: "Priority Findings",
    icon: AlertTriangle,
    path: "/supervisor/findings",
  },
  {
    name: "Analytics",
    icon: BarChart3,
    path: "/supervisor/analytics",
  },
  {
    name: "Reports",
    icon: FileText,
    path: "/supervisor/reports",
  },
];

export default function Sidebar() {
  const notify = useFeedback();
  return (
    <aside className="sidebar">
      {/* Logo */}
      <div className="sidebar-logo">
        <div className="logo-box">S</div>

        <div>
          <h1>SAT-SA</h1>
          <p>SUPERVISOR</p>
        </div>
      </div>

      {/* Main Navigation */}
      <nav className="sidebar-nav">
        <p className="nav-title">MAIN MENU</p>

        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
                isActive ? "nav-item active" : "nav-item"
            }
            >
            <Icon size={19} />
            <span>{item.name}</span>
            </NavLink>
          );
        })}
      </nav>

      {/* Bottom Navigation */}
      <div className="sidebar-bottom">
        <button className="nav-item" onClick={() => notify("Supervisor settings", "Supervisor preferences are saved locally for this session.")}>
          <Settings size={19} />
          <span>Settings</span>
        </button>

        <button className="nav-item logout" onClick={() => notify("Logout", "This local demo keeps you signed in; no remote session was ended.")}>
          <LogOut size={19} />
          <span>Logout</span>
        </button>
      </div>
    </aside>
  );
}
