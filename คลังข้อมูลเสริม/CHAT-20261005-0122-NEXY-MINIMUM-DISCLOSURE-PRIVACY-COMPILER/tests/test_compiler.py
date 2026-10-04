from __future__ import annotations

import json
import unittest

from nmdpc import (
    Classification,
    CompileDecision,
    DataRule,
    DisclosureAction,
    DisclosureCompiler,
    Recipient,
    RecipientTrust,
    TaskRequest,
    Transform,
)


class DisclosureCompilerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.compiler = DisclosureCompiler()

    def task(
        self,
        *,
        trust: RecipientTrust = RecipientTrust.EXTERNAL_MODEL,
        consents: frozenset[str] = frozenset(),
        retention: int = 3600,
        purpose: str = "summarize_support_case",
        caps: frozenset[str] = frozenset({"summarize"}),
    ) -> TaskRequest:
        return TaskRequest(
            purpose=purpose,
            capabilities=caps,
            recipient=Recipient("model-A", trust),
            requested_retention_seconds=retention,
            consents=consents,
        )

    def rule(
        self,
        name: str,
        classification: Classification,
        *,
        required: frozenset[str] = frozenset({"summarize"}),
        recipient_required: frozenset[str] = frozenset(),
        transform: Transform = Transform.NONE,
        allowed: frozenset[str] = frozenset({"summarize_support_case"}),
        max_retention: int = 600,
    ) -> DataRule:
        return DataRule(
            field_name=name,
            classification=classification,
            allowed_purposes=allowed,
            required_for_capabilities=required,
            recipient_value_required_for=recipient_required,
            preferred_transform=transform,
            max_retention_seconds=max_retention,
        )

    def test_public_required_external_is_raw_and_retention_is_clipped(self) -> None:
        plan = self.compiler.compile(self.task(retention=9999), [self.rule("title", Classification.PUBLIC)])
        self.assertEqual(plan.decision, CompileDecision.ALLOW)
        self.assertEqual(plan.field_decisions[0].action, DisclosureAction.INCLUDE_RAW)
        self.assertEqual(plan.field_decisions[0].retention_seconds, 600)
        self.assertEqual(self.compiler.build_bundle(plan, {"title": "Printer issue"}), {"title": "Printer issue"})

    def test_irrelevant_field_is_omitted_by_necessity(self) -> None:
        plan = self.compiler.compile(
            self.task(),
            [self.rule("account_history", Classification.PRIVATE, required=frozenset({"billing"}))],
        )
        self.assertEqual(plan.decision, CompileDecision.ALLOW)
        self.assertEqual(plan.field_decisions[0].action, DisclosureAction.OMIT_NOT_NEEDED)
        self.assertEqual(self.compiler.build_bundle(plan, {"account_history": "unused"}), {})

    def test_credential_is_brokered_and_never_enters_bundle(self) -> None:
        plan = self.compiler.compile(self.task(), [self.rule("provider_token", Classification.CREDENTIAL)])
        self.assertEqual(plan.decision, CompileDecision.ALLOW)
        self.assertEqual(plan.field_decisions[0].action, DisclosureAction.BROKER_OUT_OF_BAND)
        bundle = self.compiler.build_bundle(plan, {"provider_token": "demo-credential-placeholder"})
        self.assertEqual(bundle, {})
        self.assertNotIn("demo-credential-placeholder", plan.to_json())

    def test_credential_that_recipient_must_receive_freezes(self) -> None:
        rule = self.rule(
            "provider_token",
            Classification.CREDENTIAL,
            recipient_required=frozenset({"summarize"}),
        )
        plan = self.compiler.compile(self.task(), [rule])
        self.assertEqual(plan.decision, CompileDecision.FREEZE)
        self.assertIn("CREDENTIAL_VALUE_CANNOT_BE_DISCLOSED_TO_RECIPIENT", plan.freeze_reasons)
        with self.assertRaisesRegex(ValueError, "DISCLOSURE_PLAN_FROZEN"):
            self.compiler.build_bundle(plan, {"provider_token": "demo"})

    def test_private_external_without_consent_freezes(self) -> None:
        rule = self.rule("customer_name", Classification.PRIVATE, transform=Transform.MASK)
        plan = self.compiler.compile(self.task(), [rule])
        self.assertEqual(plan.decision, CompileDecision.FREEZE)
        self.assertIn("PRIVATE_EXTERNAL_CONSENT_MISSING", plan.freeze_reasons)

    def test_private_external_with_consent_masks(self) -> None:
        rule = self.rule("customer_name", Classification.PRIVATE, transform=Transform.MASK)
        plan = self.compiler.compile(
            self.task(consents=frozenset({"private_to_external_model"})),
            [rule],
        )
        self.assertEqual(plan.decision, CompileDecision.TRANSFORM)
        bundle = self.compiler.build_bundle(plan, {"customer_name": "Ada Example"})
        self.assertEqual(bundle["customer_name"], "<redacted:private:customer_name>")
        self.assertNotIn("Ada Example", json.dumps(plan.as_dict()))

    def test_private_external_tokenization_requires_runtime_key(self) -> None:
        rule = self.rule("customer_id", Classification.PRIVATE, transform=Transform.TOKENIZE)
        plan = self.compiler.compile(
            self.task(consents=frozenset({"private_to_external_model"})),
            [rule],
        )
        with self.assertRaisesRegex(ValueError, "TOKENIZATION_KEY_REQUIRED"):
            self.compiler.build_bundle(plan, {"customer_id": "C-001"})
        bundle = self.compiler.build_bundle(plan, {"customer_id": "C-001"}, tokenization_key=b"unit-test-key")
        self.assertRegex(bundle["customer_id"], r"^tok_[0-9a-f]{24}$")
        self.assertNotEqual(bundle["customer_id"], "C-001")

    def test_secret_external_model_always_freezes(self) -> None:
        plan = self.compiler.compile(
            self.task(consents=frozenset({"secret_to_trusted_processor"})),
            [self.rule("strategy", Classification.SECRET, transform=Transform.MASK)],
        )
        self.assertEqual(plan.decision, CompileDecision.FREEZE)
        self.assertIn("SECRET_EXTERNAL_MODEL_FORBIDDEN", plan.freeze_reasons)

    def test_secret_trusted_processor_requires_explicit_consent(self) -> None:
        rule = self.rule("strategy", Classification.SECRET, recipient_required=frozenset({"summarize"}))
        denied = self.compiler.compile(self.task(trust=RecipientTrust.TRUSTED_PROCESSOR), [rule])
        self.assertEqual(denied.decision, CompileDecision.FREEZE)

        allowed = self.compiler.compile(
            self.task(
                trust=RecipientTrust.TRUSTED_PROCESSOR,
                consents=frozenset({"secret_to_trusted_processor"}),
            ),
            [rule],
        )
        self.assertEqual(allowed.decision, CompileDecision.ALLOW)
        self.assertEqual(allowed.field_decisions[0].action, DisclosureAction.INCLUDE_RAW)

    def test_purpose_mismatch_freezes_even_for_public_data(self) -> None:
        plan = self.compiler.compile(
            self.task(purpose="marketing_profile"),
            [self.rule("title", Classification.PUBLIC)],
        )
        self.assertEqual(plan.decision, CompileDecision.FREEZE)
        self.assertIn("PURPOSE_NOT_ALLOWED:marketing_profile", plan.freeze_reasons)

    def test_unknown_recipient_freezes_globally(self) -> None:
        plan = self.compiler.compile(
            self.task(trust=RecipientTrust.UNKNOWN),
            [self.rule("title", Classification.PUBLIC)],
        )
        self.assertEqual(plan.decision, CompileDecision.FREEZE)
        self.assertIn("RECIPIENT_TRUST_UNKNOWN", plan.freeze_reasons)

    def test_duplicate_rule_freezes(self) -> None:
        rule = self.rule("title", Classification.PUBLIC)
        plan = self.compiler.compile(self.task(), [rule, rule])
        self.assertEqual(plan.decision, CompileDecision.FREEZE)
        self.assertIn("DUPLICATE_FIELD_RULE:title", plan.freeze_reasons)

    def test_deterministic_plan_is_order_independent(self) -> None:
        public = self.rule("title", Classification.PUBLIC)
        private = self.rule("customer_name", Classification.PRIVATE, transform=Transform.MASK)
        task = self.task(consents=frozenset({"private_to_external_model"}))
        a = self.compiler.compile(task, [public, private])
        b = self.compiler.compile(task, [private, public])
        self.assertEqual(a.policy_fingerprint, b.policy_fingerprint)
        self.assertEqual(a.to_json(), b.to_json())

    def test_negative_retention_freezes(self) -> None:
        plan = self.compiler.compile(self.task(retention=-1), [self.rule("title", Classification.PUBLIC)])
        self.assertEqual(plan.decision, CompileDecision.FREEZE)
        self.assertIn("RETENTION_NEGATIVE", plan.freeze_reasons)


if __name__ == "__main__":
    unittest.main()
