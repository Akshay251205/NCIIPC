from collections import defaultdict

from app.database import SessionLocal
from app.models import Asset
from app.models import AssetActivity

from app.services.negative_space.negative_space import (
    detect_negative_space,
)


def get_negative_space_metrics() -> list[dict]:
    """
    Analyze assets for missing or suspicious monitoring activity.
    """

    db = SessionLocal()

    try:

        # ======================================================
        # Load assets
        # ======================================================

        assets = (
            db.query(Asset)
            .order_by(Asset.asset_id)
            .all()
        )

        # ======================================================
        # Load activity
        # ======================================================

        activity_rows = (
            db.query(AssetActivity)
            .all()
        )

        activity_by_asset = defaultdict(
            list
        )

        for activity in activity_rows:

            activity_by_asset[
                activity.asset_id
            ].append(activity)

        # ======================================================
        # Analyze assets
        # ======================================================

        results = []

        for asset in assets:

            asset_id = asset.asset_id

            activities = activity_by_asset.get(
                asset_id,
                [],
            )

            # --------------------------------------------------
            # Aggregate activity
            # --------------------------------------------------

            event_count = 0

            log_sources_active = 0

            for activity in activities:

                try:
                    event_count += max(
                        int(
                            activity.event_count or 0
                        ),
                        0,
                    )
                except (
                    TypeError,
                    ValueError,
                ):
                    pass

                try:
                    log_sources_active += max(
                        int(
                            activity.log_sources_active
                            or 0
                        ),
                        0,
                    )
                except (
                    TypeError,
                    ValueError,
                ):
                    pass

            finding = detect_negative_space(
                asset_id=asset_id,
                asset_status=getattr(
                    asset,
                    "status",
                    None,
                ),
                asset_criticality=getattr(
                    asset,
                    "criticality",
                    None,
                ),
                has_activity_record=bool(
                    activities
                ),
                event_count=event_count,
                log_sources_active=(
                    log_sources_active
                ),
            )

            if finding.score > 0:

                result = finding.to_dict()

                result["organization_id"] = (
                    asset.organization_id
                )

                results.append(
                    result
                )

        return results

    finally:

        db.close()


if __name__ == "__main__":

    findings = get_negative_space_metrics()

    print()
    print(
        "SAT-SA NEGATIVE SPACE INTELLIGENCE"
    )
    print("=" * 70)

    print(
        f"Findings: {len(findings):,}"
    )

    for finding in sorted(
        findings,
        key=lambda item: item["score"],
        reverse=True,
    )[:10]:

        print()

        print(
            f"{finding['entity_id']} "
            f"- {finding['severity']}"
        )

        print(
            f"  Score: "
            f"{finding['score']}/100"
        )

        print(
            "  Indicators: "
            + ", ".join(
                finding["indicators"]
            )
        )
