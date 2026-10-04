import unittest

from nexy_lo4_lab.uncertainty import (
    ClaimNode,
    EpistemicStatus,
    LatticeError,
    UncertaintyContainmentLattice,
)


class UncertaintyContainmentLatticeTests(unittest.TestCase):
    def setUp(self):
        self.lattice = UncertaintyContainmentLattice()

    def test_unverified_propagates_only_to_dependents(self):
        out = self.lattice.evaluate(
            [
                ClaimNode("a", EpistemicStatus.NOT_VERIFIED),
                ClaimNode("b", EpistemicStatus.PASS, ("a",)),
                ClaimNode("c", EpistemicStatus.PASS),
            ]
        )
        self.assertEqual(out["b"].effective_status, EpistemicStatus.NOT_VERIFIED)
        self.assertEqual(out["b"].blockers, ("a",))
        self.assertEqual(out["c"].effective_status, EpistemicStatus.PASS)

    def test_conflict_dominates_unknown_on_dependency_path(self):
        out = self.lattice.evaluate(
            [
                ClaimNode("u", EpistemicStatus.UNKNOWN),
                ClaimNode("x", EpistemicStatus.CONFLICT),
                ClaimNode("z", EpistemicStatus.PASS, ("u", "x")),
            ]
        )
        self.assertEqual(out["z"].effective_status, EpistemicStatus.CONFLICT)
        self.assertEqual(out["z"].blockers, ("u", "x"))

    def test_local_failure_dominates_dependency(self):
        out = self.lattice.evaluate(
            [
                ClaimNode("dep", EpistemicStatus.UNKNOWN),
                ClaimNode("root", EpistemicStatus.FAIL, ("dep",)),
            ]
        )
        self.assertEqual(out["root"].effective_status, EpistemicStatus.FAIL)

    def test_missing_dependency_fails(self):
        with self.assertRaisesRegex(LatticeError, "missing dependencies"):
            self.lattice.evaluate([ClaimNode("a", EpistemicStatus.PASS, ("missing",))])

    def test_invalid_status_fails_closed(self):
        with self.assertRaisesRegex(LatticeError, "invalid epistemic status"):
            self.lattice.evaluate([ClaimNode("a", "PASS")])  # type: ignore[arg-type]

    def test_duplicate_dependency_fails(self):
        with self.assertRaisesRegex(LatticeError, "duplicate dependency"):
            self.lattice.evaluate([
                ClaimNode("a", EpistemicStatus.PASS),
                ClaimNode("b", EpistemicStatus.PASS, ("a", "a")),
            ])

    def test_cycle_fails(self):
        with self.assertRaisesRegex(LatticeError, "cycle"):
            self.lattice.evaluate(
                [
                    ClaimNode("a", EpistemicStatus.PASS, ("b",)),
                    ClaimNode("b", EpistemicStatus.PASS, ("a",)),
                ]
            )


if __name__ == "__main__":
    unittest.main()
