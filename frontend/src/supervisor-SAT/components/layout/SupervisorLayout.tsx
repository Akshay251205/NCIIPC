import type { ReactNode } from "react";
import Sidebar from "./Sidebar";
import Header from "./Header";

interface SupervisorLayoutProps {
  children: ReactNode;
}

export default function SupervisorLayout({
  children,
}: SupervisorLayoutProps) {
  return (
    <div className="supervisor-layout">
      <Sidebar />

      <div className="main-area">
        <Header />

        <main className="page-content">
          {children}
        </main>
      </div>
    </div>
  );
}