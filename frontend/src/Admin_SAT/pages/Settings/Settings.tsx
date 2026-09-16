import { useEffect, useState, type ReactNode } from "react";

import {
  User,
  Palette,
  Bell,
  ShieldCheck,
  Settings as SettingsIcon,
  Sun,
  Moon,
  Monitor,
  CheckCircle2,
  Lock,
  Database,
  ClipboardList,
  Clock3,
} from "lucide-react";

type Theme = "light" | "dark" | "system";

function Toggle({
  enabled,
  onChange,
}: {
  enabled: boolean;
  onChange: (value: boolean) => void;
}) {
  return (
    <button
      type="button"
      className={`settings-toggle ${enabled ? "enabled" : ""}`}
      onClick={() => onChange(!enabled)}
      aria-label={enabled ? "Disable setting" : "Enable setting"}
    >
      <span className="settings-toggle-circle"></span>
    </button>
  );
}

function ThemeOption({
  value,
  icon,
  title,
  description,
  selected,
  onSelect,
}: {
  value: Theme;
  icon: ReactNode;
  title: string;
  description: string;
  selected: boolean;
  onSelect: (value: Theme) => void;
}) {
  return (
    <button
      type="button"
      className={`theme-option ${selected ? "selected" : ""}`}
      onClick={() => onSelect(value)}
    >
      <div className="theme-option-icon">{icon}</div>
      <div className="theme-option-content">
        <strong>{title}</strong>
        <span>{description}</span>
      </div>
      <div className={`theme-radio ${selected ? "checked" : ""}`}>
        {selected && <span></span>}
      </div>
    </button>
  );
}

