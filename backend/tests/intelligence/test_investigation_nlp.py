from app.services.nlp.investigation_nlp import (
    analyze_investigation_notes,
    calculate_note_quality,
    detect_investigation_nlp,
)


def test_high_quality_investigation_note():
    note = (
        "Reviewed SIEM logs and endpoint process activity. "
        "Correlated the source IP with authentication events "
        "and checked the timeline. Evidence showed normal "
        "user activity and no malicious process execution."
    )

    finding = detect_investigation_nlp(
        investigation_id="INV001",
        note=note,
        evidence_reviewed=True,
    )

    assert finding.score < 40
    assert finding.severity == "LOW"
    assert finding.metrics["note_quality_score"] >= 60


def test_missing_note_is_detected():
    finding = detect_investigation_nlp(
        investigation_id="INV002",
        note=None,
        evidence_reviewed=False,
    )

    assert finding.score >= 70
    assert finding.severity == "HIGH"
    assert (
        "Missing investigation note"
        in finding.indicators
    )


def test_short_note_is_detected():
    finding = detect_investigation_nlp(
        investigation_id="INV003",
        note="Checked alert and closed.",
        evidence_reviewed=False,
    )

    assert (
        "Very short investigation note"
        in finding.indicators
    )


def test_generic_language_is_detected():
    finding = detect_investigation_nlp(
        investigation_id="INV004",
        note="Reviewed alert, nothing found, normal activity.",
        evidence_reviewed=False,
    )

    assert (
        "Generic investigation language"
        in finding.indicators
    )


def test_missing_security_context_is_detected():
    finding = detect_investigation_nlp(
        investigation_id="INV005",
        note="Checked the ticket and reviewed the information.",
        evidence_reviewed=False,
    )

    assert (
        "Limited security context"
        in finding.indicators
    )


def test_evidence_mismatch_is_detected():
    finding = detect_investigation_nlp(
        investigation_id="INV006",
        note="Reviewed the alert and confirmed activity.",
        evidence_reviewed=True,
    )

    assert (
        "Evidence review not reflected in note"
        in finding.indicators
    )


def test_high_quality_note_has_security_and_action_terms():
    quality = calculate_note_quality(
        "Reviewed SIEM logs, correlated the source IP "
        "with authentication events, inspected the "
        "endpoint process and validated the evidence."
    )

    assert quality["security_term_count"] >= 3
    assert quality["action_term_count"] >= 3
    assert quality["evidence_term_count"] >= 2
    assert quality["score"] >= 50


def test_batch_analysis():
    records = [
        {
            "investigation_id": "INV007",
            "investigation_notes": (
                "Reviewed SIEM logs and checked evidence."
            ),
            "evidence_reviewed": True,
        },
        {
            "investigation_id": "INV008",
            "investigation_notes": None,
            "evidence_reviewed": False,
        },
    ]

    results = analyze_investigation_notes(
        records
    )

    assert len(results) == 2
    assert results[0]["entity_id"] == "INV007"
    assert results[1]["entity_id"] == "INV008"
    assert results[1]["severity"] == "HIGH"


def test_to_dict_contains_expected_fields():
    finding = detect_investigation_nlp(
        investigation_id="INV009",
        note="Reviewed alert and checked logs.",
        evidence_reviewed=True,
    )

    result = finding.to_dict()

    assert result["entity_type"] == "investigation"
    assert result["entity_id"] == "INV009"
    assert "score" in result
    assert "severity" in result
    assert "confidence" in result
    assert "indicators" in result
    assert "observations" in result
    assert "metrics" in result