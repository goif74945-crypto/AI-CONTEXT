from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from nfwm.analyzer import analyze_trace
from nfwm.canonical import sha256_canonical
from nfwm.io import load_trace
from nfwm.minimize import minimize_violation, witness_is_one_minimal
from nfwm.model import Trace
from nfwm.profile import load_profile

PROFILE = load_profile(ROOT / "profiles" / "nexy-vnext-trace-profile.json")
FIX = ROOT / "tests" / "fixtures"


class AnalyzerTests(unittest.TestCase):
    def test_valid_trace_passes(self) -> None:
        result = analyze_trace(load_trace(FIX / "valid_trace.json"), PROFILE)
        self.assertTrue(result.passed)
        self.assertEqual(result.violations, ())

    def test_illegal_transition_fails(self) -> None:
        result = analyze_trace(load_trace(FIX / "illegal_transition.json"), PROFILE)
        self.assertIn("INV_FSM_TRANSITION", {v.code for v in result.violations})

    def test_freeze_without_incident_fails(self) -> None:
        raw = {
            "schema_version": "nfwm.trace.v1",
            "events": [
                {
                    "seq": 1,
                    "kind": "STATE_TRANSITION",
                    "trace_id": "t",
                    "request_id": "q",
                    "run_id": "r",
                    "state_from": "RUNNING",
                    "state_to": "FREEZE",
                }
            ],
        }
        result = analyze_trace(Trace.from_raw(raw), PROFILE)
        self.assertIn("INV_FREEZE_INCIDENT_LINK", {v.code for v in result.violations})

    def test_release_after_freeze_fails(self) -> None:
        result = analyze_trace(load_trace(FIX / "release_after_freeze.json"), PROFILE)
        self.assertIn("INV_RELEASE_AFTER_FREEZE", {v.code for v in result.violations})

    def test_duplicate_idempotency_fails(self) -> None:
        result = analyze_trace(load_trace(FIX / "duplicate_idempotency.json"), PROFILE)
        self.assertIn("INV_IDEMPOTENCY_REUSE", {v.code for v in result.violations})

    def test_non_increasing_sequence_fails(self) -> None:
        raw = {
            "schema_version": "nfwm.trace.v1",
            "events": [
                {"seq": 2, "kind": "NOISE", "trace_id": "t", "request_id": "q"},
                {"seq": 2, "kind": "NOISE", "trace_id": "t", "request_id": "q"},
            ],
        }
        result = analyze_trace(Trace.from_raw(raw), PROFILE)
        self.assertIn("INV_SEQUENCE_STRICT_INCREASE", {v.code for v in result.violations})

    def test_stop_is_terminal(self) -> None:
        raw = {
            "schema_version": "nfwm.trace.v1",
            "events": [
                {
                    "seq": 1,
                    "kind": "STATE_TRANSITION",
                    "trace_id": "t",
                    "request_id": "q",
                    "state_from": "STOP",
                    "state_to": "READY",
                }
            ],
        }
        result = analyze_trace(Trace.from_raw(raw), PROFILE)
        codes = {v.code for v in result.violations}
        self.assertIn("INV_STOP_TERMINAL", codes)
        self.assertIn("INV_FSM_TRANSITION", codes)


