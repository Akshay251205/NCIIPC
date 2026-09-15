from sqlalchemy import case, func

from app.database import SessionLocal
from app.models.alert import Alert
from app.models.investigation import Investigation


def _percentage(
    numerator: int,
    denominator: int,
) -> float:
    """
    Safely calculate a percentage.
    """

    if denominator <= 0:
        return 0.0

    return round(
        (numerator / denominator) * 100,
        2,
    )


def get_alert_metrics() -> dict:
    """
    Generate SOC-wide alert and investigation metrics.

    This function is intentionally organization-wide.

    Later, the risk engine can use the same underlying
    concepts at analyst, organization and asset level.
    """

    db = SessionLocal()

    try:

        # ==========================================================
        # 1. Aggregate alert metrics in ONE query
        # ==========================================================

        alert_summary = (
            db.query(
                func.count(
                    Alert.alert_id
                ).label("total_alerts"),

                # Severity
                func.sum(
                    case(
                        (Alert.severity == "Critical", 1),
                        else_=0,
                    )
                ).label("critical_alerts"),

                func.sum(
                    case(
                        (Alert.severity == "High", 1),
                        else_=0,
                    )
                ).label("high_alerts"),

                func.sum(
                    case(
                        (Alert.severity == "Medium", 1),
                        else_=0,
                    )
                ).label("medium_alerts"),

                func.sum(
                    case(
                        (Alert.severity == "Low", 1),
                        else_=0,
                    )
                ).label("low_alerts"),

                # Status
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
                        (Alert.status == "Closed", 1),
                        else_=0,
                    )
                ).label("closed_alerts"),

                # Quality
                func.sum(
                    case(
                        (Alert.evidence_reviewed.is_(True), 1),
                        else_=0,
                    )
                ).label("evidence_reviewed"),

                func.sum(
                    case(
                        (Alert.escalated.is_(True), 1),
                        else_=0,
                    )
                ).label("escalated_flagged"),

                func.sum(
                    case(
                        (Alert.false_positive.is_(True), 1),
                        else_=0,
                    )
                ).label("false_positives"),

                # Closure time
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
            .one()
        )

        total_alerts = int(
            alert_summary.total_alerts or 0
        )

        critical_alerts = int(
            alert_summary.critical_alerts or 0
        )

        high_alerts = int(
            alert_summary.high_alerts or 0
        )

        medium_alerts = int(
            alert_summary.medium_alerts or 0
        )

        low_alerts = int(
            alert_summary.low_alerts or 0
        )

        open_alerts = int(
            alert_summary.open_alerts or 0
        )

        investigating_alerts = int(
            alert_summary.investigating_alerts or 0
        )

        escalated_status_alerts = int(
            alert_summary.escalated_status_alerts or 0
        )

        closed_alerts = int(
            alert_summary.closed_alerts or 0
        )

        evidence_reviewed = int(
            alert_summary.evidence_reviewed or 0
        )

        escalated_flagged = int(
            alert_summary.escalated_flagged or 0
        )

        false_positives = int(
            alert_summary.false_positives or 0
        )

        # ==========================================================
        # 2. Investigation metrics
        # ==========================================================

        investigation_summary = (
            db.query(
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
            .one()
        )

        total_investigations = int(
            investigation_summary.total_investigations
            or 0
        )

        avg_investigation_time = (
            float(
                investigation_summary.avg_investigation_time
            )
            if investigation_summary.avg_investigation_time
            is not None
            else 0.0
        )

        evidence_reviewed_investigations = int(
            investigation_summary
            .evidence_reviewed_investigations
            or 0
        )

        escalated_investigations = int(
            investigation_summary
            .escalated_investigations
            or 0
        )

        # ==========================================================
        # 3. Rates
        # ==========================================================

        evidence_review_rate = _percentage(
            evidence_reviewed,
            total_alerts,
        )

        escalation_rate = _percentage(
            escalated_flagged,
            total_alerts,
        )

        false_positive_rate = _percentage(
            false_positives,
            total_alerts,
        )

        closure_rate = _percentage(
            closed_alerts,
            total_alerts,
        )

        investigation_evidence_rate = _percentage(
            evidence_reviewed_investigations,
            total_investigations,
        )

        investigation_escalation_rate = _percentage(
            escalated_investigations,
            total_investigations,
        )

        investigation_coverage_rate = _percentage(
            min(
                total_investigations,
                total_alerts,
            ),
            total_alerts,
        )

        # ==========================================================
        # 4. Return structured analytics
        # ==========================================================

        return {
            "total_alerts": total_alerts,

            "severity": {
                "critical": critical_alerts,
                "high": high_alerts,
                "medium": medium_alerts,
                "low": low_alerts,
            },

            "status": {
                "open": open_alerts,
                "investigating": investigating_alerts,
                "escalated": escalated_status_alerts,
                "closed": closed_alerts,
            },

            "quality": {
                "evidence_reviewed": evidence_reviewed,
                "false_positives": false_positives,
                "escalated": escalated_flagged,
            },

            "rates": {
                "evidence_review_rate": evidence_review_rate,
                "false_positive_rate": false_positive_rate,
                "escalation_rate": escalation_rate,
                "closure_rate": closure_rate,
            },

            "performance": {
                "average_closure_time_minutes": round(
                    float(
                        alert_summary.avg_closure_time
                    ),
                    2,
                )
                if alert_summary.avg_closure_time is not None
                else 0.0,

                "minimum_closure_time_minutes": round(
                    float(
                        alert_summary.min_closure_time
                    ),
                    2,
                )
                if alert_summary.min_closure_time is not None
                else 0.0,

                "maximum_closure_time_minutes": round(
                    float(
                        alert_summary.max_closure_time
                    ),
                    2,
                )
                if alert_summary.max_closure_time is not None
                else 0.0,

                "average_investigation_time_minutes": round(
                    avg_investigation_time,
                    2,
                ),
            },

            "investigations": {
                "total": total_investigations,

                "coverage_rate": (
                    investigation_coverage_rate
                ),

                "evidence_review_rate": (
                    investigation_evidence_rate
                ),

                "escalation_rate": (
                    investigation_escalation_rate
                ),
            },
        }

    except Exception as exc:

        raise RuntimeError(
            f"Failed to calculate alert metrics: {exc}"
        ) from exc

    finally:

        db.close()


if __name__ == "__main__":

    metrics = get_alert_metrics()

    print()
    print("SAT-SA ALERT INTELLIGENCE")
    print("=" * 70)

    print(
        f"Total alerts: "
        f"{metrics['total_alerts']:,}"
    )

    print()
    print("SEVERITY")
    print("-" * 70)

    print(
        f"Critical: "
        f"{metrics['severity']['critical']:,}"
    )

    print(
        f"High:     "
        f"{metrics['severity']['high']:,}"
    )

    print(
        f"Medium:   "
        f"{metrics['severity']['medium']:,}"
    )

    print(
        f"Low:      "
        f"{metrics['severity']['low']:,}"
    )

    print()
    print("STATUS")
    print("-" * 70)

    print(
        f"Open:          "
        f"{metrics['status']['open']:,}"
    )

    print(
        f"Investigating: "
        f"{metrics['status']['investigating']:,}"
    )

    print(
        f"Escalated:     "
        f"{metrics['status']['escalated']:,}"
    )

    print(
        f"Closed:        "
        f"{metrics['status']['closed']:,}"
    )

    print()
    print("QUALITY")
    print("-" * 70)

    print(
        f"Evidence reviewed: "
        f"{metrics['quality']['evidence_reviewed']:,}"
    )

    print(
        f"False positives:   "
        f"{metrics['quality']['false_positives']:,}"
    )

    print(
        f"Escalated:         "
        f"{metrics['quality']['escalated']:,}"
    )

    print()
    print("RATES")
    print("-" * 70)

    print(
        f"Evidence review: "
        f"{metrics['rates']['evidence_review_rate']}%"
    )

    print(
        f"False positive:  "
        f"{metrics['rates']['false_positive_rate']}%"
    )

    print(
        f"Escalation:      "
        f"{metrics['rates']['escalation_rate']}%"
    )

    print(
        f"Closure:         "
        f"{metrics['rates']['closure_rate']}%"
    )

    print()
    print("INVESTIGATIONS")
    print("-" * 70)

    print(
        f"Total: "
        f"{metrics['investigations']['total']:,}"
    )

    print(
        f"Coverage: "
        f"{metrics['investigations']['coverage_rate']}%"
    )

    print(
        f"Evidence review: "
        f"{metrics['investigations']['evidence_review_rate']}%"
    )

    print(
        f"Escalation: "
        f"{metrics['investigations']['escalation_rate']}%"
    )

    print()
    print("PERFORMANCE")
    print("-" * 70)

    print(
        f"Average closure time: "
        f"{metrics['performance']['average_closure_time_minutes']} min"
    )

    print(
        f"Average investigation time: "
        f"{metrics['performance']['average_investigation_time_minutes']} min"
    )