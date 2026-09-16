import { Bell, Search, UserCircle } from "lucide-react";
import { useFeedback } from "../../../components/feedback";
import { useApiHealth } from "../../../hooks/useApiHealth";

export default function Header() {
  const notify = useFeedback();
  const apiOnline = useApiHealth();
  return (
    <header className="header">
      <div className="header-left">
        <div>
          <h2>Supervisor Portal</h2>
          <p>Security Operations Assessment</p>
        </div>
        <span className={`api-status ${apiOnline === false ? "offline" : ""}`}>{apiOnline === null ? "Checking API" : apiOnline ? "API connected" : "API offline"}</span>
      </div>

      <div className="header-right">
        <div className="search-box">
          <Search size={18} />
          <input
            type="text"
            placeholder="Search..."
            onKeyDown={(event) => { if (event.key === "Enter") notify("Search ready", `Searching for “${event.currentTarget.value}”.`); }}
          />
        </div>

        <button className="icon-button" onClick={() => notify("Notifications", "You have 3 dashboard notifications to review.")}>
          <Bell size={20} />
          <span className="notification-dot"></span>
        </button>

        <div className="profile">
          <UserCircle size={34} />

          <div>
            <p className="profile-name">Supervisor</p>
            <p className="profile-role">Security Manager</p>
          </div>
        </div>
      </div>
    </header>
  );
}
