import unittest
from datetime import datetime, timedelta, timezone
from reference import ConsentGrant, ActionRequest, evaluate

UTC = timezone.utc
NOW = datetime(2026, 10, 5, 1, 55, tzinfo=UTC)


class TestCPAC(unittest.TestCase):
    def grant(self, **kw):
        base = dict(
            grant_id="g1", subject_id="u1", purposes=("send_report",),
            actions=("send",), resources=("report:7",),
            issued_at=NOW - timedelta(minutes=1), expires_at=NOW + timedelta(minutes=5), revoked=False,
        )
        base.update(kw)
        return ConsentGrant(**base)

    def req(self, **kw):
        base = dict(request_id="r1", subject_id="u1", purpose="send_report", action="send", resource="report:7", at=NOW)
        base.update(kw)
        return ActionRequest(**base)

    def test_exact_active_consent_allows(self):
        self.assertEqual(evaluate([self.grant()], self.req()).status, "ALLOW")

    def test_expired_requires_ask(self):
        g = self.grant(expires_at=NOW - timedelta(seconds=1), issued_at=NOW - timedelta(minutes=2))
        self.assertEqual(evaluate([g], self.req()).status, "ASK")

    def test_purpose_mismatch_requires_ask(self):
        self.assertEqual(evaluate([self.grant()], self.req(purpose="train_model")).status, "ASK")

    def test_wildcard_grant_is_blocked(self):
        self.assertEqual(evaluate([self.grant(resources=("*",))], self.req()).status, "BLOCK")

    def test_receipt_is_deterministic(self):
        a = evaluate([self.grant()], self.req())
        b = evaluate([self.grant()], self.req())
        self.assertEqual(a.receipt_digest, b.receipt_digest)


if __name__ == "__main__":
    unittest.main()
