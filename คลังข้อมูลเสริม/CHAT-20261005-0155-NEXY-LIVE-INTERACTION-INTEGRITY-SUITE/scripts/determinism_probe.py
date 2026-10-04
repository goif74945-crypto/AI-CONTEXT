from __future__ import annotations

import json

from nexy_live_integrity import (
    InputCohesionGate,
    InputRequirement,
    InputResource,
    IntentContract,
    IntentEquivalenceGate,
    InterruptEpochGate,
    build_interaction_snapshot,
    canonical_digest,
)

H = "1" * 64
POLICY = "a" * 64

gate = InterruptEpochGate("determinism-session")
token = gate.begin_directive("directive-1", {"text": "Build exact artifact", "priority": "high"})
contracts = [
    IntentContract("voice", "Build exact artifact", "BUILD", ("artifact:1",), "strict", False, True, "project:p", (("z", "2"), ("a", "1"))),
    IntentContract("text", "Build exact artifact", "BUILD", ("artifact:1",), "strict", False, True, "project:p", (("a", "1"), ("z", "2"))),
]
intent = IntentEquivalenceGate.compare(contracts)
inputs = InputCohesionGate.evaluate(
    [InputRequirement("spec", "file", expected_sha256=H)],
    [InputResource("extra", "file", "2" * 64, "external"), InputResource("spec", "file", H, "user")],
)
snapshot = build_interaction_snapshot(gate, token, intent, inputs, policy_hash=POLICY)
print(json.dumps({
    "intent": intent.fingerprint,
    "inputs": inputs.binding_fingerprint,
    "snapshot": snapshot.snapshot_digest,
    "combined": canonical_digest({"intent": intent.fingerprint, "inputs": inputs.binding_fingerprint, "snapshot": snapshot.snapshot_digest}),
}, sort_keys=True, separators=(",", ":")))
