import { request } from './client'
import type { Alert, Analyst, Asset, Finding, IntelligenceSummary, Investigation, Page, Profile } from './types'
const qs = (params: Record<string, string | number | undefined>) => { const value = new URLSearchParams(); Object.entries(params).forEach(([k, v]) => v !== undefined && v !== '' && value.set(k, String(v))); const text = value.toString(); return text ? `?${text}` : '' }
export const intelligenceApi = { summary: () => request<IntelligenceSummary>('/intelligence/summary'), findings: () => request<{count:number; findings:Finding[]}>('/intelligence/findings'), profile: (id:string) => request<Profile>(`/intelligence/analysts/${encodeURIComponent(id)}/profile`) }
export const analystApi = { list: (p: Record<string,string|number|undefined>) => request<Page<Analyst>>(`/api/v1/analysts${qs(p)}`), get: (id:string) => request<Analyst>(`/api/v1/analysts/${encodeURIComponent(id)}`) }
export const alertApi = { list: (p:Record<string,string|number|undefined>) => request<Page<Alert>>(`/api/v1/alerts${qs(p)}`), get:(id:string) => request<Alert>(`/api/v1/alerts/${encodeURIComponent(id)}`) }
export const investigationApi = { list: (p:Record<string,string|number|undefined>) => request<Page<Investigation>>(`/api/v1/investigations${qs(p)}`), get:(id:string) => request<Investigation>(`/api/v1/investigations/${encodeURIComponent(id)}`) }
export const assetApi = { list: (p:Record<string,string|number|undefined>) => request<Page<Asset>>(`/api/v1/assets${qs(p)}`), get:(id:string) => request<Asset>(`/api/v1/assets/${encodeURIComponent(id)}`) }
