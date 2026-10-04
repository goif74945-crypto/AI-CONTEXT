from __future__ import annotations

import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nexy_reflex.canonical import canonical_json, sha256_digest
from nexy_reflex.engine import evaluate_snapshot
from nexy_reflex.impact import diff_snapshots
from nexy_reflex.models import GateAction, Snapshot, TruthStatus


def base_payload() -> dict:
    return {
        "snapshot_version": "1.0",
        "target": {"id": "nexy-export", "revision": "abc123", "content_digest": "sha256:target"},
        "authority_order": ["USER_LAW", "DOC_B", "DOC_C", "DOC_D", "RUNTIME", "CONTEXT"],
        "requirements": [
            {
                "id": "R1",
                "key": "auth.otac.ttl_ms",
                "value": 300000,
                "authority": "DOC_C",
                "scope": "CURRENT_BUILD",
                "accepted_evidence_classes": ["E2"],
                "dependencies": [],
            },
            {
                "id": "R2",
                "key": "judge.freeze_on_conflict",
                "value": True,
                "authority": "DOC_B",
                "scope": "CURRENT_GOVERNING_LAW",
                "accepted_evidence_classes": ["E2", "E3"],
                "dependencies": ["R1"],
            },
        ],
        "evidence": [
            {
                "id": "EV1",
                "requirement_id": "R1",
                "class": "E2",
                "status": "PASS",
                "target_revision": "abc123",
                "target_digest": "sha256:target",
                "provenance": "unit:test_auth_ttl",
            },
            {
                "id": "EV2",
                "requirement_id": "R2",
                "class": "E3",
                "status": "PASS",
                "target_revision": "abc123",
                "target_digest": "sha256:target",
                "provenance": "integration:test_conflict_freeze",
            },
        ],
    }


class CanonicalTests(unittest.TestCase):
    def test_canonical_json_key_order_is_stable(self) -> None:
        self.assertEqual(canonical_json({"b": 2, "a": 1}), canonical_json({"a": 1, "b": 2}))

    def test_non_finite_float_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            canonical_json({"x": float("nan")})

    def test_digest_has_algorithm_prefix(self) -> None:
        self.assertTrue(sha256_digest({"x": 1}).startswith("sha256:"))


class EngineTests(unittest.TestCase):
    def test_happy_path_passes(self) -> None:
        decision = evaluate_snapshot(Snapshot.from_dict(base_payload()))
        self.assertEqual(decision.verdict, TruthStatus.PASS)
        self.assertEqual(decision.action, GateAction.ACCEPT_ADVISORY)

    def test_input_order_does_not_change_decision_digest(self) -> None:
        first = base_payload()
        second = base_payload()
        second["requirements"] = list(reversed(second["requirements"]))
        second["evidence"] = list(reversed(second["evidence"]))
        d1 = evaluate_snapshot(Snapshot.from_dict(first))
        d2 = evaluate_snapshot(Snapshot.from_dict(second))
        self.assertEqual(d1.decision_digest, d2.decision_digest)
        self.assertEqual(d1.input_digest, d2.input_digest)

    def test_higher_authority_shadows_lower_value(self) -> None:
        payload = base_payload()
        payload["requirements"].append(
            {
                "id": "R1_OLD",
                "key": "auth.otac.ttl_ms",
                "value": 900000,
                "authority": "DOC_D",
                "scope": "SUPPORTED_PRODUCT_DESIGN",
                "accepted_evidence_classes": ["E2"],
                "dependencies": [],
            }
        )
        payload["evidence"].append(
            {
                "id": "EV_OLD",
                "requirement_id": "R1_OLD",
                "class": "E2",
                "status": "FAIL",
                "target_revision": "abc123",
                "target_digest": "sha256:target",
            }
        )
        decision = evaluate_snapshot(Snapshot.from_dict(payload))
        self.assertEqual(decision.verdict, TruthStatus.PASS)
        self.assertTrue(any(x.code == "SHADOWED_LOWER_AUTHORITY" for x in decision.findings))

    def test_same_top_authority_conflict_freezes(self) -> None:
        payload = base_payload()
        payload["requirements"].append(
            {
                "id": "R1_CONFLICT",
                "key": "auth.otac.ttl_ms",
                "value": 600000,
                "authority": "DOC_C",
                "scope": "CURRENT_BUILD",
                "accepted_evidence_classes": ["E2"],
                "dependencies": [],
            }
        )
        decision = evaluate_snapshot(Snapshot.from_dict(payload))
        self.assertEqual(decision.verdict, TruthStatus.CONFLICT)
        self.assertEqual(decision.action, GateAction.FREEZE_RECOMMENDED)

    def test_stale_evidence_does_not_pass(self) -> None:
        payload = base_payload()
        payload["evidence"][0]["target_revision"] = "older"
        decision = evaluate_snapshot(Snapshot.from_dict(payload))
        self.assertEqual(decision.verdict, TruthStatus.NOT_VERIFIED)
        self.assertTrue(any(x.code == "STALE_EVIDENCE_PRESENT" for x in decision.findings))

    def test_wrong_evidence_class_does_not_substitute(self) -> None:
        payload = base_payload()
        payload["evidence"][0]["class"] = "E7"
        decision = evaluate_snapshot(Snapshot.from_dict(payload))
        self.assertEqual(decision.verdict, TruthStatus.NOT_VERIFIED)

    def test_explicit_current_failure_fails_gate(self) -> None:
        payload = base_payload()
        payload["evidence"][1]["status"] = "FAIL"
        decision = evaluate_snapshot(Snapshot.from_dict(payload))
        self.assertEqual(decision.verdict, TruthStatus.FAIL)

    def test_unknown_authority_blocks(self) -> None:
        payload = base_payload()
        payload["requirements"][0]["authority"] = "ALIEN_SPEC"
        decision = evaluate_snapshot(Snapshot.from_dict(payload))
        self.assertEqual(decision.verdict, TruthStatus.BLOCKED)

    def test_duplicate_nonidentical_requirement_id_blocks(self) -> None:
        payload = base_payload()
        duplicate = dict(payload["requirements"][0])
        duplicate["value"] = 123
        payload["requirements"].append(duplicate)
        decision = evaluate_snapshot(Snapshot.from_dict(payload))
        self.assertEqual(decision.verdict, TruthStatus.BLOCKED)
        self.assertTrue(any(x.code == "DUPLICATE_REQUIREMENT_ID" for x in decision.findings))


    def test_identical_duplicate_requirement_id_still_blocks(self) -> None:
        payload = base_payload()
        payload["requirements"].append(json.loads(json.dumps(payload["requirements"][0])))
        decision = evaluate_snapshot(Snapshot.from_dict(payload))
        self.assertEqual(decision.verdict, TruthStatus.BLOCKED)

    def test_same_top_authority_same_value_but_different_obligation_conflicts(self) -> None:
        payload = base_payload()
        variant = json.loads(json.dumps(payload["requirements"][0]))
        variant["id"] = "R1_VARIANT"
        variant["accepted_evidence_classes"] = ["E3"]
        payload["requirements"].append(variant)
        decision = evaluate_snapshot(Snapshot.from_dict(payload))
        self.assertEqual(decision.verdict, TruthStatus.CONFLICT)

    def test_orphan_evidence_blocks(self) -> None:
        payload = base_payload()
        payload["evidence"].append(
            {
                "id": "EV_ORPHAN",
                "requirement_id": "NOPE",
                "class": "E1",
                "status": "PASS",
                "target_revision": "abc123",
                "target_digest": "sha256:target",
            }
        )
        decision = evaluate_snapshot(Snapshot.from_dict(payload))
        self.assertEqual(decision.verdict, TruthStatus.BLOCKED)

    def test_dependency_cycle_blocks(self) -> None:
        payload = base_payload()
        payload["requirements"][0]["dependencies"] = ["R2"]
        decision = evaluate_snapshot(Snapshot.from_dict(payload))
        self.assertEqual(decision.verdict, TruthStatus.BLOCKED)
        self.assertTrue(any(x.code == "DEPENDENCY_CYCLE" for x in decision.findings))

    def test_non_gating_scope_does_not_require_evidence(self) -> None:
        payload = base_payload()
        payload["requirements"].append(
            {
                "id": "RFUTURE",
                "key": "robotics.future.example",
                "value": {"concept": True},
                "authority": "CONTEXT",
                "scope": "DEFERRED_FUTURE",
                "accepted_evidence_classes": ["E7"],
                "dependencies": [],
            }
        )
        decision = evaluate_snapshot(Snapshot.from_dict(payload))
        self.assertEqual(decision.verdict, TruthStatus.PASS)
        self.assertIn("RFUTURE", decision.non_gating_requirements)


