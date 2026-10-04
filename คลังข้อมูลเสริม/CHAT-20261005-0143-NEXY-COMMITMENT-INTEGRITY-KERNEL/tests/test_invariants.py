from __future__ import annotations

import ast
import itertools
import pathlib
import unittest

from ncik.engine import evaluate_commitment, fingerprint, transition
from ncik.model import (
    AuthorityState, BindingType, CapabilityManifest, Commitment, CommitmentState,
    Decision, EffectClass, EvidenceBundle, EvidenceClass, ExecutionBinding, TemporalMode,
)

ROOT = pathlib.Path(__file__).resolve().parents[1]


def base_commitment(**overrides):
    data = dict(
        commitment_id="C-INV",
        revision=1,
        issuer="NEXY",
        beneficiary="user",
        objective="Prove invariant",
        deliverable="Invariant evidence",
        scope=("project:a", "project:b"),
        protected_scope=("project:z",),
        temporal_mode=TemporalMode.IMMEDIATE,
        effect=EffectClass.READ_ONLY,
        authority_state=AuthorityState.RESOLVED,
        authority_refs=("ref:b", "ref:a"),
        required_evidence=(EvidenceClass.E1_STATIC, EvidenceClass.E2_UNIT),
        binding=ExecutionBinding(BindingType.INLINE_SESSION, "session:inv", False, "proof:inv"),
        metadata={"b":"2","a":"1"},
    )
    data.update(overrides)
    return Commitment(**data)


def all_caps():
    return CapabilityManifest(frozenset(BindingType), frozenset(EffectClass), frozenset(EvidenceClass))


