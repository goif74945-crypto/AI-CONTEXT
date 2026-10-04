import unittest
from dataclasses import replace

from nexy_live_integrity import CacheNamespace, CacheProvenanceFirewall, GateStatus
from nexy_live_integrity.cache_provenance import CacheEntry

H = "a" * 64
M = "b" * 64
T = "c" * 64


class CacheProvenanceTests(unittest.TestCase):
    def ns(self, **kwargs):
        base = dict(project_id="p1", user_scope="u1", policy_hash=H, model_contract_hash=M, tool_contract_hash=T, schema_version="1")
        base.update(kwargs)
        return CacheNamespace(**base)

    def test_exact_namespace_hit(self):
        cache = CacheProvenanceFirewall()
        ns = self.ns()
        cache.put(ns, {"q": 1}, {"answer": 2})
        decision, value = cache.get(ns, {"q": 1})
        self.assertTrue(decision.allowed)
        self.assertEqual(value, {"answer": 2})

    def test_cross_user_is_a_miss(self):
        cache = CacheProvenanceFirewall()
        cache.put(self.ns(), {"q": 1}, {"secret": "scoped"})
        decision, value = cache.get(self.ns(user_scope="u2"), {"q": 1})
        self.assertEqual(decision.code, "CACHE_MISS")
        self.assertIsNone(value)

    def test_explicit_foreign_entry_freezes(self):
        cache = CacheProvenanceFirewall()
        entry = cache.put(self.ns(), {"q": 1}, {"answer": 2})
        decision = cache.validate_entry(self.ns(project_id="p2"), {"q": 1}, entry)
        self.assertEqual(decision.status, GateStatus.FREEZE)
        self.assertEqual(decision.code, "CACHE_PROVENANCE_MISMATCH")

    def test_tampered_value_freezes(self):
        cache = CacheProvenanceFirewall()
        entry = cache.put(self.ns(), {"q": 1}, {"answer": 2})
        tampered = CacheEntry(entry.namespace, entry.input_digest, {"answer": 3}, entry.value_digest, entry.entry_digest)
        decision = cache.validate_entry(self.ns(), {"q": 1}, tampered)
        self.assertEqual(decision.code, "CACHE_VALUE_TAMPERED")


if __name__ == "__main__":
    unittest.main()
