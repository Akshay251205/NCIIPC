from collections import Counter, defaultdict

from sqlalchemy import case, func

from app.database import SessionLocal
from app.models import (
    Analyst,
    Alert,
    Asset,
    AssetActivity,
    Investigation,
    PeerBenchmark,
)
from app.services.rules.analyst_rules import evaluate_analyst_behavior

from app.services.anomaly.behavioral_anomaly import (
    calculate_population_metrics,
    detect_behavioral_anomaly,
    prepare_population_statistics,
)
from app.services.gaming.gaming_detection import detect_gaming_behavior
from app.services.nlp.investigation_nlp import detect_investigation_nlp
from app.services.peer.peer_benchmark import calculate_peer_benchmark
from app.services.negative_space.negative_space import (
    detect_negative_space,
)
from app.services.risk.risk_fusion import fuse_analyst_risk


def _safe_float(value, default=0.0):
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalise_note(note):
    if not note:
        return ""
    return " ".join(str(note).lower().split())


# ============================================================
# BASE ANALYST METRICS
# ============================================================

def _get_base_analyst_metrics(db):
    """
    Repo-1 canonical analyst metrics.

    Uses grouped SQL queries and the shared DB session.
    """

    analysts = db.query(Analyst).all()

    # --------------------------------------------------------
    # Alert aggregation
    # --------------------------------------------------------

    alert_rows = (
        db.query(
            Alert.analyst_id.label("analyst_id"),
            func.count(Alert.alert_id).label("total_alerts"),

            func.sum(
                case((Alert.status == "Closed", 1), else_=0)
            ).label("closed_alerts"),

            func.sum(
                case((Alert.status == "Open", 1), else_=0)
            ).label("open_alerts"),

            func.sum(
                case((Alert.status == "Investigating", 1), else_=0)
            ).label("investigating_alerts"),

            func.sum(
                case((Alert.escalated.is_(True), 1), else_=0)
            ).label("escalated_alerts"),

            func.sum(
                case((Alert.false_positive.is_(True), 1), else_=0)
            ).label("false_positives"),

            func.sum(
                case((Alert.evidence_reviewed.is_(True), 1), else_=0)
            ).label("evidence_reviewed_alerts"),

            func.avg(Alert.closure_time_minutes).label("avg_closure_time"),
        )
        .group_by(Alert.analyst_id)
        .all()
    )

    alert_metrics = {}

    for row in alert_rows:
        alert_metrics[row.analyst_id] = {
            "total_alerts": int(row.total_alerts or 0),
            "closed_alerts": int(row.closed_alerts or 0),
            "open_alerts": int(row.open_alerts or 0),
            "investigating_alerts": int(row.investigating_alerts or 0),
            "escalated_alerts": int(row.escalated_alerts or 0),
            "false_positives": int(row.false_positives or 0),
            "evidence_reviewed_alerts": int(
                row.evidence_reviewed_alerts or 0
            ),
            "avg_closure_time": (
                float(row.avg_closure_time)
                if row.avg_closure_time is not None
                else None
            ),
        }

    # --------------------------------------------------------
    # Investigation aggregation
    # --------------------------------------------------------

    investigation_rows = (
        db.query(
            Investigation.analyst_id.label("analyst_id"),
            func.count(
                Investigation.investigation_id
            ).label("total_investigations"),

            func.avg(
                Investigation.duration_minutes
            ).label("avg_investigation_time"),

            func.sum(
                case(
                    (
                        Investigation.evidence_reviewed.is_(True),
                        1,
                    ),
                    else_=0,
                )
            ).label("evidence_reviewed_investigations"),

            func.sum(
                case(
                    (
                        Investigation.escalation_decision == "Yes",
                        1,
                    ),
                    else_=0,
                )
            ).label("escalated_investigations"),
        )
        .group_by(Investigation.analyst_id)
        .all()
    )

    investigation_metrics = {}

    for row in investigation_rows:
        investigation_metrics[row.analyst_id] = {
            "total_investigations": int(
                row.total_investigations or 0
            ),
            "avg_investigation_time": (
                float(row.avg_investigation_time)
                if row.avg_investigation_time is not None
                else None
            ),
            "evidence_reviewed_investigations": int(
                row.evidence_reviewed_investigations or 0
            ),
            "escalated_investigations": int(
                row.escalated_investigations or 0
            ),
        }

    # --------------------------------------------------------
    # ONE investigation activity scan
    # --------------------------------------------------------

    activity_rows = (
        db.query(
            Investigation.analyst_id,
            Investigation.actions_performed,
            Investigation.queries_executed,
        )
        .all()
    )

    action_totals = defaultdict(int)
    action_records = defaultdict(int)
    query_totals = defaultdict(int)
    query_records = defaultdict(int)

    for row in activity_rows:
        analyst_id = row.analyst_id

        if row.actions_performed:
            actions = [
                x.strip()
                for x in str(row.actions_performed).split(";")
                if x.strip()
            ]

            if actions:
                action_totals[analyst_id] += len(actions)
                action_records[analyst_id] += 1

        if row.queries_executed is not None:
            try:
                query_totals[analyst_id] += int(
                    row.queries_executed
                )
                query_records[analyst_id] += 1
            except (TypeError, ValueError):
                pass

    # --------------------------------------------------------
    # Build base records
    # --------------------------------------------------------

    results = []

    for analyst in analysts:
        analyst_id = analyst.analyst_id

        alerts = alert_metrics.get(
            analyst_id,
            {
                "total_alerts": 0,
                "closed_alerts": 0,
                "open_alerts": 0,
                "investigating_alerts": 0,
                "escalated_alerts": 0,
                "false_positives": 0,
                "evidence_reviewed_alerts": 0,
                "avg_closure_time": None,
            },
        )

        investigations = investigation_metrics.get(
            analyst_id,
            {
                "total_investigations": 0,
                "avg_investigation_time": None,
                "evidence_reviewed_investigations": 0,
                "escalated_investigations": 0,
            },
        )

        total_alerts = alerts["total_alerts"]
        closed_alerts = alerts["closed_alerts"]
        avg_closure_time = alerts["avg_closure_time"]

        total_investigations = investigations[
            "total_investigations"
        ]
        avg_investigation_time = investigations[
            "avg_investigation_time"
        ]

        avg_actions = (
            action_totals[analyst_id]
            / action_records[analyst_id]
            if action_records[analyst_id] > 0
            else 0.0
        )

        avg_queries = (
            query_totals[analyst_id]
            / query_records[analyst_id]
            if query_records[analyst_id] > 0
            else 0.0
        )

        if total_alerts > 0:
            closure_rate = round(
                closed_alerts / total_alerts * 100,
                2,
            )
            escalation_rate = round(
                alerts["escalated_alerts"] / total_alerts * 100,
                2,
            )
            false_positive_rate = round(
                alerts["false_positives"] / total_alerts * 100,
                2,
            )
            evidence_review_rate = round(
                alerts["evidence_reviewed_alerts"]
                / total_alerts
                * 100,
                2,
            )
        else:
            closure_rate = 0.0
            escalation_rate = 0.0
            false_positive_rate = 0.0
            evidence_review_rate = 0.0

        if total_investigations > 0:
            investigation_evidence_rate = round(
                investigations[
                    "evidence_reviewed_investigations"
                ]
                / total_investigations
                * 100,
                2,
            )

            investigation_escalation_rate = round(
                investigations[
                    "escalated_investigations"
                ]
                / total_investigations
                * 100,
                2,
            )
        else:
            investigation_evidence_rate = 0.0
            investigation_escalation_rate = 0.0

        # Existing rule intelligence
        risk = evaluate_analyst_behavior(
            total_alerts=total_alerts,
            closed_alerts=closed_alerts,
            avg_closure_time=avg_closure_time,
            evidence_review_rate=evidence_review_rate,
            escalation_rate=escalation_rate,
            total_investigations=total_investigations,
            avg_queries=avg_queries,
            avg_investigation_time=avg_investigation_time,
        )

        results.append(
            {
                "analyst_id": analyst_id,
                "name": analyst.name,
                "organization_id": analyst.organization_id,
                "role": analyst.role,
                "team": analyst.team,
                "experience_years": analyst.experience_years,
                "shift": analyst.shift,
                "status": analyst.status,
                "confidence": risk["confidence"],

                "alerts": {
                    "total": total_alerts,
                    "closed": closed_alerts,
                    "open": alerts["open_alerts"],
                    "investigating": alerts[
                        "investigating_alerts"
                    ],
                    "escalated": alerts[
                        "escalated_alerts"
                    ],
                    "false_positives": alerts[
                        "false_positives"
                    ],
                },

                "performance": {
                    "average_closure_time_minutes": (
                        round(float(avg_closure_time), 2)
                        if avg_closure_time is not None
                        else 0.0
                    ),
                    "closure_rate": closure_rate,
                    "escalation_rate": escalation_rate,
                    "false_positive_rate": false_positive_rate,
                    "evidence_review_rate": evidence_review_rate,
                },

                "investigations": {
                    "total": total_investigations,
                    "average_duration_minutes": (
                        round(
                            float(avg_investigation_time),
                            2,
                        )
                        if avg_investigation_time is not None
                        else 0.0
                    ),
                    "average_queries": round(
                        avg_queries,
                        2,
                    ),
                    "average_actions": round(
                        avg_actions,
                        2,
                    ),
                    "evidence_review_rate": (
                        investigation_evidence_rate
                    ),
                    "escalation_rate": (
                        investigation_escalation_rate
                    ),
                },

                "risk": {
                    "score": risk["score"],
                    "level": risk["level"],
                    "indicators": risk["indicators"],
                },
            }
        )

    return results


