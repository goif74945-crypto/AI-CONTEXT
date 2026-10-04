from __future__ import annotations

import copy
import json
import unittest

from interaction_contract import ValidationError, analyze_contract


def base_contract() -> dict:
    return {
        "contract_id": "demo-001",
        "authorized_scopes": ["AI-CONTEXT:supplement"],
        "protected_scopes": ["NEXY.AI:repo"],
        "directives": [
            {
                "id": "D1",
                "text": "Write only to the supplement area",
                "kind": "constraint",
                "criticality": "critical",
                "scopes": ["AI-CONTEXT:supplement"],
                "conflicts_with": [],
                "resolved": True,
            },
            {
                "id": "D2",
                "text": "Provide executed verification evidence",
                "kind": "acceptance",
                "criticality": "high",
                "scopes": [],
                "conflicts_with": [],
                "resolved": True,
            },
        ],
        "events": [
            {
                "seq": 1,
                "actor": "assistant",
                "type": "action",
                "directive_ids": ["D1"],
                "scopes": ["AI-CONTEXT:supplement"],
                "assumptions": [],
            },
            {
                "seq": 2,
                "actor": "assistant",
                "type": "evidence",
                "directive_ids": ["D1"],
                "outcome": "pass",
                "evidence_ref": "commit:abc/path:supplement",
            },
            {
                "seq": 3,
                "actor": "assistant",
                "type": "evidence",
                "directive_ids": ["D2"],
                "outcome": "pass",
                "evidence_ref": "test:unittest:8-pass",
            },
            {
                "seq": 4,
                "actor": "assistant",
                "type": "completion",
                "directive_ids": ["D1", "D2"],
                "completion_status": "complete",
            },
        ],
    }


class AnalyzerTests(unittest.TestCase):
    def test_clean_contract_passes(self) -> None:
        report = analyze_contract(base_contract())
        self.assertEqual(report["completion_gate"], "PASS")
        self.assertEqual(report["metrics"]["retention_score"], 100)
        self.assertEqual(report["findings"], [])

    def test_missing_evidence_blocks_completion(self) -> None:
        raw = base_contract()
        raw["events"] = [event for event in raw["events"] if event.get("directive_ids") != ["D2"]]
        report = analyze_contract(raw)
        codes = {item["code"] for item in report["findings"]}
        self.assertIn("DIRECTIVE_UNEVIDENCED", codes)
        self.assertIn("PREMATURE_COMPLETION_CLAIM", codes)
        self.assertEqual(report["completion_gate"], "BLOCK")

    def test_protected_scope_is_critical(self) -> None:
        raw = base_contract()
        raw["events"][0]["scopes"] = ["NEXY.AI:repo"]
        report = analyze_contract(raw)
        self.assertIn("PROTECTED_SCOPE_TOUCHED", {f["code"] for f in report["findings"]})
        self.assertEqual(report["completion_gate"], "BLOCK")

    def test_unknown_scope_is_unauthorized(self) -> None:
        raw = base_contract()
        raw["events"][0]["scopes"] = ["OTHER:repo"]
        report = analyze_contract(raw)
        self.assertIn("UNAUTHORIZED_SCOPE_EXPANSION", {f["code"] for f in report["findings"]})

    def test_resolved_directive_reclarification_is_flagged(self) -> None:
        raw = base_contract()
        raw["events"].insert(
            0,
            {
                "seq": 0,
                "actor": "assistant",
                "type": "clarification",
                "directive_ids": ["D1"],
            },
        )
        report = analyze_contract(raw)
        self.assertIn("REDUNDANT_CLARIFICATION", {f["code"] for f in report["findings"]})

    def test_action_assumption_is_visible(self) -> None:
        raw = base_contract()
        raw["events"][0]["assumptions"] = ["Assume branch is main"]
        report = analyze_contract(raw)
        self.assertIn("ACTION_WITH_ASSUMPTION", {f["code"] for f in report["findings"]})

    def test_explicit_conflict_blocks(self) -> None:
        raw = base_contract()
        raw["directives"][0]["conflicts_with"] = ["D2"]
        report = analyze_contract(raw)
        self.assertIn("EXPLICIT_DIRECTIVE_CONFLICT", {f["code"] for f in report["findings"]})
        self.assertEqual(report["completion_gate"], "BLOCK")

    def test_pass_without_reference_is_not_accepted_as_clean(self) -> None:
        raw = base_contract()
        raw["events"][1].pop("evidence_ref")
        report = analyze_contract(raw)
        self.assertIn("PASS_WITHOUT_EVIDENCE_REF", {f["code"] for f in report["findings"]})
        self.assertLess(report["metrics"]["retention_score"], 100)

    def test_duplicate_directive_rejected(self) -> None:
        raw = base_contract()
        raw["directives"].append(copy.deepcopy(raw["directives"][0]))
        with self.assertRaises(ValidationError):
            analyze_contract(raw)

    def test_deterministic_report(self) -> None:
        raw = base_contract()
        first = json.dumps(analyze_contract(raw), sort_keys=True)
        second = json.dumps(analyze_contract(raw), sort_keys=True)
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
