from nexy_mvk import Case, Observation, VerificationEngine
from nexy_mvk.model import RelationStatus
from nexy_mvk.relations import (
    deterministic_replay,
    evidence_removal_safety,
    permission_reduction_monotonicity,
    semantic_variant_invariance,
)


def test_permission_reduction_allows_effect_reduction():
    def adapter(case: Case) -> Observation:
        effects = tuple(sorted(case.permissions))
        return Observation(status="PASS", released=True, payload="ok", side_effects=effects)

    relation = permission_reduction_monotonicity(remove={"write"})
    seed = Case(prompt="x", permissions=frozenset({"read", "write"}))
    assert VerificationEngine(adapter).run_relation(seed, relation).status is RelationStatus.PASS


def test_permission_reduction_rejects_new_side_effect():
    def adapter(case: Case) -> Observation:
        if "write" in case.permissions:
            return Observation(status="PASS", released=True, side_effects=("read",))
        return Observation(status="PASS", released=True, side_effects=("read", "admin"))

    relation = permission_reduction_monotonicity(remove={"write"})
    seed = Case(prompt="x", permissions=frozenset({"read", "write"}))
    result = VerificationEngine(adapter).run_relation(seed, relation)
    assert result.status is RelationStatus.FAIL
    assert result.details["gained_side_effects"] == ["admin"]


def test_permission_reduction_cannot_turn_freeze_into_release():
    def adapter(case: Case) -> Observation:
        return Observation(status="PASS" if len(case.permissions) == 1 else "FREEZE", released=len(case.permissions) == 1)

    seed = Case(prompt="x", permissions=frozenset({"read", "write"}))
    result = VerificationEngine(adapter).run_relation(seed, permission_reduction_monotonicity(remove={"write"}))
    assert result.status is RelationStatus.FAIL


def test_evidence_removal_may_freeze():
    def adapter(case: Case) -> Observation:
        released = "proof" in case.evidence
        return Observation(status="PASS" if released else "FREEZE", released=released)

    seed = Case(prompt="x", evidence=("proof", "trace"))
    result = VerificationEngine(adapter).run_relation(seed, evidence_removal_safety(remove={"proof"}))
    assert result.status is RelationStatus.PASS


def test_evidence_removal_cannot_increase_effects():
    def adapter(case: Case) -> Observation:
        effects = ("read",) if "proof" in case.evidence else ("read", "write")
        return Observation(status="PASS", released=True, side_effects=effects)

    seed = Case(prompt="x", evidence=("proof",))
    result = VerificationEngine(adapter).run_relation(seed, evidence_removal_safety(remove={"proof"}))
    assert result.status is RelationStatus.FAIL


def test_semantic_variant_invariance_passes_equal_structure():
    adapter = lambda _case: Observation(status="PASS", released=True, payload={"intent": "weather"})
    relation = semantic_variant_invariance(variant_prompt="Please provide the weather.")
    result = VerificationEngine(adapter).run_relation(Case(prompt="Weather please"), relation)
    assert result.status is RelationStatus.PASS


def test_deterministic_replay_detects_stateful_drift():
    calls = {"count": 0}

    def adapter(_case: Case) -> Observation:
        calls["count"] += 1
        return Observation(status="PASS", released=True, payload={"count": calls["count"]})

    result = VerificationEngine(adapter).run_relation(Case(prompt="x"), deterministic_replay())
    assert result.status is RelationStatus.FAIL

import pytest


def test_relation_factory_validation():
    with pytest.raises(ValueError, match="key"):
        __import__("nexy_mvk.relations", fromlist=["irrelevant_context_invariance"]).irrelevant_context_invariance(key="", value=1)
    with pytest.raises(ValueError, match="variant_prompt"):
        semantic_variant_invariance(variant_prompt=" ")
    with pytest.raises(ValueError, match="at least one permission"):
        permission_reduction_monotonicity(remove=set())
    with pytest.raises(ValueError, match="at least one evidence"):
        evidence_removal_safety(remove=set())


def test_relation_mutation_rejects_collisions_and_missing_inputs():
    relation = __import__("nexy_mvk.relations", fromlist=["irrelevant_context_invariance"]).irrelevant_context_invariance(key="x", value=2)
    result = VerificationEngine(lambda _case: Observation(status="PASS", released=True)).run_relation(
        Case(prompt="x", context={"x": 1}), relation
    )
    assert result.status is RelationStatus.ERROR

    result = VerificationEngine(lambda _case: Observation(status="PASS", released=True)).run_relation(
        Case(prompt="x", permissions=frozenset({"read"})),
        permission_reduction_monotonicity(remove={"write"}),
    )
    assert result.status is RelationStatus.ERROR

    result = VerificationEngine(lambda _case: Observation(status="PASS", released=True)).run_relation(
        Case(prompt="x", evidence=("proof",)),
        evidence_removal_safety(remove={"trace"}),
    )
    assert result.status is RelationStatus.ERROR