# ============================================================
# INVESTIGATION NLP
# ============================================================

def _build_investigation_intelligence(db):
    """
    Process investigation notes once.

    Returns analyst-level NLP metrics.
    """

    rows = (
        db.query(
            Investigation.investigation_id,
            Investigation.analyst_id,
            Investigation.investigation_notes,
            Investigation.evidence_reviewed,
        )
        .all()
    )

    data = defaultdict(
        lambda: {
            "total": 0,
            "scores": [],
            "confidences": [],
            "severities": [],
            "indicators": [],
            "observations": [],
            "notes": [],
        }
    )

    for row in rows:
        if not row.analyst_id:
            continue

        item = data[row.analyst_id]
        item["total"] += 1

        note = row.investigation_notes or ""

        finding = detect_investigation_nlp(
            investigation_id=str(row.investigation_id),
            note=note,
            evidence_reviewed=row.evidence_reviewed,
        )

        item["scores"].append(
            _safe_float(finding.score)
        )

        # Detector confidence is a categorical evidence-quality signal, not
        # a numeric score. Keep it intact for the analyst-level aggregate.
        item["confidences"].append(finding.confidence)
        item["severities"].append(finding.severity)

        item["indicators"].extend(
            list(finding.indicators or [])
        )

        item["observations"].extend(
            list(finding.observations or [])
        )

        normalized = _normalise_note(note)

        if normalized:
            item["notes"].append(normalized)

    result = {}

    for analyst_id, item in data.items():
        scores = item["scores"]
        confidences = item["confidences"]
        severities = item["severities"]
        notes = item["notes"]

        note_counts = Counter(notes)

        repeated_count = sum(
            count
            for count in note_counts.values()
            if count > 1
        )

        repeated_rate = (
            repeated_count / len(notes) * 100
            if notes
            else 0.0
        )

        short_count = sum(
            1
            for note in notes
            if len(note.split()) < 8
        )

        short_rate = (
            short_count / len(notes) * 100
            if notes
            else 0.0
        )

        result[analyst_id] = {
            "score": round(
                sum(scores) / len(scores),
                2,
            )
            if scores
            else 0.0,

            "confidence": max(
                confidences,
                key=lambda value: {
                    "Low": 1,
                    "Medium": 2,
                    "High": 3,
                }.get(str(value), 0),
            )
            if confidences
            else "Low",

            "high_findings": sum(
                severity == "HIGH"
                for severity in severities
            ),

            "medium_findings": sum(
                severity == "MEDIUM"
                for severity in severities
            ),

            "investigations_analyzed": item["total"],

            "short_note_rate": round(
                short_rate,
                2,
            ),

            "repeated_note_rate": round(
                repeated_rate,
                2,
            ),

            "indicators": list(
                dict.fromkeys(item["indicators"])
            ),

            "observations": list(
                dict.fromkeys(item["observations"])
            ),
        }

    return result


