from nexy_mvk.model import RelationResult, RelationStatus, VerificationReport
from nexy_mvk.report import report_to_dict


def test_report_serialization_is_plain_data():
    report = VerificationReport(
        run_id="r1",
        results=(
            RelationResult(
                relation_id="R",
                status=RelationStatus.PASS,
                reason="ok",
                seed_case_hash="a",
                derived_case_hash="b",
                baseline_observation_hash="c",
                derived_observation_hash="d",
                details={"nested": {"x", "y"}},
            ),
        ),
        metadata={"suite": "unit"},
    )
    data = report_to_dict(report)
    assert data["passed"] is True
    assert data["counts"]["PASS"] == 1
    assert data["results"][0]["details"]["nested"] == ["x", "y"]
