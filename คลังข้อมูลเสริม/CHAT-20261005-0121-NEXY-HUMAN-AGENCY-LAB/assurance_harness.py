from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from hashlib import sha256
import json
from typing import Any, Iterable

from human_agency_lab import (
    AgencyDecisionEngine,
    AgencyPolicy,
    AttentionBudget,
    Decision,
    RequestProfile,
    apply_attention_budget,
)


_RANK = {
    Decision.PROCEED: 0,
    Decision.PREVIEW: 1,
    Decision.CONFIRM: 2,
    Decision.FREEZE: 3,
}


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return sha256(_canonical_json(value)).hexdigest()


def _below(value: float) -> float:
    return max(0.0, round(value - 0.01, 10))


def _above(value: float) -> float:
    return min(1.0, round(value + 0.01, 10))


def _dedupe(requests: Iterable[RequestProfile]) -> tuple[RequestProfile, ...]:
    by_digest: dict[str, RequestProfile] = {}
    for request in requests:
        digest = _digest(request.canonical_dict())
        by_digest[digest] = request
    return tuple(by_digest[key] for key in sorted(by_digest))


def generate_boundary_corpus(policy: AgencyPolicy | None = None) -> tuple[RequestProfile, ...]:
    policy = policy or AgencyPolicy()
    requests: list[RequestProfile] = [RequestProfile(action_id="baseline")]

    continuous_axes = {
        "ambiguity": (
            0.0,
            _below(policy.preview_ambiguity),
            policy.preview_ambiguity,
            _below(policy.confirm_ambiguity),
            policy.confirm_ambiguity,
            _below(policy.freeze_ambiguity),
            policy.freeze_ambiguity,
            1.0,
        ),
        "reversibility": (
            0.0,
            _below(policy.low_reversibility),
            policy.low_reversibility,
            _above(policy.low_reversibility),
            1.0,
        ),
        "confidence": (
            0.0,
            _below(policy.low_confidence),
            policy.low_confidence,
            _above(policy.low_confidence),
            1.0,
        ),
        "scope_breadth": (
            0.0,
            _below(policy.high_impact_scope),
            policy.high_impact_scope,
            _below(policy.broad_scope),
            policy.broad_scope,
            1.0,
        ),
        "data_sensitivity": (
            0.0,
            _below(policy.sensitive_data),
            policy.sensitive_data,
            1.0,
        ),
        "monetary_cost": (
            0.0,
            _below(policy.material_cost),
            policy.material_cost,
            1.0,
        ),
    }

    for field, values in continuous_axes.items():
        for value in values:
            requests.append(
                replace(
                    RequestProfile(action_id=f"axis:{field}:{value}"),
                    **{field: value},
                )
            )

    # Full boolean boundary matrix over a neutral numeric profile.
    for mask in range(32):
        requests.append(
            RequestProfile(
                action_id=f"bool:{mask:02d}",
                external_side_effect=bool(mask & 1),
                destructive=bool(mask & 2),
                rollback_available=bool(mask & 4),
                explicit_user_authority=bool(mask & 8),
                crosses_auth_boundary=bool(mask & 16),
                reversibility=1.0,
            )
        )

    # High-value interaction surfaces near hard boundaries.
    for ambiguity in (
        _below(policy.confirm_ambiguity),
        policy.confirm_ambiguity,
        policy.freeze_ambiguity,
        1.0,
    ):
        for reversibility in (0.0, policy.low_reversibility, 1.0):
            for external in (False, True):
                requests.append(
                    RequestProfile(
                        action_id=f"amb-ext:{ambiguity}:{reversibility}:{int(external)}",
                        ambiguity=ambiguity,
                        reversibility=reversibility,
                        external_side_effect=external,
                    )
                )

    for scope in (
        _below(policy.high_impact_scope),
        policy.high_impact_scope,
        policy.broad_scope,
        1.0,
    ):
        for authority in (False, True):
            requests.append(
                RequestProfile(
                    action_id=f"scope-auth:{scope}:{int(authority)}",
                    scope_breadth=scope,
                    explicit_user_authority=authority,
                )
            )

    for sensitivity in (
        _below(policy.sensitive_data),
        policy.sensitive_data,
        1.0,
    ):
        for authority in (False, True):
            requests.append(
                RequestProfile(
                    action_id=f"sensitive:{sensitivity}:{int(authority)}",
                    external_side_effect=True,
                    data_sensitivity=sensitivity,
                    explicit_user_authority=authority,
                )
            )

    for cost in (_below(policy.material_cost), policy.material_cost, 1.0):
        for authority in (False, True):
            requests.append(
                RequestProfile(
                    action_id=f"cost:{cost}:{int(authority)}",
                    external_side_effect=True,
                    monetary_cost=cost,
                    explicit_user_authority=authority,
                )
            )

    for rollback in (False, True):
        for reversibility in (0.0, policy.low_reversibility, _above(policy.low_reversibility), 1.0):
            for authority in (False, True):
                requests.append(
                    RequestProfile(
                        action_id=f"delete:{int(rollback)}:{reversibility}:{int(authority)}",
                        destructive=True,
                        rollback_available=rollback,
                        reversibility=reversibility,
                        explicit_user_authority=authority,
                    )
                )

    return _dedupe(requests)


@dataclass(frozen=True)
class AssuranceFailure:
    property_name: str
    case_id: str
    detail: str