# ============================================================
# PEER BENCHMARKS
# ============================================================

def _build_peer_metrics(db):
    rows = (
        db.query(
            PeerBenchmark.organization_id,
            PeerBenchmark.metric_name,
            PeerBenchmark.peer_mean,
            PeerBenchmark.metric_value,
        )
        .all()
    )

    mapping = {
        "avg_closure_time":
            "average_closure_time_minutes",

        "escalation_rate":
            "escalation_rate",

        "evidence_review_rate":
            "evidence_review_rate",

        "mean_investigation_duration":
            "average_investigation_duration_minutes",
    }

    result = defaultdict(dict)

    for row in rows:
        canonical = mapping.get(row.metric_name)

        if canonical is None:
            continue

        value = (
            row.peer_mean
            if row.peer_mean is not None
            else row.metric_value
        )

        if value is not None:
            result[row.organization_id][canonical] = (
                _safe_float(value)
            )

    return dict(result)


# ============================================================
# NEGATIVE-SPACE INTELLIGENCE
# ============================================================

def _build_negative_space_intelligence(db):
    """Build analyst signals from assets assigned through their alerts.

    Assets are not directly owned by analysts in the canonical schema. An
    analyst is therefore associated only with the assets on alerts assigned to
    them. Activity is aggregated once per asset, then each analyst receives
    the highest-risk assigned asset signal. Analysts with no assigned assets
    are deliberately omitted so Risk Fusion can treat the layer as unavailable.
    """

    activity_rows = (
        db.query(
            AssetActivity.asset_id,
            func.sum(AssetActivity.event_count).label("event_count"),
            func.sum(AssetActivity.log_sources_active).label(
                "log_sources_active"
            ),
        )
        .group_by(AssetActivity.asset_id)
        .all()
    )

    activity_by_asset = {
        row.asset_id: {
            "event_count": _safe_float(row.event_count),
            "log_sources_active": _safe_float(
                row.log_sources_active
            ),
        }
        for row in activity_rows
    }

    asset_findings = {}

    for asset in db.query(Asset).all():
        activity = activity_by_asset.get(asset.asset_id)
        asset_findings[asset.asset_id] = detect_negative_space(
            asset_id=asset.asset_id,
            asset_status=asset.status,
            asset_criticality=asset.criticality,
            has_activity_record=activity is not None,
            event_count=(
                activity["event_count"] if activity else 0.0
            ),
            log_sources_active=(
                activity["log_sources_active"]
                if activity
                else 0.0
            ),
        )

    assets_by_analyst = defaultdict(set)

    for analyst_id, asset_id in (
        db.query(Alert.analyst_id, Alert.asset_id)
        .filter(Alert.analyst_id.isnot(None))
        .all()
    ):
        if analyst_id and asset_id in asset_findings:
            assets_by_analyst[analyst_id].add(asset_id)

    confidence_rank = {"Low": 1, "Medium": 2, "High": 3}
    result = {}

    for analyst_id, asset_ids in assets_by_analyst.items():
        findings = [asset_findings[asset_id] for asset_id in asset_ids]
        highest = max(findings, key=lambda finding: finding.score)
        indicators = []
        observations = []

        for finding in findings:
            for indicator in finding.indicators:
                if indicator not in indicators:
                    indicators.append(indicator)
            for observation in finding.observations:
                if observation not in observations:
                    observations.append(observation)

        result[analyst_id] = {
            "score": _safe_float(highest.score),
            "severity": highest.severity,
            "confidence": max(
                (finding.confidence for finding in findings),
                key=lambda value: confidence_rank.get(str(value), 0),
            ),
            "indicators": indicators,
            "observations": observations,
            "metrics": {
                "assets_analyzed": len(findings),
                "assets_with_findings": sum(
                    finding.score > 0 for finding in findings
                ),
                "scoring_method": "highest_assigned_asset_score",
            },
        }

    return result


