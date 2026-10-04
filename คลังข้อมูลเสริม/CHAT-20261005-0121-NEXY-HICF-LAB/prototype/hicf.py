from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Iterable, Mapping, Sequence


class Materiality(str, Enum):
    NON_MATERIAL = "NON_MATERIAL"
    MATERIAL = "MATERIAL"
    CRITICAL = "CRITICAL"


class Reversibility(str, Enum):
    REVERSIBLE = "REVERSIBLE"
    PARTIALLY_REVERSIBLE = "PARTIALLY_REVERSIBLE"
    IRREVERSIBLE = "IRREVERSIBLE"


class Impact(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AuthorityState(str, Enum):
    RESOLVED = "RESOLVED"
    UNRESOLVED = "UNRESOLVED"
    CONFLICT = "CONFLICT"


class GateDecision(str, Enum):
    PROCEED = "PROCEED"
    ASK = "ASK"
    FREEZE = "FREEZE"


class DriftClass(str, Enum):
    NONE = "NONE"
    LOW = "LOW"
    MATERIAL = "MATERIAL"
    AUTHORITY_BREAK = "AUTHORITY_BREAK"


class PreferenceScope(str, Enum):
    EPHEMERAL = "EPHEMERAL"
    PROJECT = "PROJECT"
    DURABLE = "DURABLE"


@dataclass(frozen=True, slots=True)
class Unknown:
    key: str
    materiality: Materiality
    description: str = ""

    def canonical(self) -> dict[str, str]:
        return {
            "key": self.key.strip(),
            "materiality": self.materiality.value,
            "description": self.description.strip(),
        }


@dataclass(frozen=True, slots=True)
class ActionCandidate:
    action_id: str
    capability: str
    impact: Impact
    reversibility: Reversibility
    mutates_state: bool

    def canonical(self) -> dict[str, object]:
        return {
            "action_id": self.action_id.strip(),
            "capability": self.capability.strip(),
            "impact": self.impact.value,
            "reversibility": self.reversibility.value,
            "mutates_state": self.mutates_state,
        }


@dataclass(frozen=True, slots=True)
class IntentEnvelope:
    objective: str
    constraints: tuple[str, ...] = ()
    immutables: tuple[str, ...] = ()
    prohibited: tuple[str, ...] = ()
    unknowns: tuple[Unknown, ...] = ()
    authority_state: AuthorityState = AuthorityState.RESOLVED
    authority_refs: tuple[str, ...] = ()

    @staticmethod
    def _canon_texts(values: Iterable[str]) -> tuple[str, ...]:
        normalized = {" ".join(v.split()) for v in values if v and v.strip()}
        return tuple(sorted(normalized, key=str.casefold))

    @classmethod
    def build(
        cls,
        *,
        objective: str,
        constraints: Iterable[str] = (),
        immutables: Iterable[str] = (),
        prohibited: Iterable[str] = (),
        unknowns: Iterable[Unknown] = (),
        authority_state: AuthorityState = AuthorityState.RESOLVED,
        authority_refs: Iterable[str] = (),
    ) -> "IntentEnvelope":
        obj = " ".join(objective.split())
        if not obj:
            raise ValueError("objective must be non-empty")
        unique_unknowns = {u.key.strip(): u for u in unknowns if u.key.strip()}
        return cls(
            objective=obj,
            constraints=cls._canon_texts(constraints),
            immutables=cls._canon_texts(immutables),
            prohibited=cls._canon_texts(prohibited),
            unknowns=tuple(sorted(unique_unknowns.values(), key=lambda u: u.key.casefold())),
            authority_state=authority_state,
            authority_refs=cls._canon_texts(authority_refs),
        )

    def canonical(self) -> dict[str, object]:
        return {
            "objective": self.objective,
            "constraints": list(self.constraints),
            "immutables": list(self.immutables),
            "prohibited": list(self.prohibited),
            "unknowns": [u.canonical() for u in self.unknowns],
            "authority_state": self.authority_state.value,
            "authority_refs": list(self.authority_refs),
        }

    def fingerprint(self) -> str:
        payload = json.dumps(self.canonical(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class GateResult:
    decision: GateDecision
    reason_codes: tuple[str, ...]
    required_questions: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class FrictionState:
    clarification_count: int = 0
    repeated_question_count: int = 0
    asked_keys: tuple[str, ...] = ()

    def ask(self, key: str) -> "FrictionState":
        normalized = " ".join(key.split())
        repeated = normalized in self.asked_keys
        return FrictionState(
            clarification_count=self.clarification_count + 1,
            repeated_question_count=self.repeated_question_count + int(repeated),
            asked_keys=self.asked_keys + (normalized,),
        )


@dataclass(frozen=True, slots=True)
class FrictionBudget:
    preferred_max_clarifications: int = 2
    preferred_max_repeats: int = 0

    def advisory_violation(self, state: FrictionState) -> tuple[str, ...]:
        reasons: list[str] = []
        if state.clarification_count > self.preferred_max_clarifications:
            reasons.append("CLARIFICATION_BUDGET_EXCEEDED")
        if state.repeated_question_count > self.preferred_max_repeats:
            reasons.append("REPEATED_QUESTION")
        return tuple(reasons)


@dataclass(frozen=True, slots=True)
class PreferenceRecord:
    key: str
    value: str
    scope: PreferenceScope
    explicit: bool
    provenance: str

    def validate(self) -> None:
        if not self.key.strip():
            raise ValueError("preference key must be non-empty")
        if not self.provenance.strip():
            raise ValueError("preference provenance must be non-empty")
        if self.scope is PreferenceScope.DURABLE and not self.explicit:
            raise ValueError("durable preferences require explicit user authority")


class ClarificationGate:
    """Deterministic decision gate. Safety/authority correctness outranks UX friction."""

    @staticmethod
    def _capability_prohibited(capability: str, prohibited: Sequence[str]) -> bool:
        cap = capability.casefold().strip()
        return any(token.casefold().strip() in cap for token in prohibited if token.strip())

    def evaluate(self, envelope: IntentEnvelope, action: ActionCandidate) -> GateResult:
        reasons: list[str] = []
        questions: list[str] = []

        if envelope.authority_state is AuthorityState.CONFLICT:
            return GateResult(GateDecision.FREEZE, ("AUTHORITY_CONFLICT",))

        if self._capability_prohibited(action.capability, envelope.prohibited):
            return GateResult(GateDecision.FREEZE, ("PROHIBITED_CAPABILITY",))

        critical_unknowns = [u for u in envelope.unknowns if u.materiality is Materiality.CRITICAL]
        if critical_unknowns:
            return GateResult(
                GateDecision.FREEZE,
                ("CRITICAL_UNKNOWN",),
                tuple(u.key for u in critical_unknowns),
            )

        if envelope.authority_state is AuthorityState.UNRESOLVED and (
            action.mutates_state
            or action.impact in {Impact.HIGH, Impact.CRITICAL}
            or action.reversibility is Reversibility.IRREVERSIBLE
        ):
            reasons.append("MATERIAL_AUTHORITY_UNRESOLVED")
            questions.append("resolve_authority")

        material_unknowns = [u for u in envelope.unknowns if u.materiality is Materiality.MATERIAL]
        if material_unknowns:
            reasons.append("MATERIAL_UNKNOWN")
            questions.extend(u.key for u in material_unknowns)

        if action.reversibility is Reversibility.IRREVERSIBLE and envelope.unknowns:
            reasons.append("IRREVERSIBLE_WITH_UNKNOWNS")
            questions.extend(u.key for u in envelope.unknowns)

        if action.impact is Impact.CRITICAL and envelope.unknowns:
            reasons.append("CRITICAL_IMPACT_WITH_UNKNOWNS")
            questions.extend(u.key for u in envelope.unknowns)

        if reasons:
            return GateResult(
                GateDecision.ASK,
                tuple(dict.fromkeys(reasons)),
                tuple(dict.fromkeys(questions)),
            )

        return GateResult(GateDecision.PROCEED, ("SUFFICIENTLY_RESOLVED",))


class IntentDriftDetector:
    def compare(self, baseline: IntentEnvelope, candidate: IntentEnvelope) -> DriftClass:
        if baseline.authority_state is not candidate.authority_state:
            if candidate.authority_state is AuthorityState.CONFLICT:
                return DriftClass.AUTHORITY_BREAK

        if set(baseline.immutables) != set(candidate.immutables):
            return DriftClass.AUTHORITY_BREAK

        if baseline.objective.casefold() != candidate.objective.casefold():
            return DriftClass.MATERIAL

        if set(baseline.prohibited) != set(candidate.prohibited):
            return DriftClass.MATERIAL

        if set(baseline.constraints) != set(candidate.constraints):
            return DriftClass.LOW

        baseline_unknowns = {(u.key, u.materiality.value) for u in baseline.unknowns}
        candidate_unknowns = {(u.key, u.materiality.value) for u in candidate.unknowns}
        if baseline_unknowns != candidate_unknowns:
            return DriftClass.LOW

        return DriftClass.NONE


def decision_record(
    envelope: IntentEnvelope,
    action: ActionCandidate,
    gate: GateResult,
    *,
    friction_advisories: Sequence[str] = (),
) -> Mapping[str, object]:
    return {
        "intent_fingerprint": envelope.fingerprint(),
        "action": action.canonical(),
        "decision": gate.decision.value,
        "reason_codes": list(gate.reason_codes),
        "required_questions": list(gate.required_questions),
        "friction_advisories": list(friction_advisories),
    }
