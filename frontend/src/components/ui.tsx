import type { ReactNode } from 'react'
export function State({ loading, error, children, retry }: { loading: boolean; error?: string; children: ReactNode; retry?: () => void }) { if (loading) return <div className="state">Loading supervisory data…</div>; if (error) return <div className="state error">{error}{retry && <button onClick={retry}>Retry</button>}</div>; return <>{children}</> }
export function RiskBadge({ value }: { value?: string }) { const label = value?.toUpperCase() || 'UNAVAILABLE'; return <span className={`badge ${label.toLowerCase()}`}>{label}</span> }
export function Empty({ children }: { children: ReactNode }) { return <div className="state">{children}</div> }
export function score(value?: number) { return typeof value === 'number' ? value.toFixed(2) : '—' }
