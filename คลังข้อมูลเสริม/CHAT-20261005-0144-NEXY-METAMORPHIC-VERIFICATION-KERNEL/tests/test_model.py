import pytest

from nexy_mvk.model import Case, MetamorphicRelation, Observation, OracleResult, RelationStatus, VerificationReport


def test_case_defensively_copies_mappings():
    context = {"x": 1}
    case = Case(prompt="p", context=context)
    context["x"] = 2
    assert case.context["x"] == 1


def test_observation_requires_status():
    with pytest.raises(ValueError):
        Observation(status="", released=False)


def test_relation_rejects_invalid_risk():
    with pytest.raises(ValueError):
        MetamorphicRelation("x", "x", lambda c: c, lambda *_: OracleResult(True, "ok"), risk="extreme")


def test_empty_report_not_passed():
    report = VerificationReport(run_id="r", results=())
    assert not report.passed
    assert report.counts[RelationStatus.PASS.value] == 0


def test_case_rejects_blank_prompt():
    with pytest.raises(ValueError, match="prompt"):
        Case(prompt="   ")


def test_oracle_result_requires_reason():
    with pytest.raises(ValueError, match="reason"):
        OracleResult(True, "")


def test_relation_requires_id_and_description():
    with pytest.raises(ValueError, match="relation_id"):
        MetamorphicRelation("", "x", lambda c: c, lambda *_: OracleResult(True, "ok"))
    with pytest.raises(ValueError, match="description"):
        MetamorphicRelation("x", "", lambda c: c, lambda *_: OracleResult(True, "ok"))
