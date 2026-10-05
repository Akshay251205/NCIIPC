const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'

export class ApiError extends Error { constructor(public status: number, message: string) { super(message) } }
export async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const controller = new AbortController(); const timeout = window.setTimeout(() => controller.abort(), 15000)
  try {
    const token = localStorage.getItem('sat-sa-session')
    const response = await fetch(`${BASE_URL}${path}`, { ...init, headers: { Accept: 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}), ...init?.headers }, signal: controller.signal })
    if (!response.ok) { const body = await response.json().catch(() => null) as { detail?: string } | null; throw new ApiError(response.status, body?.detail ?? `Request failed (${response.status})`) }
    if (response.status === 204) return undefined as T
    return response.json() as Promise<T>
  } catch (error) { if (error instanceof ApiError) throw error; throw new ApiError(0, error instanceof DOMException ? 'Request timed out. Please retry.' : 'Unable to reach the SAT-SA API.') } finally { window.clearTimeout(timeout) }
}
