from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from wocf import Decision, Policy, WorkstreamCollisionFirewall, WorkstreamManifest, evaluate_payloads


BASE_POLICY = {
    "protected_repository_name_substrings": ["NEXY.AI"],
    "lexical_warn_threshold": 0.45,
    "lexical_freeze_threshold": 0.72,
    "require_namespace_write_containment": True,
    "minimum_concept_tags": 2,
}


def manifest(
    workstream_id: str,
    namespace: str,
    *,
    objective: str,
    tags: list[str],
    repository: str = "goif74945-crypto/AI-CONTEXT",
    write_paths: list[str] | None = None,
    read_paths: list[str] | None = None,
    resources: list[str] | None = None,
    differentiators: list[str] | None = None,
) -> dict:
    return {
        "workstream_id": workstream_id,
        "repository": repository,
        "namespace": namespace,
        "objective": objective,
        "concept_tags": tags,
        "write_paths": write_paths or [namespace],
        "read_paths": read_paths or [],
        "exclusive_resources": resources or [],
        "status": "ACTIVE",
        "differentiators": differentiators or [],
    }


EXISTING = manifest(
    "WS-EXISTING-001",
    "คลังข้อมูลเสริม/existing-proof-planner",
    objective="Plan proof-preserving resource allocation across workers under cost and latency constraints.",
    tags=["resource-allocation", "proof-preservation", "worker-routing", "cost", "latency"],
    resources=["global-worker-budget"],
    differentiators=["resource planning below verification authority"],
)


