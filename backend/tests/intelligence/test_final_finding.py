from app.services.findings.final_finding import (
    FinalSupervisoryFinding,
    build_final_finding,
    build_final_finding_dict,
    build_final_findings,
)


def sample_result():
    return {
        "analyst_id": "AN001",
        "data_quality": {
            "observations": 20,
            "confidence": "High",
        },
        "alerts": {
            "total": 5,
        },
        "investigations": {
            "total": 5,
        },
        "performance": {
            "average_closure_time_minutes": 15,
        },
        "investigation_dna": {
            "investigation_quality_score": 72,
            "confidence": "High",
            "indicators": [
                "Strong evidence discipline",
            ],
        },
        "gaming": {
            "score": 65,
            "severity": "MEDIUM",
            "confidence": "High",
            "indicators": [
                "Suspiciously fast closure",
            ],
        },
        "peer_benchmark": {
            "score": 55,
            "severity": "MEDIUM",
            "confidence": "Medium",
            "indicators": [
                "Peer deviation",
            ],
        },
        "behavioral_anomaly": {
            "score": 80,
            "severity": "HIGH",
            "confidence": "High",
            "indicators": [
                "Unusual closure behavior",
            ],
        },
        "investigation_nlp": {
            "average_score": 45,
            "high_findings": 1,
            "medium_findings": 2,
            "investigations_analyzed": 5,
            "indicators": [
                "Generic investigation language",
            ],
        },
        "negative_space": {
            "score": 70,
            "severity": "HIGH",
            "confidence": "Medium",
            "indicators": [
                "Monitoring visibility gap",
            ],
        },
        "risk": {
            "score": 78.5,
            "level": "HIGH",
            "severity": "HIGH",
            "confidence": "High",
            "components": {
                "rule": 80,
                "behavioral": 70,
                "negative_space": 70,
                "peer": 55,
            },
            "signals": [
                {
                    "source": "rule",
                    "score": 80,
                    "weight": 0.4,
                },
            ],
            "indicators": [
                "Suspiciously fast closure",
            ],
            "explanation": (
                "Final supervisory risk is "
                "78.5/100 (HIGH)."
            ),
        },
    }


def test_build_final_finding_returns_dataclass():
    finding = build_final_finding(
        sample_result()
    )

    assert isinstance(
        finding,
        FinalSupervisoryFinding,
    )

    assert (
        finding.entity_type
        == "analyst"
    )

    assert (
        finding.entity_id
        == "AN001"
    )


def test_final_risk_fields_are_preserved():
    finding = build_final_finding(
        sample_result()
    )

    assert (
        finding.risk_score
        == 78.5
    )

    assert (
        finding.risk_level
        == "HIGH"
    )

    assert (
        finding.risk_severity
        == "HIGH"
    )

    assert (
        finding.confidence
        == "High"
    )


def test_primary_indicators_are_deduplicated():
    finding = build_final_finding(
        sample_result()
    )

    assert (
        finding.primary_indicators.count(
            "Suspiciously fast closure"
        )
        == 1
    )

    assert (
        "Strong evidence discipline"
        in finding.primary_indicators
    )

    assert (
        "Monitoring visibility gap"
        in finding.primary_indicators
    )


def test_intelligence_layers_are_present():
    finding = build_final_finding(
        sample_result()
    )

    assert (
        "investigation_dna"
        in finding.intelligence
    )

    assert (
        "gaming"
        in finding.intelligence
    )

    assert (
        "peer_benchmark"
        in finding.intelligence
    )

    assert (
        "behavioral_anomaly"
        in finding.intelligence
    )

    assert (
        "investigation_nlp"
        in finding.intelligence
    )

    assert (
        "negative_space"
        in finding.intelligence
    )


def test_evidence_contains_operational_data():
    finding = build_final_finding(
        sample_result()
    )

    assert (
        finding.evidence[
            "data_quality"
        ]["observations"]
        == 20
    )

    assert (
        finding.evidence[
            "alerts"
        ]["total"]
        == 5
    )

    assert (
        finding.evidence[
            "investigations"
        ]["total"]
        == 5
    )


def test_high_risk_generates_supervisory_actions():
    finding = build_final_finding(
        sample_result()
    )

    assert (
        len(finding.supervisory_actions)
        > 0
    )

    assert any(
        "supervisory"
        in action.lower()
        for action
        in finding.supervisory_actions
    )


def test_to_dict_has_stable_contract():
    finding = build_final_finding(
        sample_result()
    )

    result = finding.to_dict()

    expected_keys = {
        "entity_type",
        "entity_id",
        "risk_score",
        "risk_level",
        "risk_severity",
        "confidence",
        "primary_indicators",
        "explanation",
        "intelligence",
        "evidence",
        "supervisory_actions",
        "status",
    }

    assert set(result.keys()) == expected_keys

    assert (
        result["status"]
        == "complete"
    )


def test_dictionary_interface():
    result = build_final_finding_dict(
        sample_result()
    )

    assert isinstance(
        result,
        dict,
    )

    assert (
        result["entity_id"]
        == "AN001"
    )

    assert (
        result["risk_score"]
        == 78.5
    )


def test_build_multiple_findings():
    results = build_final_findings(
        [
            sample_result(),
            {
                **sample_result(),
                "analyst_id": "AN002",
            },
        ]
    )

    assert len(results) == 2

    assert (
        results[0].entity_id
        == "AN001"
    )

    assert (
        results[1].entity_id
        == "AN002"
    )


def test_invalid_collection_returns_empty():
    assert (
        build_final_findings(None)
        == []
    )

    assert (
        build_final_findings("invalid")
        == []
    )


def test_missing_layers_are_safe():
    finding = build_final_finding(
        {
            "analyst_id": "AN003",
            "risk": {
                "score": 20,
                "level": "LOW",
                "severity": "LOW",
                "confidence": "Low",
            },
        }
    )

    assert (
        finding.entity_id
        == "AN003"
    )

    assert (
        finding.risk_score
        == 20
    )

    assert (
        finding.status
        == "complete"
    )

    assert isinstance(
        finding.intelligence,
        dict,
    )