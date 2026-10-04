from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

SCHEMA_VERSION = "nexy.directive-integrity.v1"


class IntegrityStatus(str, Enum):
    PASS = "PASS"
    FREEZE = "FREEZE"


class AmbiguityState(str, Enum):
    RESOLVED = "RESOLVED"
    OPEN = "OPEN"


class MutationClass(str, Enum):
    READ_ONLY = "READ_ONLY"
    REVERSIBLE_MUTATION = "REVERSIBLE_MUTATION"
    IRREVERSIBLE_MUTATION = "IRREVERSIBLE_MUTATION"


class ImpactClass(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


_IMPACT_RANK: dict[ImpactClass, int] = {
    ImpactClass.LOW: 0,
    ImpactClass.MEDIUM: 1,
    ImpactClass.HIGH: 2,
    ImpactClass.CRITICAL: 3,
}

_MUTATION_RANK: dict[MutationClass, int] = {
    MutationClass.READ_ONLY: 0,
    MutationClass.REVERSIBLE_MUTATION: 1,
    MutationClass.IRREVERSIBLE_MUTATION: 2,
}


def _canonical_set(values: Iterable[str]) -> tuple[str, ...]:
    normalized: set[str] = set()
    for value in values:
        if not isinstance(value, str):
            raise TypeError("set-like fields require strings")
        item = value.strip()
        if not item:
            raise ValueError("set-like fields may not contain blank values")
        normalized.add(item)
    return tuple(sorted(normalized))


def _required_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    text = value.strip()
    if not text:
        raise ValueError(f"{field_name} must not be blank")
    return text


def _canonical_json(value: Mapping[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class DirectiveSnapshot:
    stage: str
    action: str
    target: str
    constraints: tuple[str, ...] = field(default_factory=tuple)
    scope_in: tuple[str, ...] = field(default_factory=tuple)
    scope_out: tuple[str, ...] = field(default_factory=tuple)
    side_effects: tuple[str, ...] = field(default_factory=tuple)
    authority_refs: tuple[str, ...] = field(default_factory=tuple)
    ambiguity: AmbiguityState = AmbiguityState.RESOLVED
    clarification_refs: tuple[str, ...] = field(default_factory=tuple)
    mutation_class: MutationClass = MutationClass.READ_ONLY
    impact_class: ImpactClass = ImpactClass.LOW
    risk_reassessment_refs: tuple[str, ...] = field(default_factory=tuple)
    parent_digest: str | None = None
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "stage", _required_text(self.stage, "stage"))
        object.__setattr__(self, "action", _required_text(self.action, "action"))
        object.__setattr__(self, "target", _required_text(self.target, "target"))
        for name in (
            "constraints",
            "scope_in",
            "scope_out",
            "side_effects",
            "authority_refs",
            "clarification_refs",
            "risk_reassessment_refs",
        ):
            object.__setattr__(self, name, _canonical_set(getattr(self, name)))
        if self.parent_digest is not None:
            digest = self.parent_digest.strip().lower()
            if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
                raise ValueError("parent_digest must be a lowercase/uppercase SHA-256 hex digest")
            object.__setattr__(self, "parent_digest", digest)
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError(f"unsupported schema_version: {self.schema_version}")

    def canonical_payload(self, *, include_parent: bool = True) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "schema_version": self.schema_version,
            "stage": self.stage,
            "action": self.action,
            "target": self.target,
            "constraints": list(self.constraints),
            "scope_in": list(self.scope_in),
            "scope_out": list(self.scope_out),
            "side_effects": list(self.side_effects),
            "authority_refs": list(self.authority_refs),
            "ambiguity": self.ambiguity.value,
            "clarification_refs": list(self.clarification_refs),
            "mutation_class": self.mutation_class.value,
            "impact_class": self.impact_class.value,
            "risk_reassessment_refs": list(self.risk_reassessment_refs),
        }
        if include_parent:
            payload["parent_digest"] = self.parent_digest
        return payload

    def digest(self) -> str:
        return hashlib.sha256(_canonical_json(self.canonical_payload()).encode("utf-8")).hexdigest()

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "DirectiveSnapshot":
        if not isinstance(raw, Mapping):
            raise TypeError("snapshot must be a JSON object")
        return cls(
            stage=raw["stage"],
            action=raw["action"],
            target=raw["target"],
            constraints=tuple(raw.get("constraints", ())),
            scope_in=tuple(raw.get("scope_in", ())),
            scope_out=tuple(raw.get("scope_out", ())),
            side_effects=tuple(raw.get("side_effects", ())),
            authority_refs=tuple(raw.get("authority_refs", ())),
            ambiguity=AmbiguityState(raw.get("ambiguity", AmbiguityState.RESOLVED.value)),
            clarification_refs=tuple(raw.get("clarification_refs", ())),
            mutation_class=MutationClass(raw.get("mutation_class", MutationClass.READ_ONLY.value)),
            impact_class=ImpactClass(raw.get("impact_class", ImpactClass.LOW.value)),
            risk_reassessment_refs=tuple(raw.get("risk_reassessment_refs", ())),
            parent_digest=raw.get("parent_digest"),
            schema_version=raw.get("schema_version", SCHEMA_VERSION),
        )


@dataclass(frozen=True)
class AuthorizedDelta:
    path: str
    evidence_ref: str
    reason: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "path", _required_text(self.path, "path"))
        object.__setattr__(self, "evidence_ref", _required_text(self.evidence_ref, "evidence_ref"))
        object.__setattr__(self, "reason", _required_text(self.reason, "reason"))

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "AuthorizedDelta":
        return cls(path=raw["path"], evidence_ref=raw["evidence_ref"], reason=raw["reason"])


