# SAT-SA backend

SAT-SA is a local Smart Analyst Trust / supervisory-security analytics demo.
The API serves explainable analyst intelligence from PostgreSQL.

## Canonical pipeline

```text
PostgreSQL -> Analytics -> Rules -> Behavioral -> Gaming -> NLP -> Peer
           -> Negative Space -> Risk Fusion -> Final Finding
           -> Supervisory Intelligence -> FastAPI
```

`app.services.analytics.analyst_metrics` is the canonical bulk pipeline.
`app.services.risk.risk_fusion` is the only authoritative analyst-risk
calculation. The supervisory engine is an aggregation and prioritisation view
over its output; it does not calculate a second risk score.

Risk Fusion uses rule (40%), AI/behavior (30%), negative space (20%), and peer
(10%) components. Unavailable components remain unavailable and the available
weights are renormalized; the service never inserts a fabricated score.

Negative-space inputs come from assets, aggregated asset activity, and the
assets assigned to an analyst through alerts. Analysts without applicable
assigned assets receive an unavailable negative-space component.

## Run and verify

Configure `DATABASE_URL` in the repository `.env`, then from this directory:

```powershell
python -m alembic current
python -m pytest -q
python -m compileall app
python -m app.services.analytics.analyst_metrics
```

Useful API routes include `GET /health`, `GET /intelligence/summary`,
`GET /intelligence/findings`, `GET /intelligence/analysts/{analyst_id}`, and
`GET /intelligence/analysts/{analyst_id}/profile`.

## Security posture

This project is **SIH local demo ready**. It has no authentication or RBAC and
must not be represented as ready for an internet-facing production deployment.
