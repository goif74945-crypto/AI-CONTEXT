from __future__ import annotations

import itertools
import unittest

from lo4lab.bitemporal import FactVersion, resolve_at
from lo4lab.failure_algebra import Status, join_statuses
from lo4lab.merge_lattice import Claim, Replica, merge_replicas
from lo4lab.terminology import TermDefinition, TerminologyRegistry


class TestAlgebraicProperties(unittest.TestCase):
    def test_failure_join_commutative_exhaustive(self):
        statuses = tuple(Status)
        for a in statuses:
            for b in statuses:
                with self.subTest(a=a, b=b):
                    self.assertEqual(join_statuses((a, b)).status, join_statuses((b, a)).status)

    def test_failure_join_associative_exhaustive(self):
        statuses = tuple(Status)
        for a in statuses:
            for b in statuses:
                for c in statuses:
                    left = join_statuses((join_statuses((a, b)).status, c)).status
                    right = join_statuses((a, join_statuses((b, c)).status)).status
                    with self.subTest(a=a, b=b, c=c):
                        self.assertEqual(left, right)

    def test_failure_join_idempotent_exhaustive(self):
        for status in Status:
            self.assertEqual(join_statuses((status, status)).status, status)

    def test_merge_permutation_invariance_four_replicas(self):
        replicas = (
            Replica(claims=(Claim("c1", "task", "state", "root", "ready", 10, "e1"),)),
            Replica(claims=(Claim("c2", "task", "owner", "root", "core", 10, "e2"),)),
            Replica(claims=(Claim("c3", "task", "state", "root", "stale", 5, "e3"),)),
            Replica(claims=(Claim("c4", "task", "mode", "root", "strict", 7, "e4"),)),
        )
        fingerprints = {merge_replicas(order).state_fingerprint for order in itertools.permutations(replicas)}
        self.assertEqual(len(fingerprints), 1)

    def test_bitemporal_result_is_input_order_invariant(self):
        rows = (
            FactVersion("f1", "svc", "version", "1", 0, 10, 1, "s1", 5),
            FactVersion("f2", "svc", "version", "2", 10, None, 12, "s2", 5),
            FactVersion("f3", "svc", "version", "2", 10, None, 13, "s3", 3),
        )
        fps = {
            resolve_at(order, subject="svc", attribute="version", valid_time=11, known_time=20).report_fingerprint
            for order in itertools.permutations(rows)
        }
        self.assertEqual(len(fps), 1)

    def test_terminology_resolution_is_definition_order_invariant(self):
        definitions = (
            TermDefinition("freeze", "", "stop legal progress", aliases=("halt",)),
            TermDefinition("freeze", "runtime", "stop runtime progress", aliases=("halt",)),
            TermDefinition("proof", "", "evidence satisfying a claim contract"),
        )
        fps = {
            TerminologyRegistry(order).resolve("halt", "runtime/worker").resolution_fingerprint
            for order in itertools.permutations(definitions)
        }
        self.assertEqual(len(fps), 1)


class TestContractTypes(unittest.TestCase):
    def test_unknown_bitemporal_result_uses_immutable_tuples(self):
        result = resolve_at((), subject="x", attribute="y", valid_time=1, known_time=1)
        self.assertIsInstance(result.values, tuple)
        self.assertIsInstance(result.supporting_fact_ids, tuple)
        self.assertIsInstance(result.ignored_lower_authority_ids, tuple)
        self.assertIsInstance(result.reason_codes, tuple)

    def test_unknown_terminology_result_uses_immutable_tuple_reason_codes(self):
        registry = TerminologyRegistry((TermDefinition("known", "", "known definition"),))
        result = registry.resolve("missing", "")
        self.assertIsInstance(result.reason_codes, tuple)


if __name__ == "__main__":
    unittest.main()
