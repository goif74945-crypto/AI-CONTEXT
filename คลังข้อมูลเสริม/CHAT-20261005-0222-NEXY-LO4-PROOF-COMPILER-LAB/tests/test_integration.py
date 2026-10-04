import unittest

from nexy_lo4_lab.integration import run_reference_pipeline


class IntegrationTests(unittest.TestCase):
    def test_all_five_systems_compose(self):
        result = run_reference_pipeline()
        self.assertEqual(result.proof_probe_ids, ("unit-check",))
        self.assertEqual(result.witness_kinds, ("positive", "negative", "missing"))
        self.assertEqual(result.compile_result.status, "PASS")
        self.assertEqual(len(result.authority_digest), 64)


if __name__ == "__main__":
    unittest.main()
