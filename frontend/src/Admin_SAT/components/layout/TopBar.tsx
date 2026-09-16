import { Bell, Search, ChevronDown } from "lucide-react";
import { useFeedback } from "../../../components/feedback";
import { useApiHealth } from "../../../hooks/useApiHealth";

function Topbar() {
  const notify = useFeedback();
  const apiOnline = useApiHealth();
  return (
    <header className="topbar">
      <div className="search-box">
        <Search size={19} />
        <input
          type="text"
          placeholder="Search anything..."
          onKeyDown={(event) => { if (event.key === "Enter") notify("Search ready", `Searching for “${event.currentTarget.value}”.`); }}
        />
      </div>

      <div className="topbar-actions">
        <span className={`api-status ${apiOnline === false ? "offline" : ""}`}>{apiOnline === null ? "Checking API" : apiOnline ? "API connected" : "API offline"}</span>
        <button className="notification-button" onClick={() => notify("Notifications", "Three administrative notifications are ready to review.")}>
          <Bell size={21} />
          <span>3</span>
        </button>

        <button className="profile" onClick={() => notify("Administrator profile", "Profile controls are available in Settings.")}>
          <div className="profile-avatar">A</div>

          <div className="profile-info">
            <strong>Admin</strong>
            <span>Administrator</span>
          </div>

          <ChevronDown size={18} />
        </button>
      </div>
    </header>
  );
}

export default Topbar;
