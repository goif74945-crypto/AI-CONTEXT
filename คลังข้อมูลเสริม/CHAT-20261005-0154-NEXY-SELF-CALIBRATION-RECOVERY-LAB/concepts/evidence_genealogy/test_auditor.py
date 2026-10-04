from __future__ import annotations

import unittest

from concepts.evidence_genealogy.auditor import EvidenceItem, audit_independence


class EvidenceGenealogyTests(unittest.TestCase):
    def test_shared_root_collapses_apparent_count(self) -> None:
        items = [
            EvidenceItem("e1", "c", "doc-A", "static", "h1", "r1"),
            EvidenceItem("e2", "c", "doc-A", "human-review", "h2", "r1"),
            EvidenceItem("e3", "c", "runtime-B", "runtime", "h3", "r1"),
        ]
        r = audit_independence(items, target_revision="r1", required_independent_groups=3)
        self.assertEqual(r["status"], "INSUFFICIENT_INDEPENDENCE")
        self.assertEqual(r["independent_group_count"], 2)

    def test_identical_content_collapses_even_across_roots(self) -> None:
        items = [
            EvidenceItem("a", "c", "root1", "m1", "same", "r"),
            EvidenceItem("b", "c", "root2", "m2", "same", "r"),
        ]
        r = audit_independence(items, target_revision="r", required_independent_groups=2)
        self.assertEqual(r["status"], "INSUFFICIENT_INDEPENDENCE")

    def test_stale_evidence_blocks_ready(self) -> None:
        items = [
            EvidenceItem("a", "c", "r1", "m1", "h1", "old"),
            EvidenceItem("b", "c", "r2", "m2", "h2", "new"),
        ]
        r = audit_independence(items, target_revision="new")
        self.assertEqual(r["status"], "STALE_EVIDENCE")
        self.assertEqual(r["stale_evidence"], ["a"])

    def test_two_independent_groups_ready(self) -> None:
        items = [
            EvidenceItem("a", "c", "r1", "m1", "h1", "x"),
            EvidenceItem("b", "c", "r2", "m2", "h2", "x"),
        ]
        r = audit_independence(items, target_revision="x")
        self.assertEqual(r["status"], "READY")

    def test_mixed_claims_rejected(self) -> None:
        items = [
            EvidenceItem("a", "c1", "r1", "m1", "h1", "x"),
            EvidenceItem("b", "c2", "r2", "m2", "h2", "x"),
        ]
        with self.assertRaises(ValueError):
            audit_independence(items, target_revision="x")


if __name__ == "__main__":
    unittest.main()
