from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Mapping, Sequence


class Classification(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    PRIVATE = "PRIVATE"
    SECRET = "SECRET"
    CREDENTIAL = "CREDENTIAL"


class RecipientTrust(str, Enum):
    LOCAL_CORE = "LOCAL_CORE"
    TRUSTED_PROCESSOR = "TRUSTED_PROCESSOR"
    EXTERNAL_MODEL = "EXTERNAL_MODEL"
    UNKNOWN = "UNKNOWN"


class Transform(str, Enum):
    NONE = "NONE"
    MASK = "MASK"
    TOKENIZE = "TOKENIZE"


class DisclosureAction(str, Enum):
    INCLUDE_RAW = "INCLUDE_RAW"
    INCLUDE_TRANSFORMED = "INCLUDE_TRANSFORMED"
    OMIT_NOT_NEEDED = "OMIT_NOT_NEEDED"
    BROKER_OUT_OF_BAND = "BROKER_OUT_OF_BAND"
    FREEZE = "FREEZE"


class CompileDecision(str, Enum):
    ALLOW = "ALLOW"
    TRANSFORM = "TRANSFORM"
    FREEZE = "FREEZE"


@dataclass(frozen=True)
class Recipient:
    recipient_id: str
    trust: RecipientTrust

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.recipient_id.strip():
            errors.append("RECIPIENT_ID_MISSING")
        if self.trust is RecipientTrust.UNKNOWN:
            errors.append("RECIPIENT_TRUST_UNKNOWN")
        return errors


@dataclass(frozen=True)
class TaskRequest:
    purpose: str
    capabilities: frozenset[str]
    recipient: Recipient
    requested_retention_seconds: int
    consents: frozenset[str] = field(default_factory=frozenset)

    def validate(self) -> list[str]:
        errors = self.recipient.validate()
        if not self.purpose.strip():
            errors.append("PURPOSE_MISSING")
        if not self.capabilities:
            errors.append("CAPABILITIES_MISSING")
        if self.requested_retention_seconds < 0:
            errors.append("RETENTION_NEGATIVE")
        return errors


@dataclass(frozen=True)
class DataRule:
    field_name: str
    classification: Classification
    allowed_purposes: frozenset[str]
    required_for_capabilities: frozenset[str]
    recipient_value_required_for: frozenset[str] = field(default_factory=frozenset)
    preferred_transform: Transform = Transform.NONE
    max_retention_seconds: int = 0

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.field_name.strip():
            errors.append("FIELD_NAME_MISSING")
        if not self.allowed_purposes:
            errors.append(f"ALLOWED_PURPOSES_MISSING:{self.field_name}")
        if self.max_retention_seconds < 0:
            errors.append(f"RETENTION_NEGATIVE:{self.field_name}")
        invalid = self.recipient_value_required_for - self.required_for_capabilities
        if invalid:
            errors.append(
                "RECIPIENT_VALUE_CAPABILITY_NOT_REQUIRED:"
                f"{self.field_name}:{','.join(sorted(invalid))}"
            )
        return errors


@dataclass(frozen=True)
class FieldDecision:
    field_name: str
    classification: Classification
    action: DisclosureAction
    transform: Transform
    retention_seconds: int
    reasons: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "field_name": self.field_name,
            "classification": self.classification.value,
            "action": self.action.value,
            "transform": self.transform.value,
            "retention_seconds": self.retention_seconds,
            "reasons": list(self.reasons),
        }


