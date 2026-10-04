from __future__ import annotations

import dataclasses
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nexy_provenance_taint import (  # noqa: E402
    ProvenanceEngine,
    ReleasePolicy,
    SourceSpec,
    Taint,
    TransformContract,
)
from nexy_provenance_taint.core import IntegrityError, ProvenanceError  # noqa: E402


class ProvenanceTaintLatticeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = ProvenanceEngine()
        self.safe_policy = ReleasePolicy(
            policy_id="release:v1",
            min_authority_rank=50,
            required_assurances=frozenset({"verified", "schema:valid"}),
            forbidden_taints=frozenset(Taint),
            max_age_epochs=10,
            require_deterministic_lineage=True,
        )

    def verified_source(self, *, rank: int = 80, epoch: int = 10, origin: str = "root:A"):
        return self.engine.source(
            "trusted",
            SourceSpec(
                origin_id=origin,
                source_kind="canonical",
                authority_rank=rank,
                assurance_tags=frozenset({"verified", "schema:valid", "unit:passed"}),
                epoch=epoch,
            ),
        )

    def unverified_source(self, *, rank: int = 20, origin: str = "model:1"):
        return self.engine.source(
            "candidate",
            SourceSpec(
                origin_id=origin,
                source_kind="model-output",
                authority_rank=rank,
                assurance_tags=frozenset(),
                epoch=10,
            ),
        )

    def test_unverified_source_is_tainted_and_blocked(self):
        artifact = self.unverified_source()
        self.assertIn(Taint.UNVERIFIED, artifact.taints)
        decision = self.engine.release_decision(artifact, self.safe_policy, current_epoch=10)
        self.assertFalse(decision.allowed)
        self.assertEqual("FREEZE", decision.state)
        self.assertIn("FORBIDDEN_TAINT:UNVERIFIED", decision.reason_codes)

    def test_transform_does_not_upgrade_authority(self):
        low = self.unverified_source(rank=17)
        derived = self.engine.derive(
            "rewritten",
            [low],
            TransformContract(contract_id="rewrite", preserved_assurances=frozenset({"verified"})),
            epoch=11,
        )
        self.assertEqual(17, derived.authority_floor)

    def test_multiple_transforms_cannot_launder_unverified_taint(self):
        artifact = self.unverified_source(rank=99)
        for i in range(5):
            artifact = self.engine.derive(
                f"stage-{i}",
                [artifact],
                TransformContract(contract_id=f"stage:{i}", preserved_assurances=frozenset({"verified"})),
                epoch=11 + i,
            )
        self.assertIn(Taint.UNVERIFIED, artifact.taints)
        decision = self.engine.release_decision(artifact, self.safe_policy, current_epoch=15)
        self.assertFalse(decision.allowed)

    def test_merge_uses_weakest_authority_floor(self):
        high = self.verified_source(rank=90, origin="root:high")
        low = self.verified_source(rank=30, origin="root:low")
        merged = self.engine.derive(
            "merge",
            [high, low],
            TransformContract(
                contract_id="merge",
                preserved_assurances=frozenset({"verified", "schema:valid"}),
            ),
            epoch=11,
        )
        self.assertEqual(30, merged.authority_floor)

    def test_merge_preserves_only_assurance_intersection_and_contract_allowlist(self):
        left = self.verified_source(rank=80, origin="left")
        right = self.engine.source(
            "right",
            SourceSpec(
                origin_id="right",
                source_kind="canonical",
                authority_rank=80,
                assurance_tags=frozenset({"verified", "schema:valid", "integration:passed"}),
                epoch=10,
            ),
        )
        merged = self.engine.derive(
            "merge",
            [left, right],
            TransformContract(
                contract_id="merge",
                preserved_assurances=frozenset({"verified", "schema:valid", "unit:passed", "integration:passed"}),
            ),
            epoch=11,
        )
        self.assertEqual(frozenset({"verified", "schema:valid"}), merged.assurances)

    def test_contract_can_intentionally_drop_parent_assurance(self):
        src = self.verified_source()
        derived = self.engine.derive(
            "changed-semantics",
            [src],
            TransformContract(contract_id="semantic-change", preserved_assurances=frozenset({"verified"})),
            epoch=11,
        )
        self.assertEqual(frozenset({"verified"}), derived.assurances)

    def test_missing_required_assurance_rejects_transform(self):
        src = self.unverified_source()
        with self.assertRaises(ProvenanceError):
            self.engine.derive(
                "x",
                [src],
                TransformContract(contract_id="must-verify", required_assurances=frozenset({"verified"})),
                epoch=11,
            )

    def test_nondeterministic_transform_adds_sticky_taint(self):
        src = self.verified_source()
        derived = self.engine.derive(
            "random-ish",
            [src],
            TransformContract(
                contract_id="nondeterministic",
                deterministic=False,
                preserved_assurances=frozenset({"verified", "schema:valid"}),
            ),
            epoch=11,
        )
        self.assertIn(Taint.NONDETERMINISTIC, derived.taints)
        decision = self.engine.release_decision(derived, self.safe_policy, current_epoch=11)
        self.assertIn("NONDETERMINISTIC_LINEAGE", decision.reason_codes)

    def test_verification_receipt_is_bound_to_exact_artifact(self):
        a = self.unverified_source(origin="a")
        b = self.unverified_source(origin="b")
        receipt = self.engine.issue_verification(
            a,
            verifier_id="judge",
            added_assurances={"verified"},
            cleared_taints={Taint.UNVERIFIED},
            issued_epoch=10,
        )
        with self.assertRaises(ProvenanceError):
            self.engine.apply_verification(b, receipt, current_epoch=10)

    def test_verification_can_add_assurance_without_upgrading_authority(self):
        src = self.unverified_source(rank=7)
        receipt = self.engine.issue_verification(
            src,
            verifier_id="judge",
            added_assurances={"verified", "schema:valid"},
            cleared_taints={Taint.UNVERIFIED},
            issued_epoch=10,
        )
        verified = self.engine.apply_verification(src, receipt, current_epoch=10)
        self.assertEqual(7, verified.authority_floor)
        self.assertIn("verified", verified.assurances)
        self.assertNotIn(Taint.UNVERIFIED, verified.taints)

    def test_receipt_replay_is_idempotent_on_same_input_and_rejected_after_state_change(self):
        src = self.unverified_source()
        receipt = self.engine.issue_verification(
            src,
            verifier_id="judge",
            added_assurances={"verified"},
            cleared_taints={Taint.UNVERIFIED},
            issued_epoch=10,
        )
        once = self.engine.apply_verification(src, receipt, current_epoch=10)
        twice_from_same_input = self.engine.apply_verification(src, receipt, current_epoch=10)
        self.assertEqual(once, twice_from_same_input)
        with self.assertRaises(ProvenanceError):
            self.engine.apply_verification(once, receipt, current_epoch=10)

    def test_expired_receipt_is_rejected(self):
        src = self.unverified_source()
        receipt = self.engine.issue_verification(
            src, verifier_id="judge", issued_epoch=10, expires_epoch=11
        )
        with self.assertRaises(ProvenanceError):
            self.engine.apply_verification(src, receipt, current_epoch=12)

    def test_future_receipt_is_rejected(self):
        src = self.unverified_source()
        receipt = self.engine.issue_verification(
            src, verifier_id="judge", issued_epoch=12
        )
        with self.assertRaises(ProvenanceError):
            self.engine.apply_verification(src, receipt, current_epoch=11)

    def test_receipt_cannot_clear_unknown_origin(self):
        src = self.engine.source(
            "x",
            SourceSpec(origin_id="", source_kind="external", authority_rank=90, epoch=1),
        )
        receipt = self.engine.issue_verification(
            src,
            verifier_id="judge",
            cleared_taints={Taint.UNKNOWN_ORIGIN},
            issued_epoch=1,
        )
        with self.assertRaises(ProvenanceError):
            self.engine.apply_verification(src, receipt, current_epoch=1)

    def test_protected_conflict_taint_survives_transform(self):
        src = self.engine.source(
            "x",
            SourceSpec(
                origin_id="conflicted",
                source_kind="external",
                authority_rank=99,
                assurance_tags=frozenset({"verified", "schema:valid"}),
                taints=frozenset({Taint.CONFLICT}),
                epoch=1,
            ),
        )
        derived = self.engine.derive(
            "y",
            [src],
            TransformContract(
                contract_id="rewrite",
                preserved_assurances=frozenset({"verified", "schema:valid"}),
            ),
            epoch=2,
        )
        self.assertIn(Taint.CONFLICT, derived.taints)

    def test_release_allows_clean_artifact_when_policy_satisfied(self):
        src = self.verified_source(rank=80, epoch=10)
        decision = self.engine.release_decision(src, self.safe_policy, current_epoch=10)
        self.assertTrue(decision.allowed)
        self.assertEqual("ALLOW", decision.state)
        self.assertEqual((), decision.reason_codes)

    def test_release_reasons_are_sorted_and_deterministic(self):
        src = self.unverified_source(rank=1)
        policy = ReleasePolicy(
            policy_id="p",
            min_authority_rank=100,
            required_assurances=frozenset({"z", "a"}),
            forbidden_taints=frozenset(Taint),
            allowed_root_origins=frozenset({"other"}),
        )
        d1 = self.engine.release_decision(src, policy, current_epoch=10)
        d2 = self.engine.release_decision(src, policy, current_epoch=10)
        self.assertEqual(d1, d2)
        self.assertEqual(tuple(sorted(d1.reason_codes)), d1.reason_codes)

    def test_release_blocks_stale_artifact(self):
        src = self.verified_source(epoch=1)
        decision = self.engine.release_decision(src, self.safe_policy, current_epoch=12)
        self.assertIn("ARTIFACT_STALE", decision.reason_codes)

    def test_release_blocks_future_artifact(self):
        src = self.verified_source(epoch=20)
        decision = self.engine.release_decision(src, self.safe_policy, current_epoch=10)
        self.assertIn("ARTIFACT_FROM_FUTURE", decision.reason_codes)

    def test_release_can_restrict_root_origins(self):
        src = self.verified_source(origin="root:not-allowed")
        policy = dataclasses.replace(self.safe_policy, allowed_root_origins=frozenset({"root:allowed"}))
        decision = self.engine.release_decision(src, policy, current_epoch=10)
        self.assertIn("DISALLOWED_ROOT:root:not-allowed", decision.reason_codes)

    def test_root_origins_union_is_sorted_and_unique(self):
        a = self.verified_source(origin="z")
        b = self.verified_source(origin="a")
        merged = self.engine.derive(
            "m",
            [a, b, a],
            TransformContract(
                contract_id="merge",
                preserved_assurances=frozenset({"verified", "schema:valid"}),
            ),
            epoch=11,
        )
        self.assertEqual(("a", "z"), merged.root_origins)

    def test_same_inputs_create_same_source_identity(self):
        spec = SourceSpec(
            origin_id="same",
            source_kind="canonical",
            authority_rank=70,
            assurance_tags=frozenset({"verified"}),
            epoch=1,
        )
        a = self.engine.source("same payload", spec, metadata={"b": "2", "a": "1"})
        b = self.engine.source("same payload", spec, metadata={"a": "1", "b": "2"})
        self.assertEqual(a.artifact_id, b.artifact_id)

    def test_parent_order_is_semantically_bound_into_identity(self):
        a = self.verified_source(origin="a")
        b = self.verified_source(origin="b")
        contract = TransformContract(
            contract_id="ordered-combine",
            preserved_assurances=frozenset({"verified", "schema:valid"}),
        )
        ab = self.engine.derive("same", [a, b], contract, epoch=11)
        ba = self.engine.derive("same", [b, a], contract, epoch=11)
        self.assertNotEqual(ab.artifact_id, ba.artifact_id)

    def test_metadata_is_canonicalized(self):
        src = self.engine.source(
            "x",
            SourceSpec(origin_id="o", source_kind="s", authority_rank=1, epoch=0),
            metadata={"z": "last", "a": "first"},
        )
        self.assertEqual((("a", "first"), ("z", "last")), src.metadata)

    def test_non_string_metadata_rejected(self):
        with self.assertRaises(ProvenanceError):
            self.engine.source(
                "x",
                SourceSpec(origin_id="o", source_kind="s", authority_rank=1, epoch=0),
                metadata={"a": 1},  # type: ignore[arg-type]
            )

    def test_tampered_artifact_fails_integrity(self):
        src = self.verified_source()
        tampered = dataclasses.replace(src, authority_floor=999)
        with self.assertRaises(IntegrityError):
            self.engine.assert_integrity(tampered)

    def test_direct_self_cycle_is_rejected(self):
        src = self.verified_source()
        forged = dataclasses.replace(src, parent_ids=(src.artifact_id,))
        with self.assertRaises(IntegrityError):
            self.engine.assert_integrity(forged)

    def test_invalid_authority_rank_rejected(self):
        with self.assertRaises(ProvenanceError):
            self.engine.source(
                "x",
                SourceSpec(origin_id="o", source_kind="s", authority_rank=-1, epoch=0),
            )

    def test_invalid_source_kind_rejected(self):
        with self.assertRaises(ProvenanceError):
            self.engine.source(
                "x",
                SourceSpec(origin_id="o", source_kind=" ", authority_rank=1, epoch=0),
            )

    def test_derive_requires_parent(self):
        with self.assertRaises(ProvenanceError):
            self.engine.derive(
                "x",
                [],
                TransformContract(contract_id="x"),
                epoch=1,
            )

    def test_policy_with_negative_max_age_is_rejected(self):
        src = self.verified_source()
        policy = dataclasses.replace(self.safe_policy, max_age_epochs=-1)
        with self.assertRaises(ProvenanceError):
            self.engine.release_decision(src, policy, current_epoch=10)

    def test_external_untrusted_taint_cannot_be_cleared_by_verification(self):
        src = self.engine.source(
            "external",
            SourceSpec(
                origin_id="external:1",
                source_kind="external",
                authority_rank=80,
                taints=frozenset({Taint.EXTERNAL_UNTRUSTED}),
                epoch=1,
            ),
        )
        receipt = self.engine.issue_verification(
            src,
            verifier_id="judge",
            cleared_taints={Taint.EXTERNAL_UNTRUSTED},
            issued_epoch=1,
        )
        with self.assertRaises(ProvenanceError):
            self.engine.apply_verification(src, receipt, current_epoch=1)

    def test_verification_changes_artifact_identity(self):
        src = self.unverified_source()
        receipt = self.engine.issue_verification(
            src,
            verifier_id="judge",
            added_assurances={"verified"},
            cleared_taints={Taint.UNVERIFIED},
            issued_epoch=10,
        )
        verified = self.engine.apply_verification(src, receipt, current_epoch=10)
        self.assertNotEqual(src.artifact_id, verified.artifact_id)
        self.assertEqual((receipt.receipt_id,), verified.applied_receipts)

    def test_tampered_receipt_identity_is_rejected(self):
        src = self.unverified_source()
        receipt = self.engine.issue_verification(
            src, verifier_id="judge", added_assurances={"verified"}, issued_epoch=10
        )
        tampered = dataclasses.replace(receipt, verifier_id="attacker")
        with self.assertRaises(ProvenanceError):
            self.engine.apply_verification(src, tampered, current_epoch=10)

    def test_receipt_expiry_cannot_precede_issue(self):
        src = self.unverified_source()
        with self.assertRaises(ProvenanceError):
            self.engine.issue_verification(
                src, verifier_id="judge", issued_epoch=10, expires_epoch=9
            )

    def test_transform_preserves_all_parent_taints(self):
        a = self.engine.source(
            "a",
            SourceSpec(
                origin_id="a",
                source_kind="external",
                authority_rank=80,
                assurance_tags=frozenset({"verified"}),
                taints=frozenset({Taint.CONFLICT}),
                epoch=1,
            ),
        )
        b = self.engine.source(
            "b",
            SourceSpec(
                origin_id="b",
                source_kind="external",
                authority_rank=80,
                assurance_tags=frozenset({"verified"}),
                taints=frozenset({Taint.POLICY_MISMATCH}),
                epoch=1,
            ),
        )
        d = self.engine.derive(
            "d",
            [a, b],
            TransformContract(contract_id="merge", preserved_assurances=frozenset({"verified"})),
            epoch=2,
        )
        self.assertTrue({Taint.CONFLICT, Taint.POLICY_MISMATCH}.issubset(d.taints))

    def test_release_does_not_require_evidence_class_ordering(self):
        src = self.engine.source(
            "x",
            SourceSpec(
                origin_id="o",
                source_kind="canonical",
                authority_rank=100,
                assurance_tags=frozenset({"verified", "evidence:E2:unit"}),
                epoch=0,
            ),
        )
        exact = ReleasePolicy(
            policy_id="exact",
            required_assurances=frozenset({"evidence:E2:unit"}),
            forbidden_taints=frozenset(),
        )
        wrong_class = ReleasePolicy(
            policy_id="wrong",
            required_assurances=frozenset({"evidence:E6:deployment"}),
            forbidden_taints=frozenset(),
        )
        self.assertTrue(self.engine.release_decision(src, exact, current_epoch=0).allowed)
        self.assertFalse(self.engine.release_decision(src, wrong_class, current_epoch=0).allowed)


if __name__ == "__main__":
    unittest.main()