# ============================================================
# INTELLIGENCE ENRICHMENT
# ============================================================

def _enrich_with_intelligence(
    base_records,
    investigation_intelligence,
    peer_data,
    negative_space_data,
):
    if not base_records:
        return []

    # Internal representation used by behavioral detector.
    internal_records = []

    for record in base_records:
        performance = record.get("performance") or {}
        investigations = record.get("investigations") or {}

        nlp = investigation_intelligence.get(
            record["analyst_id"],
            {
                "score": 0.0,
                "confidence": "Low",
                "high_findings": 0,
                "medium_findings": 0,
                "investigations_analyzed": 0,
                "short_note_rate": 0.0,
                "repeated_note_rate": 0.0,
                "indicators": [],
                "observations": [],
            },
        )

        internal = dict(record)

        internal["average_closure_time_minutes"] = (
            _safe_float(
                performance.get(
                    "average_closure_time_minutes"
                )
            )
        )

        internal["evidence_review_rate"] = (
            _safe_float(
                performance.get(
                    "evidence_review_rate"
                )
            )
        )

        internal["escalation_rate"] = (
            _safe_float(
                performance.get(
                    "escalation_rate"
                )
            )
        )

        internal["false_positive_rate"] = (
            _safe_float(
                performance.get(
                    "false_positive_rate"
                )
            )
        )

        internal["average_queries"] = _safe_float(
            investigations.get("average_queries")
        )

        internal["average_actions"] = _safe_float(
            investigations.get("average_actions")
        )

        internal[
            "average_investigation_duration_minutes"
        ] = _safe_float(
            investigations.get(
                "average_duration_minutes"
            )
        )

        internal["short_note_rate"] = nlp[
            "short_note_rate"
        ]

        internal["repeated_note_rate"] = nlp[
            "repeated_note_rate"
        ]

        internal_records.append(internal)

    population_metrics = calculate_population_metrics(
        internal_records
    )

    population_statistics = prepare_population_statistics(
        population_metrics
    )

    enriched = []

    for record in internal_records:
        analyst_id = record["analyst_id"]
        organization_id = record["organization_id"]

        performance = record["performance"]
        investigations = record["investigations"]

        nlp = investigation_intelligence.get(
            analyst_id,
            {
                "score": 0.0,
                "confidence": "Low",
                "high_findings": 0,
                "medium_findings": 0,
                "investigations_analyzed": 0,
                "short_note_rate": 0.0,
                "repeated_note_rate": 0.0,
                "indicators": [],
                "observations": [],
            },
        )

        total_alerts = int(
            (record.get("alerts") or {}).get(
                "total",
                0,
            )
            or 0
        )

        closed_alerts = int(
            (record.get("alerts") or {}).get(
                "closed",
                0,
            )
            or 0
        )

        # ----------------------------------------------------
        # Behavioral anomaly
        # ----------------------------------------------------

        behavioral = detect_behavioral_anomaly(
            analyst_id=analyst_id,
            analyst_metrics=record,
            population_metrics=population_metrics,
            population_statistics=population_statistics,
            observation_count=total_alerts,
        )

        # ----------------------------------------------------
        # Gaming
        # ----------------------------------------------------

        gaming = detect_gaming_behavior(
            analyst_id=analyst_id,
            total_alerts=total_alerts,
            closed_alerts=closed_alerts,
            average_closure_time_minutes=_safe_float(
                performance.get(
                    "average_closure_time_minutes"
                )
            ),
            evidence_review_rate=_safe_float(
                performance.get(
                    "evidence_review_rate"
                )
            ),
            investigation_evidence_review_rate=_safe_float(
                investigations.get(
                    "evidence_review_rate"
                )
            ),
            total_investigations=int(
                investigations.get("total", 0)
                or 0
            ),
            average_queries=_safe_float(
                investigations.get(
                    "average_queries"
                )
            ),
            average_actions=_safe_float(
                investigations.get(
                    "average_actions"
                )
            ),
            average_investigation_duration_minutes=_safe_float(
                investigations.get(
                    "average_duration_minutes"
                )
            ),
            short_note_rate=nlp[
                "short_note_rate"
            ],
            repeated_note_rate=nlp[
                "repeated_note_rate"
            ],
        )

        # ----------------------------------------------------
        # Peer benchmark
        # ----------------------------------------------------

        peer_metrics = peer_data.get(
            organization_id,
            {},
        )

        peer = calculate_peer_benchmark(
            analyst_id=analyst_id,
            analyst_metrics=record,
            peer_metrics=peer_metrics,
            peer_observations=total_alerts,
        )

        negative_space = negative_space_data.get(analyst_id)

        # ----------------------------------------------------
        # Rule score
        # ----------------------------------------------------

        existing_risk = record.get("risk") or {}

        rule_score = _safe_float(
            existing_risk.get("score")
        )

        rule_indicators = list(
            existing_risk.get("indicators") or []
        )

        # ----------------------------------------------------
        # Risk fusion
        # ----------------------------------------------------

        fused_risk = fuse_analyst_risk(
            analyst_id=analyst_id,
            rule_score=rule_score,

            behavioral_anomaly_score=_safe_float(
                behavioral.score
            ),

            gaming_score=_safe_float(
                gaming.score
            ),

            nlp_score=_safe_float(
                nlp["score"]
            ),

            peer_score=_safe_float(
                peer.score
            ),

            negative_space_score=(
                _safe_float(negative_space["score"])
                if negative_space is not None
                else None
            ),

            observations=total_alerts,

            rule_indicators=rule_indicators,

            behavioral_indicators=list(
                behavioral.indicators or []
            ),

            gaming_indicators=list(
                gaming.indicators or []
            ),

            nlp_indicators=list(
                nlp["indicators"]
            ),

            peer_indicators=list(
                peer.indicators or []
            ),

            negative_space_indicators=(
                list(negative_space["indicators"])
                if negative_space is not None
                else []
            ),
        )

        output = dict(record)

        output["behavioral_anomaly"] = {
            "score": _safe_float(
                behavioral.score
            ),
            "severity": behavioral.severity,
            "confidence": behavioral.confidence,
            "indicators": list(
                behavioral.indicators or []
            ),
            "observations": list(
                behavioral.observations or []
            ),
            "metrics": dict(
                behavioral.metrics or {}
            ),
        }

        output["gaming"] = {
            "score": _safe_float(
                gaming.score
            ),
            "severity": gaming.severity,
            "confidence": gaming.confidence,
            "indicators": list(
                gaming.indicators or []
            ),
            "observations": list(
                gaming.observations or []
            ),
            "metrics": dict(
                gaming.metrics or {}
            ),
        }

        output["investigation_nlp"] = {
            "average_score": _safe_float(
                nlp["score"]
            ),
            "confidence": nlp["confidence"],
            "severity": (
                "HIGH"
                if nlp["score"] >= 70
                else "MEDIUM"
                if nlp["score"] >= 40
                else "LOW"
            ),
            "indicators": list(
                nlp["indicators"]
            ),
            "observations": list(
                nlp["observations"]
            ),
            "short_note_rate": nlp[
                "short_note_rate"
            ],
            "repeated_note_rate": nlp[
                "repeated_note_rate"
            ],
            "high_findings": nlp["high_findings"],
            "medium_findings": nlp["medium_findings"],
            "investigations_analyzed": nlp[
                "investigations_analyzed"
            ],
        }

        output["peer_benchmark"] = {
            "score": _safe_float(
                peer.score
            ),
            "severity": peer.severity,
            "confidence": peer.confidence,
            "indicators": list(
                peer.indicators or []
            ),
            "observations": list(
                peer.observations or []
            ),
            "metrics": dict(
                peer.metrics or {}
            ),
        }

        if negative_space is not None:
            output["negative_space"] = negative_space

        # Canonical final risk.
        output["risk"] = fused_risk

        enriched.append(output)

    return enriched


