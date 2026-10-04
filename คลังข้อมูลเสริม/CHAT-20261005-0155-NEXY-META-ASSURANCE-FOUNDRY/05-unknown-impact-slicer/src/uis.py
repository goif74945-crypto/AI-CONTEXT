from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from itertools import product
import json
from typing import Iterable, Mapping, Any


class ContractError(ValueError):
    pass


def _name(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{field} must be a non-empty string")
    return value.strip()


def _canon(value: Any) -> str:
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise ContractError("domain values must be JSON-compatible") from exc


def _unique_domain(values: Iterable[Any]) -> tuple[Any, ...]:
    by_key: dict[str, Any] = {}
    for value in values:
        key = _canon(value)
        if key in by_key:
            raise ContractError("variable domains must not contain duplicate canonical values")
        by_key[key] = value
    if not by_key:
        raise ContractError("variable domain must not be empty")
    return tuple(by_key[key] for key in sorted(by_key))


@dataclass(frozen=True)
class Variable:
    name: str
    domain: tuple[Any, ...]

    @classmethod
    def build(cls, name: str, domain: Iterable[Any]) -> "Variable":
        return cls(name=_name(name, "variable name"), domain=_unique_domain(domain))


@dataclass(frozen=True)
class Rule:
    rule_id: str
    conditions: Mapping[str, tuple[Any, ...]]
    output: str

    @classmethod
    def build(cls, rule_id: str, conditions: Mapping[str, Iterable[Any]], output: str) -> "Rule":
        if not isinstance(conditions, Mapping):
            raise ContractError("conditions must be a mapping")
        normalized = { _name(k, "condition variable"): _unique_domain(v) for k, v in conditions.items() }
        return cls(
            rule_id=_name(rule_id, "rule_id"),
            conditions=normalized,
            output=_name(output, "output"),
        )


@dataclass(frozen=True)
class ImpactReport:
    status: str
    action: str
    outputs: tuple[str, ...]
    material_unknowns: tuple[str, ...]
    non_material_unknowns: tuple[str, ...]
    states_evaluated: int
    reason_codes: tuple[str, ...]
    fingerprint: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "action": self.action,
            "outputs": list(self.outputs),
            "material_unknowns": list(self.material_unknowns),
            "non_material_unknowns": list(self.non_material_unknowns),
            "states_evaluated": self.states_evaluated,
            "reason_codes": list(self.reason_codes),
            "fingerprint": self.fingerprint,
        }


