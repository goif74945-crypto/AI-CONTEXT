from __future__ import annotations

import random
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


class CompilerInvariantTests(unittest.TestCase):
    def setUp(self) -> None:
        self.compiler = DisclosureCompiler()
        self.rng = random.Random(74945)

    def _task(self, trust: RecipientTrust, *, consents: frozenset[str] = frozenset()) -> TaskRequest:
        return TaskRequest(
            purpose="analysis",
            capabilities=frozenset({"cap"}),
            recipient=Recipient("recipient-1", trust),
            requested_retention_seconds=1000,
            consents=consents,
        )

    def _rule(
        self,
        name: str,
        classification: Classification,
        transform: Transform,
        *,
        required: bool = True,
        recipient_value_required: bool = False,
        max_retention: int = 500,
    ) -> DataRule:
        caps = frozenset({"cap"}) if required else frozenset({"other"})
        recipient_caps = frozenset({"cap"}) if recipient_value_required else frozenset()
        return DataRule(
            field_name=name,
            classification=classification,
            allowed_purposes=frozenset({"analysis"}),
            required_for_capabilities=caps,
            recipient_value_required_for=recipient_caps,
            preferred_transform=transform,
            max_retention_seconds=max_retention,
        )

    def test_external_secret_always_freezes_across_transforms_and_consents(self) -> None:
        consent_sets = [
            frozenset(),
            frozenset({"secret_to_trusted_processor"}),
            frozenset({"private_to_external_model", "secret_to_trusted_processor"}),
        ]
        for transform in Transform:
            for consents in consent_sets:
                with self.subTest(transform=transform, consents=consents):
                    plan = self.compiler.compile(
                        self._task(RecipientTrust.EXTERNAL_MODEL, consents=consents),
                        [self._rule("secret_field", Classification.SECRET, transform)],
                    )
                    self.assertEqual(plan.decision, CompileDecision.FREEZE)
                    self.assertIn("SECRET_EXTERNAL_MODEL_FORBIDDEN", plan.freeze_reasons)

    def test_credential_never_appears_in_disclosure_bundle(self) -> None:
        for trust in (RecipientTrust.LOCAL_CORE, RecipientTrust.TRUSTED_PROCESSOR, RecipientTrust.EXTERNAL_MODEL):
            with self.subTest(trust=trust):
                plan = self.compiler.compile(
                    self._task(trust),
                    [self._rule("credential", Classification.CREDENTIAL, Transform.NONE)],
                )
                self.assertEqual(plan.field_decisions[0].action, DisclosureAction.BROKER_OUT_OF_BAND)
                bundle = self.compiler.build_bundle(plan, {"credential": "never-emit-this"})
                self.assertNotIn("credential", bundle)
                self.assertNotIn("never-emit-this", plan.to_json())

    def test_irrelevant_sensitive_fields_do_not_force_disclosure_or_consent(self) -> None:
        for classification in (Classification.PRIVATE, Classification.SECRET, Classification.CREDENTIAL):
            with self.subTest(classification=classification):
                plan = self.compiler.compile(
                    self._task(RecipientTrust.EXTERNAL_MODEL),
                    [self._rule("x", classification, Transform.NONE, required=False)],
                )
                self.assertEqual(plan.decision, CompileDecision.ALLOW)
                self.assertEqual(plan.field_decisions[0].action, DisclosureAction.OMIT_NOT_NEEDED)

    def test_retention_is_never_greater_than_request_or_field_maximum(self) -> None:
        for _ in range(250):
            requested = self.rng.randint(0, 50_000)
            maximum = self.rng.randint(0, 50_000)
            task = TaskRequest(
                purpose="analysis",
                capabilities=frozenset({"cap"}),
                recipient=Recipient("local", RecipientTrust.LOCAL_CORE),
                requested_retention_seconds=requested,
            )
            plan = self.compiler.compile(
                task,
                [self._rule("public", Classification.PUBLIC, Transform.NONE, max_retention=maximum)],
            )
            ttl = plan.field_decisions[0].retention_seconds
            self.assertLessEqual(ttl, requested)
            self.assertLessEqual(ttl, maximum)
            self.assertGreaterEqual(ttl, 0)

    def test_policy_fingerprint_is_permutation_invariant(self) -> None:
        rules = [
            self._rule("a", Classification.PUBLIC, Transform.NONE),
            self._rule("b", Classification.INTERNAL, Transform.MASK),
            self._rule("c", Classification.PRIVATE, Transform.TOKENIZE),
            self._rule("d", Classification.CREDENTIAL, Transform.NONE),
        ]
        task = self._task(
            RecipientTrust.EXTERNAL_MODEL,
            consents=frozenset({"private_to_external_model"}),
        )
        baseline = self.compiler.compile(task, rules)
        for _ in range(100):
            shuffled = list(rules)
            self.rng.shuffle(shuffled)
            candidate = self.compiler.compile(task, shuffled)
            self.assertEqual(candidate.policy_fingerprint, baseline.policy_fingerprint)
            self.assertEqual(candidate.to_json(), baseline.to_json())

    def test_frozen_plan_cannot_build_bundle(self) -> None:
        cases = [
            self.compiler.compile(
                self._task(RecipientTrust.EXTERNAL_MODEL),
                [self._rule("private", Classification.PRIVATE, Transform.MASK)],
            ),
            self.compiler.compile(
                self._task(RecipientTrust.UNKNOWN),
                [self._rule("public", Classification.PUBLIC, Transform.NONE)],
            ),
            self.compiler.compile(
                TaskRequest(
                    purpose="",
                    capabilities=frozenset({"cap"}),
                    recipient=Recipient("x", RecipientTrust.LOCAL_CORE),
                    requested_retention_seconds=0,
                ),
                [self._rule("public", Classification.PUBLIC, Transform.NONE)],
            ),
        ]
        for plan in cases:
            with self.subTest(reason=plan.freeze_reasons):
                self.assertEqual(plan.decision, CompileDecision.FREEZE)
                with self.assertRaisesRegex(ValueError, "DISCLOSURE_PLAN_FROZEN"):
                    self.compiler.build_bundle(plan, {"public": "x", "private": "y"})

    def test_transformed_private_value_is_not_echoed(self) -> None:
        raw = "person-12345@example.invalid"
        task = self._task(
            RecipientTrust.EXTERNAL_MODEL,
            consents=frozenset({"private_to_external_model"}),
        )
        for transform in (Transform.MASK, Transform.TOKENIZE):
            with self.subTest(transform=transform):
                plan = self.compiler.compile(task, [self._rule("identity", Classification.PRIVATE, transform)])
                kwargs = {"tokenization_key": b"test-key"} if transform is Transform.TOKENIZE else {}
                bundle = self.compiler.build_bundle(plan, {"identity": raw}, **kwargs)
                self.assertNotEqual(bundle["identity"], raw)
                self.assertNotIn(raw, plan.to_json())


if __name__ == "__main__":
    unittest.main()
