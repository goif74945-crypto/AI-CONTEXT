"""NEXY Frontier Five supplemental reference systems.

AI-proposed, isolated, deterministic, stdlib-only reference implementation.
This file does not modify or import NEXY.AI.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Mapping, Sequence, Set


# ---------------------------------------------------------------------------
# 1) UDM — Uncertainty Dependency Mesh
# ---------------------------------------------------------------------------

class MeshError(ValueError):
    pass


@dataclass(frozen=True)
class Claim:
    claim_id: str
    confidence: float
    evidence_age_s: int = 0
    ttl_s: int | None = None
    dependencies: tuple[str, ...] = ()
    authoritative: bool = False

    def __post_init__(self) -> None:
        if not self.claim_id:
            raise MeshError("claim_id is required")
        if not 0.0 <= self.confidence <= 1.0:
            raise MeshError("confidence must be in [0,1]")
        if self.evidence_age_s < 0:
            raise MeshError("evidence_age_s cannot be negative")
        if self.ttl_s is not None and self.ttl_s < 0:
            raise MeshError("ttl_s cannot be negative")
        if self.claim_id in self.dependencies:
            raise MeshError("claim cannot depend on itself")
        if len(set(self.dependencies)) != len(self.dependencies):
            raise MeshError("dependencies cannot contain duplicates")

    @property
    def fresh(self) -> bool:
        return self.ttl_s is None or self.evidence_age_s <= self.ttl_s


@dataclass(frozen=True)
class DecisionRule:
    decision_id: str
    required_claims: tuple[str, ...]
    min_confidence: float = 0.8

    def __post_init__(self) -> None:
        if not self.decision_id:
            raise MeshError("decision_id is required")
        if not self.required_claims:
            raise MeshError("required_claims cannot be empty")
        if len(set(self.required_claims)) != len(self.required_claims):
            raise MeshError("required_claims cannot contain duplicates")
        if not 0.0 <= self.min_confidence <= 1.0:
            raise MeshError("min_confidence must be in [0,1]")


@dataclass
class UncertaintyMesh:
    claims: Dict[str, Claim] = field(default_factory=dict)

    def add(self, claim: Claim) -> None:
        if claim.claim_id in self.claims:
            raise MeshError(f"duplicate claim: {claim.claim_id}")
        self.claims[claim.claim_id] = claim

    def _topological_order(self) -> List[str]:
        missing = {
            dep
            for claim in self.claims.values()
            for dep in claim.dependencies
            if dep not in self.claims
        }
        if missing:
            raise MeshError(f"missing dependencies: {sorted(missing)}")

        indegree = {node: len(claim.dependencies) for node, claim in self.claims.items()}
        reverse: Dict[str, Set[str]] = {node: set() for node in self.claims}
        for node, claim in self.claims.items():
            for dep in claim.dependencies:
                reverse[dep].add(node)

        ready = sorted(node for node, degree in indegree.items() if degree == 0)
        order: List[str] = []
        while ready:
            node = ready.pop(0)
            order.append(node)
            for nxt in sorted(reverse[node]):
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    lo, hi = 0, len(ready)
                    while lo < hi:
                        mid = (lo + hi) // 2
                        if ready[mid] < nxt:
                            lo = mid + 1
                        else:
                            hi = mid
                    ready.insert(lo, nxt)

        if len(order) != len(self.claims):
            cyclic = sorted(node for node, degree in indegree.items() if degree > 0)
            raise MeshError(f"cycle detected: {cyclic}")
        return order

    def validate(self) -> None:
        self._topological_order()

    def effective_confidences(self) -> Dict[str, float]:
        scores: Dict[str, float] = {}
        for node in self._topological_order():
            claim = self.claims[node]
            if not claim.fresh:
                scores[node] = 0.0
                continue
            dependency_floor = min((scores[d] for d in claim.dependencies), default=1.0)
            scores[node] = min(claim.confidence, dependency_floor)
        return scores

    def effective_confidence(self, claim_id: str) -> float:
        if claim_id not in self.claims:
            raise MeshError(f"unknown claim: {claim_id}")
        return self.effective_confidences()[claim_id]

    def decision_status(self, rule: DecisionRule) -> Mapping[str, object]:
        unknown = [claim for claim in rule.required_claims if claim not in self.claims]
        if unknown:
            return {"decision_id": rule.decision_id, "status": "BLOCKED", "unknown": unknown}
        all_scores = self.effective_confidences()
        scores = {claim: all_scores[claim] for claim in rule.required_claims}
        blockers = sorted(claim for claim, score in scores.items() if score < rule.min_confidence)
        return {
            "decision_id": rule.decision_id,
            "status": "READY" if not blockers else "BLOCKED",
            "blockers": blockers,
            "scores": scores,
        }

    def impacted_by(self, changed_claims: Iterable[str]) -> List[str]:
        self.validate()
        changed = set(changed_claims)
        unknown = changed - self.claims.keys()
        if unknown:
            raise MeshError(f"unknown changed claims: {sorted(unknown)}")

        reverse: Dict[str, Set[str]] = {key: set() for key in self.claims}
        for claim in self.claims.values():
            for dependency in claim.dependencies:
                reverse[dependency].add(claim.claim_id)

        impacted = set(changed)
        queue = list(sorted(changed))
        cursor = 0
        while cursor < len(queue):
            current = queue[cursor]
            cursor += 1
            for downstream in sorted(reverse[current]):
                if downstream not in impacted:
                    impacted.add(downstream)
                    queue.append(downstream)
        return sorted(impacted)


# ---------------------------------------------------------------------------
# 2) AEC — Ambiguity Experiment Compiler
# ---------------------------------------------------------------------------

class ExperimentError(ValueError):
    pass


@dataclass(frozen=True)
class Ambiguity:
    ambiguity_id: str
    impact: float
    branches: int
    irreversible_if_wrong: bool = False

    def __post_init__(self) -> None:
        if not self.ambiguity_id:
            raise ExperimentError("ambiguity_id is required")
        if self.impact < 0:
            raise ExperimentError("impact cannot be negative")
        if self.branches < 2:
            raise ExperimentError("branches must be >=2")


@dataclass(frozen=True)
class Experiment:
    experiment_id: str
    resolves: tuple[str, ...]
    info_gain: float
    cost: float
    risk: float
    reversible: bool
    violates_invariants: bool = False

    def __post_init__(self) -> None:
        if not self.experiment_id or not self.resolves:
            raise ExperimentError("experiment_id and resolves are required")
        if self.info_gain < 0 or self.cost < 0 or self.risk < 0:
            raise ExperimentError("info_gain/cost/risk cannot be negative")


class ExperimentCompiler:
    def __init__(self, risk_weight: float = 3.0, cost_weight: float = 1.0) -> None:
        if risk_weight < 0 or cost_weight < 0:
            raise ExperimentError("weights cannot be negative")
        self.risk_weight = risk_weight
        self.cost_weight = cost_weight

    def _score(self, experiment: Experiment, uncovered: set[str], impacts: dict[str, float]) -> float:
        coverage_value = sum(impacts[item] for item in experiment.resolves if item in uncovered)
        if coverage_value <= 0:
            return float("-inf")
        denominator = 1.0 + self.cost_weight * experiment.cost + self.risk_weight * experiment.risk
        return coverage_value * (1.0 + experiment.info_gain) / denominator

    def compile(
        self,
        ambiguities: Sequence[Ambiguity],
        experiments: Iterable[Experiment],
        *,
        min_impact: float = 0.0,
    ) -> List[str]:
        if min_impact < 0:
            raise ExperimentError("min_impact cannot be negative")

        ambiguity_map = {item.ambiguity_id: item for item in ambiguities}
        if len(ambiguity_map) != len(ambiguities):
            raise ExperimentError("duplicate ambiguity ids")

        target = {item.ambiguity_id for item in ambiguities if item.impact >= min_impact}
        impacts = {item.ambiguity_id: item.impact for item in ambiguities}
        candidates: List[Experiment] = []
        seen_experiment_ids: set[str] = set()

        for experiment in experiments:
            if experiment.experiment_id in seen_experiment_ids:
                raise ExperimentError(f"duplicate experiment id: {experiment.experiment_id}")
            seen_experiment_ids.add(experiment.experiment_id)
            unknown = set(experiment.resolves) - ambiguity_map.keys()
            if unknown:
                raise ExperimentError(f"experiment resolves unknown ambiguities: {sorted(unknown)}")
            if experiment.violates_invariants or not experiment.reversible:
                continue
            candidates.append(experiment)

        uncovered = set(target)
        chosen: List[str] = []
        while uncovered:
            ranked = sorted(
                ((self._score(item, uncovered, impacts), item.experiment_id, item) for item in candidates),
                key=lambda row: (-row[0], row[1]),
            )
            if not ranked or ranked[0][0] == float("-inf"):
                raise ExperimentError(f"unresolved ambiguities: {sorted(uncovered)}")
            _, _, best = ranked[0]
            chosen.append(best.experiment_id)
            uncovered -= set(best.resolves)
            candidates = [item for item in candidates if item.experiment_id != best.experiment_id]
        return chosen


# ---------------------------------------------------------------------------
# 3) CAMR — Capability-Aware Mission Router
# ---------------------------------------------------------------------------

class RoutingError(ValueError):
    pass


@dataclass(frozen=True)
class Capability:
    tool_id: str
    provides: frozenset[str]
    permissions: frozenset[str]
    trust: float
    latency_ms: int
    reversible: bool
    freshness_s: int | None = None
    available: bool = True

    def __post_init__(self) -> None:
        if not self.tool_id or not self.provides:
            raise RoutingError("tool_id and provides are required")
        if not 0.0 <= self.trust <= 1.0:
            raise RoutingError("trust must be in [0,1]")
        if self.latency_ms < 0:
            raise RoutingError("latency_ms cannot be negative")
        if self.freshness_s is not None and self.freshness_s < 0:
            raise RoutingError("freshness_s cannot be negative")


@dataclass(frozen=True)
class MissionStep:
    step_id: str
    need: str
    required_permission: str | None = None
    min_trust: float = 0.8
    require_reversible: bool = False
    max_freshness_s: int | None = None

    def __post_init__(self) -> None:
        if not self.step_id or not self.need:
            raise RoutingError("step_id and need are required")
        if not 0.0 <= self.min_trust <= 1.0:
            raise RoutingError("min_trust must be in [0,1]")
        if self.max_freshness_s is not None and self.max_freshness_s < 0:
            raise RoutingError("max_freshness_s cannot be negative")


class CapabilityRouter:
    def __init__(self, capabilities: Iterable[Capability]) -> None:
        self.capabilities = tuple(capabilities)
        ids = [item.tool_id for item in self.capabilities]
        if len(ids) != len(set(ids)):
            raise RoutingError("duplicate tool ids")

    @staticmethod
    def _eligible(capability: Capability, step: MissionStep) -> bool:
        if not capability.available or step.need not in capability.provides or capability.trust < step.min_trust:
            return False
        if step.required_permission and step.required_permission not in capability.permissions:
            return False
        if step.require_reversible and not capability.reversible:
            return False
        if step.max_freshness_s is not None:
            if capability.freshness_s is None or capability.freshness_s > step.max_freshness_s:
                return False
        return True

    def route(self, steps: Sequence[MissionStep]) -> List[Dict[str, object]]:
        seen: set[str] = set()
        result: List[Dict[str, object]] = []
        for step in steps:
            if step.step_id in seen:
                raise RoutingError(f"duplicate step: {step.step_id}")
            seen.add(step.step_id)
            eligible = [item for item in self.capabilities if self._eligible(item, step)]
            if not eligible:
                result.append({"step_id": step.step_id, "status": "BLOCKED", "tool_id": None})
                continue
            best = min(eligible, key=lambda item: (item.latency_ms, -item.trust, item.tool_id))
            result.append({
                "step_id": step.step_id,
                "status": "ROUTED",
                "tool_id": best.tool_id,
                "latency_ms": best.latency_ms,
                "trust": best.trust,
            })
        return result


# ---------------------------------------------------------------------------
# 4) DPC — Decision Patch Compressor
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class DecisionSnapshot:
    facts: Mapping[str, str] = field(default_factory=dict)
    recommendations: tuple[str, ...] = ()
    blockers: tuple[str, ...] = ()
    actions: tuple[str, ...] = ()


class DecisionPatchCompressor:
    @staticmethod
    def _sequence_delta(before: Sequence[str], after: Sequence[str]) -> Dict[str, List[str]]:
        old, new = set(before), set(after)
        return {"added": sorted(new - old), "removed": sorted(old - new)}

    def diff(self, before: DecisionSnapshot, after: DecisionSnapshot) -> Dict[str, object]:
        fact_changes: List[Dict[str, str | None]] = []
        for key in sorted(set(before.facts) | set(after.facts)):
            old = before.facts.get(key)
            new = after.facts.get(key)
            if old != new:
                fact_changes.append({"key": key, "before": old, "after": new})
        return {
            "fact_changes": fact_changes,
            "recommendation_delta": self._sequence_delta(before.recommendations, after.recommendations),
            "blocker_delta": self._sequence_delta(before.blockers, after.blockers),
            "action_delta": self._sequence_delta(before.actions, after.actions),
        }

    def decision_relevant(self, patch: Mapping[str, object]) -> bool:
        if patch.get("fact_changes"):
            return True
        for key in ("recommendation_delta", "blocker_delta", "action_delta"):
            delta = patch.get(key, {})
            if isinstance(delta, Mapping) and (delta.get("added") or delta.get("removed")):
                return True
        return False

    def render_lines(self, patch: Mapping[str, object]) -> List[str]:
        if not self.decision_relevant(patch):
            return ["NO_DECISION_CHANGE"]
        lines: List[str] = []
        for item in patch["fact_changes"]:  # type: ignore[index]
            lines.append(f"FACT {item['key']}: {item['before']} -> {item['after']}")
        labels = {
            "recommendation_delta": "RECOMMENDATION",
            "blocker_delta": "BLOCKER",
            "action_delta": "ACTION",
        }
        for key, label in labels.items():
            delta = patch[key]  # type: ignore[index]
            for value in delta["removed"]:
                lines.append(f"{label} REMOVED: {value}")
            for value in delta["added"]:
                lines.append(f"{label} ADDED: {value}")
        return lines


# ---------------------------------------------------------------------------
# 5) RSE — Resilience Scenario Engine
# ---------------------------------------------------------------------------

class ResilienceError(ValueError):
    pass


@dataclass(frozen=True)
class FailureScenario:
    scenario_id: str
    unavailable_tools: frozenset[str] = frozenset()
    revoked_permissions: frozenset[str] = frozenset()
    stale_sources: frozenset[str] = frozenset()
    schema_breaks: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if not self.scenario_id:
            raise ResilienceError("scenario_id is required")


@dataclass(frozen=True)
class Plan:
    plan_id: str
    required_tools: frozenset[str] = frozenset()
    required_permissions: frozenset[str] = frozenset()
    required_fresh_sources: frozenset[str] = frozenset()
    schema_dependencies: frozenset[str] = frozenset()
    fallbacks: Mapping[str, str] | None = None

    def __post_init__(self) -> None:
        if not self.plan_id:
            raise ResilienceError("plan_id is required")


class ResilienceEngine:
    def evaluate(self, plan: Plan, scenario: FailureScenario) -> Dict[str, object]:
        fallbacks = dict(plan.fallbacks or {})
        failures: List[str] = []
        recovered: List[str] = []

        categories = (
            ("tool", plan.required_tools & scenario.unavailable_tools),
            ("permission", plan.required_permissions & scenario.revoked_permissions),
            ("freshness", plan.required_fresh_sources & scenario.stale_sources),
            ("schema", plan.schema_dependencies & scenario.schema_breaks),
        )
        for category, items in categories:
            for item in sorted(items):
                key = f"{category}:{item}"
                if key in fallbacks:
                    recovered.append(f"{key}->{fallbacks[key]}")
                else:
                    failures.append(key)

        return {
            "plan_id": plan.plan_id,
            "scenario_id": scenario.scenario_id,
            "status": "SURVIVES" if not failures else "FAILS",
            "failures": failures,
            "recovered": recovered,
        }

    def matrix(self, plan: Plan, scenarios: Sequence[FailureScenario]) -> Dict[str, object]:
        if len({item.scenario_id for item in scenarios}) != len(scenarios):
            raise ResilienceError("duplicate scenario ids")
        results = [self.evaluate(plan, item) for item in scenarios]
        survived = sum(1 for row in results if row["status"] == "SURVIVES")
        return {
            "plan_id": plan.plan_id,
            "survived": survived,
            "total": len(results),
            "survival_ratio": 1.0 if not results else survived / len(results),
            "results": results,
        }
