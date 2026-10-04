import unittest

from lo4lab.bitemporal import BitemporalError, FactVersion, resolve_at


class TestBitemporal(unittest.TestCase):
    def base(self):
        return FactVersion("f1", "NEXY", "count", 837, 0, None, 10, "matrix", 10)

    def test_known_time_prevents_future_knowledge_leak(self):
        late = FactVersion("f2", "NEXY", "count", 900, 0, None, 20, "later", 10, ("f1",))
        before = resolve_at([self.base(), late], subject="NEXY", attribute="count", valid_time=5, known_time=15)
        after = resolve_at([self.base(), late], subject="NEXY", attribute="count", valid_time=5, known_time=25)
        self.assertEqual(before.values, (837,))
        self.assertEqual(after.values, (900,))

    def test_valid_time_separates_real_world_change(self):
        old = FactVersion("a", "svc", "state", "A", 0, 10, 1, "obs", 5)
        new = FactVersion("b", "svc", "state", "B", 10, None, 11, "obs", 5)
        self.assertEqual(resolve_at([old, new], subject="svc", attribute="state", valid_time=9, known_time=20).values, ("A",))
        self.assertEqual(resolve_at([old, new], subject="svc", attribute="state", valid_time=10, known_time=20).values, ("B",))

    def test_explicit_supersession_removes_prior_fact(self):
        correction = FactVersion("f2", "NEXY", "count", 838, 0, None, 11, "matrix", 10, ("f1",))
        report = resolve_at([self.base(), correction], subject="NEXY", attribute="count", valid_time=1, known_time=20)
        self.assertEqual(report.status, "PASS")
        self.assertEqual(report.values, (838,))

    def test_equal_top_authority_disagreement_is_conflict(self):
        other = FactVersion("f2", "NEXY", "count", 999, 0, None, 11, "other", 10)
        report = resolve_at([self.base(), other], subject="NEXY", attribute="count", valid_time=1, known_time=20)
        self.assertEqual(report.status, "CONFLICT")
        self.assertEqual(set(report.values), {837, 999})

    def test_lower_authority_does_not_override(self):
        low = FactVersion("f2", "NEXY", "count", 999, 0, None, 11, "rumor", 1)
        report = resolve_at([self.base(), low], subject="NEXY", attribute="count", valid_time=1, known_time=20)
        self.assertEqual(report.values, (837,))
        self.assertEqual(report.ignored_lower_authority_ids, ("f2",))

    def test_supersession_cycle_rejected(self):
        a = FactVersion("a", "x", "y", 1, 0, None, 1, "s", 1, ("b",))
        b = FactVersion("b", "x", "y", 2, 0, None, 1, "s", 1, ("a",))
        with self.assertRaises(BitemporalError):
            resolve_at([a, b], subject="x", attribute="y", valid_time=1, known_time=1)

    def test_unknown_when_no_eligible_fact(self):
        report = resolve_at([self.base()], subject="NEXY", attribute="count", valid_time=-1, known_time=5)
        self.assertEqual(report.status, "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
