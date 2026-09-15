from collections import defaultdict

from sqlalchemy import case, func

from app.database import SessionLocal
from app.models import Alert
from app.models import Asset
from app.models import AssetActivity


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


def get_asset_metrics() -> list[dict]:
    """
    Generate intelligence metrics for every asset.

    These metrics will later feed the Negative Space detector.

    Important concepts:

        asset
          ↓
        activity
          ↓
        alerts
          ↓
        expected vs observed behavior
    """

    db = SessionLocal()

    try:

        # ==========================================================
        # 1. Load assets
        # ==========================================================

        assets = (
            db.query(Asset)
            .order_by(Asset.asset_id)
            .all()
        )

        # ==========================================================
        # 2. Aggregate alerts by asset
        # ==========================================================

        alert_rows = (
            db.query(
                Alert.asset_id.label("asset_id"),

                func.count(
                    Alert.alert_id
                ).label("total_alerts"),

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
                        (Alert.escalated.is_(True), 1),
                        else_=0,
                    )
                ).label("escalated_alerts"),

                func.avg(
                    Alert.closure_time_minutes
                ).label("avg_closure_time"),
            )
            .group_by(
                Alert.asset_id
            )
            .all()
        )

        alert_metrics = {}

        for row in alert_rows:

            alert_metrics[row.asset_id] = {
                "total_alerts": int(
                    row.total_alerts or 0
                ),

                "critical_alerts": int(
                    row.critical_alerts or 0
                ),

                "high_alerts": int(
                    row.high_alerts or 0
                ),

                "escalated_alerts": int(
                    row.escalated_alerts or 0
                ),

                "avg_closure_time": (
                    float(row.avg_closure_time)
                    if row.avg_closure_time is not None
                    else None
                ),
            }

        # ==========================================================
        # 3. Load asset activity
        # ==========================================================

        activity_rows = (
            db.query(
                AssetActivity.asset_id,
                AssetActivity.timestamp,
                AssetActivity.event_count,
                AssetActivity.log_sources_active,
                AssetActivity.network_events,
                AssetActivity.authentication_events,
                AssetActivity.status,
            )
            .order_by(
                AssetActivity.timestamp
            )
            .all()
        )

        activity_metrics = defaultdict(
            lambda: {
                "activity_records": 0,
                "total_events": 0,
                "total_network_events": 0,
                "total_authentication_events": 0,
                "max_log_sources_active": 0,
                "latest_timestamp": None,
                "latest_event_count": 0,
                "latest_log_sources_active": 0,
                "latest_network_events": 0,
                "latest_authentication_events": 0,
                "latest_status": None,
            }
        )

        for row in activity_rows:

            metric = activity_metrics[
                row.asset_id
            ]

            metric[
                "activity_records"
            ] += 1

            metric[
                "total_events"
            ] += int(
                row.event_count or 0
            )

            metric[
                "total_network_events"
            ] += int(
                row.network_events or 0
            )

            metric[
                "total_authentication_events"
            ] += int(
                row.authentication_events or 0
            )

            metric[
                "max_log_sources_active"
            ] = max(
                metric["max_log_sources_active"],
                int(
                    row.log_sources_active or 0
                ),
            )

            # Because rows are ordered by timestamp,
            # the latest row overwrites the previous one.
            metric[
                "latest_timestamp"
            ] = row.timestamp

            metric[
                "latest_event_count"
            ] = int(
                row.event_count or 0
            )

            metric[
                "latest_log_sources_active"
            ] = int(
                row.log_sources_active or 0
            )

            metric[
                "latest_network_events"
            ] = int(
                row.network_events or 0
            )

            metric[
                "latest_authentication_events"
            ] = int(
                row.authentication_events or 0
            )

            metric[
                "latest_status"
            ] = row.status

        # ==========================================================
        # 4. Build final asset intelligence
        # ==========================================================

        results = []

        for asset in assets:

            asset_id = asset.asset_id

            alerts = alert_metrics.get(
                asset_id,
                {
                    "total_alerts": 0,
                    "critical_alerts": 0,
                    "high_alerts": 0,
                    "escalated_alerts": 0,
                    "avg_closure_time": None,
                },
            )

            activity = activity_metrics[
                asset_id
            ]

            total_alerts = alerts[
                "total_alerts"
            ]

            critical_alerts = alerts[
                "critical_alerts"
            ]

            high_alerts = alerts[
                "high_alerts"
            ]

            activity_records = activity[
                "activity_records"
            ]

            total_events = activity[
                "total_events"
            ]

            latest_event_count = activity[
                "latest_event_count"
            ]

            latest_log_sources = activity[
                "latest_log_sources_active"
            ]

            latest_status = activity[
                "latest_status"
            ]

            # ======================================================
            # 5. Determine whether asset appears silent
            # ======================================================

            is_silent = (
                latest_status == "Silent"
                or (
                    activity_records > 0
                    and latest_event_count == 0
                    and latest_log_sources == 0
                )
            )

            # ======================================================
            # 6. Determine monitoring indicators
            # ======================================================

            has_security_activity = (
                activity_records > 0
                and (
                    total_events > 0
                    or latest_log_sources > 0
                )
            )

            has_alert_activity = (
                total_alerts > 0
            )

            # ======================================================
            # 7. Build result
            # ======================================================

            results.append(
                {
                    "asset_id": asset.asset_id,

                    "organization_id": (
                        asset.organization_id
                    ),

                    "asset_identifier": (
                        asset.asset_identifier
                    ),

                    "asset_name": asset.asset_name,

                    "asset_type": asset.asset_type,

                    "criticality": asset.criticality,

                    "environment": asset.environment,

                    "location": asset.location,

                    "status": asset.status,

                    "alerts": {
                        "total": total_alerts,

                        "critical": critical_alerts,

                        "high": high_alerts,

                        "escalated": alerts[
                            "escalated_alerts"
                        ],

                        "average_closure_time_minutes": (
                            round(
                                alerts[
                                    "avg_closure_time"
                                ],
                                2,
                            )
                            if alerts[
                                "avg_closure_time"
                            ] is not None
                            else 0.0
                        ),
                    },

                    "activity": {
                        "records": activity_records,

                        "total_events": total_events,

                        "total_network_events": (
                            activity[
                                "total_network_events"
                            ]
                        ),

                        "total_authentication_events": (
                            activity[
                                "total_authentication_events"
                            ]
                        ),

                        "max_log_sources_active": (
                            activity[
                                "max_log_sources_active"
                            ]
                        ),

                        "latest_timestamp": (
                            activity[
                                "latest_timestamp"
                            ]
                        ),

                        "latest_event_count": (
                            latest_event_count
                        ),

                        "latest_log_sources_active": (
                            latest_log_sources
                        ),

                        "latest_network_events": (
                            activity[
                                "latest_network_events"
                            ]
                        ),

                        "latest_authentication_events": (
                            activity[
                                "latest_authentication_events"
                            ]
                        ),

                        "latest_status": (
                            latest_status
                        ),
                    },

                    "monitoring": {
                        "is_silent": is_silent,

                        "has_security_activity": (
                            has_security_activity
                        ),

                        "has_alert_activity": (
                            has_alert_activity
                        ),
                    },
                }
            )

        return results

    finally:

        db.close()


if __name__ == "__main__":

    metrics = get_asset_metrics()

    print()
    print("SAT-SA ASSET INTELLIGENCE")
    print("=" * 70)

    print(
        f"Assets analyzed: "
        f"{len(metrics):,}"
    )

    silent_assets = [
        asset
        for asset in metrics
        if asset["monitoring"]["is_silent"]
    ]

    print(
        f"Silent assets: "
        f"{len(silent_assets):,}"
    )

    critical_silent = [
        asset
        for asset in silent_assets
        if str(
            asset["criticality"]
        ).lower() == "critical"
    ]

    print(
        f"Critical silent assets: "
        f"{len(critical_silent):,}"
    )

    print()
    print("Top silent assets:")
    print("-" * 70)

    for asset in critical_silent[:10]:

        print(
            f"{asset['asset_id']} | "
            f"{asset['asset_name']} | "
            f"Criticality: {asset['criticality']} | "
            f"Alerts: {asset['alerts']['total']} | "
            f"Activity: {asset['activity']['latest_event_count']} | "
            f"Status: {asset['activity']['latest_status']}"
        )
