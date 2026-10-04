from __future__ import annotations

import dataclasses
import unittest

from lbcc.codec import compact, rehydrate
from lbcc.model import CodecPolicy, CodecStatus, ContextAtom, ContextBundle, TruthClass
from lbcc.serialization import canonical_json_bytes
from lbcc.verify import verify_against_source


def atom(
    atom_id: str,
    text: str = "x",
    truth: TruthClass = TruthClass.INFERENCE,
    authority: int = 10,
    immutable: bool = False,
    provenance: tuple[str, ...] = (),
    evidence: tuple[str, ...] = (),
) -> ContextAtom:
    return ContextAtom(
        atom_id=atom_id,
        text=text,
        truth_class=truth,
        authority_rank=authority,
        immutable=immutable,
        provenance=provenance,
        evidence=evidence,
    )


class CodecTests(unittest.TestCase):
    def test_deterministic_output(self) -> None:
        bundle = ContextBundle("b", (atom("b", "B" * 200), atom("a", "A" * 200)))
        policy = CodecPolicy(max_capsule_bytes=1600, max_loss_ppm=1_000_000)
        r1 = compact(bundle, policy)
        r2 = compact(bundle, policy)
        self.assertEqual(canonical_json_bytes(r1), canonical_json_bytes(r2))

    def test_full_fit_zero_loss(self) -> None:
        bundle = ContextBundle("b", (atom("a", "small"), atom("b", "small2")))
        result = compact(bundle, CodecPolicy(max_capsule_bytes=5000, max_loss_ppm=0))
        self.assertEqual(result.status, CodecStatus.PASS)
        self.assertEqual(result.metrics.dropped_atoms, 0)
        self.assertEqual(result.metrics.loss_ppm, 0)

    def test_protected_immutable_causes_freeze_if_too_large(self) -> None:
        bundle = ContextBundle("b", (atom("law", "L" * 5000, authority=100, immutable=True),))
        result = compact(bundle, CodecPolicy(max_capsule_bytes=500, max_loss_ppm=1_000_000))
        self.assertEqual(result.status, CodecStatus.FREEZE)
        self.assertIn("protected atoms exceed", result.reason or "")

    def test_unknown_is_protected(self) -> None:
        u = atom("u", "U" * 500, truth=TruthClass.UNKNOWN, authority=20)
        low = atom("l", "L" * 500, truth=TruthClass.INFERENCE, authority=20)
        bundle = ContextBundle("b", (u, low))
        result = compact(bundle, CodecPolicy(max_capsule_bytes=1300, max_loss_ppm=1_000_000))
        self.assertEqual(result.status, CodecStatus.PASS)
        retained = {a.atom_id for a in result.capsule.retained_atoms}  # type: ignore[union-attr]
        self.assertIn("u", retained)

    def test_conflict_is_protected(self) -> None:
        c = atom("c", "conflict", truth=TruthClass.CONFLICT)
        result = compact(ContextBundle("b", (c,)), CodecPolicy(max_capsule_bytes=3000))
        self.assertEqual(result.status, CodecStatus.PASS)
        self.assertEqual(result.capsule.retained_atoms[0].atom_id, "c")  # type: ignore[union-attr]

    def test_authority_threshold_protects_atom(self) -> None:
        high = atom("h", "H" * 1000, authority=95)
        bundle = ContextBundle("b", (high, atom("l", "L" * 1000)))
        result = compact(bundle, CodecPolicy(max_capsule_bytes=1800, max_loss_ppm=1_000_000))
        self.assertEqual(result.status, CodecStatus.PASS)
        self.assertIn("h", {a.atom_id for a in result.capsule.retained_atoms})  # type: ignore[union-attr]

    def test_loss_budget_freezes(self) -> None:
        bundle = ContextBundle("b", tuple(atom(str(i), "X" * 500) for i in range(6)))
        result = compact(bundle, CodecPolicy(max_capsule_bytes=1100, max_loss_ppm=100_000))
        self.assertEqual(result.status, CodecStatus.FREEZE)
        self.assertIn("loss budget exceeded", result.reason or "")

    def test_capsule_never_exceeds_budget_on_pass(self) -> None:
        bundle = ContextBundle("b", tuple(atom(str(i), "X" * 350) for i in range(10)))
        policy = CodecPolicy(max_capsule_bytes=1800, max_loss_ppm=1_000_000)
        result = compact(bundle, policy)
        self.assertEqual(result.status, CodecStatus.PASS)
        self.assertLessEqual(result.metrics.capsule_bytes, policy.max_capsule_bytes)

    def test_provenance_and_evidence_preserved(self) -> None:
        a = atom("a", "exact", provenance=("src:1",), evidence=("test:1",), authority=100)
        result = compact(ContextBundle("b", (a,)), CodecPolicy(max_capsule_bytes=3000))
        kept = result.capsule.retained_atoms[0]  # type: ignore[union-attr]
        self.assertEqual(kept.provenance, ("src:1",))
        self.assertEqual(kept.evidence, ("test:1",))
        self.assertEqual(kept.text, "exact")

    def test_verifier_accepts_valid_result(self) -> None:
        bundle = ContextBundle("b", (atom("a", "A" * 100), atom("b", "B" * 100)))
        policy = CodecPolicy(max_capsule_bytes=1300, max_loss_ppm=1_000_000)
        result = compact(bundle, policy)
        report = verify_against_source(bundle, result, policy)
        self.assertTrue(report.passed, report.failures)

    def test_verifier_rejects_tampered_metrics(self) -> None:
        bundle = ContextBundle("b", (atom("a", "original", authority=100),))
        policy = CodecPolicy(max_capsule_bytes=3000)
        result = compact(bundle, policy)
        bad_metrics = dataclasses.replace(result.metrics, capsule_bytes=result.metrics.capsule_bytes + 1)
        tampered = dataclasses.replace(result, metrics=bad_metrics)
        report = verify_against_source(bundle, tampered, policy)
        self.assertFalse(report.passed)
        self.assertIn("result metrics mismatch", report.failures)

    def test_verifier_rejects_tampered_loss_ledger(self) -> None:
        bundle = ContextBundle("b", (atom("a", "A" * 700), atom("b", "B" * 700)))
        policy = CodecPolicy(max_capsule_bytes=1100, max_loss_ppm=1_000_000)
        result = compact(bundle, policy)
        self.assertEqual(result.status, CodecStatus.PASS)
        self.assertTrue(result.loss_ledger)
        bad_ref = dataclasses.replace(result.loss_ledger[0], atom_sha256="0" * 64)
        tampered = dataclasses.replace(result, loss_ledger=(bad_ref, *result.loss_ledger[1:]))
        report = verify_against_source(bundle, tampered, policy)
        self.assertFalse(report.passed)
        self.assertTrue(any("loss ledger" in x or "commitment" in x for x in report.failures))

    def test_verifier_rejects_tampered_retained_atom(self) -> None:
        bundle = ContextBundle("b", (atom("a", "original", authority=100),))
        policy = CodecPolicy(max_capsule_bytes=3000)
        result = compact(bundle, policy)
        cap = result.capsule
        self.assertIsNotNone(cap)
        tampered_atom = dataclasses.replace(cap.retained_atoms[0], text="tampered")
        tampered_cap = dataclasses.replace(cap, retained_atoms=(tampered_atom,))
        tampered_result = dataclasses.replace(result, capsule=tampered_cap)
        report = verify_against_source(bundle, tampered_result, policy)
        self.assertFalse(report.passed)
        self.assertTrue(any("retained atom mismatch" in x for x in report.failures))

    def test_rehydrate_roundtrip(self) -> None:
        atoms = tuple(atom(str(i), f"text-{i}" * 50) for i in range(5))
        bundle = ContextBundle("b", atoms)
        policy = CodecPolicy(max_capsule_bytes=1200, max_loss_ppm=1_000_000)
        result = compact(bundle, policy)
        self.assertEqual(result.status, CodecStatus.PASS)
        restored = rehydrate(result.capsule, result.loss_ledger, {a.atom_id: a for a in atoms})  # type: ignore[arg-type]
        self.assertEqual(
            tuple(sorted(restored.atoms, key=lambda a: a.atom_id)),
            tuple(sorted(bundle.atoms, key=lambda a: a.atom_id)),
        )

    def test_rehydrate_rejects_wrong_store_value(self) -> None:
        atoms = (atom("a", "A" * 600), atom("b", "B" * 600))
        bundle = ContextBundle("b", atoms)
        result = compact(bundle, CodecPolicy(max_capsule_bytes=1000, max_loss_ppm=1_000_000))
        self.assertEqual(result.status, CodecStatus.PASS)
        store = {a.atom_id: a for a in atoms}
        dropped = result.loss_ledger[0].atom_id
        store[dropped] = dataclasses.replace(store[dropped], text="bad")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            rehydrate(result.capsule, result.loss_ledger, store)  # type: ignore[arg-type]

    def test_duplicate_ids_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate atom_id"):
            ContextBundle("b", (atom("x"), atom("x")))

    def test_invalid_authority_rejected(self) -> None:
        with self.assertRaises(ValueError):
            atom("x", authority=101)

    def test_empty_text_rejected(self) -> None:
        with self.assertRaises(ValueError):
            atom("x", text="   ")

    def test_metadata_is_deep_frozen_against_caller_mutation(self) -> None:
        raw = {"nested": ["a", {"n": 1}]}
        a = ContextAtom("x", "text", TruthClass.INFERENCE, metadata=raw)
        before = canonical_json_bytes(a)
        raw["nested"].append("mutated")
        raw["other"] = "later"
        self.assertEqual(canonical_json_bytes(a), before)

    def test_metadata_rejects_non_string_keys_and_floats(self) -> None:
        with self.assertRaisesRegex(ValueError, "keys must be strings"):
            ContextAtom("x", "text", TruthClass.INFERENCE, metadata={1: "bad"})
        with self.assertRaisesRegex(ValueError, "must not contain floats"):
            ContextAtom("x", "text", TruthClass.INFERENCE, metadata={"ratio": 0.5})


if __name__ == "__main__":
    unittest.main()