class MinimizerTests(unittest.TestCase):
    def test_release_after_freeze_minimizes_to_two_events(self) -> None:
        trace = load_trace(FIX / "release_after_freeze.json")
        witness = minimize_violation(trace.events, PROFILE, "INV_RELEASE_AFTER_FREEZE")
        self.assertEqual(len(witness.witness_events), 2)
        self.assertTrue(witness_is_one_minimal(witness, PROFILE))
        self.assertEqual([e.seq for e in witness.witness_events], [4, 6])

    def test_idempotency_minimizes_to_two_events(self) -> None:
        trace = load_trace(FIX / "duplicate_idempotency.json")
        witness = minimize_violation(trace.events, PROFILE, "INV_IDEMPOTENCY_REUSE")
        self.assertEqual(len(witness.witness_events), 2)
        self.assertTrue(witness_is_one_minimal(witness, PROFILE))
        self.assertEqual([e.seq for e in witness.witness_events], [1, 3])

    def test_single_event_violation_stays_single(self) -> None:
        trace = load_trace(FIX / "illegal_transition.json")
        witness = minimize_violation(trace.events, PROFILE, "INV_FSM_TRANSITION")
        self.assertEqual(len(witness.witness_events), 1)
        self.assertTrue(witness_is_one_minimal(witness, PROFILE))

    def test_deterministic_witness_hash(self) -> None:
        trace = load_trace(FIX / "release_after_freeze.json")
        a = minimize_violation(trace.events, PROFILE, "INV_RELEASE_AFTER_FREEZE")
        b = minimize_violation(trace.events, PROFILE, "INV_RELEASE_AFTER_FREEZE")
        self.assertEqual(a.witness_hash, b.witness_hash)
        self.assertEqual(a.to_raw(), b.to_raw())


class ValidationTests(unittest.TestCase):
    def test_unknown_event_field_rejected(self) -> None:
        with self.assertRaises(Exception):
            Trace.from_raw(
                {
                    "schema_version": "nfwm.trace.v1",
                    "events": [
                        {
                            "seq": 1,
                            "kind": "NOISE",
                            "trace_id": "t",
                            "request_id": "q",
                            "surprise": True,
                        }
                    ],
                }
            )

    def test_canonical_hash_key_order_independent(self) -> None:
        self.assertEqual(sha256_canonical({"a": 1, "b": 2}), sha256_canonical({"b": 2, "a": 1}))


class CLITests(unittest.TestCase):
    def _run(self, *args: str) -> subprocess.CompletedProcess[str]:
        env = dict(__import__("os").environ)
        env["PYTHONPATH"] = str(SRC)
        return subprocess.run(
            [sys.executable, "-m", "nfwm.cli", *args],
            cwd=ROOT,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_cli_valid_returns_zero(self) -> None:
        p = self._run(
            "analyze",
            str(FIX / "valid_trace.json"),
            "--profile",
            str(ROOT / "profiles" / "nexy-vnext-trace-profile.json"),
        )
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        self.assertEqual(out["status"], "PASS")

    def test_cli_failure_returns_two_and_witness(self) -> None:
        p = self._run(
            "analyze",
            str(FIX / "release_after_freeze.json"),
            "--profile",
            str(ROOT / "profiles" / "nexy-vnext-trace-profile.json"),
            "--minimize",
        )
        self.assertEqual(p.returncode, 2, p.stderr)
        out = json.loads(p.stdout)
        self.assertEqual(out["status"], "FAIL")
        witness = next(w for w in out["witnesses"] if w["violation_code"] == "INV_RELEASE_AFTER_FREEZE")
        self.assertEqual(witness["witness_event_count"], 2)

    def test_cli_witness_round_trip_verification(self) -> None:
        trace = load_trace(FIX / "release_after_freeze.json")
        witness = minimize_violation(trace.events, PROFILE, "INV_RELEASE_AFTER_FREEZE")
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "witness.json"
            path.write_text(json.dumps(witness.to_raw()), encoding="utf-8")
            p = self._run(
                "verify-witness",
                str(path),
                "--profile",
                str(ROOT / "profiles" / "nexy-vnext-trace-profile.json"),
            )
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(json.loads(p.stdout)["status"], "PASS")

    def test_cli_detects_tampered_witness_hash(self) -> None:
        trace = load_trace(FIX / "release_after_freeze.json")
        raw = minimize_violation(trace.events, PROFILE, "INV_RELEASE_AFTER_FREEZE").to_raw()
        raw["witness_hash"] = "0" * 64
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "witness.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            p = self._run(
                "verify-witness",
                str(path),
                "--profile",
                str(ROOT / "profiles" / "nexy-vnext-trace-profile.json"),
            )
            self.assertEqual(p.returncode, 3, p.stderr)
            out = json.loads(p.stdout)
            self.assertEqual(out["status"], "FAIL")
            self.assertFalse(out["hash_ok"])


if __name__ == "__main__":
    unittest.main()
