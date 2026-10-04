from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from nexy_signal_intelligence import (  # noqa: E402
    AckRecord,
    Delivery,
    EvidenceState,
    OperatorSignal,
    Salience,
    Severity,
    SignalKind,
    build_ack_debt,
    classify_salience,
    compile_outcome_delta,
    compress_milestones,
    route_signal,
)


def sig(
    signal_id: str,
    sequence: int,
    *,
    component: str = "core",
    kind: SignalKind = SignalKind.INFO,
    severity: Severity = Severity.NORMAL,
    evidence: EvidenceState = EvidenceState.PASS,
    state: str = "RUNNING",
    message: str = "",
    requires_user: bool = False,
    blocking: bool = False,
    state_changed: bool = False,
    evidence_changed: bool = False,
    requires_ack: bool = False,
) -> OperatorSignal:
    return OperatorSignal(
        signal_id=signal_id,
        sequence=sequence,
        component=component,
        kind=kind,
        severity=severity,
        evidence=evidence,
        state=state,
        message=message,
        requires_user=requires_user,
        blocking=blocking,
        state_changed=state_changed,
        evidence_changed=evidence_changed,
        requires_ack=requires_ack,
    )


class ModelTests(unittest.TestCase):
    def test_from_dict_rejects_missing(self) -> None:
        with self.assertRaises(ValueError):
            OperatorSignal.from_dict({})

    def test_from_dict_rejects_bool_sequence(self) -> None:
        raw = sig("a", 1).canonical_dict()
        raw["sequence"] = True
        with self.assertRaises(ValueError):
            OperatorSignal.from_dict(raw)

    def test_from_dict_round_trip(self) -> None:
        original = sig("a", 1, kind=SignalKind.WARNING, state_changed=True)
        self.assertEqual(OperatorSignal.from_dict(original.canonical_dict()), original)


class SalienceTests(unittest.TestCase):
    def test_freeze_is_critical(self) -> None:
        decision = classify_salience(sig("f", 1, kind=SignalKind.FREEZE, severity=Severity.LOW))
        self.assertEqual(decision.salience, Salience.CRITICAL)

    def test_security_is_critical(self) -> None:
        self.assertEqual(classify_salience(sig("s", 1, kind=SignalKind.SECURITY)).salience, Salience.CRITICAL)

    def test_blocking_conflict_is_critical(self) -> None:
        x = sig("c", 1, evidence=EvidenceState.CONFLICT, blocking=True)
        self.assertEqual(classify_salience(x).salience, Salience.CRITICAL)

    def test_user_decision_is_high(self) -> None:
        x = sig("d", 1, kind=SignalKind.DECISION_REQUIRED, requires_user=True)
        self.assertEqual(classify_salience(x).salience, Salience.HIGH)

    def test_state_change_is_normal(self) -> None:
        self.assertEqual(classify_salience(sig("n", 1, state_changed=True)).salience, Salience.NORMAL)

    def test_routine_is_low(self) -> None:
        self.assertEqual(classify_salience(sig("l", 1)).salience, Salience.LOW)

    def test_salience_is_deterministic(self) -> None:
        x = sig("x", 3, requires_user=True)
        self.assertEqual(classify_salience(x).fingerprint, classify_salience(x).fingerprint)


class RoutingTests(unittest.TestCase):
    def test_quiet_cannot_silence_freeze(self) -> None:
        x = sig("f", 1, kind=SignalKind.FREEZE)
        self.assertEqual(route_signal(x, quiet_mode=True).delivery, Delivery.NOW)

    def test_quiet_silences_routine_low(self) -> None:
        self.assertEqual(route_signal(sig("i", 1), quiet_mode=True).delivery, Delivery.SILENT_LOG)

    def test_ack_signal_stays_visible(self) -> None:
        x = sig("a", 1, requires_ack=True)
        self.assertEqual(route_signal(x, quiet_mode=True).delivery, Delivery.BATCH)

    def test_user_required_is_now(self) -> None:
        x = sig("u", 1, requires_user=True)
        self.assertEqual(route_signal(x, quiet_mode=False).delivery, Delivery.NOW)

    def test_normal_is_batched(self) -> None:
        x = sig("w", 1, kind=SignalKind.WARNING)
        self.assertEqual(route_signal(x).delivery, Delivery.BATCH)


