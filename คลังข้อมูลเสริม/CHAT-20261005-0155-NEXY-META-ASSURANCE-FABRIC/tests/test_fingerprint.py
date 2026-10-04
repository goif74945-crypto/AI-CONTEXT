import unittest

from nexy_meta_assurance.fingerprint import (
    FingerprintError,
    ScenarioRecord,
    build_fingerprint,
    diff_fingerprints,
)


class FingerprintTests(unittest.TestCase):
    def test_mapping_key_order_does_not_change_digest(self):
        a = build_fingerprint([
            ScenarioRecord("S1", {"a": 1, "b": 2}, "PASS", {"x": 1, "y": 2})
        ])
        b = build_fingerprint([
            ScenarioRecord("S1", {"b": 2, "a": 1}, "PASS", {"y": 2, "x": 1})
        ])
        self.assertEqual(a.digest, b.digest)

    def test_behavior_change_is_precisely_reported(self):
        old = build_fingerprint([
            ScenarioRecord("S1", {"n": 1}, "PASS", {"v": 2}),
            ScenarioRecord("S2", {"n": 2}, "PASS", {"v": 4}),
        ])
        new = build_fingerprint([
            ScenarioRecord("S1", {"n": 1}, "PASS", {"v": 3}),
            ScenarioRecord("S3", {"n": 3}, "PASS", {"v": 6}),
        ])
        diff = diff_fingerprints(old, new)
        self.assertEqual(diff.changed, ("S1",))
        self.assertEqual(diff.removed, ("S2",))
        self.assertEqual(diff.added, ("S3",))

    def test_scenario_order_does_not_change_digest(self):
        records = [
            ScenarioRecord("B", 2, "PASS", 4),
            ScenarioRecord("A", 1, "PASS", 2),
        ]
        self.assertEqual(build_fingerprint(records).digest, build_fingerprint(reversed(records)).digest)

    def test_duplicate_scenario_ids_fail_closed(self):
        with self.assertRaises(FingerprintError):
            build_fingerprint([
                ScenarioRecord("S1", 1, "PASS", 2),
                ScenarioRecord("S1", 2, "PASS", 4),
            ])

    def test_float_payload_is_rejected_for_canonicality(self):
        with self.assertRaises(FingerprintError):
            build_fingerprint([ScenarioRecord("S1", {"x": 1.5}, "PASS", 1)])


if __name__ == "__main__":
    unittest.main()
