import pytest

from nexy_mvk import Case, Observation, VerificationEngine
from nexy_mvk.model import MetamorphicRelation, OracleResult, RelationStatus
from nexy_mvk.relations import deterministic_replay, irrelevant_context_invariance


def stable_adapter(case: Case) -> Observation:
    return Observation(status="PASS", released=True, payload={"answer": 42}, side_effects=("read",))


def test_engine_passes_invariance_relation():
    engine = VerificationEngine(stable_adapter)
    relation = irrelevant_context_invariance(key="noise", value="ignored")
    result = engine.run_relation(Case(prompt="compute"), relation)
    assert result.status is RelationStatus.PASS
    assert result.baseline_observation_hash == result.derived_observation_hash


def test_engine_detects_semantic_change():
    def adapter(case: Case) -> Observation:
        return Observation(status="PASS", released=True, payload={"context": dict(case.context)})

    result = VerificationEngine(adapter).run_relation(
        Case(prompt="compute"),
        irrelevant_context_invariance(key="noise", value="ignored"),
    )
    assert result.status is RelationStatus.FAIL


def test_adapter_exception_is_error_not_crash():
    def broken(_case: Case) -> Observation:
        raise RuntimeError("boom")

    result = VerificationEngine(broken).run_relation(Case(prompt="x"), deterministic_replay())
    assert result.status is RelationStatus.ERROR
    assert "adapter execution failed" in result.reason


def test_mutator_exception_is_error():
    def bad_mutator(_case: Case) -> Case:
        raise ValueError("bad relation")

    relation = MetamorphicRelation(
        relation_id="BAD",
        description="bad",
        mutator=bad_mutator,
        oracle=lambda *_: OracleResult(True, "never"),
    )
    result = VerificationEngine(stable_adapter).run_relation(Case(prompt="x"), relation)
    assert result.status is RelationStatus.ERROR
    assert "mutation failed" in result.reason


def test_oracle_exception_is_error():
    relation = MetamorphicRelation(
        relation_id="ORACLE-ERROR",
        description="bad oracle",
        mutator=lambda c: c,
        oracle=lambda *_: (_ for _ in ()).throw(RuntimeError("oracle boom")),
    )
    result = VerificationEngine(stable_adapter).run_relation(Case(prompt="x"), relation)
    assert result.status is RelationStatus.ERROR
    assert "oracle execution failed" in result.reason


def test_run_rejects_duplicate_relation_ids():
    engine = VerificationEngine(stable_adapter)
    relations = [deterministic_replay(), deterministic_replay()]
    with pytest.raises(ValueError, match="duplicate relation ids"):
        engine.run(Case(prompt="x"), relations)


def test_run_requires_relation():
    with pytest.raises(ValueError, match="at least one"):
        VerificationEngine(stable_adapter).run(Case(prompt="x"), [])


def test_uncanonicalizable_seed_is_structured_error():
    result = VerificationEngine(stable_adapter).run_relation(
        Case(prompt="x", context={"bad": object()}),
        deterministic_replay(),
    )
    assert result.status is RelationStatus.ERROR
    assert result.seed_case_hash == "UNAVAILABLE"
    assert "seed canonicalization failed" in result.reason


def test_derived_adapter_failure_is_structured_error():
    def adapter(case: Case) -> Observation:
        if "noise" in case.context:
            raise RuntimeError("derived-only failure")
        return Observation(status="PASS", released=True)

    result = VerificationEngine(adapter).run_relation(
        Case(prompt="x"), irrelevant_context_invariance(key="noise", value=True)
    )
    assert result.status is RelationStatus.ERROR
    assert result.baseline_observation_hash is not None
    assert result.derived_observation_hash is None


def test_adapter_wrong_return_type_is_structured_error():
    result = VerificationEngine(lambda _case: {"status": "PASS"}).run_relation(  # type: ignore[arg-type]
        Case(prompt="x"), deterministic_replay()
    )
    assert result.status is RelationStatus.ERROR
    assert "adapter must return Observation" in result.reason


def test_mutator_wrong_return_type_is_structured_error():
    relation = MetamorphicRelation(
        relation_id="WRONG-TYPE",
        description="wrong return type",
        mutator=lambda _case: "bad",  # type: ignore[arg-type,return-value]
        oracle=lambda *_: OracleResult(True, "never"),
    )
    result = VerificationEngine(stable_adapter).run_relation(Case(prompt="x"), relation)
    assert result.status is RelationStatus.ERROR
    assert "mutator must return Case" in result.reason


def test_run_generates_run_id_and_counts():
    report = VerificationEngine(stable_adapter).run(Case(prompt="x"), [deterministic_replay()])
    assert report.run_id.startswith("mvk-")
    assert report.passed
    assert report.counts["PASS"] == 1
