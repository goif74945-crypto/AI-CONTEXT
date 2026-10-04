from __future__ import annotations

import json
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from nexy_model_conformance.canonical import canonical_json, sha256_hex
from nexy_model_conformance.engine import ConformanceEngine
from nexy_model_conformance.errors import CanonicalizationError, ContractError
from nexy_model_conformance.jsonpath import resolve_path
from nexy_model_conformance.model import CaseContract, Observation, ProviderManifest, Status


class HarnessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = ProviderManifest.from_dict(
            {
                "provider_id": "provider-a",
                "model_id": "model-x",
                "adapter_version": "1.2.3",
                "capabilities": ["structured_output", "evidence_envelope"],
            }
        )
        self.case_raw = {
            "case_id": "CASE-001",
            "request": {"task": "classify", "input": "alpha"},
            "required_capabilities": ["structured_output", "evidence_envelope"],
            "invariants": [
                {"kind": "exists", "path": "data.answer"},
                {"kind": "type", "path": "data.answer", "value": "string"},
                {"kind": "equals", "path": "status", "value": "PASS"},
                {"kind": "min_evidence", "minimum": 2},
                {"kind": "no_sensitive_keys"},
            ],
            "deterministic_paths": ["status", "data.answer"],
            "cross_provider_paths": ["status", "data.answer"],
            "min_observations": 2,
        }
        self.case = CaseContract.from_dict(self.case_raw)
        self.request_hash = sha256_hex(self.case.request)

    def observation(self, obs_id: str, *, answer: str = "A", provider_ref: str | None = None, output=None):
        return Observation.from_dict(
            {
                "observation_id": obs_id,
                "case_id": self.case.case_id,
                "provider_ref": provider_ref or self.manifest.ref,
                "request_hash": self.request_hash,
                "output": output if output is not None else {"status": "PASS", "data": {"answer": answer}},
                "evidence": [{"id": "e1", "hash": "h1"}, {"id": "e2", "hash": "h2"}],
                "trace_id": f"trace-{obs_id}",
            }
        )

    def test_canonical_hash_stable_across_object_order(self):
        a = {"b": [2, 3], "a": 1}
        b = {"a": 1, "b": [2, 3]}
        self.assertEqual(canonical_json(a), canonical_json(b))
        self.assertEqual(sha256_hex(a), sha256_hex(b))

    def test_canonical_rejects_non_finite_float(self):
        with self.assertRaises(CanonicalizationError):
            canonical_json({"x": math.nan})

    def test_path_grammar_rejects_expression_like_path(self):
        with self.assertRaises(ContractError):
            resolve_path({"a": [1]}, "a.[0]")

    def test_valid_replay_passes(self):
        report = ConformanceEngine().verify(self.manifest, self.case, [self.observation("o1"), self.observation("o2")])
        self.assertEqual(Status.PASS, report.status)
        self.assertEqual(2, report.observation_count)
        self.assertEqual(64, len(report.evidence_fingerprint))

    def test_missing_capability_fails(self):
        manifest = ProviderManifest.from_dict(
            {
                "provider_id": "provider-a",
                "model_id": "model-x",
                "adapter_version": "1.2.3",
                "capabilities": ["structured_output"],
            }
        )
        report = ConformanceEngine().verify(manifest, self.case, [
            self.observation("o1", provider_ref=manifest.ref),
            self.observation("o2", provider_ref=manifest.ref),
        ])
        self.assertEqual(Status.FAIL, report.status)
        self.assertIn("CAPABILITY_MISSING", {f.code for f in report.findings})

    def test_request_tampering_is_rejected(self):
        raw = {
            "observation_id": "o1",
            "case_id": self.case.case_id,
            "provider_ref": self.manifest.ref,
            "request_hash": "0" * 64,
            "output": {"status": "PASS", "data": {"answer": "A"}},
            "evidence": [{"id": "e1"}, {"id": "e2"}],
            "trace_id": "trace-o1",
        }
        bad = Observation.from_dict(raw)
        report = ConformanceEngine().verify(self.manifest, self.case, [bad, self.observation("o2")])
        self.assertEqual(Status.FAIL, report.status)
        self.assertIn("REQUEST_HASH_MISMATCH", {f.code for f in report.findings})

    def test_sensitive_key_in_output_fails(self):
        output = {"status": "PASS", "data": {"answer": "A", "api_key": "do-not-store"}}
        report = ConformanceEngine().verify(self.manifest, self.case, [
            self.observation("o1", output=output), self.observation("o2", output=output)
        ])
        self.assertEqual(Status.FAIL, report.status)
        self.assertIn("SENSITIVE_KEY_PRESENT", {f.code for f in report.findings})

    def test_deterministic_replay_mismatch_is_conflict(self):
        report = ConformanceEngine().verify(
            self.manifest,
            self.case,
            [self.observation("o1", answer="A"), self.observation("o2", answer="B")],
        )
        self.assertEqual(Status.CONFLICT, report.status)
        self.assertIn("DETERMINISTIC_REPLAY_CONFLICT", {f.code for f in report.findings})

    def test_cross_provider_conflict(self):
        other_ref = "provider-b/model-y@9"
        status, findings = ConformanceEngine().compare_reports(
            self.case,
            {
                self.manifest.ref: [self.observation("o1", answer="A")],
                other_ref: [self.observation("o2", answer="B", provider_ref=other_ref)],
            },
        )
        self.assertEqual(Status.CONFLICT, status)
        self.assertIn("CROSS_PROVIDER_CONFLICT", {f.code for f in findings})

    def test_insufficient_observations_not_verified(self):
        report = ConformanceEngine().verify(self.manifest, self.case, [self.observation("o1")])
        self.assertEqual(Status.NOT_VERIFIED, report.status)

    def test_cross_provider_rejects_wrong_request_binding(self):
        other_ref = "provider-b/model-y@9"
        bad = Observation.from_dict(
            {
                "observation_id": "bad",
                "case_id": self.case.case_id,
                "provider_ref": other_ref,
                "request_hash": "0" * 64,
                "output": {"status": "PASS", "data": {"answer": "A"}},
                "evidence": [],
                "trace_id": "bad-trace",
            }
        )
        status, findings = ConformanceEngine().compare_reports(
            self.case,
            {self.manifest.ref: [self.observation("o1")], other_ref: [bad]},
        )
        self.assertEqual(Status.FAIL, status)
        self.assertIn("REQUEST_HASH_MISMATCH", {f.code for f in findings})

    def test_observation_limit_fails_closed(self):
        engine = ConformanceEngine(max_observations=1)
        report = engine.verify(self.manifest, self.case, [self.observation("o1"), self.observation("o2")])
        self.assertEqual(Status.FAIL, report.status)
        self.assertIn("OBSERVATION_LIMIT_EXCEEDED", {f.code for f in report.findings})

    def test_size_limit_fails_closed(self):
        engine = ConformanceEngine(max_document_bytes=1024)
        output = {"status": "PASS", "data": {"answer": "A", "padding": "x" * 5000}}
        report = engine.verify(self.manifest, self.case, [self.observation("o1", output=output), self.observation("o2")])
        self.assertEqual(Status.FAIL, report.status)
        self.assertIn("OBSERVATION_SIZE_LIMIT_EXCEEDED", {f.code for f in report.findings})

    def test_boolean_is_not_integer(self):
        raw = dict(self.case_raw)
        raw["invariants"] = [{"kind": "type", "path": "data.n", "value": "integer"}]
        raw["min_observations"] = 1
        raw["deterministic_paths"] = []
        case = CaseContract.from_dict(raw)
        obs = Observation.from_dict(
            {
                "observation_id": "o1",
                "case_id": case.case_id,
                "provider_ref": self.manifest.ref,
                "request_hash": sha256_hex(case.request),
                "output": {"data": {"n": True}},
                "evidence": [],
                "trace_id": "t1",
            }
        )
        report = ConformanceEngine().verify(self.manifest, case, [obs])
        self.assertEqual(Status.FAIL, report.status)
        self.assertIn("TYPE_MISMATCH", {f.code for f in report.findings})

    def test_cli_verify_end_to_end(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manifest = {
                "provider_id": self.manifest.provider_id,
                "model_id": self.manifest.model_id,
                "adapter_version": self.manifest.adapter_version,
                "capabilities": sorted(self.manifest.capabilities),
            }
            docs = {
                "manifest.json": manifest,
                "case.json": self.case_raw,
            }
            docs["o1.json"] = {
                "observation_id": "o1", "case_id": self.case.case_id, "provider_ref": self.manifest.ref,
                "request_hash": self.request_hash, "output": {"status": "PASS", "data": {"answer": "A"}},
                "evidence": [{"id": "e1"}, {"id": "e2"}], "trace_id": "t1"
            }
            docs["o2.json"] = {
                "observation_id": "o2", "case_id": self.case.case_id, "provider_ref": self.manifest.ref,
                "request_hash": self.request_hash, "output": {"status": "PASS", "data": {"answer": "A"}},
                "evidence": [{"id": "e1"}, {"id": "e2"}], "trace_id": "t2"
            }
            for name, payload in docs.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, "-m", "nexy_model_conformance", "verify",
                 "--manifest", str(root / "manifest.json"), "--case", str(root / "case.json"),
                 "--observation", str(root / "o1.json"), "--observation", str(root / "o2.json")],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(0, proc.returncode, proc.stderr)
            payload = json.loads(proc.stdout)
            self.assertEqual("PASS", payload["status"])


if __name__ == "__main__":
    unittest.main()
