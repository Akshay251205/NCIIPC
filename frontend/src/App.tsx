import { useLocation } from "react-router-dom";
import AdminRoutes from "./Admin_SAT/routes/AppRoutes";
import SupervisorRoutes from "./supervisor-SAT/routes/SupervisorRoutes";

function App() {
  const { pathname } = useLocation();

  return pathname.startsWith("/admin") ? <AdminRoutes /> : <SupervisorRoutes />;
}

export default App;
