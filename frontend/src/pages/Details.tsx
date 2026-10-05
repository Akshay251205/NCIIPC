import { Link, useParams } from 'react-router-dom'
import { alertApi, analystApi, assetApi, intelligenceApi, investigationApi } from '../api/services'
import type { Profile, Signal } from '../api/types'
import { RiskBadge, State, score } from '../components/ui'
import { useResource } from '../hooks/useResource'

function SignalCard({ title, signal }: { title: string; signal?: Signal }) {
  if (!signal) return null
  return <article className="card"><h3>{title}</h3><p><b>{score(signal.score ?? signal.average_score)}</b> <RiskBadge value={signal.severity}/></p><small>Confidence: {signal.confidence ?? 'Not provided'}</small>{signal.indicators?.length ? <ul>{signal.indicators.map((indicator) => <li key={indicator}>{indicator}</li>)}</ul> : <p>No indicators were supplied.</p>}</article>
}

function RiskOverview({ profile }: { profile: Profile }) {
  const components = profile.risk.components ?? {}
  return <article className="card risk-overview"><div><small>Overall risk score</small><strong>{score(profile.risk.score)}</strong><p><RiskBadge value={profile.risk.level}/> Severity: {profile.risk.severity ?? '—'} · Confidence: {profile.risk.confidence ?? '—'}</p></div><div className="components">{Object.entries(components).map(([name, value]) => <div key={name}><span>{name.replaceAll('_', ' ')}</span><b>{score(value)}</b><meter min="0" max="100" value={value}/></div>)}</div></article>
}

function Evidence({ profile }: { profile: Profile }) {
  return <div className="grid"><article className="card"><h2>Indicators</h2>{profile.evidence?.length ? <ul>{profile.evidence.map((item) => <li key={item}>{item}</li>)}</ul> : <p>No indicators were supplied.</p>}</article><article className="card"><h2>Recommendations</h2>{profile.recommendations?.length ? <ul>{profile.recommendations.map((item) => <li key={item}>{item}</li>)}</ul> : <p>No recommendations were supplied.</p>}</article><details className="card"><summary>Evidence context</summary><pre>{JSON.stringify(profile.evidence_context ?? {}, null, 2)}</pre></details></div>
}

export function AnalystDetail() {
  const { analystId = '' } = useParams(); const profile = useResource(() => intelligenceApi.profile(analystId), [analystId]); const analyst = useResource(() => analystApi.get(analystId), [analystId])
  return <State loading={profile.loading} error={profile.error} retry={profile.refresh}>{profile.data && <section><Link className="back-link" to="/analysts">← Analysts</Link><div className="page-title"><div><h1>{analyst.data?.name ?? profile.data.analyst_id}</h1><p>{profile.data.analyst_id} · {analyst.data?.role ?? 'Role not available'} · {analyst.data?.team ?? 'Team not available'} · {analyst.data?.organization_id ?? 'Organization not available'}</p></div><RiskBadge value={profile.data.risk.level}/></div><RiskOverview profile={profile.data}/><div className="grid"><SignalCard title="Behavioral anomaly" signal={profile.data.behavioral_anomaly}/><SignalCard title="Potential metric-gaming patterns" signal={profile.data.gaming}/><SignalCard title="Investigation NLP" signal={profile.data.investigation_nlp}/><SignalCard title="Peer benchmark" signal={profile.data.peer_benchmark}/><SignalCard title="Negative-space intelligence" signal={profile.data.negative_space}/></div><Evidence profile={profile.data}/></section>}</State>
}

export function FindingDetail() {
  const { findingId = '' } = useParams(); const resource = useResource(() => intelligenceApi.profile(findingId), [findingId])
  return <State loading={resource.loading} error={resource.error} retry={resource.refresh}>{resource.data && <section><Link className="back-link" to="/findings">← Findings</Link><div className="page-title"><div><h1>Finding for {resource.data.analyst_id}</h1><p>Canonical analyst finding detail</p></div></div><RiskOverview profile={resource.data}/><Evidence profile={resource.data}/></section>}</State>
}

export function RecordDetail({ kind }: { kind: 'alert' | 'investigation' | 'asset' }) {
  const { id = '' } = useParams(); const load = kind === 'alert' ? () => alertApi.get(id) : kind === 'investigation' ? () => investigationApi.get(id) : () => assetApi.get(id); const resource = useResource<object>(async () => load(), [id, kind])
  return <State loading={resource.loading} error={resource.error} retry={resource.refresh}>{resource.data && <section><Link className="back-link" to={`/${kind}s`}>← {kind}s</Link><div className="page-title"><div><h1>{kind[0].toUpperCase() + kind.slice(1)} {id}</h1><p>Backend record detail</p></div></div><details open className="card"><summary>Record data</summary><pre>{JSON.stringify(resource.data, null, 2)}</pre></details></section>}</State>
}
