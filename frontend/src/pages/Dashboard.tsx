import { Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts'
import { useNavigate } from 'react-router-dom'
import { State, score } from '../components/ui'
import { intelligenceApi } from '../api/services'
import { useResource } from '../hooks/useResource'

const colors: Record<string, string> = { LOW: '#2eaa76', MEDIUM: '#e7a534', HIGH: '#dc6a37', CRITICAL: '#c74352' }

export function Dashboard() {
  const resource = useResource(intelligenceApi.summary, [])
  const navigate = useNavigate(); const summary = resource.data?.summary
  const distribution = Object.entries(summary?.risk_distribution ?? {}).map(([name, value]) => ({ name, value }))
  const cards: [string, string | number | undefined, string][] = [['Total Analysts', summary?.analysts_analyzed, ''], ['Requires Attention', summary?.analysts_requiring_attention, 'accent-cyan'], ['Average Risk', score(summary?.average_risk_score), 'accent-purple'], ['Critical Analysts', summary?.risk_distribution?.CRITICAL, ''], ['High Risk Analysts', summary?.risk_distribution?.HIGH, ''], ['Investigations Analyzed', summary?.investigations_analyzed, ''], ['Alerts Analyzed', summary?.alerts_analyzed, '']]
  return <><div className="page-title"><div><h1>Supervisory dashboard</h1><p>Live view of the backend’s canonical risk-fusion output.</p></div><button className="primary-button" onClick={resource.refresh}>Refresh data</button></div><State loading={resource.loading} error={resource.error} retry={resource.refresh}>{summary && <><article className="card dashboard-hero"><div><span className="intel-tag">Risk fusion intelligence</span><h2>Supervisory posture at a glance</h2><p>Prioritized signals from the current analyst, investigation, and alert intelligence output.</p></div><div className="risk-summary"><small>Average risk score</small><strong>{score(summary.average_risk_score)}</strong></div></article><div className="kpis">{cards.map(([label, value, accent]) => <article className={`card metric-card ${accent}`} key={label}><small>{label}</small><strong>{typeof value === 'number' ? value.toLocaleString() : value}</strong></article>)}</div><div className="card chart"><div className="chart-header"><div><span className="intel-tag">Distribution</span><h2>Risk distribution</h2><p>Click a segment to filter canonical findings.</p></div></div><ResponsiveContainer width="100%" height={300}><PieChart><Pie data={distribution} dataKey="value" nameKey="name" innerRadius={65} outerRadius={105} onClick={(entry) => navigate(`/findings?risk_level=${entry.name}`)}>{distribution.map((item) => <Cell key={item.name} fill={colors[item.name] ?? '#73849c'}/>)}</Pie><Tooltip/><Legend/></PieChart></ResponsiveContainer><p className="sr-only">{distribution.map((item) => `${item.name}: ${item.value}`).join(', ')}</p></div></>}</State></>
}
