import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from types import SimpleNamespace
from nexy_aqt.common import ContractError, canonical_json, pointer_tokens, resolve_pointer
from nexy_aqt.counterexample import distill
from nexy_aqt.example_linter import lint_examples
from nexy_aqt.freshness import plan_revalidation
from nexy_aqt.recovery import plan_recovery
from nexy_aqt.unsat_core import find_minimal_core
from nexy_aqt import cli as cli_module

n = SimpleNamespace(
    ContractError=ContractError, canonical_json=canonical_json, pointer_tokens=pointer_tokens,
    resolve_pointer=resolve_pointer, distill=distill, lint_examples=lint_examples,
    plan_revalidation=plan_revalidation, plan_recovery=plan_recovery, find_minimal_core=find_minimal_core,
    __file__=cli_module.__file__,
)


class CoreTests(unittest.TestCase):
    def test_canonical_order_independent(self):
        self.assertEqual(n.canonical_json({"b": 2, "a": 1}), '{"a":1,"b":2}')

    def test_pointer_escape(self):
        self.assertEqual(n.resolve_pointer({"a/b": {"~x": 7}}, "/a~1b/~0x"), 7)

    def test_bad_pointer(self):
        with self.assertRaises(n.ContractError): n.pointer_tokens("bad")


class CounterexampleTests(unittest.TestCase):
    def base(self):
        return {"case":{"status":"FAIL","trace":{"id":"t-1","noise":[1,2]},"junk":"x"},
                "interesting_when":[{"id":"fail","path":"/status","op":"eq","value":"FAIL"}],
                "protected_paths":["/trace/id"]}

    def test_reduces(self):
        r=n.distill(self.base())
        self.assertEqual(r["status"],"PASS")
        self.assertEqual(r["reduced_case"]["trace"]["id"],"t-1")
        self.assertNotIn("junk",r["reduced_case"])

    def test_deterministic(self):
        self.assertEqual(n.distill(self.base()), n.distill(self.base()))

    def test_missing_protected_rejected(self):
        p=self.base(); p["protected_paths"]=["/missing"]
        with self.assertRaises(n.ContractError): n.distill(p)

    def test_baseline_not_interesting(self):
        p=self.base(); p["case"]["status"]="PASS"
        self.assertEqual(n.distill(p)["status"],"FREEZE")


class UnsatTests(unittest.TestCase):
    def test_min_core(self):
        p={"candidates":[{"latency":5,"region":"remote"},{"latency":20,"region":"local"}],
           "constraints":[{"id":"fast","path":"/latency","op":"lte","value":10},
                          {"id":"local","path":"/region","op":"eq","value":"local"}]}
        r=n.find_minimal_core(p)
        self.assertEqual(r["status"],"FREEZE")
        self.assertEqual(r["minimal_unsat_core"],["fast","local"])

    def test_feasible(self):
        p={"candidates":[{"x":1}],"constraints":[{"id":"one","path":"/x","op":"eq","value":1}]}
        self.assertEqual(n.find_minimal_core(p)["status"],"PASS")

    def test_bound(self):
        p={"candidates":[{"x":1}],"max_constraints":1,"constraints":[
           {"id":"a","path":"/x","op":"eq","value":1},{"id":"b","path":"/x","op":"eq","value":2}]}
        with self.assertRaises(n.ContractError): n.find_minimal_core(p)