function Settings() {
  const [activeSection, setActiveSection] = useState("Profile");

  // Load saved theme or default to light
  const [theme, setTheme] = useState<Theme>(() => {
    const savedTheme = localStorage.getItem("sat-sa-theme");

    if (
      savedTheme === "light" ||
      savedTheme === "dark" ||
      savedTheme === "system"
    ) {
      return savedTheme;
    }

    return "light";
  });

  const [emailNotifications, setEmailNotifications] = useState(true);
  const [systemAlerts, setSystemAlerts] = useState(true);
  const [datasetProcessing, setDatasetProcessing] = useState(true);
  const [securityNotifications, setSecurityNotifications] = useState(true);

  const [auditLogging, setAuditLogging] = useState(true);
  const [automaticRefresh, setAutomaticRefresh] = useState(true);

  /*
   * Apply selected theme to the entire application
   */
  useEffect(() => {
    const root = document.documentElement;

    root.classList.remove("theme-light", "theme-dark");

    if (theme === "dark") {
      root.classList.add("theme-dark");
    } else if (theme === "light") {
      root.classList.add("theme-light");
    } else {
      const mediaQuery = window.matchMedia(
        "(prefers-color-scheme: dark)"
      );

      root.classList.add(
        mediaQuery.matches ? "theme-dark" : "theme-light"
      );

      const handleSystemThemeChange = (event: MediaQueryListEvent) => {
        root.classList.remove("theme-light", "theme-dark");

        root.classList.add(
          event.matches ? "theme-dark" : "theme-light"
        );
      };

      mediaQuery.addEventListener("change", handleSystemThemeChange);

      return () => {
        mediaQuery.removeEventListener(
          "change",
          handleSystemThemeChange
        );
      };
    }

    // Save selected theme
    localStorage.setItem("sat-sa-theme", theme);
  }, [theme]);

  /*
   * Settings navigation
   */
  const sections = [
    {
      label: "Profile",
      icon: User,
    },
    {
      label: "Appearance",
      icon: Palette,
    },
    {
      label: "Notifications",
      icon: Bell,
    },
    {
      label: "Security",
      icon: ShieldCheck,
    },
    {
      label: "System Preferences",
      icon: SettingsIcon,
    },
  ];

  /*
   * Save settings
   */
  const handleSave = () => {
    localStorage.setItem("sat-sa-theme", theme);

    alert("Settings saved for this session.");
  };

  return (
    <div className="settings-page">
      {/* Page Header */}
      <div className="page-header">
        <div>
          <h1>Settings</h1>
          <p>
            Manage your administrator profile, system preferences,
            security and application settings.
          </p>
        </div>

        <button
          type="button"
          className="primary-button"
          onClick={handleSave}
        >
          Save Changes
        </button>
      </div>

      <div className="settings-layout">
        {/* Settings Navigation */}
        <aside className="settings-sidebar">
          <div className="settings-sidebar-title">
            Settings
          </div>

          <nav className="settings-nav">
            {sections.map((section) => {
              const Icon = section.icon;

              return (
                <button
                  type="button"
                  key={section.label}
                  className={`settings-nav-item ${
                    activeSection === section.label
                      ? "active"
                      : ""
                  }`}
                  onClick={() =>
                    setActiveSection(section.label)
                  }
                >
                  <Icon size={18} />
                  <span>{section.label}</span>
                </button>
              );
            })}
          </nav>
        </aside>

        {/* Settings Content */}
        <section className="settings-content">
          {/* =====================================================
              PROFILE
          ===================================================== */}
          {activeSection === "Profile" && (
            <div className="settings-section">
              <div className="settings-section-header">
                <div>
                  <h2>Administrator Profile</h2>
                  <p>
                    View and manage your administrator account
                    information.
                  </p>
                </div>
              </div>

              <div className="profile-header">
                <div className="settings-profile-avatar">
                  A
                </div>

                <div>
                  <h3>Administrator</h3>
                  <p>System Administrator</p>

                  <span className="status-badge status-active">
                    <CheckCircle2 size={14} />
                    Active
                  </span>
                </div>
              </div>

              <div className="settings-form-grid">
                <div className="settings-field">
                  <label>Full Name</label>
                  <input
                    type="text"
                    value="Administrator"
                    disabled
                  />
                </div>

                <div className="settings-field">
                  <label>Username</label>
                  <input
                    type="text"
                    value="admin"
                    disabled
                  />
                </div>

                <div className="settings-field">
                  <label>Role</label>
                  <input
                    type="text"
                    value="Administrator"
                    disabled
                  />
                </div>

                <div className="settings-field">
                  <label>Account Status</label>
                  <input
                    type="text"
                    value="Active"
                    disabled
                  />
                </div>
              </div>

              <div className="settings-info-box">
                <ShieldCheck size={18} />

                <div>
                  <strong>Administrator account</strong>
                  <p>
                    Profile information is managed by the system
                    administrator and authentication service.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* =====================================================
              APPEARANCE
          ===================================================== */}
          {activeSection === "Appearance" && (
            <div className="settings-section">
              <div className="settings-section-header">
                <div>
                  <h2>Appearance</h2>
                  <p>
                    Customize how SAT-SA appears on your device.
                  </p>
                </div>
              </div>

              <div className="appearance-section">
                <h3>Application Theme</h3>

                <p className="settings-description">
                  Choose a theme for the SAT-SA administration
                  portal.
                </p>

                <div className="theme-options">
                  <ThemeOption
                    value="light"
                    selected={theme === "light"}
                    onSelect={setTheme}
                    icon={<Sun size={22} />}
                    title="Light"
                    description="Use the professional light interface."
                  />

                  <ThemeOption
                    value="dark"
                    selected={theme === "dark"}
                    onSelect={setTheme}
                    icon={<Moon size={22} />}
                    title="Dark"
                    description="Use the dark interface for lower brightness."
                  />

                  <ThemeOption
                    value="system"
                    selected={theme === "system"}
                    onSelect={setTheme}
                    icon={<Monitor size={22} />}
                    title="System"
                    description="Automatically follow your device theme."
                  />
                </div>
              </div>

              <div className="settings-info-box">
                <Palette size={18} />

                <div>
                  <strong>Theme preference</strong>
                  <p>
                    Your selected theme is stored locally on this
                    device and remains active after refreshing the
                    page.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* =====================================================
              NOTIFICATIONS
          ===================================================== */}
          {activeSection === "Notifications" && (
            <div className="settings-section">
              <div className="settings-section-header">
                <div>
                  <h2>Notifications</h2>
                  <p>
                    Configure which system notifications should
                    appear.
                  </p>
                </div>
              </div>

              <div className="settings-list">
                <div className="settings-row">
                  <div className="settings-row-icon">
                    <Bell size={18} />
                  </div>

                  <div className="settings-row-content">
                    <strong>Email Notifications</strong>
                    <p>
                      Receive important system notifications
                      through email.
                    </p>
                  </div>

                  <Toggle
                    enabled={emailNotifications}
                    onChange={setEmailNotifications}
                  />
                </div>

                <div className="settings-row">
                  <div className="settings-row-icon">
                    <ShieldCheck size={18} />
                  </div>

                  <div className="settings-row-content">
                    <strong>System Alerts</strong>
                    <p>
                      Receive alerts regarding system health and
                      critical events.
                    </p>
                  </div>

                  <Toggle
                    enabled={systemAlerts}
                    onChange={setSystemAlerts}
                  />
                </div>

                <div className="settings-row">
                  <div className="settings-row-icon">
                    <Database size={18} />
                  </div>

                  <div className="settings-row-content">
                    <strong>Dataset Processing</strong>
                    <p>
                      Get notified when dataset validation and
                      processing is completed.
                    </p>
                  </div>

                  <Toggle
                    enabled={datasetProcessing}
                    onChange={setDatasetProcessing}
                  />
                </div>

                <div className="settings-row">
                  <div className="settings-row-icon">
                    <Lock size={18} />
                  </div>

                  <div className="settings-row-content">
                    <strong>Security Notifications</strong>
                    <p>
                      Receive notifications for important security
                      events.
                    </p>
                  </div>

                  <Toggle
                    enabled={securityNotifications}
                    onChange={setSecurityNotifications}
                  />
                </div>
              </div>
            </div>
          )}

          {/* =====================================================
              SECURITY
          ===================================================== */}
          {activeSection === "Security" && (
            <div className="settings-section">
              <div className="settings-section-header">
                <div>
                  <h2>Security</h2>
                  <p>
                    Review administrator security and audit
                    configuration.
                  </p>
                </div>
              </div>

              <div className="security-status-card">
                <div className="security-status-icon">
                  <ShieldCheck size={26} />
                </div>

                <div>
                  <strong>System Security Status</strong>
                  <p>
                    Administrator authentication and audit
                    controls are currently active.
                  </p>
                </div>

                <span className="status-badge status-active">
                  <CheckCircle2 size={14} />
                  Protected
                </span>
              </div>

              <div className="settings-list">
                <div className="settings-row">
                  <div className="settings-row-icon">
                    <Lock size={18} />
                  </div>

                  <div className="settings-row-content">
                    <strong>Authentication</strong>
                    <p>
                      Administrator authentication is protected.
                    </p>
                  </div>

                  <span className="status-badge status-active">
                    Active
                  </span>
                </div>

                <div className="settings-row">
                  <div className="settings-row-icon">
                    <Clock3 size={18} />
                  </div>

                  <div className="settings-row-content">
                    <strong>Session</strong>
                    <p>
                      Current administrator session is active.
                    </p>
                  </div>

                  <span className="status-badge status-active">
                    Active
                  </span>
                </div>

                <div className="settings-row">
                  <div className="settings-row-icon">
                    <ClipboardList size={18} />
                  </div>

                  <div className="settings-row-content">
                    <strong>Audit Logging</strong>
                    <p>
                      Administrative actions are recorded in the
                      audit trail.
                    </p>
                  </div>

                  <Toggle
                    enabled={auditLogging}
                    onChange={setAuditLogging}
                  />
                </div>
              </div>

              <div className="settings-info-box">
                <Lock size={18} />

                <div>
                  <strong>Security configuration</strong>
                  <p>
                    Authentication and authorization will be
                    connected to the backend security system during
                    integration.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* =====================================================
              SYSTEM PREFERENCES
          ===================================================== */}
          {activeSection === "System Preferences" && (
            <div className="settings-section">
              <div className="settings-section-header">
                <div>
                  <h2>System Preferences</h2>
                  <p>
                    Configure system-level behaviour for the
                    administration portal.
                  </p>
                </div>
              </div>

              <div className="settings-list">
                <div className="settings-row">
                  <div className="settings-row-icon">
                    <Clock3 size={18} />
                  </div>

                  <div className="settings-row-content">
                    <strong>Automatic Data Refresh</strong>
                    <p>
                      Automatically refresh dashboard information
                      when supported by the backend.
                    </p>
                  </div>

                  <Toggle
                    enabled={automaticRefresh}
                    onChange={setAutomaticRefresh}
                  />
                </div>

                <div className="settings-row">
                  <div className="settings-row-icon">
                    <Database size={18} />
                  </div>

                  <div className="settings-row-content">
                    <strong>Data Processing</strong>
                    <p>
                      Dataset processing and ingestion are
                      controlled by the backend service.
                    </p>
                  </div>

                  <span className="status-badge status-info">
                    Backend Controlled
                  </span>
                </div>

                <div className="settings-row">
                  <div className="settings-row-icon">
                    <ClipboardList size={18} />
                  </div>

                  <div className="settings-row-content">
                    <strong>Audit Trail</strong>
                    <p>
                      Administrative activities are recorded for
                      supervision and accountability.
                    </p>
                  </div>

                  <span className="status-badge status-active">
                    Enabled
                  </span>
                </div>
              </div>

              <div className="system-information">
                <h3>System Information</h3>

                <div className="system-info-grid">
                  <div>
                    <span>Application</span>
                    <strong>SAT-SA</strong>
                  </div>

                  <div>
                    <span>Portal</span>
                    <strong>Admin Portal</strong>
                  </div>

                  <div>
                    <span>Version</span>
                    <strong>0.1.0</strong>
                  </div>

                  <div>
                    <span>Environment</span>
                    <strong>Development</strong>
                  </div>
                </div>
              </div>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

export default Settings;
