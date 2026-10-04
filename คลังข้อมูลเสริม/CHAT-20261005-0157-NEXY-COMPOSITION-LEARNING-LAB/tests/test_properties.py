from __future__ import annotations

import itertools
import random
import unittest

from nexy_aux.composition import compose
from nexy_aux.corrections import compile_correction, evaluate
from nexy_aux.distiller import distill
from nexy_aux.emergence import analyze_plan
from nexy_aux.portability import assess_portability


class PropertyTests(unittest.TestCase):
    def test_composition_is_stable_across_component_permutations(self) -> None:
        components = [
            {"id": "a", "assumptions": ["seed"], "guarantees": ["x"]},
            {"id": "b", "assumptions": ["seed"], "guarantees": ["y"]},
            {"id": "c", "assumptions": ["x", "y"], "guarantees": ["done"]},
        ]
        baseline = compose(components, ["seed"])
        self.assertEqual(baseline["status"], "PASS")
        for perm in itertools.permutations(components):
            current = compose(list(perm), ["seed"])
            self.assertEqual(current, baseline)

    def test_emergent_risk_has_no_bypass_from_irrelevant_steps(self) -> None:
        base_steps = [
            {"id": "copy", "consumes": ["secret"], "produces": ["copy"], "capabilities": []},
            {"id": "send", "consumes": ["copy"], "produces": [], "capabilities": ["EXTERNAL_EGRESS"]},
        ]
        rng = random.Random(74945)
        for case in range(50):
            noise_steps = []
            previous = "public"
            for idx in range(rng.randint(0, 5)):
                out = f"noise_{case}_{idx}"
                noise_steps.append({"id": f"n_{case}_{idx}", "consumes": [previous], "produces": [out], "capabilities": []})
                previous = out
            steps = noise_steps + list(base_steps)
            result = analyze_plan({"artifacts": {"secret": ["SECRET"], "public": []}, "steps": steps})
            self.assertEqual(result["status"], "FREEZE")
            self.assertTrue(any(f["code"] == "E_SECRET_EGRESS" for f in result["findings"]))

    def test_portability_policy_cross_product(self) -> None:
        evidence = {
            "claim_id": "C",
            "evidence_class": "E2",
            "source_context": {"code": "A", "runtime": "R1", "region": "TH"},
        }
        target_base = {
            "claim_id": "C",
            "required_evidence_classes": ["E2"],
            "target_context": {"code": "A", "runtime": "R1", "region": "TH"},
        }
        rules = ["MUST_EQUAL", "REVERIFY_IF_DIFFERENT", "CAN_DIFFER"]
        expected = {
            "MUST_EQUAL": "INVALID",
            "REVERIFY_IF_DIFFERENT": "REVERIFY",
            "CAN_DIFFER": "PORTABLE",
        }
        for rule in rules:
            target = {**target_base, "target_context": dict(target_base["target_context"])}
            target["target_context"]["runtime"] = "R2"
            result = assess_portability(
                evidence,
                target,
                {"code": "MUST_EQUAL", "runtime": rule, "region": "CAN_DIFFER"},
            )
            self.assertEqual(result["status"], expected[rule])

    def test_correction_selector_never_applies_outside_exact_bound(self) -> None:
        contract = compile_correction({
            "id": "fix-1",
            "authority": "USER_DIRECTIVE",
            "scope_mode": "BOUNDED",
            "selector": {"project": "p", "operation": "summarize", "surface": "report"},
            "assertions": [{"field": "mode", "op": "eq", "value": "strict"}],
        })
        dimensions = ["project", "operation", "surface"]
        for dimension in dimensions:
            context = {"project": "p", "operation": "summarize", "surface": "report"}
            context[dimension] = "other"
            result = evaluate(contract, context, {"mode": "wrong"})
            self.assertEqual(result["status"], "NOT_APPLICABLE")

    def test_distiller_result_is_1_minimal_across_seeded_cores(self) -> None:
        rng = random.Random(5601)
        universe = list(range(12))
        for _ in range(80):
            core = set(rng.sample(universe, rng.randint(1, 4)))
            ordered = universe[:]
            rng.shuffle(ordered)
            def oracle(candidate: list[int]) -> str | None:
                return "TARGET" if core.issubset(set(candidate)) else None
            result = distill(ordered, oracle, "TARGET")
            self.assertEqual(result["status"], "PASS")
            self.assertTrue(result["one_minimal"])
            minimal = result["minimal_items"]
            self.assertTrue(core.issubset(set(minimal)))
            for idx in range(len(minimal)):
                self.assertNotEqual(oracle(minimal[:idx] + minimal[idx + 1:]), "TARGET")


if __name__ == "__main__":
    unittest.main()
