from __future__ import annotations

import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hcas.validator import validate_manifest  # noqa: E402


def load_example(name: str) -> dict:
    return json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))


class ValidatorTests(unittest.TestCase):
    def test_safe_manifest_passes(self) -> None:
        report = validate_manifest(load_example("safe_manifest.json"))
        self.assertTrue(report.passed, report.to_dict())
        self.assertEqual(report.errors, ())

    def test_unsafe_manifest_fails_multiple_independent_rules(self) -> None:
        report = validate_manifest(load_example("unsafe_manifest.json"))
        self.assertFalse(report.passed)
        ids = {item.rule_id for item in report.errors}
        self.assertTrue({"HCAS-030", "HCAS-041", "HCAS-050", "HCAS-111", "HCAS-121"} <= ids)

    def test_ui_visibility_cannot_replace_backend_authorization(self) -> None:
        manifest = load_example("safe_manifest.json")
        manifest["actions"][0]["backend_authorization"] = False
        report = validate_manifest(manifest)
        self.assertIn("HCAS-030", {item.rule_id for item in report.errors})

    def test_loading_cannot_be_evidence(self) -> None:
        manifest = load_example("safe_manifest.json")
        manifest["pending_state"]["is_evidence"] = True
        report = validate_manifest(manifest)
        self.assertIn("HCAS-121", {item.rule_id for item in report.errors})

    def test_freeze_cannot_be_masked(self) -> None:
        manifest = load_example("safe_manifest.json")
        manifest["freeze_surface"]["maskable"] = True
        report = validate_manifest(manifest)
        self.assertIn("HCAS-111", {item.rule_id for item in report.errors})

    def test_duplicate_action_id_is_rejected(self) -> None:
        manifest = load_example("safe_manifest.json")
        manifest["actions"].append(deepcopy(manifest["actions"][0]))
        report = validate_manifest(manifest)
        self.assertIn("HCAS-011", {item.rule_id for item in report.errors})

    def test_reversible_action_requires_rollback_path(self) -> None:
        manifest = load_example("safe_manifest.json")
        action = manifest["actions"][0]
        action["reversible"] = True
        action["rollback_path"] = ""
        report = validate_manifest(manifest)
        self.assertIn("HCAS-141", {item.rule_id for item in report.errors})

    def test_irreversible_action_requires_warning(self) -> None:
        manifest = load_example("safe_manifest.json")
        action = manifest["actions"][0]
        action["irreversible_warning"] = False
        report = validate_manifest(manifest)
        self.assertIn("HCAS-142", {item.rule_id for item in report.errors})

    def test_strict_future_requires_dual_approval_for_destructive(self) -> None:
        manifest = load_example("safe_manifest.json")
        manifest["profile"] = "strict_future"
        action = manifest["actions"][0]
        action["side_effect"] = "DESTRUCTIVE"
        action["confirmation"] = "EXPLICIT_TYPED"
        report = validate_manifest(manifest)
        self.assertIn("HCAS-042", {item.rule_id for item in report.errors})

    def test_deterministic_output_for_same_input(self) -> None:
        manifest = load_example("unsafe_manifest.json")
        a = validate_manifest(manifest).to_dict()
        b = validate_manifest(deepcopy(manifest)).to_dict()
        self.assertEqual(a, b)

    def test_non_object_manifest_fails_cleanly(self) -> None:
        report = validate_manifest([])  # type: ignore[arg-type]
        self.assertFalse(report.passed)
        self.assertEqual(report.errors[0].rule_id, "HCAS-000")


if __name__ == "__main__":
    unittest.main()
