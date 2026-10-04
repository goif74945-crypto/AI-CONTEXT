from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatchcase
from typing import Iterable, Mapping, Sequence

from .common import FrontierInputError, require_text, stable_hash


_VALID_EFFECTS = {"ALLOW", "DENY"}
_SEVERITY = {
    "AUTHORITY_EXPANSION": 5,
    "CONFLICT_INTRODUCED": 4,
    "FREEZE_REMOVED_TO_ALLOW": 4,
    "AVAILABILITY_REGRESSION": 3,
    "FREEZE_INTRODUCED": 2,
    "OTHER_DIVERGENCE": 1,
}


@dataclass(frozen=True, slots=True)
class AuthorityRule:
    rule_id: str
    priority: int
    effect: str
    action_pattern: str = "*"
    resource_pattern: str = "*"
    required_attributes: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True, slots=True)
class DecisionCase:
    case_id: str
    actor: str
    action: str
    resource: str
    attributes: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True, slots=True)
class Decision:
    state: str
    rule_ids: tuple[str, ...]
    reason: str
    fingerprint: str


@dataclass(frozen=True, slots=True)
class Divergence:
    case_id: str
    baseline: str
    candidate: str
    category: str
    severity: int


@dataclass(frozen=True, slots=True)
class WindTunnelReport:
    status: str
    total_cases: int
    divergence_count: int
    blast_radius_bps: int
    dangerous_divergence_count: int
    divergences: tuple[Divergence, ...]
    minimal_witness: Divergence | None
    baseline_policy_hash: str
    candidate_policy_hash: str
    fingerprint: str


def _canon_attrs(items: Iterable[tuple[str, str]], field: str) -> tuple[tuple[str, str], ...]:
    out: dict[str, str] = {}
    for item in items:
        if not isinstance(item, tuple) or len(item) != 2:
            raise FrontierInputError(f"{field}:ATTRIBUTE_NOT_PAIR")
        key, value = require_text(item[0], f"{field}.key"), require_text(item[1], f"{field}.value")
        if key in out and out[key] != value:
            raise FrontierInputError(f"{field}:DUPLICATE_ATTRIBUTE:{key}")
        out[key] = value
    return tuple(sorted(out.items()))


def _canon_rule(rule: AuthorityRule) -> AuthorityRule:
    rid = require_text(rule.rule_id, "rule_id")
    if not isinstance(rule.priority, int):
        raise FrontierInputError(f"{rid}:PRIORITY_NOT_INT")
    effect = require_text(rule.effect, f"{rid}.effect").upper()
    if effect not in _VALID_EFFECTS:
        raise FrontierInputError(f"{rid}:BAD_EFFECT:{effect}")
    action = require_text(rule.action_pattern, f"{rid}.action_pattern")
    resource = require_text(rule.resource_pattern, f"{rid}.resource_pattern")
    return AuthorityRule(rid, rule.priority, effect, action, resource, _canon_attrs(rule.required_attributes, rid))


def _canon_case(case: DecisionCase) -> DecisionCase:
    return DecisionCase(
        require_text(case.case_id, "case_id"),
        require_text(case.actor, "actor"),
        require_text(case.action, "action"),
        require_text(case.resource, "resource"),
        _canon_attrs(case.attributes, case.case_id),
    )


def _rule_matches(rule: AuthorityRule, case: DecisionCase) -> bool:
    attrs = dict(case.attributes)
    return (
        fnmatchcase(case.action, rule.action_pattern)
        and fnmatchcase(case.resource, rule.resource_pattern)
        and all(attrs.get(k) == v for k, v in rule.required_attributes)
    )


