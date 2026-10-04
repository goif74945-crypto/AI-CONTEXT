import unittest

from nexy_live_integrity import (
    CacheNamespace,
    CacheProvenanceFirewall,
    CompletionBoundaryGate,
    InputCohesionGate,
    InputRequirement,
    InputResource,
    IntentContract,
    IntentEquivalenceGate,
    InterruptEpochGate,
    StreamChunk,
    build_interaction_snapshot,
)

H1 = "1" * 64
POLICY = "a" * 64
MODEL = "b" * 64
TOOL = "c" * 64


class IntegrationTests(unittest.TestCase):
    def intent(self, modality):
        return IntentContract(
            modality=modality,
            objective="Generate verified report",
            operation="GENERATE",
            targets=("report:7",),
            mode="strict",
            allow_external=True,
            deterministic_required=True,
            authority_scope="project:alpha",
        )

    def test_preemption_completion_and_cache_are_bound_to_current_interaction(self):
        epoch_gate = InterruptEpochGate("session-1")
        token1 = epoch_gate.begin_directive("d1", {"text": "generate report"})
        intent1 = IntentEquivalenceGate.compare([self.intent("text"), self.intent("voice")])
        inputs1 = InputCohesionGate.evaluate(
            [InputRequirement("report-source", "file", expected_sha256=H1)],
            [InputResource("report-source", "file", H1, "project")],
        )
        snap1 = build_interaction_snapshot(epoch_gate, token1, intent1, inputs1, policy_hash=POLICY)

        parts = ("verified ", "report")
        payload_hash = CompletionBoundaryGate.payload_sha256("".join(parts))
        chunks = (
            StreamChunk("run-1", 0, parts[0], snap1.snapshot_digest),
            StreamChunk("run-1", 1, parts[1], snap1.snapshot_digest, True, payload_hash),
        )
        completion = CompletionBoundaryGate.verify(
            chunks,
            expected_run_id="run-1",
            expected_contract_hash=snap1.snapshot_digest,
            expected_chunk_count=2,
        )
        self.assertTrue(completion.allowed)

        cache = CacheProvenanceFirewall()
        ns = CacheNamespace("alpha", "user-1", POLICY, MODEL, TOOL, "1")
        cache.put(ns, {"snapshot": snap1.snapshot_digest, "release": completion.release_fingerprint}, {"payload_sha256": completion.payload_sha256})
        hit, value = cache.get(ns, {"snapshot": snap1.snapshot_digest, "release": completion.release_fingerprint})
        self.assertTrue(hit.allowed)
        self.assertEqual(value["payload_sha256"], payload_hash)

        token2 = epoch_gate.begin_directive("d2", {"text": "stop and use a different source"})
        self.assertNotEqual(token1.epoch, token2.epoch)
        self.assertEqual(epoch_gate.validate_token(token1).code, "INTERRUPT_STALE_EPOCH")

        stale_miss, value = cache.get(ns, {"snapshot": "f" * 64, "release": completion.release_fingerprint})
        self.assertEqual(stale_miss.code, "CACHE_MISS")
        self.assertIsNone(value)

    def test_snapshot_builder_rejects_superseded_epoch(self):
        epoch_gate = InterruptEpochGate("session-stale")
        stale = epoch_gate.begin_directive("d1", {"text": "first"})
        epoch_gate.begin_directive("d2", {"text": "replacement"})
        intent = IntentEquivalenceGate.compare([self.intent("text"), self.intent("voice")])
        inputs = InputCohesionGate.evaluate([], [])
        with self.assertRaisesRegex(RuntimeError, "INTERRUPT_STALE_EPOCH"):
            build_interaction_snapshot(epoch_gate, stale, intent, inputs, policy_hash=POLICY)


if __name__ == "__main__":
    unittest.main()
