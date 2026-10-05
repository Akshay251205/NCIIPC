import type { ReactNode } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { alertApi, analystApi, assetApi, intelligenceApi, investigationApi } from '../api/services'
import type { Alert, Analyst, Asset, Finding, Investigation } from '../api/types'
import { Empty, RiskBadge, State, score } from '../components/ui'
import { useResource } from '../hooks/useResource'

function Title({ title, description }: { title: string; description: string }) {
  return <div className="page-title"><div><h1>{title}</h1><p>{description}</p></div></div>
}

function Table({ headers, children }: { headers: string[]; children: ReactNode }) {
  return <div className="table-wrap"><table><thead><tr>{headers.map((header) => <th key={header}>{header}</th>)}</tr></thead>{children}</table></div>
}

function Pager({ page, total, limit, setPage }: { page: number; total: number; limit: number; setPage: (value: number) => void }) {
  return <div className="pager"><button disabled={page === 1} onClick={() => setPage(page - 1)}>Previous</button><span>Page {page} of {Math.max(1, Math.ceil(total / limit))} · {total.toLocaleString()} records</span><button disabled={page * limit >= total} onClick={() => setPage(page + 1)}>Next</button></div>
}

export function Analysts() {
  const [params, setParams] = useSearchParams(); const page = Number(params.get('page') ?? '1'); const status = params.get('status') ?? ''; const organization = params.get('organization_id') ?? ''
  const resource = useResource(() => analystApi.list({ page, limit: 25, status, organization_id: organization }), [page, status, organization])
  const setPage = (next: number) => setParams({ page: String(next), ...(status ? { status } : {}), ...(organization ? { organization_id: organization } : {}) })
  return <section><Title title="Analysts" description="Operational analyst records from PostgreSQL. Intelligence is available in each profile."/><div className="filters"><label>Status <input value={status} onChange={(event) => setParams({ page: '1', ...(event.target.value ? { status: event.target.value } : {}), ...(organization ? { organization_id: organization } : {}) })} placeholder="e.g. Active"/></label><label>Organization <input value={organization} onChange={(event) => setParams({ page: '1', ...(status ? { status } : {}), ...(event.target.value ? { organization_id: event.target.value } : {}) })} placeholder="Organization ID"/></label></div><State loading={resource.loading} error={resource.error} retry={resource.refresh}>{resource.data && <><Table headers={['Analyst', 'Role / team', 'Organization', 'Experience', 'Status']}><tbody>{resource.data.data.map((analyst: Analyst) => <tr key={analyst.analyst_id}><td><Link to={`/analysts/${analyst.analyst_id}`}>{analyst.name}</Link><small>{analyst.analyst_id}</small></td><td>{analyst.role ?? '—'}<small>{analyst.team ?? '—'}</small></td><td>{analyst.organization_id}</td><td>{analyst.experience_years ?? '—'} years</td><td>{analyst.status ?? '—'}</td></tr>)}</tbody></Table>{resource.data.data.length === 0 && <Empty>No analysts found.</Empty>}<Pager page={page} total={resource.data.total} limit={resource.data.limit} setPage={setPage}/></>}</State></section>
}

export function Findings() {
  const [params, setParams] = useSearchParams(); const page = Number(params.get('page') ?? '1'); const riskLevel = params.get('risk_level') ?? ''; const limit = 25
  const resource = useResource(intelligenceApi.findings, []); const filtered = (resource.data?.findings ?? []).filter((finding) => !riskLevel || finding.risk_level === riskLevel); const visible = filtered.slice((page - 1) * limit, page * limit)
  return <section><Title title="Findings" description="Canonical, backend-generated findings. The backend currently provides this collection as a bulk endpoint; only one page is rendered at a time."/><div className="filters"><label>Risk level <select value={riskLevel} onChange={(event) => setParams({ page: '1', ...(event.target.value ? { risk_level: event.target.value } : {}) })}><option value="">All levels</option><option>LOW</option><option>MEDIUM</option><option>HIGH</option><option>CRITICAL</option></select></label></div><State loading={resource.loading} error={resource.error} retry={resource.refresh}>{resource.data && <>{visible.length ? <Table headers={['Analyst', 'Score', 'Risk level', 'Indicators']}><tbody>{visible.map((finding: Finding) => <tr key={finding.analyst_id}><td><Link to={`/findings/${finding.analyst_id}`}>{finding.analyst_name ?? finding.analyst_id}</Link><small>{finding.analyst_id}</small></td><td>{score(finding.score)}</td><td><RiskBadge value={finding.risk_level}/></td><td>{finding.indicators?.slice(0, 2).join(', ') || '—'}</td></tr>)}</tbody></Table> : <Empty>No findings match this risk level.</Empty>}<Pager page={page} total={filtered.length} limit={limit} setPage={(next) => setParams({ page: String(next), ...(riskLevel ? { risk_level: riskLevel } : {}) })}/></>}</State></section>
}

export function Alerts() { return <Operational title="Alerts" description="Database-backed alert records." load={alertApi.list} headers={['Alert ID', 'Analyst', 'Severity', 'Status', 'Closure minutes']} render={(alert: Alert) => <tr key={alert.alert_id}><td><Link to={`/alerts/${alert.alert_id}`}>{alert.alert_id}</Link></td><td>{alert.analyst_id ?? '—'}</td><td><RiskBadge value={alert.severity}/></td><td>{alert.status ?? '—'}</td><td>{alert.closure_time_minutes ?? '—'}</td></tr>}/>} 
export function Investigations() { return <Operational title="Investigations" description="Database-backed investigation records." load={investigationApi.list} headers={['Investigation ID', 'Analyst', 'Duration', 'Queries']} render={(item: Investigation) => <tr key={item.investigation_id}><td><Link to={`/investigations/${item.investigation_id}`}>{item.investigation_id}</Link></td><td>{item.analyst_id}</td><td>{item.duration_minutes ?? '—'}</td><td>{item.queries_executed ?? '—'}</td></tr>}/>} 
export function Assets() { return <Operational title="Assets" description="Database-backed asset inventory." load={assetApi.list} headers={['Asset', 'Type', 'Organization', 'Criticality', 'Status']} render={(asset: Asset) => <tr key={asset.asset_id}><td><Link to={`/assets/${asset.asset_id}`}>{asset.asset_name}</Link><small>{asset.asset_id}</small></td><td>{asset.asset_type ?? '—'}</td><td>{asset.organization_id}</td><td>{asset.criticality ?? '—'}</td><td>{asset.status ?? '—'}</td></tr>}/>} 

function Operational<T extends object>({ title, description, load, headers, render }: { title: string; description: string; load: (params: Record<string, string | number | undefined>) => Promise<{ total: number; limit: number; data: T[] }>; headers: string[]; render: (item: T) => ReactNode }) {
  const [params, setParams] = useSearchParams(); const page = Number(params.get('page') ?? '1'); const resource = useResource(() => load({ page, limit: 25 }), [page])
  return <section><Title title={title} description={description}/><State loading={resource.loading} error={resource.error} retry={resource.refresh}>{resource.data && <>{resource.data.data.length ? <Table headers={headers}><tbody>{resource.data.data.map(render)}</tbody></Table> : <Empty>No {title.toLowerCase()} found.</Empty>}<Pager page={page} total={resource.data.total} limit={resource.data.limit} setPage={(next) => setParams({ page: String(next) })}/></>}</State></section>
}