class CompressionTests(unittest.TestCase):
    def test_duplicate_routine_events_collapse(self) -> None:
        events = [sig("a", 1), sig("b", 2), sig("c", 3)]
        result = compress_milestones(events)
        self.assertEqual(result.input_count, 3)
        self.assertEqual(result.output_count, 1)
        self.assertEqual(result.milestones[0].collapsed_before, 0)
        self.assertEqual(result.trailing_collapsed, 2)

    def test_state_transition_retained(self) -> None:
        events = [sig("a", 1), sig("b", 2, state="VERIFYING", state_changed=True)]
        self.assertEqual(compress_milestones(events).output_count, 2)

    def test_critical_retained_even_same_state(self) -> None:
        events = [sig("a", 1), sig("b", 2, kind=SignalKind.SECURITY, state="RUNNING")]
        self.assertEqual(compress_milestones(events).output_count, 2)

    def test_completion_retained(self) -> None:
        events = [sig("a", 1), sig("b", 2, kind=SignalKind.COMPLETION)]
        self.assertEqual(compress_milestones(events).output_count, 2)

    def test_duplicate_sequences_rejected(self) -> None:
        with self.assertRaises(ValueError):
            compress_milestones([sig("a", 1), sig("b", 1)])

    def test_duplicate_ids_rejected(self) -> None:
        with self.assertRaises(ValueError):
            compress_milestones([sig("a", 1), sig("a", 2)])

    def test_order_is_normalized_by_sequence(self) -> None:
        a = compress_milestones([sig("b", 2), sig("a", 1)]).as_dict()
        b = compress_milestones([sig("a", 1), sig("b", 2)]).as_dict()
        self.assertEqual(a, b)


class DeltaTests(unittest.TestCase):
    def test_nested_changes(self) -> None:
        result = compile_outcome_delta({"a": {"x": 1}}, {"a": {"x": 2, "y": 3}})
        kinds = {(e.path, e.kind.value) for e in result.entries}
        self.assertIn(("/a/x", "CHANGED"), kinds)
        self.assertIn(("/a/y", "ADDED"), kinds)

    def test_removed(self) -> None:
        result = compile_outcome_delta({"a": 1}, {})
        self.assertEqual(result.entries[0].kind.value, "REMOVED")

    def test_list_diff(self) -> None:
        result = compile_outcome_delta([1, 2], [1, 3, 4])
        self.assertEqual([(e.path, e.kind.value) for e in result.entries], [("/1", "CHANGED"), ("/2", "ADDED")])

    def test_unknown_is_not_claimed_as_change(self) -> None:
        unknown = {"$nexy_state": "UNKNOWN"}
        result = compile_outcome_delta({"x": unknown}, {"x": 4})
        self.assertEqual(result.entries[0].kind.value, "UNKNOWN")

    def test_redaction_hides_value(self) -> None:
        result = compile_outcome_delta({"secret": "old"}, {"secret": "new"}, redact_paths=["/secret"])
        self.assertEqual(result.entries[0].before, "[REDACTED]")
        self.assertEqual(result.entries[0].after, "[REDACTED]")

    def test_pointer_escape(self) -> None:
        result = compile_outcome_delta({"a/b": 1, "x~y": 1}, {"a/b": 2, "x~y": 2})
        self.assertEqual([e.path for e in result.entries], ["/a~1b", "/x~0y"])

    def test_root_redaction_hides_every_changed_value(self) -> None:
        result = compile_outcome_delta({"x": 1}, {"x": 2}, redact_paths=[""])
        self.assertEqual(result.entries[0].before, "[REDACTED]")
        self.assertEqual(result.entries[0].after, "[REDACTED]")

    def test_invalid_redaction_rejected(self) -> None:
        with self.assertRaises(ValueError):
            compile_outcome_delta({}, {}, redact_paths=["not-a-pointer"])

    def test_equal_data_has_no_entries_but_stable_hash(self) -> None:
        result = compile_outcome_delta({"b": 2, "a": 1}, {"a": 1, "b": 2})
        self.assertEqual(result.entries, ())
        self.assertEqual(result.before_hash, result.after_hash)


