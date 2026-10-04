from __future__ import annotations

import math
import unittest

from nexy_aux.canonical import dumps
from nexy_aux.composition import compose
from nexy_aux.corrections import compile_correction, compile_corrections
from nexy_aux.distiller import distill
from nexy_aux.emergence import analyze_plan
from nexy_aux.portability import assess_portability


class HardeningTests(unittest.TestCase):
    def test_nonfinite_float_is_rejected_from_canonical_form(self) -> None:
        for value in (math.nan, math.inf, -math.inf):
            with self.assertRaises(ValueError):
                dumps({"x": value})

    def test_portability_freezes_if_any_context_dimension_is_ungoverned(self) -> None:
        evidence = {
            "claim_id": "C1",
            "evidence_class": "E2",
            "source_context": {"code_sha": "a", "runtime": "3.13"},
        }
        target = {
            "claim_id": "C1",
            "required_evidence_classes": ["E2"],
            "target_context": {"code_sha": "b", "runtime": "3.13"},
        }
        result = assess_portability(evidence, target, {"runtime": "MUST_EQUAL"})
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["reason"], "UNGOVERNED_PORTABILITY_DIMENSIONS")
        self.assertEqual(result["dimensions"], ["code_sha"])

    def test_portability_expires_at_exact_boundary(self) -> None:
        evidence = {
            "claim_id": "C1",
            "evidence_class": "E2",
            "source_context": {"code_sha": "a"},
            "expires_at": "2026-10-05T02:00:00+07:00",
        }
        target = {
            "claim_id": "C1",
            "required_evidence_classes": ["E2"],
            "target_context": {"code_sha": "a"},
            "evaluation_time": "2026-10-05T02:00:00+07:00",
        }
        result = assess_portability(evidence, target, {"code_sha": "MUST_EQUAL"})
        self.assertEqual(result["status"], "REVERIFY")

    def test_portability_rejects_evidence_evaluated_before_collection(self) -> None:
        evidence = {
            "claim_id": "C1",
            "evidence_class": "E2",
            "source_context": {"code_sha": "a"},
            "collected_at": "2026-10-05T02:00:00+07:00",
        }
        target = {
            "claim_id": "C1",
            "required_evidence_classes": ["E2"],
            "target_context": {"code_sha": "a"},
            "evaluation_time": "2026-10-05T01:59:59+07:00",
        }
        result = assess_portability(evidence, target, {"code_sha": "MUST_EQUAL"})
        self.assertEqual(result["status"], "INVALID")
        self.assertEqual(result["reason"], "TEMPORAL_INCONSISTENCY")

    def test_distiller_freezes_on_nondeterministic_oracle(self) -> None:
        calls = 0
        def oracle(_: list[str]) -> str | None:
            nonlocal calls
            calls += 1
            return "X" if calls % 2 else None
        result = distill(["A"], oracle, "X")
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["reason"], "ORACLE_NONDETERMINISTIC")

    def test_correction_detects_conflicting_equalities(self) -> None:
        base = {
            "authority": "USER_DIRECTIVE",
            "scope_mode": "BOUNDED",
            "selector": {"project": "p", "operation": "x"},
        }
        result = compile_corrections([
            {**base, "id": "a", "assertions": [{"field": "mode", "op": "eq", "value": "strict"}]},
            {**base, "id": "b", "assertions": [{"field": "mode", "op": "eq", "value": "creative"}]},
        ])
        self.assertEqual(result["status"], "FREEZE")

    def test_correction_detects_exists_not_exists_conflict(self) -> None:
        base = {
            "authority": "USER_DIRECTIVE",
            "scope_mode": "BOUNDED",
            "selector": {"project": "p", "operation": "x"},
        }
        result = compile_corrections([
            {**base, "id": "a", "assertions": [{"field": "citation", "op": "exists"}]},
            {**base, "id": "b", "assertions": [{"field": "citation", "op": "not_exists"}]},
        ])
        self.assertEqual(result["status"], "FREEZE")

    def test_correction_rejects_malformed_supersedes(self) -> None:
        with self.assertRaises(ValueError):
            compile_correction({
                "id": "x",
                "authority": "USER_DIRECTIVE",
                "scope_mode": "BOUNDED",
                "selector": {"project": "p", "operation": "x"},
                "assertions": [{"field": "mode", "op": "eq", "value": "strict"}],
                "supersedes": "abc",
            })

    def test_emergence_rejects_duplicate_outputs_within_step(self) -> None:
        with self.assertRaises(ValueError):
            analyze_plan({
                "artifacts": {"x": []},
                "steps": [{"id": "dup", "consumes": ["x"], "produces": ["y", "y"], "capabilities": []}],
            })

    def test_all_terminal_results_have_fingerprint(self) -> None:
        results = [
            compose([{"id": "x", "assumptions": ["missing"], "guarantees": []}], []),
            analyze_plan({"artifacts": {}, "steps": [{"id": "x", "consumes": ["missing"], "produces": [], "capabilities": []}]}),
            assess_portability(
                {"claim_id": "a", "evidence_class": "E2", "source_context": {"code": "a"}},
                {"claim_id": "b", "required_evidence_classes": ["E2"], "target_context": {"code": "a"}},
                {"code": "MUST_EQUAL"},
            ),
            distill(["A"], lambda _: None, "X"),
        ]
        for result in results:
            self.assertIn("fingerprint", result, result)


if __name__ == "__main__":
    unittest.main()
