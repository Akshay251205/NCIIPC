import { Navigate, Outlet, Route, Routes } from 'react-router-dom'
import { Layout } from './components/Layout'
import { AnalystDetail, FindingDetail, RecordDetail } from './pages/Details'
import { Dashboard } from './pages/Dashboard'
import { Alerts, Analysts, Assets, Findings, Investigations } from './pages/ListPages'
import { Settings, Unsupported } from './pages/Settings'
import { Login } from './pages/Login'
import { SignUp } from './pages/SignUp'
import { sessionToken } from './auth'

function RequireAuth() { return sessionToken() ? <Outlet/> : <Navigate to="/login" replace/> }

export default function App() {
  return <Routes><Route path="login" element={<Login/>}/><Route path="signup" element={<SignUp/>}/><Route element={<RequireAuth/>}><Route element={<Layout/>}><Route index element={<Navigate to="/dashboard" replace/>}/><Route path="dashboard" element={<Dashboard/>}/><Route path="analysts" element={<Analysts/>}/><Route path="analysts/:analystId" element={<AnalystDetail/>}/><Route path="findings" element={<Findings/>}/><Route path="findings/:findingId" element={<FindingDetail/>}/><Route path="alerts" element={<Alerts/>}/><Route path="alerts/:id" element={<RecordDetail kind="alert"/>}/><Route path="investigations" element={<Investigations/>}/><Route path="investigations/:id" element={<RecordDetail kind="investigation"/>}/><Route path="assets" element={<Assets/>}/><Route path="assets/:id" element={<RecordDetail kind="asset"/>}/><Route path="settings" element={<Settings/>}/><Route path="settings/preferences" element={<Settings/>}/><Route path="settings/account" element={<Unsupported name="Account settings"/>}/><Route path="settings/security" element={<Unsupported name="Security settings"/>}/><Route path="settings/notifications" element={<Unsupported name="Notification settings"/>}/><Route path="notifications" element={<Unsupported name="Notifications"/>}/><Route path="profile" element={<Unsupported name="User profile"/>}/><Route path="forgot-password" element={<Unsupported name="Password recovery"/>}/><Route path="reset-password" element={<Unsupported name="Password reset"/>}/><Route path="404" element={<Unsupported name="Page not found"/>}/><Route path="*" element={<Navigate to="/404" replace/>}/></Route></Route></Routes>
}