class FreshnessTests(unittest.TestCase):
    def test_version_propagation(self):
        p={"now":"2026-10-05T02:00:00+07:00","current_versions":{"spec":"v2"},"artifacts":[
           {"id":"unit","observed_at":"2026-10-05T01:50:00+07:00","max_age_seconds":3600,"captured_versions":{"spec":"v1"},"depends_on_artifacts":[]},
           {"id":"integration","observed_at":"2026-10-05T01:55:00+07:00","max_age_seconds":3600,"captured_versions":{"spec":"v2"},"depends_on_artifacts":["unit"]}]}
        r=n.plan_revalidation(p)
        self.assertEqual(r["status"],"FREEZE")
        self.assertEqual(r["revalidation_order"],["unit","integration"])

    def test_future_observation_freezes(self):
        p={"now":"2026-10-05T02:00:00+07:00","current_versions":{},"artifacts":[{"id":"x","observed_at":"2026-10-05T02:01:00+07:00","max_age_seconds":3600,"captured_versions":{},"depends_on_artifacts":[]}]}
        r=n.plan_revalidation(p)
        self.assertIn("OBSERVED_IN_FUTURE",r["stale"]["x"])

    def test_cycle_rejected(self):
        p={"now":"2026-10-05T02:00:00+07:00","current_versions":{},"artifacts":[
           {"id":"a","observed_at":"2026-10-05T01:59:00+07:00","max_age_seconds":3600,"captured_versions":{},"depends_on_artifacts":["b"]},
           {"id":"b","observed_at":"2026-10-05T01:59:00+07:00","max_age_seconds":3600,"captured_versions":{},"depends_on_artifacts":["a"]}]}
        with self.assertRaises(n.ContractError): n.plan_revalidation(p)


class LinterTests(unittest.TestCase):
    def test_contradiction(self):
        p={"rules":[{"id":"verified","path":"/verified","op":"eq","value":True}],"examples":[
           {"id":"good","expected":"PASS","data":{"verified":True}},
           {"id":"bad-doc","expected":"PASS","data":{"verified":False}}]}
        r=n.lint_examples(p)
        self.assertEqual(r["status"],"FAIL")
        self.assertEqual(r["findings"][0]["example_id"],"bad-doc")

    def test_consistent(self):
        p={"rules":[{"id":"ok","path":"/x","op":"eq","value":1}],"examples":[
           {"id":"a","expected":"PASS","data":{"x":1}},{"id":"b","expected":"FREEZE","data":{"x":2}}]}
        self.assertEqual(n.lint_examples(p)["status"],"PASS")


class RecoveryTests(unittest.TestCase):
    def payload(self):
        return {"states":["broken","restored","safe"],"current_state":"broken","safe_states":["safe"],
                "available_evidence":["snapshot","checks"],"transitions":[
                  {"id":"restore-snapshot","from":"broken","to":"restored","requires_evidence":["snapshot"]},
                  {"id":"revalidate","from":"restored","to":"safe","requires_evidence":["checks"]}]}

    def test_shortest_path(self):
        self.assertEqual(n.plan_recovery(self.payload())["chosen_path"],["restore-snapshot","revalidate"])

    def test_missing_evidence_freezes(self):
        p=self.payload(); p["available_evidence"]=["snapshot"]
        self.assertEqual(n.plan_recovery(p)["status"],"FREEZE")

    def test_already_safe(self):
        p=self.payload(); p["current_state"]="safe"
        self.assertEqual(n.plan_recovery(p)["reason_codes"],["ALREADY_SAFE"])

    def test_step_bound(self):
        p=self.payload(); p["max_steps"]=65
        with self.assertRaises(n.ContractError): n.plan_recovery(p)


class CliTests(unittest.TestCase):
    def test_invalid_json_freezes(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"in.json"; path.write_text("{")
            cp=subprocess.run([sys.executable,"-m","nexy_aqt.cli","recovery",str(path)],text=True,capture_output=True)
            self.assertEqual(cp.returncode,2)
            self.assertEqual(json.loads(cp.stderr)["status"],"FREEZE")

    def test_unsat_cli(self):
        p={"candidates":[{"x":1}],"constraints":[{"id":"x2","path":"/x","op":"eq","value":2}]}
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"in.json"; path.write_text(json.dumps(p))
            cp=subprocess.run([sys.executable,"-m","nexy_aqt.cli","unsat-core",str(path)],text=True,capture_output=True)
            self.assertEqual(cp.returncode,0)
            self.assertEqual(json.loads(cp.stdout)["status"],"FREEZE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