class ImpactModel:
    def __init__(
        self,
        variables: Iterable[Variable],
        rules: Iterable[Rule],
        *,
        default_output: str,
        max_states: int = 100_000,
    ) -> None:
        self.variables: dict[str, Variable] = {}
        for variable in variables:
            if not isinstance(variable, Variable):
                raise ContractError("variables must contain Variable instances")
            if variable.name in self.variables:
                raise ContractError(f"duplicate variable: {variable.name}")
            self.variables[variable.name] = variable
        if not self.variables:
            raise ContractError("at least one variable is required")

        rule_values = tuple(rules)
        if any(not isinstance(rule, Rule) for rule in rule_values):
            raise ContractError("rules must contain Rule instances")
        ids = [rule.rule_id for rule in rule_values]
        if len(set(ids)) != len(ids):
            raise ContractError("rule_id values must be unique")
        self.rules = tuple(sorted(rule_values, key=lambda r: r.rule_id))
        self.default_output = _name(default_output, "default_output")
        if not isinstance(max_states, int) or max_states < 1:
            raise ContractError("max_states must be an integer >= 1")
        self.max_states = max_states
        self._validate_rules()

    def _validate_rules(self) -> None:
        for rule in self.rules:
            unknown_vars = set(rule.conditions) - set(self.variables)
            if unknown_vars:
                raise ContractError(f"rule {rule.rule_id} references unknown variables: {sorted(unknown_vars)}")
            for name, allowed in rule.conditions.items():
                domain_keys = {_canon(v) for v in self.variables[name].domain}
                allowed_keys = {_canon(v) for v in allowed}
                if not allowed_keys <= domain_keys:
                    raise ContractError(f"rule {rule.rule_id} contains values outside domain of {name}")

    def _matches(self, rule: Rule, assignment: Mapping[str, Any]) -> bool:
        for name, allowed in rule.conditions.items():
            value_key = _canon(assignment[name])
            if value_key not in {_canon(v) for v in allowed}:
                return False
        return True

    def _evaluate(self, assignment: Mapping[str, Any]) -> tuple[str | None, tuple[str, ...]]:
        matched = [rule for rule in self.rules if self._matches(rule, assignment)]
        outputs = sorted({rule.output for rule in matched})
        if len(outputs) > 1:
            return None, tuple(rule.rule_id for rule in matched)
        if outputs:
            return outputs[0], tuple(rule.rule_id for rule in matched)
        return self.default_output, ()

    def _fingerprint(self, known: Mapping[str, Any]) -> str:
        payload = {
            "variables": [
                {"name": name, "domain": list(self.variables[name].domain)}
                for name in sorted(self.variables)
            ],
            "rules": [
                {
                    "rule_id": rule.rule_id,
                    "conditions": {k: list(rule.conditions[k]) for k in sorted(rule.conditions)},
                    "output": rule.output,
                }
                for rule in self.rules
            ],
            "default_output": self.default_output,
            "max_states": self.max_states,
            "known": {k: known[k] for k in sorted(known)},
        }
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        return sha256(raw).hexdigest()

    def analyze(self, known: Mapping[str, Any] | None = None) -> ImpactReport:
        known = dict(known or {})
        unknown_known_vars = set(known) - set(self.variables)
        if unknown_known_vars:
            raise ContractError(f"known bindings reference unknown variables: {sorted(unknown_known_vars)}")
        for name, value in known.items():
            if _canon(value) not in {_canon(v) for v in self.variables[name].domain}:
                raise ContractError(f"known value for {name} is outside its domain")

        unknown_names = tuple(sorted(set(self.variables) - set(known)))
        state_count = 1
        for name in unknown_names:
            state_count *= len(self.variables[name].domain)
            if state_count > self.max_states:
                return ImpactReport(
                    status="FREEZE",
                    action="FREEZE",
                    outputs=(),
                    material_unknowns=unknown_names,
                    non_material_unknowns=(),
                    states_evaluated=0,
                    reason_codes=("ENUMERATION_LIMIT_EXCEEDED",),
                    fingerprint=self._fingerprint(known),
                )

        records: list[tuple[dict[str, Any], str]] = []
        domains = [self.variables[name].domain for name in unknown_names]
        combinations = product(*domains) if domains else [()]
        for values in combinations:
            assignment = dict(known)
            assignment.update(zip(unknown_names, values))
            output, matched = self._evaluate(assignment)
            if output is None:
                return ImpactReport(
                    status="FREEZE",
                    action="FREEZE",
                    outputs=(),
                    material_unknowns=unknown_names,
                    non_material_unknowns=(),
                    states_evaluated=len(records) + 1,
                    reason_codes=("CONFLICTING_MATCHED_RULES",) + matched,
                    fingerprint=self._fingerprint(known),
                )
            records.append((assignment, output))

        outputs = tuple(sorted({output for _, output in records}))
        material: set[str] = set()
        for target in unknown_names:
            grouped: dict[tuple[tuple[str, str], ...], set[str]] = {}
            for assignment, output in records:
                key = tuple(
                    (name, _canon(assignment[name]))
                    for name in unknown_names
                    if name != target
                )
                grouped.setdefault(key, set()).add(output)
            if any(len(group_outputs) > 1 for group_outputs in grouped.values()):
                material.add(target)

        non_material = set(unknown_names) - material
        if len(outputs) == 1:
            status = "STABLE"
            action = "PROCEED_WITH_UNKNOWNS"
            reasons = ("OUTPUT_INVARIANT_ACROSS_DECLARED_UNKNOWNS",)
        else:
            status = "MATERIAL_UNKNOWNS"
            action = "CLARIFY_OR_FREEZE"
            reasons = ("OUTPUT_DEPENDS_ON_UNKNOWNS",)

        return ImpactReport(
            status=status,
            action=action,
            outputs=outputs,
            material_unknowns=tuple(sorted(material)),
            non_material_unknowns=tuple(sorted(non_material)),
            states_evaluated=len(records),
            reason_codes=reasons,
            fingerprint=self._fingerprint(known),
        )
