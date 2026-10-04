import unittest

from nexy_aux.portability import assess_portability


class PortabilityTests(unittest.TestCase):
    def base(self):
        evidence = {
            "claim_id": "C1",
            "evidence_class": "E2",
            "source_context": {"code_sha": "aaa", "policy": "p1", "runtime": "py3.11"},
            "expires_at": "2026-10-06T00:00:00+00:00",
        }
        target = {
            "claim_id": "C1",
            "required_evidence_classes": ["E2"],
            "target_context": {"code_sha": "aaa", "policy": "p1", "runtime": "py3.11"},
            "evaluation_time": "2026-10-05T00:00:00+00:00",
        }
        policy = {"code_sha": "MUST_EQUAL", "policy": "MUST_EQUAL", "runtime": "REVERIFY_IF_DIFFERENT"}
        return evidence, target, policy

    def test_portable_when_required_dimensions_match(self):
        e, t, p = self.base()
        result = assess_portability(e, t, p)
        self.assertEqual(result["status"], "PORTABLE")

    def test_runtime_difference_requires_reverification(self):
        e, t, p = self.base()
        t["target_context"]["runtime"] = "py3.12"
        result = assess_portability(e, t, p)
        self.assertEqual(result["status"], "REVERIFY")
        self.assertEqual(result["reverify_dimensions"][0]["dimension"], "runtime")

    def test_code_difference_invalidates(self):
        e, t, p = self.base()
        t["target_context"]["code_sha"] = "bbb"
        result = assess_portability(e, t, p)
        self.assertEqual(result["status"], "INVALID")
        self.assertEqual(result["reason"], "NON_PORTABLE_CONTEXT")

    def test_missing_dimension_freezes(self):
        e, t, p = self.base()
        del t["target_context"]["policy"]
        result = assess_portability(e, t, p)
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["dimension"], "policy")

    def test_expired_evidence_requires_reverification(self):
        e, t, p = self.base()
        t["evaluation_time"] = "2026-10-07T00:00:00+00:00"
        result = assess_portability(e, t, p)
        self.assertEqual(result["status"], "REVERIFY")
        self.assertTrue(any(x["dimension"] == "freshness" for x in result["reverify_dimensions"]))

    def test_evidence_class_is_not_substituted(self):
        e, t, p = self.base()
        e["evidence_class"] = "E1"
        result = assess_portability(e, t, p)
        self.assertEqual(result["status"], "INVALID")
        self.assertEqual(result["reason"], "EVIDENCE_CLASS_NOT_ACCEPTED")

    def test_claim_mismatch_invalidates(self):
        e, t, p = self.base()
        t["claim_id"] = "C2"
        result = assess_portability(e, t, p)
        self.assertEqual(result["reason"], "CLAIM_ID_MISMATCH")


if __name__ == "__main__":
    unittest.main()