class DebtTests(unittest.TestCase):
    def test_non_ack_signals_do_not_create_debt(self) -> None:
        result = build_ack_debt([sig("x", 1)], [], current_sequence=20)
        self.assertEqual(result.items, ())
        self.assertTrue(result.all_clear)

    def test_critical_unacked_blocks_all_clear(self) -> None:
        x = sig("x", 1, severity=Severity.CRITICAL, requires_ack=True)
        result = build_ack_debt([x], [], current_sequence=1)
        self.assertFalse(result.all_clear)
        self.assertEqual(result.items[0].state.value, "ACTIVE")

    def test_overdue_uses_logical_sequence(self) -> None:
        x = sig("x", 1, severity=Severity.CRITICAL, requires_ack=True)
        result = build_ack_debt([x], [], current_sequence=3)
        self.assertEqual(result.items[0].state.value, "OVERDUE")

    def test_ack_clears_critical(self) -> None:
        x = sig("x", 1, severity=Severity.CRITICAL, requires_ack=True)
        result = build_ack_debt([x], [AckRecord("x", 2)], current_sequence=2)
        self.assertTrue(result.all_clear)
        self.assertEqual(result.items[0].state.value, "ACKNOWLEDGED")

    def test_ack_unknown_rejected(self) -> None:
        with self.assertRaises(ValueError):
            build_ack_debt([], [AckRecord("x", 1)], current_sequence=1)

    def test_ack_before_signal_rejected(self) -> None:
        x = sig("x", 4, requires_ack=True)
        with self.assertRaises(ValueError):
            build_ack_debt([x], [AckRecord("x", 3)], current_sequence=4)

    def test_future_signal_rejected(self) -> None:
        x = sig("x", 5, requires_ack=True)
        with self.assertRaises(ValueError):
            build_ack_debt([x], [], current_sequence=4)

    def test_budget_must_cover_all_severities(self) -> None:
        with self.assertRaises(ValueError):
            build_ack_debt([], [], current_sequence=1, budget={Severity.LOW: 1})


class CliTests(unittest.TestCase):
    def run_cli(self, command: str, payload: object) -> tuple[int, dict[str, object]]:
        env = dict(os.environ)
        env["PYTHONPATH"] = str(SRC)
        proc = subprocess.run(
            [sys.executable, "-m", "nexy_signal_intelligence", command],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )
        return proc.returncode, json.loads(proc.stdout)

    def test_cli_classify(self) -> None:
        code, out = self.run_cli("classify", sig("x", 1, kind=SignalKind.FREEZE).canonical_dict())
        self.assertEqual(code, 0)
        self.assertEqual(out["result"]["salience"], "CRITICAL")

    def test_cli_route(self) -> None:
        code, out = self.run_cli("route", {"signal": sig("x", 1).canonical_dict(), "quiet_mode": True})
        self.assertEqual(code, 0)
        self.assertEqual(out["result"]["delivery"], "SILENT_LOG")

    def test_cli_compress(self) -> None:
        code, out = self.run_cli("compress", {"signals": [sig("a", 1).canonical_dict(), sig("b", 2).canonical_dict()]})
        self.assertEqual(code, 0)
        self.assertEqual(out["result"]["output_count"], 1)

    def test_cli_delta(self) -> None:
        code, out = self.run_cli("delta", {"before": {"x": 1}, "after": {"x": 2}})
        self.assertEqual(code, 0)
        self.assertEqual(out["result"]["entries"][0]["kind"], "CHANGED")

    def test_cli_debt(self) -> None:
        payload = {"signals": [sig("x", 1, severity=Severity.HIGH, requires_ack=True).canonical_dict()], "acknowledgements": [], "current_sequence": 1}
        code, out = self.run_cli("debt", payload)
        self.assertEqual(code, 0)
        self.assertFalse(out["result"]["all_clear"])

    def test_cli_invalid_freezes(self) -> None:
        code, out = self.run_cli("classify", {"bad": "input"})
        self.assertEqual(code, 2)
        self.assertEqual(out["status"], "FREEZE")

    def test_cli_output_is_byte_stable(self) -> None:
        payload = {"before": {"b": 2, "a": 1}, "after": {"a": 1, "b": 3}}
        code1, out1 = self.run_cli("delta", payload)
        code2, out2 = self.run_cli("delta", payload)
        self.assertEqual(code1, code2)
        self.assertEqual(out1, out2)


