import json
import unittest

from hicf import (
    ActionCandidate,
    AuthorityState,
    ClarificationGate,
    DriftClass,
    FrictionBudget,
    FrictionState,
    GateDecision,
    Impact,
    IntentDriftDetector,
    IntentEnvelope,
    Materiality,
    PreferenceRecord,
    PreferenceScope,
    Reversibility,
    Unknown,
    decision_record,
)


class HICFTests(unittest.TestCase):
    def setUp(self) -> None:
        self.gate = ClarificationGate()
        self.safe_action = ActionCandidate(
            action_id="a1",
            capability="read-only analysis",
            impact=Impact.LOW,
            reversibility=Reversibility.REVERSIBLE,
            mutates_state=False,
        )

    def test_fingerprint_is_canonical_across_ordering(self) -> None:
        a = IntentEnvelope.build(
            objective="  Analyze   project state ",
            constraints=["Do not guess", "Preserve scope"],
            immutables=["User Law", "Safety"],
        )
        b = IntentEnvelope.build(
            objective="Analyze project state",
            constraints=["Preserve scope", "Do not guess"],
            immutables=["Safety", "User Law"],
        )
        self.assertEqual(a.fingerprint(), b.fingerprint())

    def test_nonmaterial_unknown_allows_reversible_read_only_work(self) -> None:
        env = IntentEnvelope.build(
            objective="Analyze project state",
            unknowns=[Unknown("nice_to_have_format", Materiality.NON_MATERIAL)],
        )
        result = self.gate.evaluate(env, self.safe_action)
        self.assertEqual(result.decision, GateDecision.PROCEED)

    def test_material_unknown_requires_clarification(self) -> None:
        env = IntentEnvelope.build(
            objective="Modify configuration",
            unknowns=[Unknown("target_environment", Materiality.MATERIAL)],
        )
        result = self.gate.evaluate(env, self.safe_action)
        self.assertEqual(result.decision, GateDecision.ASK)
        self.assertIn("target_environment", result.required_questions)

    def test_critical_unknown_freezes(self) -> None:
        env = IntentEnvelope.build(
            objective="Execute critical action",
            unknowns=[Unknown("safety_boundary", Materiality.CRITICAL)],
        )
        result = self.gate.evaluate(env, self.safe_action)
        self.assertEqual(result.decision, GateDecision.FREEZE)

    def test_authority_conflict_freezes(self) -> None:
        env = IntentEnvelope.build(
            objective="Do work",
            authority_state=AuthorityState.CONFLICT,
        )
        self.assertEqual(self.gate.evaluate(env, self.safe_action).decision, GateDecision.FREEZE)

    def test_prohibited_capability_freezes(self) -> None:
        env = IntentEnvelope.build(
            objective="Analyze only",
            prohibited=["delete"],
        )
        action = ActionCandidate("a2", "delete repository file", Impact.HIGH, Reversibility.IRREVERSIBLE, True)
        result = self.gate.evaluate(env, action)
        self.assertEqual(result.decision, GateDecision.FREEZE)
        self.assertEqual(result.reason_codes, ("PROHIBITED_CAPABILITY",))

    def test_unresolved_authority_blocks_high_impact_mutation(self) -> None:
        env = IntentEnvelope.build(
            objective="Change release policy",
            authority_state=AuthorityState.UNRESOLVED,
        )
        action = ActionCandidate("a3", "update policy", Impact.HIGH, Reversibility.PARTIALLY_REVERSIBLE, True)
        result = self.gate.evaluate(env, action)
        self.assertEqual(result.decision, GateDecision.ASK)
        self.assertIn("resolve_authority", result.required_questions)

    def test_friction_budget_never_suppresses_material_question(self) -> None:
        env = IntentEnvelope.build(
            objective="Modify configuration",
            unknowns=[Unknown("target", Materiality.MATERIAL)],
        )
        state = FrictionState().ask("target").ask("target").ask("target")
        advisories = FrictionBudget(preferred_max_clarifications=1).advisory_violation(state)
        self.assertTrue(advisories)
        self.assertEqual(self.gate.evaluate(env, self.safe_action).decision, GateDecision.ASK)

    def test_repeat_question_is_detected(self) -> None:
        state = FrictionState().ask("target").ask("target")
        self.assertEqual(state.repeated_question_count, 1)
        self.assertIn("REPEATED_QUESTION", FrictionBudget().advisory_violation(state))

    def test_durable_preference_requires_explicit_authority(self) -> None:
        p = PreferenceRecord("verbosity", "compact", PreferenceScope.DURABLE, False, "inferred from behavior")
        with self.assertRaises(ValueError):
            p.validate()

    def test_project_preference_may_be_explicit(self) -> None:
        p = PreferenceRecord("format", "structured", PreferenceScope.PROJECT, True, "user message")
        p.validate()

    def test_immutable_drift_is_authority_break(self) -> None:
        detector = IntentDriftDetector()
        a = IntentEnvelope.build(objective="Build", immutables=["No NEXY source mutation"])
        b = IntentEnvelope.build(objective="Build", immutables=[])
        self.assertEqual(detector.compare(a, b), DriftClass.AUTHORITY_BREAK)

    def test_objective_drift_is_material(self) -> None:
        detector = IntentDriftDetector()
        a = IntentEnvelope.build(objective="Analyze")
        b = IntentEnvelope.build(objective="Deploy")
        self.assertEqual(detector.compare(a, b), DriftClass.MATERIAL)

    def test_decision_record_is_json_serializable(self) -> None:
        env = IntentEnvelope.build(objective="Analyze")
        gate = self.gate.evaluate(env, self.safe_action)
        record = decision_record(env, self.safe_action, gate)
        payload = json.dumps(record, sort_keys=True)
        self.assertIn('"decision": "PROCEED"', payload)

    def test_empty_objective_rejected(self) -> None:
        with self.assertRaises(ValueError):
            IntentEnvelope.build(objective="   ")


if __name__ == "__main__":
    unittest.main()
