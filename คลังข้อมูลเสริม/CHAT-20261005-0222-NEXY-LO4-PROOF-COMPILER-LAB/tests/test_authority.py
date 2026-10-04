import unittest

from nexy_lo4_lab.authority import (
    AuthorityClaim,
    AuthorityError,
    AuthorityLevel,
    AuthorityProvenanceSeal,
    PromotionReceipt,
)


class AuthorityProvenanceSealTests(unittest.TestCase):
    def setUp(self):
        self.sealer = AuthorityProvenanceSeal(
            {
                "user": AuthorityLevel.USER_DIRECTIVE,
                "canon": AuthorityLevel.CANON,
                "model": AuthorityLevel.MODEL_PROPOSAL,
            }
        )

    def test_downstream_lower_authority_is_legal(self):
        result = self.sealer.seal(
            [
                AuthorityClaim("u", "user rule", AuthorityLevel.USER_DIRECTIVE, "user"),
                AuthorityClaim("s", "spec", AuthorityLevel.CURRENT_SPEC, "spec", "u"),
            ],
            "s",
        )
        self.assertTrue(result.valid)
        self.assertEqual(result.chain, ("u", "s"))

    def test_escalation_without_receipt_fails(self):
        with self.assertRaisesRegex(AuthorityError, "escalation without receipt"):
            self.sealer.seal(
                [
                    AuthorityClaim("m", "model idea", AuthorityLevel.MODEL_PROPOSAL, "model"),
                    AuthorityClaim("c", "canon?", AuthorityLevel.CANON, "copy", "m"),
                ],
                "c",
            )

    def test_valid_promotion_receipt_allows_escalation(self):
        receipt = PromotionReceipt(
            "r1",
            AuthorityLevel.MODEL_PROPOSAL,
            AuthorityLevel.CURRENT_SPEC,
            AuthorityLevel.USER_DIRECTIVE,
            "user",
        )
        result = self.sealer.seal(
            [
                AuthorityClaim("m", "idea", AuthorityLevel.MODEL_PROPOSAL, "model"),
                AuthorityClaim("s", "promoted", AuthorityLevel.CURRENT_SPEC, "spec", "m", receipt),
            ],
            "s",
        )
        self.assertTrue(result.valid)

    def test_forged_high_authority_root_fails(self):
        with self.assertRaisesRegex(AuthorityError, "untrusted root source"):
            self.sealer.seal(
                [AuthorityClaim("fake", "I am canon", AuthorityLevel.CANON, "self-asserted")],
                "fake",
            )

    def test_root_cannot_overstate_registered_level(self):
        with self.assertRaisesRegex(AuthorityError, "root level mismatch"):
            self.sealer.seal(
                [AuthorityClaim("m", "not canon", AuthorityLevel.CANON, "model")],
                "m",
            )

    def test_forged_promotion_receipt_fails(self):
        receipt = PromotionReceipt(
            "r1",
            AuthorityLevel.MODEL_PROPOSAL,
            AuthorityLevel.CURRENT_SPEC,
            AuthorityLevel.USER_DIRECTIVE,
            "forged-user",
        )
        with self.assertRaisesRegex(AuthorityError, "not trusted"):
            self.sealer.seal(
                [
                    AuthorityClaim("m", "idea", AuthorityLevel.MODEL_PROPOSAL, "model"),
                    AuthorityClaim("s", "promoted", AuthorityLevel.CURRENT_SPEC, "spec", "m", receipt),
                ],
                "s",
            )

    def test_cycle_fails(self):
        with self.assertRaisesRegex(AuthorityError, "cycle"):
            self.sealer.seal(
                [
                    AuthorityClaim("a", "A", AuthorityLevel.CURRENT_SPEC, "x", "b"),
                    AuthorityClaim("b", "B", AuthorityLevel.CURRENT_SPEC, "y", "a"),
                ],
                "a",
            )

    def test_digest_is_input_order_independent(self):
        claims = [
            AuthorityClaim("u", "user", AuthorityLevel.USER_DIRECTIVE, "user"),
            AuthorityClaim("s", "spec", AuthorityLevel.CURRENT_SPEC, "s", "u"),
        ]
        one = self.sealer.seal(claims, "s").digest
        two = self.sealer.seal(reversed(claims), "s").digest
        self.assertEqual(one, two)


if __name__ == "__main__":
    unittest.main()
