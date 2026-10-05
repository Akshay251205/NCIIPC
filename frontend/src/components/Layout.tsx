import { Bell, ChartNoAxesCombined, ChevronLeft, Files, LogOut, Menu, Moon, ShieldAlert, Sun, Users, Search, Box, Settings } from 'lucide-react'
import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { savedSupervisor, signOut } from '../auth'
const links = [{to:'/dashboard', label:'Dashboard', icon:ChartNoAxesCombined}, {to:'/analysts', label:'Analysts', icon:Users}, {to:'/findings', label:'Findings', icon:Files}, {to:'/alerts', label:'Alerts', icon:ShieldAlert}, {to:'/investigations', label:'Investigations', icon:Search}, {to:'/assets', label:'Assets', icon:Box}]
export function Layout() {
  const nav = useNavigate()
  const [collapsed, setCollapsed] = useState(() => localStorage.getItem('sat-sa-sidebar') === 'collapsed')
  const [theme, setTheme] = useState<'dark' | 'light'>(() => localStorage.getItem('sat-sa-theme') === 'light' ? 'light' : 'dark')
  const supervisor = savedSupervisor()
  useEffect(() => { document.documentElement.dataset.theme = theme; localStorage.setItem('sat-sa-theme', theme) }, [theme])
  useEffect(() => { document.body.classList.toggle('density-compact', localStorage.getItem('sat-sa-density') === 'compact') }, [])
  useEffect(() => { localStorage.setItem('sat-sa-sidebar', collapsed ? 'collapsed' : 'expanded') }, [collapsed])
  return <div className="shell"><aside className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
    <div className="brand"><span className="brand-mark"><ShieldAlert size={17}/></span><span className="brand-copy">SAT-SA<small>SUPERVISORY INTELLIGENCE</small></span></div>
    <div className="nav-label">Command center</div><nav>{links.map(({to,label,icon:Icon}) => <NavLink key={to} to={to} title={collapsed ? label : undefined}><Icon size={18}/><span className="link-text">{label}</span></NavLink>)}</nav>
    <div className="sidebar-bottom-actions"><button className="logout" type="button" title={collapsed ? 'Log out' : undefined} onClick={async () => { await signOut(); nav('/login', { replace: true }) }}><LogOut size={18}/><span className="link-text">Log out</span></button><NavLink className="settings" to="/settings" title={collapsed ? 'Preferences' : undefined}><Settings size={18}/><span className="link-text">Preferences</span></NavLink></div>
  </aside><main><header><div><b>Security Analyst Trust & Supervisory Assessment</b><small>Canonical intelligence and operational telemetry</small></div><div className="header-actions">
    <button className="icon-button" aria-label={collapsed ? 'Expand navigation' : 'Collapse navigation'} onClick={() => setCollapsed(value => !value)}>{collapsed ? <Menu size={18}/> : <ChevronLeft size={18}/>}</button>
    <span className="api-dot">API connected</span><button className="icon-button" aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`} onClick={() => setTheme(value => value === 'dark' ? 'light' : 'dark')}>{theme === 'dark' ? <Sun size={17}/> : <Moon size={17}/>}</button>
    <button className="icon-button" aria-label="Open notifications" title="Notifications are not available from this backend" onClick={() => nav('/notifications')}><Bell size={18}/></button><NavLink className="profile-link" to="/profile" title="User profile"><span className="profile-avatar">{supervisor?.username.slice(0, 2).toUpperCase() ?? 'SA'}</span><span>{supervisor?.username ?? 'Supervisor'}</span></NavLink>
  </div></header><section className="content"><Outlet /></section></main></div>
}