class AdditionalBoundaryTests(unittest.TestCase):
    def test_model_field_validation(self) -> None:
        base = sig("x", 1).canonical_dict()
        for key, bad in (("signal_id", ""), ("component", ""), ("state", ""), ("message", 7), ("requires_user", "yes")):
            raw = dict(base)
            raw[key] = bad
            with self.subTest(key=key), self.assertRaises(ValueError):
                OperatorSignal.from_dict(raw)

    def test_model_enum_validation(self) -> None:
        raw = sig("x", 1).canonical_dict()
        raw["kind"] = "BOGUS"
        with self.assertRaises(ValueError):
            OperatorSignal.from_dict(raw)

    def test_salience_explicit_severity_branches(self) -> None:
        self.assertEqual(classify_salience(sig("c", 1, severity=Severity.CRITICAL)).salience, Salience.CRITICAL)
        self.assertEqual(classify_salience(sig("h", 2, severity=Severity.HIGH)).salience, Salience.HIGH)
        self.assertEqual(classify_salience(sig("b", 3, blocking=True)).salience, Salience.HIGH)
        self.assertEqual(classify_salience(sig("e", 4, kind=SignalKind.ERROR)).salience, Salience.HIGH)
        self.assertEqual(classify_salience(sig("v", 5, evidence_changed=True)).salience, Salience.NORMAL)
        self.assertEqual(classify_salience(sig("w", 6, kind=SignalKind.WARNING)).salience, Salience.NORMAL)

    def test_empty_compression(self) -> None:
        result = compress_milestones([])
        self.assertEqual(result.input_count, 0)
        self.assertEqual(result.output_count, 0)
        self.assertEqual(result.trailing_collapsed, 0)

    def test_delta_list_removal_and_scalar_root(self) -> None:
        removed = compile_outcome_delta([1, 2], [1])
        self.assertEqual((removed.entries[0].path, removed.entries[0].kind.value), ("/1", "REMOVED"))
        root = compile_outcome_delta(1, 2)
        self.assertEqual((root.entries[0].path, root.entries[0].kind.value), ("", "CHANGED"))

    def test_equal_unknown_marker_has_no_delta(self) -> None:
        x = {"$nexy_state": "UNKNOWN"}
        self.assertEqual(compile_outcome_delta(x, x).entries, ())

    def test_ack_record_validation_and_roundtrip(self) -> None:
        self.assertEqual(AckRecord.from_dict({"signal_id": "x", "sequence": 2}), AckRecord("x", 2))
        for raw in ({"signal_id": "", "sequence": 2}, {"signal_id": "x", "sequence": True}):
            with self.assertRaises(ValueError):
                AckRecord.from_dict(raw)

    def test_debt_validation_edges(self) -> None:
        x = sig("x", 2, requires_ack=True)
        with self.assertRaises(ValueError):
            build_ack_debt([x], [], current_sequence=True)
        bad_budget = {sev: 1 for sev in Severity}
        bad_budget[Severity.LOW] = -1
        with self.assertRaises(ValueError):
            build_ack_debt([], [], current_sequence=0, budget=bad_budget)
        with self.assertRaises(ValueError):
            build_ack_debt([x, x], [], current_sequence=2)
        with self.assertRaises(ValueError):
            build_ack_debt([x], [AckRecord("x", 2), AckRecord("x", 2)], current_sequence=2)
        with self.assertRaises(ValueError):
            build_ack_debt([x], [AckRecord("x", 3)], current_sequence=2)

    def test_debt_snapshot_dict(self) -> None:
        x = sig("x", 1, severity=Severity.LOW, requires_ack=True)
        result = build_ack_debt([x], [], current_sequence=1)
        data = result.as_dict()
        self.assertEqual(data["current_sequence"], 1)
        self.assertTrue(data["all_clear"])
        self.assertEqual(data["items"][0]["state"], "ACTIVE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
