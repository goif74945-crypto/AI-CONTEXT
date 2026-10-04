import unittest

from sncg import SemanticNamespaceCollisionGuard, SymbolContract


class SemanticNamespaceCollisionGuardTests(unittest.TestCase):
    def test_allows_same_identity_with_same_signature(self):
        a = SymbolContract("api", "TTL", "session-ttl", "duration", "auth", "seconds", "DOC-C", "runtime", ("session ttl",))
        b = SymbolContract("ui", "Session TTL", "session-ttl", "duration", "auth", "seconds", "DOC-C", "runtime", ("TTL",))
        self.assertEqual(SemanticNamespaceCollisionGuard.analyze([a, b]), ())

    def test_detects_same_label_different_semantics(self):
        a = SymbolContract("auth", "TTL", "otac-ttl", "duration", "auth", "seconds", "DOC-C", "runtime")
        b = SymbolContract("cache", "TTL", "cache-ttl", "duration", "cache", "seconds", "runtime-config", "runtime")
        result = SemanticNamespaceCollisionGuard.analyze([a, b])
        self.assertTrue(any(c.collision_type == "NAMESPACE_COLLISION" and c.label == "ttl" for c in result))

    def test_detects_semantic_id_drift_even_without_label_collision(self):
        a = SymbolContract("api", "SessionLifetime", "session-ttl", "duration", "auth", "seconds", "DOC-C", "runtime")
        b = SymbolContract("db", "SessionExpiry", "session-ttl", "timestamp", "auth", "epoch-ms", "DOC-C", "persisted")
        result = SemanticNamespaceCollisionGuard.analyze([a, b])
        self.assertTrue(any(c.collision_type == "IDENTITY_DRIFT" for c in result))

    def test_unicode_nfkc_normalization_catches_lookalike_width_variants(self):
        a = SymbolContract("a", "ＴＴＬ", "one", "duration", "x", "s", "A", "runtime")
        b = SymbolContract("b", "TTL", "two", "counter", "x", None, "B", "runtime")
        result = SemanticNamespaceCollisionGuard.analyze([a, b])
        self.assertTrue(any(c.label == "ttl" for c in result))


if __name__ == "__main__":
    unittest.main()