@dataclass(frozen=True)
class AssuranceReport:
    corpus_size: int
    determinism_checks: int
    hard_gate_budget_checks: int
    monotonicity_checks: int
    authority_removal_checks: int
    destructive_rollback_checks: int
    failures: tuple[AssuranceFailure, ...]

    @property
    def passed(self) -> bool:
        return not self.failures

    @property
    def total_checks(self) -> int:
        return (
            self.determinism_checks
            + self.hard_gate_budget_checks
            + self.monotonicity_checks
            + self.authority_removal_checks
            + self.destructive_rollback_checks
        )

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "authority_removal_checks": self.authority_removal_checks,
            "corpus_size": self.corpus_size,
            "destructive_rollback_checks": self.destructive_rollback_checks,
            "determinism_checks": self.determinism_checks,
            "failures": [asdict(failure) for failure in self.failures],
            "hard_gate_budget_checks": self.hard_gate_budget_checks,
            "monotonicity_checks": self.monotonicity_checks,
            "passed": self.passed,
            "total_checks": self.total_checks,
        }

    def digest(self) -> str:
        return _digest(self.canonical_dict())


def _nondecreasing(decisions: list[Decision]) -> bool:
    ranks = [_RANK[decision] for decision in decisions]
    return ranks == sorted(ranks)


def run_assurance(policy: AgencyPolicy | None = None) -> AssuranceReport:
    policy = policy or AgencyPolicy()
    engine = AgencyDecisionEngine(policy)
    corpus = generate_boundary_corpus(policy)
    failures: list[AssuranceFailure] = []

    determinism_checks = 0
    hard_gate_budget_checks = 0
    authority_removal_checks = 0
    destructive_rollback_checks = 0
    monotonicity_checks = 0

    for request in corpus:
        first = engine.evaluate(request)
        second = engine.evaluate(request)
        determinism_checks += 1
        if first.digest() != second.digest():
            failures.append(
                AssuranceFailure(
                    "determinism",
                    request.action_id,
                    "same normalized request produced different decision digest",
                )
            )

        if first.hard_gate:
            for capacity in (0, 1, 2, 3, 100):
                effective = apply_attention_budget(first, AttentionBudget(capacity))
                hard_gate_budget_checks += 1
                if effective.decision is not first.decision or not effective.hard_gate:
                    failures.append(
                        AssuranceFailure(
                            "hard_gate_budget_invariance",
                            f"{request.action_id}@{capacity}",
                            f"{first.decision.value}->{effective.decision.value}",
                        )
                    )

        if (
            request.destructive
            or request.crosses_auth_boundary
            or request.scope_breadth >= policy.high_impact_scope
            or request.monetary_cost >= policy.material_cost
            or request.data_sensitivity >= policy.sensitive_data
        ):
            with_authority = engine.evaluate(replace(request, explicit_user_authority=True)).decision
            without_authority = engine.evaluate(replace(request, explicit_user_authority=False)).decision
            authority_removal_checks += 1
            if _RANK[without_authority] < _RANK[with_authority]:
                failures.append(
                    AssuranceFailure(
                        "authority_removal_non_relaxing",
                        request.action_id,
                        f"with={with_authority.value}, without={without_authority.value}",
                    )
                )

        if request.destructive:
            safer = engine.evaluate(
                replace(request, rollback_available=True, reversibility=1.0)
            ).decision
            less_safe = engine.evaluate(
                replace(request, rollback_available=False, reversibility=0.0)
            ).decision
            destructive_rollback_checks += 1
            if _RANK[less_safe] < _RANK[safer]:
                failures.append(
                    AssuranceFailure(
                        "rollback_removal_non_relaxing",
                        request.action_id,
                        f"safer={safer.value}, less_safe={less_safe.value}",
                    )
                )

    trace_specs = (
        (
            "ambiguity_external",
            [0.0, policy.preview_ambiguity, policy.confirm_ambiguity, policy.freeze_ambiguity, 1.0],
            lambda value: RequestProfile(
                action_id=f"trace:ambiguity:{value}",
                ambiguity=value,
                external_side_effect=True,
                reversibility=1.0,
            ),
        ),
        (
            "scope_without_authority",
            [0.0, _below(policy.high_impact_scope), policy.high_impact_scope, policy.broad_scope, 1.0],
            lambda value: RequestProfile(
                action_id=f"trace:scope:{value}",
                scope_breadth=value,
                explicit_user_authority=False,
            ),
        ),
        (
            "sensitive_external",
            [0.0, _below(policy.sensitive_data), policy.sensitive_data, 1.0],
            lambda value: RequestProfile(
                action_id=f"trace:sensitive:{value}",
                data_sensitivity=value,
                external_side_effect=True,
            ),
        ),
        (
            "cost_external",
            [0.0, _below(policy.material_cost), policy.material_cost, 1.0],
            lambda value: RequestProfile(
                action_id=f"trace:cost:{value}",
                monetary_cost=value,
                external_side_effect=True,
            ),
        ),
    )

    for name, values, factory in trace_specs:
        decisions = [engine.evaluate(factory(value)).decision for value in values]
        monotonicity_checks += len(values) - 1
        if not _nondecreasing(decisions):
            failures.append(
                AssuranceFailure(
                    "risk_monotonicity",
                    name,
                    ",".join(decision.value for decision in decisions),
                )
            )

    return AssuranceReport(
        corpus_size=len(corpus),
        determinism_checks=determinism_checks,
        hard_gate_budget_checks=hard_gate_budget_checks,
        monotonicity_checks=monotonicity_checks,
        authority_removal_checks=authority_removal_checks,
        destructive_rollback_checks=destructive_rollback_checks,
        failures=tuple(failures),
    )


if __name__ == "__main__":
    report = run_assurance()
    print(json.dumps(report.canonical_dict(), ensure_ascii=False, sort_keys=True, indent=2))
    raise SystemExit(0 if report.passed else 1)
