import copy
import unittest
from reference import build_capsule, verify_capsule

SECRET = b"unit-test-only-secret"
NOW = 1791140100


class TestCDHC(unittest.TestCase):
    def state(self):
        return {
            "objective": "resume task",
            "verified_state": {"status": "PARTIAL", "api_token": "must-disappear"},
            "next_action": "run unit tests",
            "evidence_refs": ["e1"],
            "chat_dump": "not allowed",
        }

    def test_build_minimizes_and_redacts(self):
        c = build_capsule(self.state(), SECRET, "device-B", NOW)
        self.assertNotIn("chat_dump", c["payload"])
        self.assertNotIn("api_token", c["payload"]["verified_state"])

    def test_valid_capsule_allows(self):
        c = build_capsule(self.state(), SECRET, "device-B", NOW)
        status, _, payload = verify_capsule(c, SECRET, "device-B", NOW + 10)
        self.assertEqual(status, "ALLOW")
        self.assertEqual(payload["objective"], "resume task")

    def test_tamper_is_detected(self):
        c = build_capsule(self.state(), SECRET, "device-B", NOW)
        bad = copy.deepcopy(c)
        bad["payload"]["objective"] = "changed"
        self.assertEqual(verify_capsule(bad, SECRET, "device-B", NOW + 1)[1], "SIGNATURE_MISMATCH")

    def test_expiry_is_detected(self):
        c = build_capsule(self.state(), SECRET, "device-B", NOW, ttl_seconds=10)
        self.assertEqual(verify_capsule(c, SECRET, "device-B", NOW + 10)[1], "EXPIRED")

    def test_target_mismatch_freezes(self):
        c = build_capsule(self.state(), SECRET, "device-B", NOW)
        self.assertEqual(verify_capsule(c, SECRET, "device-C", NOW + 1)[1], "TARGET_MISMATCH")


if __name__ == "__main__":
    unittest.main()
