from __future__ import annotations

import itertools
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nexy_provenance_taint import ProvenanceEngine, SourceSpec, Taint, TransformContract  # noqa: E402


class MonotonicityPropertyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = ProvenanceEngine()

    def mk(self, name: str, rank: int, assurances: frozenset[str], taints: frozenset[Taint]):
        return self.engine.source(
            name,
            SourceSpec(
                origin_id=f"origin:{name}",
                source_kind="property",
                authority_rank=rank,
                assurance_tags=assurances,
                taints=taints,
                epoch=1,
            ),
        )

    def test_authority_is_monotone_non_increasing_for_pairwise_merges(self):
        ranks = [0, 1, 7, 50, 100]
        for left_rank, right_rank in itertools.product(ranks, repeat=2):
            with self.subTest(left=left_rank, right=right_rank):
                left = self.mk("l", left_rank, frozenset({"verified"}), frozenset())
                right = self.mk("r", right_rank, frozenset({"verified"}), frozenset())
                out = self.engine.derive(
                    "out",
                    [left, right],
                    TransformContract(contract_id="pair", preserved_assurances=frozenset({"verified"})),
                    epoch=2,
                )
                self.assertEqual(min(left_rank, right_rank), out.authority_floor)
                self.assertLessEqual(out.authority_floor, left_rank)
                self.assertLessEqual(out.authority_floor, right_rank)

    def test_assurance_output_is_subset_of_every_parent_and_preservation_allowlist(self):
        universe = ["verified", "schema", "unit"]
        sets = [frozenset(s) for r in range(4) for s in itertools.combinations(universe, r)]
        preserve = frozenset(universe)
        for a_set, b_set in itertools.product(sets, repeat=2):
            with self.subTest(a=a_set, b=b_set):
                a = self.mk("a", 10, a_set, frozenset())
                b = self.mk("b", 10, b_set, frozenset())
                out = self.engine.derive(
                    "out",
                    [a, b],
                    TransformContract(contract_id="pair", preserved_assurances=preserve),
                    epoch=2,
                )
                self.assertTrue(out.assurances.issubset(a.assurances))
                self.assertTrue(out.assurances.issubset(b.assurances))
                self.assertTrue(out.assurances.issubset(preserve))

    def test_taints_are_monotone_non_decreasing_under_ordinary_transform(self):
        candidates = [Taint.CONFLICT, Taint.POLICY_MISMATCH, Taint.EXTERNAL_UNTRUSTED]
        taint_sets = [frozenset(s) for r in range(4) for s in itertools.combinations(candidates, r)]
        for a_taints, b_taints in itertools.product(taint_sets, repeat=2):
            with self.subTest(a=a_taints, b=b_taints):
                a = self.mk("a", 10, frozenset({"verified"}), a_taints)
                b = self.mk("b", 10, frozenset({"verified"}), b_taints)
                out = self.engine.derive(
                    "out",
                    [a, b],
                    TransformContract(contract_id="pair", preserved_assurances=frozenset({"verified"})),
                    epoch=2,
                )
                self.assertTrue(a.taints.issubset(out.taints))
                self.assertTrue(b.taints.issubset(out.taints))

    def test_long_chain_cannot_erase_protected_taint(self):
        artifact = self.mk("root", 100, frozenset({"verified"}), frozenset({Taint.CONFLICT}))
        for i in range(64):
            artifact = self.engine.derive(
                f"payload:{i}",
                [artifact],
                TransformContract(
                    contract_id=f"step:{i}",
                    preserved_assurances=frozenset({"verified"}),
                ),
                epoch=2 + i,
            )
        self.assertIn(Taint.CONFLICT, artifact.taints)


if __name__ == "__main__":
    unittest.main()
