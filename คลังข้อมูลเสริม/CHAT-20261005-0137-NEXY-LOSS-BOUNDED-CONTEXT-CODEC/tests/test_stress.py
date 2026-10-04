from __future__ import annotations

import random
import unittest

from lbcc.codec import compact, is_protected
from lbcc.model import CodecPolicy, CodecStatus, ContextAtom, ContextBundle, TruthClass
from lbcc.serialization import canonical_json_bytes
from lbcc.verify import verify_against_source


class StressInvariantTests(unittest.TestCase):
    def test_randomized_budget_determinism_and_verification(self) -> None:
        truths = list(TruthClass)
        for seed in range(40):
            rng = random.Random(seed)
            atoms = []
            for i in range(rng.randint(8, 60)):
                atoms.append(
                    ContextAtom(
                        atom_id=f"{seed}-{i}",
                        text="x" * rng.randint(5, 180),
                        truth_class=truths[rng.randrange(len(truths))],
                        authority_rank=rng.randint(0, 94),
                        provenance=(f"seed:{seed}",),
                        evidence=(f"ev:{i}",) if rng.random() < 0.2 else (),
                    )
                )
            bundle = ContextBundle(f"b-{seed}", tuple(atoms))
            policy = CodecPolicy(
                max_capsule_bytes=rng.randint(2500, 9000),
                max_loss_ppm=1_000_000,
            )
            r1 = compact(bundle, policy)
            r2 = compact(bundle, policy)
            self.assertEqual(canonical_json_bytes(r1), canonical_json_bytes(r2))
            if r1.status == CodecStatus.PASS:
                self.assertLessEqual(r1.metrics.capsule_bytes, policy.max_capsule_bytes)
                report = verify_against_source(bundle, r1, policy)
                self.assertTrue(report.passed, report.failures)

    def test_all_protected_atoms_are_retained_on_pass(self) -> None:
        rng = random.Random(20261005)
        atoms = tuple(
            ContextAtom(
                atom_id=f"a-{i}",
                text="z" * rng.randint(20, 100),
                truth_class=TruthClass.CONFLICT if i % 17 == 0 else TruthClass.INFERENCE,
                authority_rank=99 if i % 23 == 0 else rng.randint(0, 80),
                immutable=(i % 29 == 0),
            )
            for i in range(200)
        )
        bundle = ContextBundle("protected-stress", atoms)
        policy = CodecPolicy(max_capsule_bytes=30000, max_loss_ppm=1_000_000)
        result = compact(bundle, policy)
        self.assertEqual(result.status, CodecStatus.PASS)
        kept = {a.atom_id for a in result.capsule.retained_atoms}  # type: ignore[union-attr]
        expected = {a.atom_id for a in atoms if is_protected(a, policy)}
        self.assertTrue(expected <= kept)


if __name__ == "__main__":
    unittest.main()