@dataclass(frozen=True)
class Violation:
    code: str
    path: str
    parent_value: Any
    child_value: Any
    message: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "path": self.path,
            "parent_value": self.parent_value,
            "child_value": self.child_value,
            "message": self.message,
        }


@dataclass(frozen=True)
class TransitionResult:
    status: IntegrityStatus
    parent_digest: str
    child_digest: str
    violations: tuple[Violation, ...]
    authorized_deltas: tuple[AuthorizedDelta, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "status": self.status.value,
            "parent_digest": self.parent_digest,
            "child_digest": self.child_digest,
            "violations": [item.as_dict() for item in self.violations],
            "authorized_deltas": [
                {"path": d.path, "evidence_ref": d.evidence_ref, "reason": d.reason}
                for d in self.authorized_deltas
            ],
        }


def _added(parent: Sequence[str], child: Sequence[str]) -> tuple[str, ...]:
    return tuple(sorted(set(child) - set(parent)))


def _removed(parent: Sequence[str], child: Sequence[str]) -> tuple[str, ...]:
    return tuple(sorted(set(parent) - set(child)))


def _authorize(violations: list[Violation], grants: Sequence[AuthorizedDelta]) -> tuple[list[Violation], list[AuthorizedDelta]]:
    by_path: dict[str, AuthorizedDelta] = {}
    for grant in grants:
        if grant.path in by_path:
            raise ValueError(f"duplicate authorization path: {grant.path}")
        by_path[grant.path] = grant

    remaining: list[Violation] = []
    used: list[AuthorizedDelta] = []
    for violation in violations:
        grant = by_path.get(violation.path)
        if grant is None:
            remaining.append(violation)
        else:
            used.append(grant)
    return remaining, sorted(used, key=lambda item: item.path)


def compare_transition(
    parent: DirectiveSnapshot,
    child: DirectiveSnapshot,
    *,
    authorized_deltas: Sequence[AuthorizedDelta] = (),
) -> TransitionResult:
    violations: list[Violation] = []
    parent_digest = parent.digest()

    if child.parent_digest is not None and child.parent_digest != parent_digest:
        violations.append(Violation(
            "PARENT_DIGEST_MISMATCH",
            "/parent_digest",
            parent_digest,
            child.parent_digest,
            "child is not bound to the supplied parent snapshot",
        ))

    if child.action != parent.action:
        violations.append(Violation(
            "ACTION_CHANGED",
            "/action",
            parent.action,
            child.action,
            "material action changed across the transformation boundary",
        ))

    if child.target != parent.target:
        violations.append(Violation(
            "TARGET_CHANGED",
            "/target",
            parent.target,
            child.target,
            "target identity changed across the transformation boundary",
        ))

    dropped_constraints = _removed(parent.constraints, child.constraints)
    if dropped_constraints:
        violations.append(Violation(
            "CONSTRAINT_DROPPED",
            "/constraints",
            list(parent.constraints),
            list(child.constraints),
            f"downstream snapshot dropped constraints: {', '.join(dropped_constraints)}",
        ))

    added_scope = _added(parent.scope_in, child.scope_in)
    if added_scope:
        violations.append(Violation(
            "SCOPE_BROADENED",
            "/scope_in",
            list(parent.scope_in),
            list(child.scope_in),
            f"downstream snapshot broadened in-scope resources: {', '.join(added_scope)}",
        ))

    removed_exclusions = _removed(parent.scope_out, child.scope_out)
    if removed_exclusions:
        violations.append(Violation(
            "SCOPE_EXCLUSION_REMOVED",
            "/scope_out",
            list(parent.scope_out),
            list(child.scope_out),
            f"downstream snapshot removed out-of-scope exclusions: {', '.join(removed_exclusions)}",
        ))

    new_side_effects = _added(parent.side_effects, child.side_effects)
    if new_side_effects:
        violations.append(Violation(
            "SIDE_EFFECT_ADDED",
            "/side_effects",
            list(parent.side_effects),
            list(child.side_effects),
            f"downstream snapshot introduced new side effects: {', '.join(new_side_effects)}",
        ))

    removed_authority = _removed(parent.authority_refs, child.authority_refs)
    if removed_authority:
        violations.append(Violation(
            "AUTHORITY_REF_REMOVED",
            "/authority_refs",
            list(parent.authority_refs),
            list(child.authority_refs),
            f"downstream snapshot removed authority references: {', '.join(removed_authority)}",
        ))

    if _MUTATION_RANK[child.mutation_class] > _MUTATION_RANK[parent.mutation_class]:
        violations.append(Violation(
            "MUTATION_ESCALATED",
            "/mutation_class",
            parent.mutation_class.value,
            child.mutation_class.value,
            "downstream snapshot increased mutation capability",
        ))

    if _IMPACT_RANK[child.impact_class] < _IMPACT_RANK[parent.impact_class] and not child.risk_reassessment_refs:
        violations.append(Violation(
            "IMPACT_DOWNGRADED_WITHOUT_EVIDENCE",
            "/impact_class",
            parent.impact_class.value,
            child.impact_class.value,
            "impact classification decreased without a risk reassessment reference",
        ))

    if parent.ambiguity is AmbiguityState.OPEN and child.ambiguity is AmbiguityState.RESOLVED and not child.clarification_refs:
        violations.append(Violation(
            "AMBIGUITY_RESOLVED_WITHOUT_CLARIFICATION",
            "/ambiguity",
            parent.ambiguity.value,
            child.ambiguity.value,
            "material ambiguity became resolved without clarification evidence",
        ))

    unresolved, used = _authorize(violations, tuple(authorized_deltas))
    return TransitionResult(
        status=IntegrityStatus.PASS if not unresolved else IntegrityStatus.FREEZE,
        parent_digest=parent_digest,
        child_digest=child.digest(),
        violations=tuple(sorted(unresolved, key=lambda item: (item.path, item.code))),
        authorized_deltas=tuple(used),
    )


