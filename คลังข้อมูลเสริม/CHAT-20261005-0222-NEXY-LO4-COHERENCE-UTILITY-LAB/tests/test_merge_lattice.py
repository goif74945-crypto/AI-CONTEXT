import itertools
import unittest

from lo4lab.merge_lattice import Claim, MergeError, Replica, Retraction, merge_replicas


class TestMergeLattice(unittest.TestCase):
    def claims(self):
        a = Claim("a", "NEXY", "count", "project", 837, 10, "e1")
        b = Claim("b", "NEXY", "count", "project", 837, 10, "e2")
        c = Claim("c", "NEXY", "mode", "project", "verify-only", 10, "e3")
        return a, b, c

    def test_merge_is_commutative_across_permutations(self):
        a, b, c = self.claims()
        replicas = [Replica((a,)), Replica((b,)), Replica((c,))]
        fps = {merge_replicas(order).state_fingerprint for order in itertools.permutations(replicas)}
        self.assertEqual(len(fps), 1)

    def test_merge_is_idempotent(self):
        a, _, _ = self.claims()
        one = merge_replicas([Replica((a,))])
        two = merge_replicas([Replica((a,)), Replica((a,))])
        self.assertEqual(one.state_fingerprint, two.state_fingerprint)

    def test_top_authority_conflict_preserved(self):
        a = Claim("a", "x", "p", "s", 1, 5, "e1")
        b = Claim("b", "x", "p", "s", 2, 5, "e2")
        result = merge_replicas([Replica((a,)), Replica((b,))])
        self.assertEqual(result.status, "CONFLICT")
        self.assertEqual(result.resolved[0].status, "CONFLICT")

    def test_lower_authority_disagreement_not_promoted(self):
        a = Claim("a", "x", "p", "s", 1, 10, "e1")
        b = Claim("b", "x", "p", "s", 2, 1, "e2")
        result = merge_replicas([Replica((a, b))])
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.resolved[0].values, (1,))

    def test_retraction_is_append_only_tombstone(self):
        a = Claim("a", "x", "p", "s", 1, 10, "e1")
        r = Retraction("r1", "a", "superseded")
        result = merge_replicas([Replica((a,)), Replica((), (r,))])
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.resolved, ())
        self.assertEqual(result.retractions, (r,))

    def test_identity_collision_rejected(self):
        a = Claim("same", "x", "p", "s", 1, 1, "e")
        b = Claim("same", "x", "p", "s", 2, 1, "e")
        with self.assertRaises(MergeError):
            merge_replicas([Replica((a,)), Replica((b,))])

    def test_unknown_retraction_target_rejected(self):
        with self.assertRaises(MergeError):
            merge_replicas([Replica((), (Retraction("r", "missing", "bad"),))])


if __name__ == "__main__":
    unittest.main()