class StaticSafetyTests(unittest.TestCase):
    def test_reference_source_has_no_forbidden_runtime_imports(self):
        forbidden = {"time", "datetime", "random", "socket", "urllib", "requests", "httpx", "openai", "anthropic", "google.generativeai"}
        seen = set()
        for path in (ROOT / "src" / "ncik").glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    seen.update(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    seen.add(node.module)
        violations = sorted(x for x in seen if x.split(".")[0] in forbidden)
        self.assertEqual(violations, [])

    def test_reference_source_does_not_import_subprocess_or_os(self):
        forbidden = {"subprocess", "os"}
        seen = set()
        for path in (ROOT / "src" / "ncik").glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    seen.update(alias.name.split(".")[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    seen.add(node.module.split(".")[0])
        self.assertTrue(forbidden.isdisjoint(seen), seen & forbidden)


class DeterminismTests(unittest.TestCase):
    def test_same_input_same_decision_1000_times(self):
        c = base_commitment()
        expected = evaluate_commitment(c, all_caps())
        for _ in range(1000):
            self.assertEqual(evaluate_commitment(c, all_caps()), expected)

    def test_fingerprint_ignores_set_like_order(self):
        base = base_commitment()
        expected = fingerprint(base)
        for scopes in itertools.permutations(base.scope):
            for refs in itertools.permutations(base.authority_refs):
                c = base_commitment(scope=scopes, authority_refs=refs, required_evidence=tuple(reversed(base.required_evidence)))
                self.assertEqual(fingerprint(c), expected)

    def test_fingerprint_ignores_duplicate_set_like_values(self):
        a = base_commitment(scope=("project:a", "project:b"))
        b = base_commitment(scope=("project:a", "project:b", "project:a"), authority_refs=("ref:a","ref:b","ref:a"))
        self.assertEqual(fingerprint(a), fingerprint(b))

    def test_metadata_key_order_stable(self):
        a = base_commitment(metadata={"a":"1","b":"2"})
        b = base_commitment(metadata={"b":"2","a":"1"})
        self.assertEqual(fingerprint(a), fingerprint(b))


class EvidenceSemanticsTests(unittest.TestCase):
    def test_higher_evidence_class_does_not_substitute_for_required_class_at_acceptance(self):
        c = base_commitment(required_evidence=(EvidenceClass.E4_E2E,))
        caps = CapabilityManifest(frozenset(BindingType), frozenset(EffectClass), frozenset({EvidenceClass.E6_DEPLOYMENT}))
        result = evaluate_commitment(c, caps)
        self.assertEqual(result.decision, Decision.FREEZE)
        self.assertIn("EVIDENCE_CAPABILITY_MISSING:E4_E2E", result.reason_codes)

    def test_higher_evidence_class_does_not_substitute_at_completion(self):
        c = base_commitment(required_evidence=(EvidenceClass.E4_E2E,))
        evidence = EvidenceBundle(fingerprint(c), 1, frozenset({EvidenceClass.E6_DEPLOYMENT}), ("deploy:1",), "PASS")
        with self.assertRaisesRegex(ValueError, "E4_E2E"):
            transition(c, CommitmentState.ACTIVE, "COMPLETE", evidence)

    def test_exact_multiple_required_classes_succeeds(self):
        c = base_commitment(required_evidence=(EvidenceClass.E1_STATIC, EvidenceClass.E2_UNIT))
        evidence = EvidenceBundle(fingerprint(c), 1, frozenset({EvidenceClass.E1_STATIC, EvidenceClass.E2_UNIT}), ("static:1","unit:1"), "PASS")
        result = transition(c, CommitmentState.ACTIVE, "COMPLETE", evidence)
        self.assertEqual(result.current, CommitmentState.FULFILLED)

    def test_extra_evidence_is_allowed_but_does_not_replace_required(self):
        c = base_commitment(required_evidence=(EvidenceClass.E2_UNIT,))
        evidence = EvidenceBundle(fingerprint(c), 1, frozenset({EvidenceClass.E1_STATIC, EvidenceClass.E2_UNIT, EvidenceClass.E5_RUNTIME}), ("unit:1",), "PASS")
        result = transition(c, CommitmentState.ACTIVE, "COMPLETE", evidence)
        self.assertEqual(result.current, CommitmentState.FULFILLED)


class FailClosedTests(unittest.TestCase):
    def test_all_temporal_modes_have_exact_binding_mapping(self):
        mapping = {
            TemporalMode.IMMEDIATE: BindingType.INLINE_SESSION,
            TemporalMode.SCHEDULED: BindingType.SCHEDULED_TASK,
            TemporalMode.CONDITIONAL: BindingType.CONDITION_WATCH,
            TemporalMode.RECURRING: BindingType.RECURRING_TASK,
        }
        for mode, correct in mapping.items():
            for candidate in BindingType:
                c = base_commitment(
                    temporal_mode=mode,
                    trigger_spec="trigger" if mode in {TemporalMode.CONDITIONAL, TemporalMode.RECURRING} else None,
                    deadline_spec="deadline" if mode is TemporalMode.SCHEDULED else None,
                    binding=ExecutionBinding(candidate, "ref", mode is not TemporalMode.IMMEDIATE, "proof"),
                )
                r = evaluate_commitment(c, all_caps())
                if candidate is correct:
                    self.assertEqual(r.decision, Decision.ALLOW_COMMITMENT, (mode, candidate, r))
                else:
                    self.assertEqual(r.decision, Decision.FREEZE, (mode, candidate, r))

    def test_terminal_states_are_irreversible_for_all_events(self):
        c = base_commitment()
        terminals = [CommitmentState.FULFILLED, CommitmentState.FAILED, CommitmentState.CANCELLED, CommitmentState.EXPIRED, CommitmentState.SUPERSEDED]
        events = ["ACCEPT","ACTIVATE","BLOCK","RESUME","FAIL","CANCEL","EXPIRE","SUPERSEDE","COMPLETE"]
        for state in terminals:
            for event in events:
                with self.assertRaisesRegex(ValueError, "TERMINAL_STATE_IMMUTABLE"):
                    transition(c, state, event)


if __name__ == "__main__":
    unittest.main()