def evaluate_policy(rules: Sequence[AuthorityRule], case: DecisionCase) -> Decision:
    canonical_rules = tuple(sorted((_canon_rule(r) for r in rules), key=lambda r: (-r.priority, r.rule_id)))
    canonical_case = _canon_case(case)
    ids = [r.rule_id for r in canonical_rules]
    if len(ids) != len(set(ids)):
        raise FrontierInputError("DUPLICATE_RULE_ID")
    matched = [r for r in canonical_rules if _rule_matches(r, canonical_case)]
    if not matched:
        payload = {"state": "FREEZE", "reason": "NO_MATCHING_AUTHORITY_RULE", "rule_ids": [], "case": canonical_case}
        return Decision("FREEZE", (), "NO_MATCHING_AUTHORITY_RULE", stable_hash(payload))
    top_priority = matched[0].priority
    top = tuple(r for r in matched if r.priority == top_priority)
    effects = {r.effect for r in top}
    rule_ids = tuple(sorted(r.rule_id for r in top))
    if len(effects) != 1:
        payload = {"state": "FREEZE", "reason": "TOP_PRIORITY_CONFLICT", "rule_ids": rule_ids, "case": canonical_case}
        return Decision("FREEZE", rule_ids, "TOP_PRIORITY_CONFLICT", stable_hash(payload))
    state = next(iter(effects))
    payload = {"state": state, "reason": "TOP_PRIORITY_RULE", "rule_ids": rule_ids, "case": canonical_case}
    return Decision(state, rule_ids, "TOP_PRIORITY_RULE", stable_hash(payload))


def _category(before: Decision, after: Decision) -> str:
    if before.state == after.state:
        if before.reason != after.reason or before.rule_ids != after.rule_ids:
            return "OTHER_DIVERGENCE"
        return "NONE"
    if before.state == "DENY" and after.state == "ALLOW":
        return "AUTHORITY_EXPANSION"
    if before.state == "ALLOW" and after.state == "DENY":
        return "AVAILABILITY_REGRESSION"
    if after.reason == "TOP_PRIORITY_CONFLICT":
        return "CONFLICT_INTRODUCED"
    if before.state == "FREEZE" and after.state == "ALLOW":
        return "FREEZE_REMOVED_TO_ALLOW"
    if before.state != "FREEZE" and after.state == "FREEZE":
        return "FREEZE_INTRODUCED"
    return "OTHER_DIVERGENCE"


def simulate_authority_change(
    baseline_rules: Sequence[AuthorityRule],
    candidate_rules: Sequence[AuthorityRule],
    cases: Iterable[DecisionCase],
) -> WindTunnelReport:
    baseline = tuple(sorted((_canon_rule(r) for r in baseline_rules), key=lambda r: r.rule_id))
    candidate = tuple(sorted((_canon_rule(r) for r in candidate_rules), key=lambda r: r.rule_id))
    canonical_cases = tuple(sorted((_canon_case(c) for c in cases), key=lambda c: c.case_id))
    if not canonical_cases:
        raise FrontierInputError("NO_DECISION_CASES")
    case_ids = [c.case_id for c in canonical_cases]
    if len(case_ids) != len(set(case_ids)):
        raise FrontierInputError("DUPLICATE_CASE_ID")

    divergences: list[Divergence] = []
    for case in canonical_cases:
        before = evaluate_policy(baseline, case)
        after = evaluate_policy(candidate, case)
        category = _category(before, after)
        if category != "NONE":
            divergences.append(Divergence(case.case_id, before.state, after.state, category, _SEVERITY[category]))

    ordered = tuple(sorted(divergences, key=lambda d: (-d.severity, d.case_id, d.category)))
    dangerous = sum(d.severity >= 4 for d in ordered)
    witness = ordered[0] if ordered else None
    blast = (len(ordered) * 10_000) // len(canonical_cases)
    status = "FREEZE" if dangerous else "PASS"
    base_hash, cand_hash = stable_hash(baseline), stable_hash(candidate)
    payload = {
        "status": status,
        "total_cases": len(canonical_cases),
        "blast_radius_bps": blast,
        "divergences": ordered,
        "baseline_policy_hash": base_hash,
        "candidate_policy_hash": cand_hash,
    }
    return WindTunnelReport(status, len(canonical_cases), len(ordered), blast, dangerous, ordered, witness, base_hash, cand_hash, stable_hash(payload))
