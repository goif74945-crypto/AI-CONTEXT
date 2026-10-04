from __future__ import annotations

import unittest

from nexy_proposal_forge.collision import Scope, WorkManifest, compare_work_manifests
from nexy_proposal_forge.models import ProposalValidationError


def manifest(execution_id: str, scope: str, *, status: str = "IN_PROGRESS", proposal_ids: list[str] | None = None) -> WorkManifest:
    return WorkManifest.from_dict(
        {
            "execution_id": execution_id,
            "status": status,
            "target_repository": "goif74945-crypto/AI-CONTEXT",
            "objective": "test",
            "write_scopes": [scope],
            "proposal_ids": proposal_ids or [],
        }
    )


class CollisionTests(unittest.TestCase):
    def test_recursive_scope_overlap(self) -> None:
        root = Scope.parse("คลังข้อมูลเสริม/NEXY-PROPOSAL-FORGE/**")
        child = Scope.parse("คลังข้อมูลเสริม/NEXY-PROPOSAL-FORGE/file.md")
        self.assertTrue(root.overlaps(child))
        self.assertTrue(child.overlaps(root))

    def test_separate_sibling_scope_is_clear(self) -> None:
        current = manifest("A", "คลังข้อมูลเสริม/A/**")
        other = manifest("B", "คลังข้อมูลเสริม/B/**")
        report = compare_work_manifests(current, (other,))
        self.assertEqual(report.recommendation, "CLEAR")

    def test_write_scope_collision_is_reported(self) -> None:
        current = manifest("A", "คลังข้อมูลเสริม/A/**")
        other = manifest("B", "คลังข้อมูลเสริม/A/sub/**")
        report = compare_work_manifests(current, (other,))
        self.assertEqual(report.recommendation, "COLLISION")
        self.assertEqual(report.collisions[0].kind, "WRITE_SCOPE")

    def test_proposal_id_collision_is_reported(self) -> None:
        current = manifest("A", "คลังข้อมูลเสริม/A/**", proposal_ids=["NPF-1"])
        other = manifest("B", "คลังข้อมูลเสริม/B/**", proposal_ids=["NPF-1"])
        report = compare_work_manifests(current, (other,))
        self.assertEqual(report.recommendation, "COLLISION")
        self.assertTrue(any(item.kind == "PROPOSAL_ID" for item in report.collisions))

    def test_complete_manifest_is_ignored(self) -> None:
        current = manifest("A", "คลังข้อมูลเสริม/A/**")
        other = manifest("B", "คลังข้อมูลเสริม/A/**", status="COMPLETE")
        report = compare_work_manifests(current, (other,))
        self.assertEqual(report.recommendation, "CLEAR")
        self.assertEqual(report.ignored_inactive_manifests, ("B",))

    def test_parent_traversal_scope_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Scope.parse("คลังข้อมูลเสริม/../secret/**")

    def test_unknown_manifest_field_is_rejected(self) -> None:
        data = {
            "execution_id": "A",
            "status": "IN_PROGRESS",
            "target_repository": "repo/x",
            "objective": "test",
            "write_scopes": ["safe/**"],
            "proposal_ids": [],
            "hidden": True,
        }
        with self.assertRaises(ProposalValidationError):
            WorkManifest.from_dict(data)


if __name__ == "__main__":
    unittest.main()
