from app.services.nlp.investigation_nlp import (
    analyze_investigation_notes,
)

from collections import defaultdict

from sqlalchemy import case, func

from app.database import SessionLocal
from app.models.analyst import Analyst
from app.models.alert import Alert
from app.models.investigation import Investigation
from app.models.peer_benchmark import PeerBenchmark
from app.services.rules.analyst_rules import evaluate_analyst_behavior
from app.services.analytics.investigation_dna import (
    build_investigation_dna,
)
from app.services.gaming.gaming_detection import (
    detect_gaming_behavior,
)
from app.services.peer.peer_benchmark import (
    calculate_peer_benchmark,
)

from app.services.anomaly.behavioral_anomaly import (
    calculate_population_metrics,
    detect_behavioral_anomaly,
)

from app.services.risk.risk_fusion import (
    fuse_analyst_risk,
)

def _percentage(numerator: int, denominator: int) -> float:
    """
    Safely calculate a percentage.

    Example:
        _percentage(5, 10) -> 50.0

    If denominator is zero, return 0 instead of crashing.
    """

    if denominator <= 0:
        return 0.0

    return round(
        (numerator / denominator) * 100,
        2,
    )


def get_analyst_metrics() -> list[dict]:
    """
    Generate intelligence metrics for every analyst.

    The function performs grouped SQL aggregation instead of
    running one database query for every analyst.

    This keeps the analytics layer efficient for large datasets.
    """

    db = SessionLocal()

    try:
        # ==========================================================
        # 1. Load analysts
        # ==========================================================

        analysts = (
            db.query(Analyst)
            .order_by(Analyst.analyst_id)
            .all()
        )

        # ==========================================================
        # 2. Aggregate alert metrics
        # ==========================================================

        alert_rows = (
            db.query(
                Alert.analyst_id.label("analyst_id"),

                func.count(
                    Alert.alert_id
                ).label("total_alerts"),

                func.sum(
                    case(
                        (Alert.status == "Closed", 1),
                        else_=0,
                    )
                ).label("closed_alerts"),

                func.sum(
                    case(
                        (Alert.status == "Open", 1),
                        else_=0,
                    )
                ).label("open_alerts"),

                func.sum(
                    case(
                        (Alert.status == "Investigating", 1),
                        else_=0,
                    )
                ).label("investigating_alerts"),

                func.sum(
                    case(
                        (Alert.status == "Escalated", 1),
                        else_=0,
                    )
                ).label("escalated_status_alerts"),

                func.sum(
                    case(
                        (Alert.escalated.is_(True), 1),
                        else_=0,
                    )
                ).label("escalated_flagged_alerts"),

                func.sum(
                    case(
                        (Alert.false_positive.is_(True), 1),
                        else_=0,
                    )
                ).label("false_positives"),

                func.sum(
                    case(
                        (Alert.evidence_reviewed.is_(True), 1),
                        else_=0,
                    )
                ).label("evidence_reviewed_alerts"),

                func.avg(
                    Alert.closure_time_minutes
                ).label("avg_closure_time"),

                func.min(
                    Alert.closure_time_minutes
                ).label("min_closure_time"),

                func.max(
                    Alert.closure_time_minutes
                ).label("max_closure_time"),
            )
            .filter(
                Alert.analyst_id.isnot(None)
            )
            .group_by(
                Alert.analyst_id
            )
            .all()
        )

        alert_metrics = {}

        for row in alert_rows:

            alert_metrics[row.analyst_id] = {
                "total_alerts": int(
                    row.total_alerts or 0
                ),

                "closed_alerts": int(
                    row.closed_alerts or 0
                ),

                "open_alerts": int(
                    row.open_alerts or 0
                ),

                "investigating_alerts": int(
                    row.investigating_alerts or 0
                ),

                "escalated_status_alerts": int(
                    row.escalated_status_alerts or 0
                ),

                "escalated_flagged_alerts": int(
                    row.escalated_flagged_alerts or 0
                ),

                "false_positives": int(
                    row.false_positives or 0
                ),

                "evidence_reviewed_alerts": int(
                    row.evidence_reviewed_alerts or 0
                ),

                "avg_closure_time": (
                    float(row.avg_closure_time)
                    if row.avg_closure_time is not None
                    else None
                ),

                "min_closure_time": (
                    float(row.min_closure_time)
                    if row.min_closure_time is not None
                    else None
                ),

                "max_closure_time": (
                    float(row.max_closure_time)
                    if row.max_closure_time is not None
                    else None
                ),
            }

        # ==========================================================
        # 3. Aggregate investigation metrics
        # ==========================================================

        investigation_rows = (
            db.query(
                Investigation.analyst_id.label(
                    "analyst_id"
                ),

                func.count(
                    Investigation.investigation_id
                ).label(
                    "total_investigations"
                ),

                func.avg(
                    Investigation.duration_minutes
                ).label(
                    "avg_investigation_time"
                ),

                func.min(
                    Investigation.duration_minutes
                ).label(
                    "min_investigation_time"
                ),

                func.max(
                    Investigation.duration_minutes
                ).label(
                    "max_investigation_time"
                ),

                func.sum(
                    case(
                        (
                            Investigation.evidence_reviewed.is_(True),
                            1,
                        ),
                        else_=0,
                    )
                ).label(
                    "evidence_reviewed_investigations"
                ),

                # IMPORTANT:
                # escalation_decision is BOOLEAN.
                # Therefore we check for True.
                func.sum(
                    case(
                        (
                            Investigation.escalation_decision.is_(True),
                            1,
                        ),
                        else_=0,
                    )
                ).label(
                    "escalated_investigations"
                ),
            )
            .group_by(
                Investigation.analyst_id
            )
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

                "min_investigation_time": (
                    float(row.min_investigation_time)
                    if row.min_investigation_time is not None
                    else None
                ),

                "max_investigation_time": (
                    float(row.max_investigation_time)
                    if row.max_investigation_time is not None
                    else None
                ),

                "evidence_reviewed_investigations": int(
                    row.evidence_reviewed_investigations or 0
                ),

                "escalated_investigations": int(
                    row.escalated_investigations or 0
                ),
            }

        # ==========================================================
        # 4. Aggregate investigation activity
        # ==========================================================

        investigation_activity = (
            db.query(
                Investigation.investigation_id,
                Investigation.analyst_id,
                Investigation.actions_performed,
                Investigation.queries_executed,
                Investigation.investigation_notes,
                Investigation.evidence_reviewed,
            )
            .all()

            
        )

        # ==========================================================
        # Investigation NLP analysis
        # ==========================================================

        investigation_nlp_records = []

        for investigation in investigation_activity:

            investigation_nlp_records.append(
                {
                    "investigation_id": (
                        investigation.investigation_id
                    ),
                    "investigation_notes": (
                        investigation.investigation_notes
                    ),
                    "evidence_reviewed": (
                        investigation.evidence_reviewed
                    ),
                }
            )

        investigation_nlp_results = (
            analyze_investigation_notes(
                investigation_nlp_records
            )
        )

        # ==========================================================
        # Aggregate investigation NLP by analyst
        # ==========================================================

        investigation_nlp_by_analyst = defaultdict(
            list
        )

        for (
            investigation,
            nlp_result,
        ) in zip(
            investigation_activity,
            investigation_nlp_results,
        ):

            investigation_nlp_by_analyst[
                investigation.analyst_id
            ].append(
                nlp_result
            )

        action_totals = defaultdict(int)
        query_totals = defaultdict(int)

        # Number of investigations observed.
        activity_investigation_counts = defaultdict(int)

        # Investigation note analytics.
        note_records = defaultdict(int)

        short_note_records = defaultdict(int)

        note_frequency = defaultdict(
        lambda: defaultdict(int)
)

        for investigation in investigation_activity:

            analyst_id = investigation.analyst_id

            activity_investigation_counts[
                analyst_id
            ] += 1

            # ------------------------------------------------------
            # Actions
            # ------------------------------------------------------

            if investigation.actions_performed:

                actions = [
                    action.strip()
                    for action in str(
                        investigation.actions_performed
                    ).split(";")
                    if action.strip()
                ]

                action_totals[analyst_id] += len(
                    actions
                )

            # ------------------------------------------------------
            # Queries
            # ------------------------------------------------------

            if investigation.queries_executed is not None:

                try:
                    query_value = int(
                        investigation.queries_executed
                    )

                    # Protect against invalid negative data.
                    query_value = max(
                        query_value,
                        0,
                    )

                    query_totals[analyst_id] += (
                        query_value
                    )

                except (
                    TypeError,
                    ValueError,
                ):
                    pass

            # ------------------------------------------------------
            # Investigation notes
            # ------------------------------------------------------

            note = investigation.investigation_notes

            if note is not None:

                normalized_note = " ".join(
                    str(note)
                    .lower()
                    .split()
                )

                if normalized_note:

                    # Count every usable investigation note.
                    note_records[
                        analyst_id
                    ] += 1

                    # Treat notes shorter than 30 characters
                    # as short notes.
                    if len(normalized_note) < 30:

                        short_note_records[
                            analyst_id
                        ] += 1

                    # Count identical normalized notes.
                    note_frequency[
                        analyst_id
                    ][
                        normalized_note
                    ] += 1

        # ==========================================================
        # 5. Load peer benchmark baselines
        # ==========================================================

        peer_rows = (
            db.query(PeerBenchmark)
            .order_by(
                PeerBenchmark.organization_id,
                PeerBenchmark.metric_name,
                PeerBenchmark.calculated_at.desc().nullslast(),
                PeerBenchmark.benchmark_id.desc(),
            )
            .all()
        )

        peer_benchmarks = {}

        for row in peer_rows:

            organization_id = row.organization_id
            metric_name = row.metric_name

            organization_metrics = peer_benchmarks.setdefault(
                organization_id,
                {},
            )

            # Keep the first row for each organization + metric.
            # The query is ordered by calculated_at descending,
            # so the newest benchmark baseline is preferred.
            if metric_name in organization_metrics:
                continue

            organization_metrics[metric_name] = {
                "peer_mean": (
                    float(row.peer_mean)
                    if row.peer_mean is not None
                    else None
                ),
                "peer_stddev": (
                    float(row.peer_stddev)
                    if row.peer_stddev is not None
                    else None
                ),
                "benchmark_period": row.benchmark_period,
                "calculated_at": (
                    row.calculated_at.isoformat()
                    if row.calculated_at is not None
                    else None
                ),
            }

        # ==========================================================
        # 5. Build final analyst metrics
        # ==========================================================

        results = []

        for analyst in analysts:

            analyst_id = analyst.analyst_id

            # ------------------------------------------------------
            # Investigation NLP summary
            # ------------------------------------------------------

            analyst_nlp_findings = (
                investigation_nlp_by_analyst.get(
                    analyst_id,
                    [],
                )
            )

            if analyst_nlp_findings:

                nlp_scores = [
                    finding["score"]
                    for finding in analyst_nlp_findings
                ]

                average_nlp_score = round(
                    sum(nlp_scores)
                    / len(nlp_scores),
                    2,
                )

                high_nlp_findings = sum(
                    1
                    for finding in analyst_nlp_findings
                    if finding["severity"] == "HIGH"
                )

                medium_nlp_findings = sum(
                    1
                    for finding in analyst_nlp_findings
                    if finding["severity"] == "MEDIUM"
                )

                nlp_indicators = []

                for finding in analyst_nlp_findings:

                    for indicator in finding[
                        "indicators"
                    ]:

                        if indicator not in nlp_indicators:
                            nlp_indicators.append(
                                indicator
                            )

            else:

                average_nlp_score = 0.0
                high_nlp_findings = 0
                medium_nlp_findings = 0
                nlp_indicators = []

            # ------------------------------------------------------
            # Alert defaults
            # ------------------------------------------------------

            alerts = alert_metrics.get(
                analyst_id,
                {
                    "total_alerts": 0,
                    "closed_alerts": 0,
                    "open_alerts": 0,
                    "investigating_alerts": 0,
                    "escalated_status_alerts": 0,
                    "escalated_flagged_alerts": 0,
                    "false_positives": 0,
                    "evidence_reviewed_alerts": 0,
                    "avg_closure_time": None,
                    "min_closure_time": None,
                    "max_closure_time": None,
                },
            )

            total_alerts = alerts[
                "total_alerts"
            ]

            closed_alerts = alerts[
                "closed_alerts"
            ]

            open_alerts = alerts[
                "open_alerts"
            ]

            investigating_alerts = alerts[
                "investigating_alerts"
            ]

            escalated_alerts = alerts[
                "escalated_flagged_alerts"
            ]

            false_positives = alerts[
                "false_positives"
            ]

            evidence_reviewed_alerts = alerts[
                "evidence_reviewed_alerts"
            ]

            avg_closure_time = alerts[
                "avg_closure_time"
            ]

            min_closure_time = alerts[
                "min_closure_time"
            ]

            max_closure_time = alerts[
                "max_closure_time"
            ]

            # ------------------------------------------------------
            # Investigation defaults
            # ------------------------------------------------------

            investigations = investigation_metrics.get(
                analyst_id,
                {
                    "total_investigations": 0,
                    "avg_investigation_time": None,
                    "min_investigation_time": None,
                    "max_investigation_time": None,
                    "evidence_reviewed_investigations": 0,
                    "escalated_investigations": 0,
                },
            )

            total_investigations = investigations[
                "total_investigations"
            ]

            avg_investigation_time = investigations[
                "avg_investigation_time"
            ]

            min_investigation_time = investigations[
                "min_investigation_time"
            ]

            max_investigation_time = investigations[
                "max_investigation_time"
            ]

            evidence_reviewed_investigations = investigations[
                "evidence_reviewed_investigations"
            ]

            escalated_investigations = investigations[
                "escalated_investigations"
            ]

            # ------------------------------------------------------
            # Average actions
            # ------------------------------------------------------

            if total_investigations > 0:

                avg_actions = (
                    action_totals[analyst_id]
                    / total_investigations
                )

                avg_queries = (
                    query_totals[analyst_id]
                    / total_investigations
                )

            else:

                avg_actions = 0.0
                avg_queries = 0.0
            # ------------------------------------------------------
            # Investigation note quality
            # ------------------------------------------------------

            total_notes = note_records[
                analyst_id
            ]

            short_notes = short_note_records[
                analyst_id
            ]

            # ------------------------------------------------------
            # Short note rate
            # ------------------------------------------------------

            if total_notes > 0:

                short_note_rate = round(
                    (
                        short_notes
                        / total_notes
                    ) * 100,
                    2,
                )

            else:

                short_note_rate = 0.0

            # ------------------------------------------------------
            # Repeated note rate
            # ------------------------------------------------------

            repeated_notes = 0

            for (
                note,
                count,
            ) in note_frequency[
                analyst_id
            ].items():

                if count > 1:

                    # If a note occurs 3 times,
                    # we count 2 as repetitions.
                    repeated_notes += (
                        count - 1
                    )

            if total_notes > 0:

                repeated_note_rate = round(
                    (
                        repeated_notes
                        / total_notes
                    ) * 100,
                    2,
                )

            else:

                repeated_note_rate = 0.0
                
            # ======================================================
            # 6. Alert rates
            # ======================================================

            closure_rate = _percentage(
                closed_alerts,
                total_alerts,
            )

            escalation_rate = _percentage(
                escalated_alerts,
                total_alerts,
            )

            false_positive_rate = _percentage(
                false_positives,
                total_alerts,
            )

            evidence_review_rate = _percentage(
                evidence_reviewed_alerts,
                total_alerts,
            )

            # ======================================================
            # 7. Investigation rates
            # ======================================================

            investigation_evidence_rate = _percentage(
                evidence_reviewed_investigations,
                total_investigations,
            )

            investigation_escalation_rate = _percentage(
                escalated_investigations,
                total_investigations,
            )

            # ======================================================
            # 8. Investigation coverage
            # ======================================================

            investigation_coverage_rate = _percentage(
                min(
                    total_investigations,
                    total_alerts,
                ),
                total_alerts,
            )

            # ======================================================
            # Peer Benchmark
            # ======================================================

            organization_peer_data = peer_benchmarks.get(
                analyst.organization_id,
                {},
            )

            # These are the metrics calculated specifically for
            # this analyst.
            #
            # Percentage-based peer benchmark values are stored
            # as decimal ratios in the database (for example,
            # 0.76 means 76%). Convert our percentage metrics
            # to the same representation before comparison.
            analyst_peer_metrics = {
                "average_closure_time_minutes": (
                    avg_closure_time
                ),
                "evidence_review_rate": (
                    evidence_review_rate / 100.0
                ),
                "escalation_rate": (
                    escalation_rate / 100.0
                ),
                "false_positive_rate": (
                    false_positive_rate / 100.0
                ),
                "average_investigation_duration_minutes": (
                    avg_investigation_time
                ),
            }

            # These names match the metric_name values currently
            # present in the peer_benchmarks table.
            peer_metric_mapping = {
                "average_closure_time_minutes":
                    "avg_closure_time",
                "evidence_review_rate":
                    "evidence_review_rate",
                "escalation_rate":
                    "escalation_rate",
                "false_positive_rate":
                    "false_positive_rate",
                "average_investigation_duration_minutes":
                    "mean_investigation_duration",
            }

            peer_metrics = {}
            peer_observations = 0

            for (
                analyst_metric,
                benchmark_metric,
            ) in peer_metric_mapping.items():

                benchmark = organization_peer_data.get(
                    benchmark_metric
                )

                if not benchmark:
                    continue

                peer_mean = benchmark.get("peer_mean")

                if peer_mean is None:
                    continue

                analyst_value = analyst_peer_metrics.get(
                    analyst_metric
                )

                if analyst_value is None:
                    continue

                peer_metrics[analyst_metric] = peer_mean
                peer_observations += 1

            peer = calculate_peer_benchmark(
                analyst_id=analyst_id,
                analyst_metrics=analyst_peer_metrics,
                peer_metrics=peer_metrics,
                peer_observations=peer_observations,
            )

            # ======================================================
            # Investigation DNA
            # ======================================================

            dna_features = {
                "analyst_id": analyst_id,

                "total_alerts": total_alerts,

                "closed_alerts": closed_alerts,

                "average_closure_time_minutes": (
                    avg_closure_time
                ),

                "evidence_review_rate": (
                    evidence_review_rate
                ),

                "investigation_evidence_review_rate": (
                    investigation_evidence_rate
                ),

                "escalation_rate": (
                    escalation_rate
                ),

                "investigation_escalation_rate": (
                    investigation_escalation_rate
                ),

                "total_investigations": (
                    total_investigations
                ),

                "average_queries": (
                    avg_queries
                ),

                "average_actions": (
                    avg_actions
                ),

                "average_investigation_duration_minutes": (
                    avg_investigation_time
                ),

                "short_note_rate": (
                    short_note_rate
                ),

                "repeated_note_rate": (
                    repeated_note_rate
                ),
            }

            dna = build_investigation_dna(
                dna_features
            )

            # ======================================================
            # Gaming Detection
            # ======================================================

            gaming = detect_gaming_behavior(
                analyst_id=analyst_id,
                total_alerts=total_alerts,
                closed_alerts=closed_alerts,
                average_closure_time_minutes=avg_closure_time,
                evidence_review_rate=evidence_review_rate,
                investigation_evidence_review_rate=investigation_evidence_rate,
                total_investigations=total_investigations,
                average_queries=avg_queries,
                average_actions=avg_actions,
                average_investigation_duration_minutes=avg_investigation_time,
                short_note_rate=short_note_rate,
                repeated_note_rate=repeated_note_rate,
            )

            # ======================================================
            # 9. Existing deterministic analyst rule score
            # ======================================================

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

            # ======================================================
            # 10. Data confidence
            # ======================================================

            observations = (
                total_alerts
                + total_investigations
            )

            if observations >= 10:
                data_confidence = "High"

            elif observations >= 3:
                data_confidence = "Medium"

            else:
                data_confidence = "Low"

            # ======================================================
            # 11. Final result
            # ======================================================

            results.append(
                {
                    "analyst_id": analyst.analyst_id,
                    "name": analyst.name,
                    "organization_id": analyst.organization_id,
                    "role": analyst.role,
                    "team": analyst.team,
                    "experience_years": analyst.experience_years,
                    "shift": analyst.shift,
                    "status": analyst.status,

                    "confidence": risk["confidence"],

                    "data_quality": {
                        "observations": observations,
                        "data_confidence": data_confidence,
                    },

                    "alerts": {
                        "total": total_alerts,
                        "closed": closed_alerts,
                        "open": open_alerts,
                        "investigating": investigating_alerts,
                        "escalated": escalated_alerts,
                        "false_positives": false_positives,
                    },

                    "performance": {
                        "average_closure_time_minutes": (
                            round(
                                avg_closure_time,
                                2,
                            )
                            if avg_closure_time is not None
                            else 0.0
                        ),

                        "minimum_closure_time_minutes": (
                            round(
                                min_closure_time,
                                2,
                            )
                            if min_closure_time is not None
                            else 0.0
                        ),

                        "maximum_closure_time_minutes": (
                            round(
                                max_closure_time,
                                2,
                            )
                            if max_closure_time is not None
                            else 0.0
                        ),

                        "closure_rate": closure_rate,

                        "escalation_rate": escalation_rate,

                        "false_positive_rate": false_positive_rate,

                        "evidence_review_rate": evidence_review_rate,
                    },

                    "investigations": {
                        "total": total_investigations,

                        "coverage_rate": (
                            investigation_coverage_rate
                        ),

                        "average_duration_minutes": (
                            round(
                                avg_investigation_time,
                                2,
                            )
                            if avg_investigation_time is not None
                            else 0.0
                        ),

                        "minimum_duration_minutes": (
                            round(
                                min_investigation_time,
                                2,
                            )
                            if min_investigation_time is not None
                            else 0.0
                        ),

                        "maximum_duration_minutes": (
                            round(
                                max_investigation_time,
                                2,
                            )
                            if max_investigation_time is not None
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
                    # ======================================================
                    # Investigation DNA
                    # ======================================================
                    "investigation_dna": {
                        "evidence_discipline_score": (
                            dna.evidence_discipline_score
                        ),

                        "investigation_depth_score": (
                            dna.investigation_depth_score
                        ),

                        "escalation_discipline_score": (
                            dna.escalation_discipline_score
                        ),

                        "closure_behavior_score": (
                            dna.closure_behavior_score
                        ),

                        "note_quality_score": (
                            dna.note_quality_score
                        ),

                        "investigation_quality_score": (
                            dna.investigation_quality_score
                        ),

                        "confidence": dna.confidence,

                        "observations": dna.observations,

                        "indicators": dna.indicators,

                        "metrics": dna.metrics,
                    },

                    "peer_benchmark": {
                        "score": peer.score,
                        "severity": peer.severity,
                        "confidence": peer.confidence,
                        "indicators": peer.indicators,
                        "observations": peer.observations,
                        "metrics": peer.metrics,
                    },

                    "gaming": {
                        "score": gaming.score,
                        "severity": gaming.severity,
                        "confidence": gaming.confidence,
                        "indicators": gaming.indicators,
                        "observations": gaming.observations,
                        "metrics": gaming.metrics,
                    },

                    # ======================================================
                    # Investigation NLP
                    # ======================================================
                    "investigation_nlp": {
                        "average_score": (
                            average_nlp_score
                        ),
                        "high_findings": (
                            high_nlp_findings
                        ),
                        "medium_findings": (
                            medium_nlp_findings
                        ),
                        "indicators": (
                            nlp_indicators
                        ),
                        "investigations_analyzed": (
                            len(
                                analyst_nlp_findings
                            )
                        ),
                    },

                    # Keep the existing risk block because
                    # other parts of the project may already
                    # expect it.
                    "risk": {
                        "score": risk["score"],

                        "level": risk["level"],

                        "severity": risk.get(
                            "severity",
                            "LOW",
                        ),

                        "confidence": risk.get(
                            "confidence",
                            "Low",
                        ),

                        "indicators": risk.get(
                            "indicators",
                            [],
                        ),

                        "triggered_rules": risk.get(
                            "triggered_rules",
                            [],
                        ),

                        "signals": risk.get(
                            "signals",
                            [],
                        ),
                    },
                }
            )


        # ==========================================================
        # Behavioral Anomaly Detection
        # ==========================================================
        #
        # Run this after all analyst metrics have been calculated
        # so every analyst can be compared against the complete
        # observed analyst population.

        population_metrics = calculate_population_metrics(
            results
        )

        for analyst_result in results:

            anomaly = detect_behavioral_anomaly(
                analyst_id=analyst_result["analyst_id"],
                analyst_metrics=analyst_result,
                population_metrics=population_metrics,
                observation_count=(
                    analyst_result["data_quality"]["observations"]
                ),
            )

            analyst_result["behavioral_anomaly"] = {
                "score": anomaly.score,
                "severity": anomaly.severity,
                "confidence": anomaly.confidence,
                "indicators": anomaly.indicators,
                "observations": anomaly.observations,
                "metrics": anomaly.metrics,
            }


                # ==============================================================
        # 12. Final Supervisory Risk Fusion
        # ==============================================================

        for analyst_result in results:

            rule_block = analyst_result.get(
                "risk",
                {},
            )

            dna_block = analyst_result.get(
                "investigation_dna",
                {},
            )

            gaming_block = analyst_result.get(
                "gaming",
                {},
            )

            nlp_block = analyst_result.get(
                "investigation_nlp",
                {},
            )

            peer_block = analyst_result.get(
                "peer_benchmark",
                {},
            )

            anomaly_block = analyst_result.get(
                "behavioral_anomaly",
                {},
            )

            # ----------------------------------------------------------
            # Existing deterministic rule risk
            # ----------------------------------------------------------

            rule_score = float(
                rule_block.get(
                    "score",
                    0,
                ) or 0
            )

            rule_indicators = rule_block.get(
                "indicators",
                [],
            )

            # ----------------------------------------------------------
            # Behavioral anomaly
            # ----------------------------------------------------------

            behavioral_score = float(
                anomaly_block.get(
                    "score",
                    0,
                ) or 0
            )

            behavioral_indicators = (
                anomaly_block.get(
                    "indicators",
                    [],
                )
            )

            # ----------------------------------------------------------
            # Gaming
            # ----------------------------------------------------------

            gaming_score = float(
                gaming_block.get(
                    "score",
                    0,
                ) or 0
            )

            gaming_indicators = (
                gaming_block.get(
                    "indicators",
                    [],
                )
            )

            # ----------------------------------------------------------
            # NLP
            #
            # NLP average_score is already a concern score:
            # higher = more concerning.
            # ----------------------------------------------------------

            nlp_score = float(
                nlp_block.get(
                    "average_score",
                    0,
                ) or 0
            )

            nlp_indicators = (
                nlp_block.get(
                    "indicators",
                    [],
                )
            )

            # ----------------------------------------------------------
            # Investigation DNA
            #
            # DNA is a quality score:
            # higher = better.
            #
            # Risk fusion inverts this internally.
            # ----------------------------------------------------------

            dna_quality = dna_block.get(
                "investigation_quality_score"
            )

            # ----------------------------------------------------------
            # Peer benchmark
            # ----------------------------------------------------------

            peer_score = peer_block.get(
                "score"
            )

            if peer_score is not None:
                peer_score = float(
                    peer_score
                )

            peer_indicators = (
                peer_block.get(
                    "indicators",
                    [],
                )
            )

            # ----------------------------------------------------------
            # Negative Space
            #
            # If Negative Space has already been attached to the
            # analyst result, use it.
            #
            # If it is not available yet, the fusion engine
            # renormalizes the available components rather than
            # falsely treating missing data as zero risk.
            # ----------------------------------------------------------

            negative_space_block = (
                analyst_result.get(
                    "negative_space",
                    {},
                )
            )

            negative_space_score = (
                negative_space_block.get(
                    "score"
                )
                if negative_space_block
                else None
            )

            if negative_space_score is not None:
                negative_space_score = float(
                    negative_space_score
                )

            negative_space_indicators = (
                negative_space_block.get(
                    "indicators",
                    [],
                )
            )

            # ----------------------------------------------------------
            # Component confidence
            # ----------------------------------------------------------

            component_confidences = []

            for block in (
                anomaly_block,
                gaming_block,
                peer_block,
            ):
                confidence = block.get(
                    "confidence"
                )

                if confidence:
                    component_confidences.append(
                        str(confidence)
                    )

            dna_confidence = dna_block.get(
                "confidence"
            )

            if dna_confidence:
                component_confidences.append(
                    str(dna_confidence)
                )

            # ----------------------------------------------------------
            # Observations
            # ----------------------------------------------------------

            observations = (
                analyst_result
                .get(
                    "data_quality",
                    {},
                )
                .get(
                    "observations",
                    0,
                )
            )

            # ----------------------------------------------------------
            # Fusion
            # ----------------------------------------------------------

            fused_risk = fuse_analyst_risk(
                analyst_id=(
                    analyst_result[
                        "analyst_id"
                    ]
                ),
                rule_score=rule_score,
                behavioral_anomaly_score=(
                    behavioral_score
                ),
                gaming_score=gaming_score,
                nlp_score=nlp_score,
                investigation_dna_quality=(
                    dna_quality
                ),
                negative_space_score=(
                    negative_space_score
                ),
                peer_score=peer_score,
                observations=observations,
                component_confidences=(
                    component_confidences
                ),
                rule_indicators=(
                    rule_indicators
                ),
                behavioral_indicators=(
                    behavioral_indicators
                ),
                gaming_indicators=(
                    gaming_indicators
                ),
                nlp_indicators=(
                    nlp_indicators
                ),
                negative_space_indicators=(
                    negative_space_indicators
                ),
                peer_indicators=(
                    peer_indicators
                ),
            )

            # ----------------------------------------------------------
            # Replace risk with fused supervisory risk
            # ----------------------------------------------------------

            analyst_result["risk"] = fused_risk
        

        return results

    finally:
        db.close()


# ==============================================================
# CLI
# ==============================================================

if __name__ == "__main__":

    metrics = get_analyst_metrics()

    print()
    print("SAT-SA ANALYST INTELLIGENCE")
    print("=" * 70)

    print(
        f"Analysts analyzed: {len(metrics):,}"
    )

    suspicious = [
        analyst
        for analyst in metrics
        if analyst["risk"]["score"] >= 40
    ]

    print(
        f"Analysts requiring attention: "
        f"{len(suspicious):,}"
    )

    print()
    print("Top suspicious analysts:")
    print("-" * 70)

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
            f"  Investigations: "
            f"{analyst['investigations']['total']}"
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
            f"  Gaming score: "
            f"{analyst['gaming']['score']}/100 "
            f"({analyst['gaming']['severity']})"
        )

        print(
            f"  Indicators: "
            f"{', '.join(analyst['risk']['indicators'])}"
        )