class WOCFTests(unittest.TestCase):
    def test_unique_workstream_is_allowed(self) -> None:
        proposal = manifest(
            "WS-NEW-001",
            "คลังข้อมูลเสริม/new-collision-firewall",
            objective="Detect concurrent workstream path collisions and duplicate concept overlap before repository mutation.",
            tags=["concurrency", "collision-detection", "namespace", "write-set"],
            read_paths=["คลังข้อมูลเสริม"],
            differentiators=["preflight only; no execution authority"],
        )
        result = evaluate_payloads(proposal, [EXISTING], BASE_POLICY)
        self.assertEqual(result.decision, Decision.ALLOW)
        self.assertEqual(result.compared_workstreams, 1)
        self.assertLess(result.max_lexical_overlap, BASE_POLICY["lexical_warn_threshold"])

    def test_protected_repository_freezes(self) -> None:
        proposal = manifest(
            "WS-NEW-002",
            "lab/protected-target",
            repository="goif74945-crypto/NEXY.AI-PROD",
            objective="Create a collision preflight in a repository that current policy marks protected.",
            tags=["collision", "preflight"],
        )
        result = evaluate_payloads(proposal, [], BASE_POLICY)
        self.assertEqual(result.decision, Decision.FREEZE)
        self.assertIn("PROTECTED_REPOSITORY", {f.code for f in result.findings})

    def test_workstream_id_collision_freezes(self) -> None:
        proposal = manifest(
            EXISTING["workstream_id"],
            "คลังข้อมูลเสริม/other",
            objective="Detect unrelated namespace conflicts before mutation begins in shared context repositories.",
            tags=["namespace", "collision"],
        )
        result = evaluate_payloads(proposal, [EXISTING], BASE_POLICY)
        self.assertIn("WORKSTREAM_ID_COLLISION", {f.code for f in result.findings})
        self.assertEqual(result.decision, Decision.FREEZE)

    def test_namespace_ancestor_collision_freezes(self) -> None:
        proposal = manifest(
            "WS-NEW-003",
            "คลังข้อมูลเสริม/existing-proof-planner/subproject",
            objective="Build a child workstream that would overwrite an existing workstream namespace.",
            tags=["namespace", "collision"],
        )
        result = evaluate_payloads(proposal, [EXISTING], BASE_POLICY)
        self.assertIn("NAMESPACE_COLLISION", {f.code for f in result.findings})
        self.assertEqual(result.decision, Decision.FREEZE)

    def test_write_path_collision_freezes(self) -> None:
        existing = copy.deepcopy(EXISTING)
        existing["namespace"] = "คลังข้อมูลเสริม/team-a"
        existing["write_paths"] = ["คลังข้อมูลเสริม/team-a/shared"]
        proposal = manifest(
            "WS-NEW-004",
            "คลังข้อมูลเสริม/team-b",
            objective="Create a separate namespace but intentionally target an existing shared write subtree.",
            tags=["write-set", "collision"],
            write_paths=["คลังข้อมูลเสริม/team-b", "คลังข้อมูลเสริม/team-a/shared/file.json"],
        )
        policy = dict(BASE_POLICY)
        policy["require_namespace_write_containment"] = False
        result = evaluate_payloads(proposal, [existing], policy)
        self.assertIn("WRITE_PATH_COLLISION", {f.code for f in result.findings})
        self.assertEqual(result.decision, Decision.FREEZE)

    def test_exclusive_resource_collision_freezes(self) -> None:
        proposal = manifest(
            "WS-NEW-005",
            "คลังข้อมูลเสริม/new-budget-work",
            objective="Coordinate a distinct process that nevertheless claims the same exclusive worker budget.",
            tags=["coordination", "budget"],
            resources=["GLOBAL-WORKER-BUDGET"],
        )
        result = evaluate_payloads(proposal, [EXISTING], BASE_POLICY)
        self.assertIn("EXCLUSIVE_RESOURCE_COLLISION", {f.code for f in result.findings})
        self.assertEqual(result.decision, Decision.FREEZE)


    def test_completed_workstream_does_not_hold_exclusive_resource(self) -> None:
        completed = copy.deepcopy(EXISTING)
        completed["status"] = "COMPLETE"
        proposal = manifest(
            "WS-NEW-005B",
            "คลังข้อมูลเสริม/new-budget-after-complete",
            objective="Use an exclusive worker budget after a previous unrelated workstream has completed and released it.",
            tags=["exclusive-resource", "handoff"],
            resources=["GLOBAL-WORKER-BUDGET"],
        )
        result = evaluate_payloads(proposal, [completed], BASE_POLICY)
        self.assertNotIn("EXCLUSIVE_RESOURCE_COLLISION", {f.code for f in result.findings})
        self.assertNotEqual(result.decision, Decision.FREEZE)

    def test_exact_concept_signature_freezes_even_in_new_namespace(self) -> None:
        proposal = manifest(
            "WS-NEW-006",
            "คลังข้อมูลเสริม/fresh-namespace",
            objective=EXISTING["objective"],
            tags=list(reversed(EXISTING["concept_tags"])),
            differentiators=EXISTING["differentiators"],
        )
        result = evaluate_payloads(proposal, [EXISTING], BASE_POLICY)
        self.assertIn("DUPLICATE_CONCEPT_SIGNATURE", {f.code for f in result.findings})
        self.assertEqual(result.decision, Decision.FREEZE)

    def test_high_lexical_overlap_freezes(self) -> None:
        proposal = manifest(
            "WS-NEW-007",
            "คลังข้อมูลเสริม/resource-plan-clone",
            objective="Plan proof preserving resource allocation across AI workers with cost and latency constraints.",
            tags=["resource-allocation", "proof-preservation", "worker-routing", "cost", "latency", "optimizer"],
            differentiators=["slightly different optimizer"],
        )
        result = evaluate_payloads(proposal, [EXISTING], BASE_POLICY)
        self.assertIn("HIGH_LEXICAL_CONCEPT_OVERLAP", {f.code for f in result.findings})
        self.assertEqual(result.decision, Decision.FREEZE)

    def test_moderate_overlap_warns(self) -> None:
        proposal = manifest(
            "WS-NEW-008",
            "คลังข้อมูลเสริม/resource-observability",
            objective="Observe worker resource allocation cost latency and routing decisions and publish telemetry without selecting workers.",
            tags=["resource-allocation", "cost", "latency", "worker-routing", "telemetry", "observability"],
            differentiators=["observability only"],
        )
        result = evaluate_payloads(proposal, [EXISTING], BASE_POLICY)
        self.assertIn("MODERATE_LEXICAL_CONCEPT_OVERLAP", {f.code for f in result.findings})
        self.assertEqual(result.decision, Decision.WARN)

    def test_read_overlap_does_not_block(self) -> None:
        proposal = manifest(
            "WS-NEW-009",
            "คลังข้อมูลเสริม/reader",
            objective="Read shared context to build an independent namespace collision detector with no shared writes.",
            tags=["read-only", "collision-detection"],
            read_paths=EXISTING["write_paths"],
        )
        result = evaluate_payloads(proposal, [EXISTING], BASE_POLICY)
        self.assertEqual(result.decision, Decision.ALLOW)

    def test_namespace_containment_violation_fails_closed(self) -> None:
        proposal = manifest(
            "WS-NEW-010",
            "คลังข้อมูลเสริม/safe-zone",
            objective="Attempt a write outside the declared namespace to verify containment enforcement behavior.",
            tags=["scope", "containment"],
            write_paths=["คลังข้อมูลเสริม/other-zone/file.txt"],
        )
        result = evaluate_payloads(proposal, [], BASE_POLICY)
        self.assertEqual(result.decision, Decision.FREEZE)
        self.assertIn("INVALID_PROPOSAL", {f.code for f in result.findings})

    def test_path_traversal_fails_closed(self) -> None:
        proposal = manifest(
            "WS-NEW-011",
            "คลังข้อมูลเสริม/safe-zone",
            objective="Attempt path traversal through a write path to verify normalization rejects unsafe input.",
            tags=["scope", "path-safety"],
            write_paths=["คลังข้อมูลเสริม/safe-zone/../escape.txt"],
        )
        result = evaluate_payloads(proposal, [], BASE_POLICY)
        self.assertEqual(result.decision, Decision.FREEZE)
        self.assertIn("INVALID_PROPOSAL", {f.code for f in result.findings})

    def test_invalid_catalog_entry_fails_closed(self) -> None:
        proposal = manifest(
            "WS-NEW-012",
            "คลังข้อมูลเสริม/clean",
            objective="Evaluate a normal workstream while the catalog contains malformed state that prevents safe comparison.",
            tags=["catalog", "validation"],
        )
        bad_catalog = [{"workstream_id": "x"}]
        result = evaluate_payloads(proposal, bad_catalog, BASE_POLICY)
        self.assertEqual(result.decision, Decision.FREEZE)
        self.assertIn("INVALID_CATALOG_ENTRY", {f.code for f in result.findings})


    def test_duplicate_catalog_ids_fail_closed(self) -> None:
        proposal = manifest(
            "WS-NEW-012B",
            "คลังข้อมูลเสริม/clean-duplicate-catalog-check",
            objective="Verify duplicate catalog identities fail closed because catalog lineage is ambiguous.",
            tags=["catalog", "identity"],
        )
        duplicate = copy.deepcopy(EXISTING)
        duplicate["namespace"] = "คลังข้อมูลเสริม/second-copy"
        duplicate["write_paths"] = ["คลังข้อมูลเสริม/second-copy"]
        result = evaluate_payloads(proposal, [EXISTING, duplicate], BASE_POLICY)
        self.assertEqual(result.decision, Decision.FREEZE)
        self.assertIn("INVALID_CATALOG_ENTRY", {f.code for f in result.findings})

    def test_deterministic_hash_and_finding_order(self) -> None:
        proposal = manifest(
            "WS-NEW-013",
            "คลังข้อมูลเสริม/deterministic",
            objective="Verify that repeated evaluations produce byte-equivalent deterministic result structures.",
            tags=["determinism", "replay"],
        )
        first = evaluate_payloads(proposal, [EXISTING], BASE_POLICY).to_dict()
        second = evaluate_payloads(copy.deepcopy(proposal), [copy.deepcopy(EXISTING)], dict(BASE_POLICY)).to_dict()
        self.assertEqual(first, second)

    def test_catalog_order_does_not_change_result(self) -> None:
        second_existing = manifest(
            "WS-EXISTING-002",
            "คลังข้อมูลเสริม/other-existing",
            objective="Validate multilingual localization presentation contracts while preserving authoritative backend truth.",
            tags=["localization", "presentation", "truth"],
        )
        proposal = manifest(
            "WS-NEW-014",
            "คลังข้อมูลเสริม/order-test",
            objective="Detect repository workstream collisions deterministically regardless of input catalog ordering.",
            tags=["collision", "determinism"],
        )
        a = evaluate_payloads(proposal, [EXISTING, second_existing], BASE_POLICY).to_dict()
        b = evaluate_payloads(proposal, [second_existing, EXISTING], BASE_POLICY).to_dict()
        self.assertEqual(a, b)

    def test_cli_freeze_exit_code_and_json_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            proposal = manifest(
                "WS-CLI-001",
                "lab/protected",
                repository="goif74945-crypto/NEXY.AI",
                objective="Exercise the command line entry point against a protected repository mutation target.",
                tags=["cli", "protected-target"],
            )
            (tmp_path / "proposal.json").write_text(json.dumps(proposal), encoding="utf-8")
            (tmp_path / "catalog.json").write_text("[]", encoding="utf-8")
            (tmp_path / "policy.json").write_text(json.dumps(BASE_POLICY), encoding="utf-8")
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SRC / "wocf.py"),
                    "evaluate",
                    "--proposal",
                    str(tmp_path / "proposal.json"),
                    "--catalog",
                    str(tmp_path / "catalog.json"),
                    "--policy",
                    str(tmp_path / "policy.json"),
                ],
                check=False,
                capture_output=True,
                text=True,
                env={**os.environ, "PYTHONUTF8": "1"},
            )
            self.assertEqual(completed.returncode, 2, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["decision"], "FREEZE")
            self.assertIn("PROTECTED_REPOSITORY", {item["code"] for item in payload["findings"]})


if __name__ == "__main__":
    unittest.main()
