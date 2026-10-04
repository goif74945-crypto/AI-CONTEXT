import unittest
from dataclasses import replace

from nexy_live_integrity import (
    CacheNamespace, CacheProvenanceFirewall, CompletionBoundaryGate, GateStatus,
    InputCohesionGate, InputRequirement, InputResource, IntentContract,
    IntentEquivalenceGate, InterruptEpochGate, StreamChunk,
    build_interaction_snapshot, canonical_digest, canonical_json,
)
from nexy_live_integrity.cache_provenance import CacheEntry

A = "a" * 64
B = "b" * 64
C = "c" * 64
E = "e" * 64


class AdversarialTests(unittest.TestCase):
    def intent(self, modality="text", **overrides):
        data = dict(modality=modality, objective="Build exact artifact", operation="BUILD",
                    targets=("artifact:1",), mode="strict", allow_external=False,
                    deterministic_required=True, authority_scope="project:p",
                    constraints=(("preserve", "yes"),))
        data.update(overrides)
        return IntentContract(**data)

    def namespace(self, **overrides):
        data = dict(project_id="p", user_scope="u", policy_hash=A,
                    model_contract_hash=B, tool_contract_hash=C, schema_version="1")
        data.update(overrides)
        return CacheNamespace(**data)

    def test_canonical_mapping_order_is_stable(self):
        self.assertEqual(canonical_json({"b": 2, "a": 1}), canonical_json({"a": 1, "b": 2}))
        self.assertEqual(canonical_digest({"b": 2, "a": 1}), canonical_digest({"a": 1, "b": 2}))

    def test_cross_session_epoch_token_freezes(self):
        g1, g2 = InterruptEpochGate("s1"), InterruptEpochGate("s2")
        foreign = g1.begin_directive("d", {"x": 1})
        g2.begin_directive("d", {"x": 1})
        self.assertEqual(g2.validate_token(foreign).code, "INTERRUPT_SESSION_MISMATCH")

    def test_tampered_action_lease_freezes(self):
        gate = InterruptEpochGate("s")
        token = gate.begin_directive("d", {"x": 1})
        lease = gate.prepare_action(token, {"op": "x"})
        tampered = replace(lease, directive_id="evil")
        self.assertEqual(gate.commit_action(tampered, {"op": "x"}).code, "INTERRUPT_LEASE_TAMPERED")

    def test_cache_policy_change_is_miss(self):
        cache = CacheProvenanceFirewall(); cache.put(self.namespace(), {"x": 1}, {"y": 2})
        self.assertEqual(cache.get(self.namespace(policy_hash=E), {"x": 1})[0].code, "CACHE_MISS")

    def test_cache_model_contract_change_is_miss(self):
        cache = CacheProvenanceFirewall(); cache.put(self.namespace(), {"x": 1}, {"y": 2})
        self.assertEqual(cache.get(self.namespace(model_contract_hash=E), {"x": 1})[0].code, "CACHE_MISS")

    def test_cache_tool_contract_change_is_miss(self):
        cache = CacheProvenanceFirewall(); cache.put(self.namespace(), {"x": 1}, {"y": 2})
        self.assertEqual(cache.get(self.namespace(tool_contract_hash=E), {"x": 1})[0].code, "CACHE_MISS")

    def test_cache_envelope_tamper_freezes(self):
        cache = CacheProvenanceFirewall(); entry = cache.put(self.namespace(), {"x": 1}, {"y": 2})
        tampered = CacheEntry(entry.namespace, entry.input_digest, entry.value, entry.value_digest, E)
        self.assertEqual(cache.validate_entry(self.namespace(), {"x": 1}, tampered).code, "CACHE_ENTRY_TAMPERED")

    def test_intent_fingerprint_is_modality_order_independent(self):
        a = IntentEquivalenceGate.compare([self.intent("text"), self.intent("voice")])
        b = IntentEquivalenceGate.compare([self.intent("voice"), self.intent("text")])
        self.assertEqual(a.fingerprint, b.fingerprint)

    def test_duplicate_modality_freezes(self):
        self.assertEqual(IntentEquivalenceGate.compare([self.intent("text"), self.intent("text")]).code, "INTENT_DUPLICATE_MODALITY")

    def test_constraint_drift_freezes(self):
        result = IntentEquivalenceGate.compare([self.intent("text"), self.intent("voice", constraints=(("preserve", "no"),))])
        self.assertIn("voice:constraints", result.mismatches)

    def test_input_trust_mismatch_freezes(self):
        result = InputCohesionGate.evaluate([InputRequirement("f", "file", allowed_trust=("user",))], [InputResource("f", "file", A, "external")])
        self.assertIn("trust_mismatch:f", result.problems)

    def test_input_kind_mismatch_freezes(self):
        result = InputCohesionGate.evaluate([InputRequirement("f", "file")], [InputResource("f", "url", A, "user")])
        self.assertIn("kind_mismatch:f", result.problems)

    def test_optional_missing_input_is_legal(self):
        self.assertTrue(InputCohesionGate.evaluate([InputRequirement("f", "file", required=False)], []).allowed)

    def test_duplicate_requirement_id_freezes(self):
        result = InputCohesionGate.evaluate([InputRequirement("f", "file"), InputRequirement("f", "file")], [])
        self.assertEqual(result.code, "INPUT_DUPLICATE_REQUIREMENT")

    def test_coordinator_rejects_non_equivalent_intent(self):
        gate = InterruptEpochGate("s"); token = gate.begin_directive("d", {"x": 1})
        intent = IntentEquivalenceGate.compare([self.intent("text"), self.intent("voice", mode="fast")])
        with self.assertRaises(RuntimeError):
            build_interaction_snapshot(gate, token, intent, InputCohesionGate.evaluate([], []), policy_hash=A)

    def test_completion_eof_without_final_marker_is_not_completion(self):
        result = CompletionBoundaryGate.verify((StreamChunk("r", 0, "partial", A),), expected_run_id="r", expected_contract_hash=A)
        self.assertEqual(result.status, GateStatus.FREEZE)
        self.assertIn("missing_final_marker", result.problems)

    def test_repeated_fingerprints_are_deterministic(self):
        values = [canonical_digest({"i": 7, "x": (1, 2, 3)}) for _ in range(250)]
        self.assertEqual(len(set(values)), 1)


if __name__ == "__main__":
    unittest.main()
