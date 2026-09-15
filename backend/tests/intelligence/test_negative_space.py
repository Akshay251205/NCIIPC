from app.services.negative_space.negative_space import (
    NegativeSpaceFinding,
    detect_negative_space,
    detect_negative_space_batch,
)


def test_silent_asset_has_negative_space_score():

    finding = detect_negative_space(
        asset_id="ASSET001",
        asset_status="Active",
        asset_criticality="High",
        has_activity_record=True,
        event_count=0,
        log_sources_active=0,
    )

    assert isinstance(
        finding,
        NegativeSpaceFinding,
    )

    assert finding.score > 0

    assert (
        "Silent asset activity"
        in finding.indicators
    )

    assert (
        "No active log sources"
        in finding.indicators
    )


def test_missing_activity_record():

    finding = detect_negative_space(
        asset_id="ASSET002",
        asset_status="Active",
        asset_criticality="Critical",
        has_activity_record=False,
        event_count=0,
        log_sources_active=0,
    )

    assert finding.score > 0

    assert (
        "No monitoring activity record"
        in finding.indicators
    )

    assert finding.severity == "HIGH"


def test_normal_monitored_asset_has_no_finding():

    finding = detect_negative_space(
        asset_id="ASSET003",
        asset_status="Active",
        asset_criticality="Medium",
        has_activity_record=True,
        event_count=100,
        log_sources_active=3,
    )

    assert finding.score == 0

    assert finding.indicators == []


def test_batch_negative_space_detection():

    assets = [
        {
            "asset_id": "ASSET001",
            "asset_status": "Active",
            "asset_criticality": "High",
            "has_activity_record": True,
            "event_count": 0,
            "log_sources_active": 0,
        },
        {
            "asset_id": "ASSET002",
            "asset_status": "Active",
            "asset_criticality": "Medium",
            "has_activity_record": True,
            "event_count": 100,
            "log_sources_active": 3,
        },
    ]

    findings = detect_negative_space_batch(
        assets
    )

    assert len(findings) == 1

    assert (
        findings[0]["entity_id"]
        == "ASSET001"
    )


def test_zero_data_is_explicitly_low_confidence():
    finding = detect_negative_space(
        asset_id="ASSET004",
        has_activity_record=False,
    )

    assert finding.score > 0
    assert finding.confidence == "Low"
    assert "No monitoring activity record" in finding.indicators
