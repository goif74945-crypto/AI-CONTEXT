import json
import unittest

from lo4q64 import Q64, SPECS, canonical_evaluation, evaluate, list_concepts, sha256_hex


class IntegrationTests(unittest.TestCase):
    def test_catalog_and_execution_agree(self):
        catalog = list_concepts()
        self.assertEqual(len(catalog), 20)
        self.assertEqual({x["concept_id"] for x in catalog}, set(SPECS))

    def test_all_ones_and_zeros_are_defined(self):
        for cid, spec in SPECS.items():
            for point in (Q64.zero(), Q64.one()):
                result = evaluate(cid, {k: point for k in spec.required_inputs})
                encoded = canonical_evaluation(result)
                decoded = json.loads(encoded)
                self.assertEqual(decoded["concept_id"], cid)
                self.assertEqual(len(sha256_hex(encoded)), 64)

    def test_release_artifact_is_byte_stable(self):
        cid = "L4Q64-20"
        spec = SPECS[cid]
        values = {k: Q64.from_basis_points((i + 1) * 1379 % 10001) for i, k in enumerate(spec.required_inputs)}
        hashes = {sha256_hex(canonical_evaluation(evaluate(cid, values))) for _ in range(100)}
        self.assertEqual(len(hashes), 1)


if __name__ == "__main__":
    unittest.main()
