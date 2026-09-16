import {
  LayoutDashboard,
  Building2,
  Users,
  Database,
  ShieldCheck,
  ClipboardList,
  Settings,
} from "lucide-react";

import { NavLink } from "react-router-dom";

const menuItems = [
  {
    label: "Dashboard",
    icon: LayoutDashboard,
    path: "/admin/dashboard",
  },
  {
    label: "Organizations",
    icon: Building2,
    path: "/admin/organizations",
  },
  {
    label: "Users & Analysts",
    icon: Users,
    path: "/admin/users",
  },
  {
    label: "Data Management",
    icon: Database,
    path: "/admin/data",
  },
  {
    label: "Rules & AI",
    icon: ShieldCheck,
    path: "/admin/rules",
  },
  {
    label: "Audit Logs",
    icon: ClipboardList,
    path: "/admin/audit",
  },
  {
    label: "Settings",
    icon: Settings,
    path: "/admin/settings",
  },
];

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-logo">
          <ShieldCheck size={24} />
        </div>

        <div>
          <h1>SAT-SA</h1>
          <span>ADMIN PORTAL</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item) => {
  const Icon = item.icon;

  return (
    <NavLink
      key={item.label}
      to={item.path}
      end={item.path === "/admin/dashboard"}
      className={({ isActive }) =>
        `nav-item ${isActive ? "active" : ""}`
      }
    >
      <Icon size={20} />
      <span>{item.label}</span>
    </NavLink>
  );
})}
      </nav>

      <div className="sidebar-footer">
        <div className="admin-avatar">A</div>

        <div className="admin-info">
          <strong>Administrator</strong>
          <span>
            <i></i>
            Online
          </span>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
