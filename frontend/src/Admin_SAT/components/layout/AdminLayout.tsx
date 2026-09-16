import Sidebar from "./Sidebar";
import Topbar from "./TopBar";

interface AdminLayoutProps {
  children: React.ReactNode;
}

function AdminLayout({ children }: AdminLayoutProps) {
  return (
    <div className="admin-layout">
      <Sidebar />

      <div className="main-section">
        <Topbar />

        <main className="main-content">
          {children}
        </main>
      </div>
    </div>
  );
}

export default AdminLayout;