def operator_explanation(snapshot: DirectiveSnapshot, result: TransitionResult | None = None) -> dict[str, Any]:
    explanation: dict[str, Any] = {
        "action": snapshot.action,
        "target": snapshot.target,
        "mutation_class": snapshot.mutation_class.value,
        "impact_class": snapshot.impact_class.value,
        "scope_in": list(snapshot.scope_in),
        "scope_out": list(snapshot.scope_out),
        "constraints": list(snapshot.constraints),
        "side_effects": list(snapshot.side_effects),
        "ambiguity": snapshot.ambiguity.value,
        "contract_digest": snapshot.digest(),
    }
    if result is not None:
        explanation["integrity_status"] = result.status.value
        explanation["blocking_issues"] = [
            {"code": violation.code, "path": violation.path, "message": violation.message}
            for violation in result.violations
        ]
        explanation["authorized_changes"] = [
            {"path": delta.path, "evidence_ref": delta.evidence_ref, "reason": delta.reason}
            for delta in result.authorized_deltas
        ]
    return explanation


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _cmd_digest(args: argparse.Namespace) -> int:
    snapshot = DirectiveSnapshot.from_mapping(_load_json(Path(args.snapshot)))
    print(snapshot.digest())
    return 0


def _cmd_compare(args: argparse.Namespace) -> int:
    parent = DirectiveSnapshot.from_mapping(_load_json(Path(args.parent)))
    child = DirectiveSnapshot.from_mapping(_load_json(Path(args.child)))
    grants: tuple[AuthorizedDelta, ...] = ()
    if args.authorization:
        raw = _load_json(Path(args.authorization))
        if not isinstance(raw, list):
            raise TypeError("authorization file must be a JSON array")
        grants = tuple(AuthorizedDelta.from_mapping(item) for item in raw)
    result = compare_transition(parent, child, authorized_deltas=grants)
    print(json.dumps(result.as_dict(), ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if result.status is IntegrityStatus.PASS else 2


def _cmd_explain(args: argparse.Namespace) -> int:
    snapshot = DirectiveSnapshot.from_mapping(_load_json(Path(args.snapshot)))
    print(json.dumps(operator_explanation(snapshot), ensure_ascii=False, sort_keys=True, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NEXY Directive Integrity reference engine")
    sub = parser.add_subparsers(dest="command", required=True)

    digest = sub.add_parser("digest", help="compute deterministic snapshot digest")
    digest.add_argument("snapshot")
    digest.set_defaults(func=_cmd_digest)

    compare = sub.add_parser("compare", help="verify semantic continuity from parent to child")
    compare.add_argument("parent")
    compare.add_argument("child")
    compare.add_argument("--authorization", help="JSON array of AuthorizedDelta objects")
    compare.set_defaults(func=_cmd_compare)

    explain = sub.add_parser("explain", help="render an operator-safe contract summary")
    explain.add_argument("snapshot")
    explain.set_defaults(func=_cmd_explain)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"DIRECTIVE_INTEGRITY_INPUT_INVALID: {exc}", file=sys.stderr)
        return 64


if __name__ == "__main__":
    raise SystemExit(main())