class ImpactTests(unittest.TestCase):
    def test_change_propagates_to_dependents_and_invalidates_evidence(self) -> None:
        before_payload = base_payload()
        after_payload = json.loads(json.dumps(before_payload))
        after_payload["requirements"][0]["value"] = 299999
        report = diff_snapshots(Snapshot.from_dict(before_payload), Snapshot.from_dict(after_payload))
        self.assertEqual(report.changed_requirement_ids, ("R1",))
        self.assertEqual(report.transitively_impacted_ids, ("R1", "R2"))
        self.assertEqual(report.evidence_ids_to_invalidate, ("EV1", "EV2"))


    def test_diff_digest_is_invariant_to_input_list_order(self) -> None:
        first = base_payload()
        second = json.loads(json.dumps(first))
        second["requirements"] = list(reversed(second["requirements"]))
        second["evidence"] = list(reversed(second["evidence"]))
        report = diff_snapshots(Snapshot.from_dict(first), Snapshot.from_dict(second))
        self.assertEqual(report.before_digest, report.after_digest)
        self.assertEqual(report.transitively_impacted_ids, ())

    def test_target_change_invalidates_all_current_evidence(self) -> None:
        before_payload = base_payload()
        after_payload = json.loads(json.dumps(before_payload))
        after_payload["target"]["revision"] = "def456"
        report = diff_snapshots(Snapshot.from_dict(before_payload), Snapshot.from_dict(after_payload))
        self.assertTrue(report.target_changed)
        self.assertEqual(report.transitively_impacted_ids, ("R1", "R2"))
        self.assertEqual(report.evidence_ids_to_invalidate, ("EV1", "EV2"))


class ValidationTests(unittest.TestCase):
    def test_unsupported_snapshot_version_rejected(self) -> None:
        payload = base_payload()
        payload["snapshot_version"] = "2.0"
        with self.assertRaises(ValueError):
            Snapshot.from_dict(payload)


    def test_unknown_scope_rejected(self) -> None:
        payload = base_payload()
        payload["requirements"][0]["scope"] = "MAYBE_CURRENT"
        with self.assertRaises(ValueError):
            Snapshot.from_dict(payload)

    def test_invalid_evidence_class_rejected(self) -> None:
        payload = base_payload()
        payload["evidence"][0]["class"] = "E99"
        with self.assertRaises(ValueError):
            Snapshot.from_dict(payload)


if __name__ == "__main__":
    unittest.main()
