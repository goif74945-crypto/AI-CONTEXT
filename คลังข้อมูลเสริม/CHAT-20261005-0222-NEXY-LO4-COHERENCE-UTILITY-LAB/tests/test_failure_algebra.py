import itertools
import unittest

from lo4lab.failure_algebra import FailureAlgebraError, Status, gate_required_dependencies, join_statuses


class TestFailureAlgebra(unittest.TestCase):
    def test_pass_is_identity(self):
        self.assertEqual(join_statuses([Status.PASS]).status, Status.PASS)
        self.assertEqual(join_statuses([Status.PASS, Status.NOT_VERIFIED]).status, Status.NOT_VERIFIED)

    def test_conflict_dominates_default_safe_policy(self):
        self.assertEqual(join_statuses([Status.FAIL, Status.CONFLICT, Status.PASS]).status, Status.CONFLICT)

    def test_join_is_commutative(self):
        statuses = [Status.PASS, Status.UNKNOWN, Status.FAIL]
        outputs = {join_statuses(order).aggregate_fingerprint for order in itertools.permutations(statuses)}
        self.assertEqual(len(outputs), 1)

    def test_join_is_idempotent(self):
        a = join_statuses([Status.FREEZE])
        b = join_statuses([Status.FREEZE, Status.FREEZE])
        self.assertEqual(a.aggregate_fingerprint, b.aggregate_fingerprint)

    def test_required_dependency_blocks_local_pass(self):
        result = gate_required_dependencies(Status.PASS, [Status.NOT_VERIFIED])
        self.assertEqual(result.status, Status.BLOCKED)

    def test_existing_failure_not_hidden_by_dependency_block(self):
        result = gate_required_dependencies(Status.FAIL, [Status.NOT_VERIFIED])
        self.assertEqual(result.status, Status.FAIL)

    def test_empty_join_rejected(self):
        with self.assertRaises(FailureAlgebraError):
            join_statuses([])


if __name__ == "__main__":
    unittest.main()
