import { ApiError, request } from './api/client'
export type Supervisor = { username: string; email: string }; type AuthResponse = { token: string; user: Supervisor }; const SESSION_KEY = 'sat-sa-session'
export function sessionToken() { return localStorage.getItem(SESSION_KEY) }
export function saveSession(response: AuthResponse) { localStorage.setItem(SESSION_KEY, response.token); localStorage.setItem('sat-sa-supervisor', JSON.stringify(response.user)) }
export function clearSession() { localStorage.removeItem(SESSION_KEY); localStorage.removeItem('sat-sa-supervisor') }
export function savedSupervisor(): Supervisor | null { try { return JSON.parse(localStorage.getItem('sat-sa-supervisor') ?? 'null') as Supervisor | null } catch { return null } }
export async function signIn(identity: string, password: string) { const response = await request<AuthResponse>('/api/v1/auth/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ identity, password }) }); saveSession(response); return response.user }
export async function signUp(username: string, email: string, password: string) { const response = await request<AuthResponse>('/api/v1/auth/signup', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ username, email, password }) }); saveSession(response); return response.user }
export async function signOut() { try { await request<void>('/api/v1/auth/logout', { method: 'POST' }) } catch (error) { if (!(error instanceof ApiError) || error.status !== 401) throw error } finally { clearSession() } }
