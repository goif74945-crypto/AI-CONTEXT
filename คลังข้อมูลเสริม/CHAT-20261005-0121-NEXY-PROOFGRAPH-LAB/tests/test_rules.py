from __future__ import annotations

import hashlib
import unittest

from nexy_proofgraph.model import Document
from nexy_proofgraph.policy import NEXYPolicy
from nexy_proofgraph.rules import run_rules


def doc(path: str, text: str) -> Document:
    raw = text.encode("utf-8")
    return Document(path, hashlib.sha256(raw).hexdigest(), len(raw), path.rsplit(".", 1)[-1], text)


POLICY = NEXYPolicy(
    current_requirement_rows=837,
    current_build_rows=773,
    deprecated_registry_count=215,
    historical_partial_registry_count=262,
    ontology_entity_count=518,
    proposal_root="คลังข้อมูลเสริม",
    protected_repo_name_fragment="NEXY.AI",
    scan_max_bytes=2_000_000,
)


class RuleTests(unittest.TestCase):
    def ids(self, text: str, path: str = "x.md") -> set[str]:
        return {f.rule_id for f in run_rules([doc(path, text)], POLICY)}

    def test_deprecated_registry_current_misuse_is_critical(self):
        self.assertIn("PG002", self.ids("Current total system count: 215"))

    def test_historical_215_is_allowed(self):
        self.assertNotIn("PG002", self.ids("Historical deprecated 215-entry registry retained for provenance only."))

    def test_wrong_current_requirement_denominator_is_rejected(self):
        self.assertIn("PG003", self.ids("Current total is 836 normalized requirement rows."))

    def test_correct_current_requirement_denominator_is_allowed(self):
        self.assertNotIn("PG003", self.ids("Current total is 837 normalized requirement rows."))

    def test_wrong_current_build_count_is_rejected(self):
        self.assertIn("PG004", self.ids("Current Build contains 772 rows."))


    def test_current_build_selects_nearest_number(self):
        self.assertNotIn("PG004", self.ids("837 normalized requirement rows and 773 Current Build rows."))

    def test_current_build_does_not_parse_rule_identifier(self):
        self.assertNotIn("PG004", self.ids("R6 | Detect Current Build denominator drift | PG004 | unit test"))

    def test_unlabeled_supplemental_design_is_rejected(self):
        self.assertIn("PG005", self.ids("# Design\nSomething", "คลังข้อมูลเสริม/a/DESIGN.md"))

    def test_labeled_supplemental_design_is_allowed(self):
        self.assertNotIn("PG005", self.ids("# AI-PROPOSED / EXPERIMENTAL\nSomething", "คลังข้อมูลเสริม/a/DESIGN.md"))


    def test_broken_local_link_is_error(self):
        findings = run_rules([doc("a.md", "[missing](missing.md)")], POLICY)
        self.assertIn("PG001", {f.rule_id for f in findings})

    def test_existing_local_link_is_allowed(self):
        findings = run_rules([doc("a.md", "[b](b.md)"), doc("b.md", "# B")], POLICY)
        self.assertNotIn("PG001", {f.rule_id for f in findings})

    def test_completion_without_nearby_evidence_is_warning(self):
        findings = run_rules([doc("x.md", "STATUS: COMPLETE")], POLICY)
        hit = next(f for f in findings if f.rule_id == "PG006")
        self.assertEqual(hit.severity.name, "WARNING")

    def test_completion_with_evidence_marker_is_allowed(self):
        findings = run_rules([doc("x.md", "STATUS: COMPLETE\nEVIDENCE: unit test")], POLICY)
        self.assertNotIn("PG006", {f.rule_id for f in findings})

    def test_secret_value_is_never_echoed_in_finding(self):
        secret = "sk-proj-ABCDEFGHIJKLMNOPQRSTUVWXYZ123456"
        findings = run_rules([doc("x.md", f"token={secret}")], POLICY)
        hit = next(f for f in findings if f.rule_id == "PG007")
        self.assertNotIn(secret, str(hit.to_dict()))
        self.assertIn("fingerprint", hit.evidence)


if __name__ == "__main__":
    unittest.main()
