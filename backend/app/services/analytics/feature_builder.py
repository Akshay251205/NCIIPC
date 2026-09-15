from typing import Any


def _number(
    value: Any,
    default: float = 0.0,
) -> float:
    """
    Convert a value into a float safely.

    Examples:

        _number(10) -> 10.0
        _number("10") -> 10.0
        _number(None) -> 0.0
    """

    if value is None:
        return default

    try:
        return float(value)

    except (
        TypeError,
        ValueError,
    ):
        return default


def clamp(
    value: float,
    minimum: float = 0.0,
    maximum: float = 100.0,
) -> float:
    """
    Keep a numeric value inside a defined range.
    """

    return max(
        minimum,
        min(
            maximum,
            value,
        ),
    )


def percentage(
    numerator: float,
    denominator: float,
) -> float:
    """
    Calculate a percentage safely.
    """

    numerator = _number(numerator)
    denominator = _number(denominator)

    if denominator <= 0:
        return 0.0

    return round(
        clamp(
            (numerator / denominator) * 100
        ),
        2,
    )


def build_analyst_feature_record(
    analyst: dict,
) -> dict:
    """
    Convert one analyst analytics record into a flat
    intelligence feature record.

    The output is deliberately simple.

    Future intelligence modules should be able to consume
    this structure without needing to understand SQLAlchemy.
    """

    alerts = analyst.get(
        "alerts",
        {},
    )

    performance = analyst.get(
        "performance",
        {},
    )

    investigations = analyst.get(
        "investigations",
        {},
    )

    data_quality = analyst.get(
        "data_quality",
        {},
    )

    total_alerts = int(
        _number(
            alerts.get("total")
        )
    )

    total_investigations = int(
        _number(
            investigations.get("total")
        )
    )

    return {
        # ----------------------------------------------------------
        # Identity
        # ----------------------------------------------------------

        "analyst_id": analyst.get(
            "analyst_id"
        ),

        "organization_id": analyst.get(
            "organization_id"
        ),

        "role": analyst.get(
            "role"
        ),

        "team": analyst.get(
            "team"
        ),

        "shift": analyst.get(
            "shift"
        ),

        "experience_years": _number(
            analyst.get("experience_years")
        ),

        # ----------------------------------------------------------
        # Workload
        # ----------------------------------------------------------

        "total_alerts": total_alerts,

        "closed_alerts": int(
            _number(
                alerts.get("closed")
            )
        ),

        "open_alerts": int(
            _number(
                alerts.get("open")
            )
        ),

        "investigating_alerts": int(
            _number(
                alerts.get("investigating")
            )
        ),

        "total_investigations": (
            total_investigations
        ),

        # ----------------------------------------------------------
        # Alert behavior
        # ----------------------------------------------------------

        "average_closure_time_minutes": (
            _number(
                performance.get(
                    "average_closure_time_minutes"
                )
            )
        ),

        "minimum_closure_time_minutes": (
            _number(
                performance.get(
                    "minimum_closure_time_minutes"
                )
            )
        ),

        "maximum_closure_time_minutes": (
            _number(
                performance.get(
                    "maximum_closure_time_minutes"
                )
            )
        ),

        "closure_rate": _number(
            performance.get(
                "closure_rate"
            )
        ),

        "escalation_rate": _number(
            performance.get(
                "escalation_rate"
            )
        ),

        "false_positive_rate": _number(
            performance.get(
                "false_positive_rate"
            )
        ),

        "evidence_review_rate": _number(
            performance.get(
                "evidence_review_rate"
            )
        ),

        # ----------------------------------------------------------
        # Investigation behavior
        # ----------------------------------------------------------

        "investigation_coverage_rate": (
            _number(
                investigations.get(
                    "coverage_rate"
                )
            )
        ),

        "average_investigation_duration_minutes": (
            _number(
                investigations.get(
                    "average_duration_minutes"
                )
            )
        ),

        "minimum_investigation_duration_minutes": (
            _number(
                investigations.get(
                    "minimum_duration_minutes"
                )
            )
        ),

        "maximum_investigation_duration_minutes": (
            _number(
                investigations.get(
                    "maximum_duration_minutes"
                )
            )
        ),

        "average_queries": _number(
            investigations.get(
                "average_queries"
            )
        ),

        "average_actions": _number(
            investigations.get(
                "average_actions"
            )
        ),

        "investigation_evidence_review_rate": (
            _number(
                investigations.get(
                    "evidence_review_rate"
                )
            )
        ),

        "investigation_escalation_rate": (
            _number(
                investigations.get(
                    "escalation_rate"
                )
            )
        ),

        # ----------------------------------------------------------
        # Data quality
        # ----------------------------------------------------------

        "observations": int(
            _number(
                data_quality.get(
                    "observations"
                )
            )
        ),

        "data_confidence": data_quality.get(
            "data_confidence"
        ),

        # ----------------------------------------------------------
        # Existing rule score
        # ----------------------------------------------------------

        "existing_rule_score": _number(
            analyst.get(
                "risk",
                {},
            ).get(
                "score"
            )
        ),
    }


def build_analyst_feature_records(
    analysts: list[dict],
) -> list[dict]:
    """
    Convert many analyst metric records into feature records.
    """

    return [
        build_analyst_feature_record(
            analyst
        )
        for analyst in analysts
    ]


def group_features_by_organization(
    analyst_features: list[dict],
) -> dict[str, list[dict]]:
    """
    Group analyst features by organization.

    This will later be useful for peer benchmarking
    and organization-level risk analysis.
    """

    grouped: dict[
        str,
        list[dict],
    ] = {}

    for feature in analyst_features:

        organization_id = feature.get(
            "organization_id"
        )

        if organization_id is None:
            continue

        grouped.setdefault(
            str(organization_id),
            [],
        ).append(feature)

    return grouped


def get_feature_statistics(
    analyst_features: list[dict],
) -> dict:
    """
    Produce simple summary statistics using pure Python.

    We deliberately avoid NumPy here so that the core analytics
    layer does not depend on native scientific libraries.
    """

    if not analyst_features:
        return {
            "analysts": 0,
            "total_alerts": 0,
            "total_investigations": 0,
            "average_alerts_per_analyst": 0.0,
            "average_investigations_per_analyst": 0.0,
        }

    total_alerts = sum(
        int(
            _number(
                item.get("total_alerts")
            )
        )
        for item in analyst_features
    )

    total_investigations = sum(
        int(
            _number(
                item.get(
                    "total_investigations"
                )
            )
        )
        for item in analyst_features
    )

    analyst_count = len(
        analyst_features
    )

    return {
        "analysts": analyst_count,

        "total_alerts": total_alerts,

        "total_investigations": (
            total_investigations
        ),

        "average_alerts_per_analyst": round(
            total_alerts / analyst_count,
            2,
        ),

        "average_investigations_per_analyst": round(
            total_investigations / analyst_count,
            2,
        ),
    }