# ============================================================
# PUBLIC API
# ============================================================

def get_analyst_metrics():
    """
    Complete analyst intelligence pipeline.

    Repo-1 analytics
        +
    Repo-2 behavioral/gaming/NLP/peer intelligence
        +
    risk fusion
    """

    db = SessionLocal()

    try:
        # IMPORTANT:
        # Everything uses ONE database session.
        base_records = _get_base_analyst_metrics(db)

        investigation_intelligence = (
            _build_investigation_intelligence(db)
        )

        peer_data = _build_peer_metrics(db)

        negative_space_data = (
            _build_negative_space_intelligence(db)
        )

        return _enrich_with_intelligence(
            base_records,
            investigation_intelligence,
            peer_data,
            negative_space_data,
        )

    finally:
        db.close()


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    metrics = get_analyst_metrics()

    print("\nSAT-SA ANALYST INTELLIGENCE")
    print("=" * 70)

    print(
        f"Analysts analyzed: {len(metrics)}"
    )

    suspicious = [
        analyst
        for analyst in metrics
        if analyst["risk"]["score"] >= 40
    ]

    print(
        f"Analysts requiring attention: "
        f"{len(suspicious)}"
    )

    print("\nTop suspicious analysts:")

    for analyst in sorted(
        suspicious,
        key=lambda item: item["risk"]["score"],
        reverse=True,
    )[:10]:

        print(
            f"\n{analyst['analyst_id']} - "
            f"{analyst['name']}"
        )

        print(
            f"  Risk: "
            f"{analyst['risk']['score']}/100 "
            f"({analyst['risk']['level']})"
        )

        print(
            f"  Alerts: "
            f"{analyst['alerts']['total']}"
        )

        print(
            f"  Avg closure: "
            f"{analyst['performance']['average_closure_time_minutes']} min"
        )

        print(
            f"  Evidence review: "
            f"{analyst['performance']['evidence_review_rate']}%"
        )

        print(
            f"  Indicators: "
            f"{', '.join(analyst['risk']['indicators'])}"
        )