@dataclass(frozen=True)
class DisclosurePlan:
    decision: CompileDecision
    purpose: str
    recipient_id: str
    recipient_trust: RecipientTrust
    capabilities: tuple[str, ...]
    field_decisions: tuple[FieldDecision, ...]
    freeze_reasons: tuple[str, ...]
    policy_fingerprint: str

    def as_dict(self) -> dict[str, object]:
        return {
            "decision": self.decision.value,
            "purpose": self.purpose,
            "recipient_id": self.recipient_id,
            "recipient_trust": self.recipient_trust.value,
            "capabilities": list(self.capabilities),
            "field_decisions": [d.as_dict() for d in self.field_decisions],
            "freeze_reasons": list(self.freeze_reasons),
            "policy_fingerprint": self.policy_fingerprint,
        }

    def to_json(self) -> str:
        return json.dumps(self.as_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


class DisclosureCompiler:
    """Deterministic disclosure-plan compiler.

    This reference engine compiles policy metadata into a disclosure plan. It is
    intentionally fail-closed for material ambiguity. Payload values are only
    accepted later by ``build_bundle`` so policy fingerprints and audit records do
    not contain raw values.
    """

    _CONSENT_PRIVATE_PROCESSOR = "private_to_trusted_processor"
    _CONSENT_PRIVATE_EXTERNAL = "private_to_external_model"
    _CONSENT_PRIVATE_EXTERNAL_RAW = "private_raw_to_external_model"
    _CONSENT_SECRET_PROCESSOR = "secret_to_trusted_processor"

    def compile(self, task: TaskRequest, rules: Sequence[DataRule]) -> DisclosurePlan:
        global_errors = list(task.validate())
        seen_names: set[str] = set()
        for rule in rules:
            global_errors.extend(rule.validate())
            if rule.field_name in seen_names:
                global_errors.append(f"DUPLICATE_FIELD_RULE:{rule.field_name}")
            seen_names.add(rule.field_name)

        if global_errors:
            field_decisions = tuple(
                FieldDecision(
                    field_name=rule.field_name,
                    classification=rule.classification,
                    action=DisclosureAction.FREEZE,
                    transform=Transform.NONE,
                    retention_seconds=0,
                    reasons=("GLOBAL_PRECONDITION_FAILED",),
                )
                for rule in sorted(rules, key=lambda r: r.field_name)
            )
            return self._finalize(task, field_decisions, tuple(sorted(set(global_errors))))

        decisions: list[FieldDecision] = []
        freeze_reasons: list[str] = []
        for rule in sorted(rules, key=lambda r: r.field_name):
            decision = self._decide_field(task, rule)
            decisions.append(decision)
            if decision.action is DisclosureAction.FREEZE:
                freeze_reasons.extend(decision.reasons)

        return self._finalize(task, tuple(decisions), tuple(sorted(set(freeze_reasons))))

    def build_bundle(
        self,
        plan: DisclosurePlan,
        payload: Mapping[str, object],
        *,
        tokenization_key: bytes | None = None,
    ) -> dict[str, object]:
        if plan.decision is CompileDecision.FREEZE:
            raise ValueError("DISCLOSURE_PLAN_FROZEN")

        bundle: dict[str, object] = {}
        for item in plan.field_decisions:
            if item.action in {DisclosureAction.OMIT_NOT_NEEDED, DisclosureAction.BROKER_OUT_OF_BAND}:
                continue
            if item.action is DisclosureAction.FREEZE:
                raise ValueError("FIELD_FROZEN")
            if item.field_name not in payload:
                raise KeyError(f"MISSING_PAYLOAD_FIELD:{item.field_name}")

            value = payload[item.field_name]
            if item.action is DisclosureAction.INCLUDE_RAW:
                bundle[item.field_name] = value
            elif item.action is DisclosureAction.INCLUDE_TRANSFORMED:
                bundle[item.field_name] = self._transform(
                    item.field_name,
                    item.classification,
                    item.transform,
                    value,
                    tokenization_key=tokenization_key,
                )
            else:  # defensive exhaustiveness
                raise AssertionError(f"UNHANDLED_ACTION:{item.action}")
        return bundle

    def _decide_field(self, task: TaskRequest, rule: DataRule) -> FieldDecision:
        relevant_caps = rule.required_for_capabilities & task.capabilities
        if not relevant_caps:
            return self._decision(
                task,
                rule,
                DisclosureAction.OMIT_NOT_NEEDED,
                Transform.NONE,
                ("NOT_REQUIRED_FOR_REQUESTED_CAPABILITIES",),
            )

        if task.purpose not in rule.allowed_purposes:
            return self._decision(
                task,
                rule,
                DisclosureAction.FREEZE,
                Transform.NONE,
                (f"PURPOSE_NOT_ALLOWED:{task.purpose}",),
            )

        recipient_needs_value = bool(rule.recipient_value_required_for & task.capabilities)
        c = rule.classification
        trust = task.recipient.trust

        if c is Classification.CREDENTIAL:
            if recipient_needs_value:
                return self._decision(
                    task,
                    rule,
                    DisclosureAction.FREEZE,
                    Transform.NONE,
                    ("CREDENTIAL_VALUE_CANNOT_BE_DISCLOSED_TO_RECIPIENT",),
                )
            return self._decision(
                task,
                rule,
                DisclosureAction.BROKER_OUT_OF_BAND,
                Transform.NONE,
                ("CREDENTIAL_MUST_USE_LOCAL_BROKER",),
            )

        if c is Classification.PUBLIC:
            return self._decision(
                task,
                rule,
                DisclosureAction.INCLUDE_RAW,
                Transform.NONE,
                ("PUBLIC_AND_NECESSARY",),
            )

        if c is Classification.INTERNAL:
            if trust is RecipientTrust.LOCAL_CORE:
                return self._decision(task, rule, DisclosureAction.INCLUDE_RAW, Transform.NONE, ("LOCAL_CORE",))
            return self._transformed_or_freeze(task, rule, "INTERNAL_EXTERNAL_REQUIRES_TRANSFORM")

        if c is Classification.PRIVATE:
            if trust is RecipientTrust.LOCAL_CORE:
                return self._decision(task, rule, DisclosureAction.INCLUDE_RAW, Transform.NONE, ("LOCAL_CORE",))
            if trust is RecipientTrust.TRUSTED_PROCESSOR:
                if self._CONSENT_PRIVATE_PROCESSOR not in task.consents:
                    return self._decision(
                        task,
                        rule,
                        DisclosureAction.FREEZE,
                        Transform.NONE,
                        ("PRIVATE_TRUSTED_PROCESSOR_CONSENT_MISSING",),
                    )
                return self._transformed_or_freeze(task, rule, "PRIVATE_TRUSTED_PROCESSOR_TRANSFORM")
            if trust is RecipientTrust.EXTERNAL_MODEL:
                if self._CONSENT_PRIVATE_EXTERNAL not in task.consents:
                    return self._decision(
                        task,
                        rule,
                        DisclosureAction.FREEZE,
                        Transform.NONE,
                        ("PRIVATE_EXTERNAL_CONSENT_MISSING",),
                    )
                if recipient_needs_value and rule.preferred_transform is Transform.NONE:
                    if self._CONSENT_PRIVATE_EXTERNAL_RAW in task.consents:
                        return self._decision(
                            task,
                            rule,
                            DisclosureAction.INCLUDE_RAW,
                            Transform.NONE,
                            ("PRIVATE_EXTERNAL_RAW_EXPLICITLY_AUTHORIZED",),
                        )
                    return self._decision(
                        task,
                        rule,
                        DisclosureAction.FREEZE,
                        Transform.NONE,
                        ("PRIVATE_EXTERNAL_RAW_NOT_AUTHORIZED",),
                    )
                return self._transformed_or_freeze(task, rule, "PRIVATE_EXTERNAL_TRANSFORM")

        if c is Classification.SECRET:
            if trust is RecipientTrust.LOCAL_CORE:
                return self._decision(task, rule, DisclosureAction.INCLUDE_RAW, Transform.NONE, ("LOCAL_CORE_ONLY",))
            if trust is RecipientTrust.TRUSTED_PROCESSOR:
                if self._CONSENT_SECRET_PROCESSOR not in task.consents:
                    return self._decision(
                        task,
                        rule,
                        DisclosureAction.FREEZE,
                        Transform.NONE,
                        ("SECRET_TRUSTED_PROCESSOR_CONSENT_MISSING",),
                    )
                if rule.preferred_transform is Transform.NONE and recipient_needs_value:
                    return self._decision(
                        task,
                        rule,
                        DisclosureAction.INCLUDE_RAW,
                        Transform.NONE,
                        ("SECRET_TRUSTED_PROCESSOR_EXPLICITLY_AUTHORIZED",),
                    )
                return self._transformed_or_freeze(task, rule, "SECRET_TRUSTED_PROCESSOR_TRANSFORM")
            return self._decision(
                task,
                rule,
                DisclosureAction.FREEZE,
                Transform.NONE,
                ("SECRET_EXTERNAL_MODEL_FORBIDDEN",),
            )

        return self._decision(task, rule, DisclosureAction.FREEZE, Transform.NONE, ("UNHANDLED_CLASSIFICATION",))

    def _transformed_or_freeze(self, task: TaskRequest, rule: DataRule, reason: str) -> FieldDecision:
        if rule.preferred_transform is Transform.NONE:
            return self._decision(
                task,
                rule,
                DisclosureAction.FREEZE,
                Transform.NONE,
                (f"{reason}:NO_TRANSFORM_AVAILABLE",),
            )
        return self._decision(
            task,
            rule,
            DisclosureAction.INCLUDE_TRANSFORMED,
            rule.preferred_transform,
            (reason,),
        )

    def _decision(
        self,
        task: TaskRequest,
        rule: DataRule,
        action: DisclosureAction,
        transform: Transform,
        reasons: Iterable[str],
    ) -> FieldDecision:
        retention = 0
        if action in {DisclosureAction.INCLUDE_RAW, DisclosureAction.INCLUDE_TRANSFORMED}:
            retention = min(task.requested_retention_seconds, rule.max_retention_seconds)
        return FieldDecision(
            field_name=rule.field_name,
            classification=rule.classification,
            action=action,
            transform=transform,
            retention_seconds=retention,
            reasons=tuple(sorted(set(reasons))),
        )

    def _finalize(
        self,
        task: TaskRequest,
        field_decisions: tuple[FieldDecision, ...],
        freeze_reasons: tuple[str, ...],
    ) -> DisclosurePlan:
        if freeze_reasons:
            overall = CompileDecision.FREEZE
        elif any(d.action is DisclosureAction.INCLUDE_TRANSFORMED for d in field_decisions):
            overall = CompileDecision.TRANSFORM
        else:
            overall = CompileDecision.ALLOW

        canonical = {
            "decision": overall.value,
            "purpose": task.purpose,
            "recipient_id": task.recipient.recipient_id,
            "recipient_trust": task.recipient.trust.value,
            "capabilities": sorted(task.capabilities),
            "consents": sorted(task.consents),
            "fields": [d.as_dict() for d in field_decisions],
            "freeze_reasons": list(freeze_reasons),
        }
        encoded = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        fingerprint = hashlib.sha256(encoded).hexdigest()
        return DisclosurePlan(
            decision=overall,
            purpose=task.purpose,
            recipient_id=task.recipient.recipient_id,
            recipient_trust=task.recipient.trust,
            capabilities=tuple(sorted(task.capabilities)),
            field_decisions=field_decisions,
            freeze_reasons=freeze_reasons,
            policy_fingerprint=fingerprint,
        )

    @staticmethod
    def _transform(
        field_name: str,
        classification: Classification,
        transform: Transform,
        value: object,
        *,
        tokenization_key: bytes | None,
    ) -> object:
        if transform is Transform.MASK:
            return f"<redacted:{classification.value.lower()}:{field_name}>"
        if transform is Transform.TOKENIZE:
            if not tokenization_key:
                raise ValueError("TOKENIZATION_KEY_REQUIRED")
            raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
            digest = hmac.new(tokenization_key, raw, hashlib.sha256).hexdigest()[:24]
            return f"tok_{digest}"
        if transform is Transform.NONE:
            return value
        raise AssertionError(f"UNHANDLED_TRANSFORM:{transform}")
