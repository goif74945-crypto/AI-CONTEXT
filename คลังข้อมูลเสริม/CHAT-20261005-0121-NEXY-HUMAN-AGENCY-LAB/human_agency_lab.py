from __future__ import annotations


# ===== models.py =====

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Any, Iterable, Tuple


class Decision(str, Enum):
    PROCEED = "PROCEED"
    PREVIEW = "PREVIEW"
    CONFIRM = "CONFIRM"
    FREEZE = "FREEZE"


class ReasonCode(str, Enum):
    LOW_RISK_REVERSIBLE = "LOW_RISK_REVERSIBLE"
    USER_AUTHORITY_MISSING = "USER_AUTHORITY_MISSING"
    IRREVERSIBLE_WITHOUT_ROLLBACK = "IRREVERSIBLE_WITHOUT_ROLLBACK"
    DESTRUCTIVE_ACTION = "DESTRUCTIVE_ACTION"
    SENSITIVE_EXTERNAL_EFFECT = "SENSITIVE_EXTERNAL_EFFECT"
    MATERIAL_COST = "MATERIAL_COST"
    BROAD_SCOPE = "BROAD_SCOPE"
    HIGH_AMBIGUITY = "HIGH_AMBIGUITY"
    MODERATE_AMBIGUITY = "MODERATE_AMBIGUITY"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"
    PREVIEW_RECOMMENDED = "PREVIEW_RECOMMENDED"
    REQUIRED_CONFIRMATION = "REQUIRED_CONFIRMATION"
    ATTENTION_BUDGET_CONSTRAINED = "ATTENTION_BUDGET_CONSTRAINED"


def _unit_interval(name: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be within [0, 1], got {value!r}")


@dataclass(frozen=True)
class RequestProfile:
    action_id: str
    ambiguity: float = 0.0
    reversibility: float = 1.0
    confidence: float = 1.0
    scope_breadth: float = 0.0
    data_sensitivity: float = 0.0
    monetary_cost: float = 0.0
    external_side_effect: bool = False
    destructive: bool = False
    rollback_available: bool = True
    explicit_user_authority: bool = True
    crosses_auth_boundary: bool = False
    user_attention_cost: int = 1

    def __post_init__(self) -> None:
        if not self.action_id.strip():
            raise ValueError("action_id must be non-empty")
        for name in (
            "ambiguity",
            "reversibility",
            "confidence",
            "scope_breadth",
            "data_sensitivity",
            "monetary_cost",
        ):
            _unit_interval(name, float(getattr(self, name)))
        if self.user_attention_cost < 0:
            raise ValueError("user_attention_cost must be >= 0")

    def canonical_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InteractionDecision:
    decision: Decision
    reasons: Tuple[ReasonCode, ...]
    attention_cost: int
    hard_gate: bool
    action_id: str

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "action_id": self.action_id,
            "attention_cost": self.attention_cost,
            "decision": self.decision.value,
            "hard_gate": self.hard_gate,
            "reasons": [reason.value for reason in self.reasons],
        }

    def digest(self) -> str:
        payload = json.dumps(
            self.canonical_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        return sha256(payload).hexdigest()


def stable_reasons(reasons: Iterable[ReasonCode]) -> Tuple[ReasonCode, ...]:
    unique = {reason.value: reason for reason in reasons}
    return tuple(unique[key] for key in sorted(unique))

# ===== policy.py =====

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class AgencyPolicy:
    freeze_ambiguity: float = 0.90
    confirm_ambiguity: float = 0.60
    preview_ambiguity: float = 0.30
    low_reversibility: float = 0.30
    broad_scope: float = 0.70
    sensitive_data: float = 0.65
    material_cost: float = 0.50
    low_confidence: float = 0.65
    high_impact_scope: float = 0.60
    confirm_attention_cost: int = 3
    preview_attention_cost: int = 1

    def __post_init__(self) -> None:
        bounded = (
            "freeze_ambiguity",
            "confirm_ambiguity",
            "preview_ambiguity",
            "low_reversibility",
            "broad_scope",
            "sensitive_data",
            "material_cost",
            "low_confidence",
            "high_impact_scope",
        )
        for name in bounded:
            value = float(getattr(self, name))
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be within [0, 1]")
        if not self.preview_ambiguity <= self.confirm_ambiguity <= self.freeze_ambiguity:
            raise ValueError(
                "ambiguity thresholds must satisfy preview <= confirm <= freeze"
            )
        if self.confirm_attention_cost < 0 or self.preview_attention_cost < 0:
            raise ValueError("attention costs must be non-negative")

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "AgencyPolicy":
        unknown = set(raw) - set(cls.__dataclass_fields__)
        if unknown:
            raise ValueError(f"unknown policy keys: {sorted(unknown)}")
        return cls(**dict(raw))

    @classmethod
    def from_json(cls, text: str) -> "AgencyPolicy":
        raw = json.loads(text)
        if not isinstance(raw, dict):
            raise ValueError("policy JSON must be an object")
        return cls.from_mapping(raw)

    @classmethod
    def from_file(cls, path: str | Path) -> "AgencyPolicy":
        return cls.from_json(Path(path).read_text(encoding="utf-8"))

# ===== engine.py =====



class AgencyDecisionEngine:
    """Deterministic interaction-gating engine.

    The engine decides the minimum user interruption compatible with preserving
    explicit user authority and a bounded rollback/recovery posture.
    """

    def __init__(self, policy: AgencyPolicy | None = None) -> None:
        self.policy = policy or AgencyPolicy()

    def evaluate(self, request: RequestProfile) -> InteractionDecision:
        p = self.policy
        reasons: list[ReasonCode] = []

        high_impact = (
            request.destructive
            or request.crosses_auth_boundary
            or request.scope_breadth >= p.high_impact_scope
            or request.monetary_cost >= p.material_cost
            or request.data_sensitivity >= p.sensitive_data
        )

        # Hard freeze gates. These cannot be downgraded by attention budgeting.
        if high_impact and not request.explicit_user_authority:
            return self._result(
                request,
                Decision.FREEZE,
                [ReasonCode.USER_AUTHORITY_MISSING],
                hard_gate=True,
            )

        if request.destructive and (
            not request.rollback_available or request.reversibility <= p.low_reversibility
        ):
            return self._result(
                request,
                Decision.FREEZE,
                [ReasonCode.IRREVERSIBLE_WITHOUT_ROLLBACK, ReasonCode.DESTRUCTIVE_ACTION],
                hard_gate=True,
            )

        if (
            request.ambiguity >= p.freeze_ambiguity
            and request.external_side_effect
            and request.reversibility <= p.low_reversibility
        ):
            return self._result(
                request,
                Decision.FREEZE,
                [ReasonCode.HIGH_AMBIGUITY, ReasonCode.IRREVERSIBLE_WITHOUT_ROLLBACK],
                hard_gate=True,
            )

        # Mandatory confirmation gates.
        if request.destructive:
            reasons.extend([ReasonCode.DESTRUCTIVE_ACTION, ReasonCode.REQUIRED_CONFIRMATION])
            return self._result(request, Decision.CONFIRM, reasons, hard_gate=True)

        if request.crosses_auth_boundary:
            reasons.append(ReasonCode.REQUIRED_CONFIRMATION)
            return self._result(request, Decision.CONFIRM, reasons, hard_gate=True)

        if request.external_side_effect and request.data_sensitivity >= p.sensitive_data:
            reasons.extend(
                [ReasonCode.SENSITIVE_EXTERNAL_EFFECT, ReasonCode.REQUIRED_CONFIRMATION]
            )
            return self._result(request, Decision.CONFIRM, reasons, hard_gate=True)

        if request.external_side_effect and request.monetary_cost >= p.material_cost:
            reasons.extend([ReasonCode.MATERIAL_COST, ReasonCode.REQUIRED_CONFIRMATION])
            return self._result(request, Decision.CONFIRM, reasons, hard_gate=True)

        if (
            request.external_side_effect
            and request.ambiguity >= p.confirm_ambiguity
        ):
            reasons.extend([ReasonCode.HIGH_AMBIGUITY, ReasonCode.REQUIRED_CONFIRMATION])
            return self._result(request, Decision.CONFIRM, reasons, hard_gate=True)

        # Soft preview gates. These preserve momentum while surfacing material uncertainty.
        if request.scope_breadth >= p.broad_scope:
            reasons.append(ReasonCode.BROAD_SCOPE)
        if request.ambiguity >= p.preview_ambiguity:
            reasons.append(ReasonCode.MODERATE_AMBIGUITY)
        if request.confidence <= p.low_confidence:
            reasons.append(ReasonCode.LOW_CONFIDENCE)
        if request.external_side_effect and request.reversibility <= p.low_reversibility:
            reasons.append(ReasonCode.PREVIEW_RECOMMENDED)

        if reasons:
            return self._result(request, Decision.PREVIEW, reasons, hard_gate=False)

        return self._result(
            request,
            Decision.PROCEED,
            [ReasonCode.LOW_RISK_REVERSIBLE],
            hard_gate=False,
        )

    def _result(
        self,
        request: RequestProfile,
        decision: Decision,
        reasons: list[ReasonCode],
        *,
        hard_gate: bool,
    ) -> InteractionDecision:
        if decision is Decision.CONFIRM:
            attention_cost = max(request.user_attention_cost, self.policy.confirm_attention_cost)
        elif decision is Decision.PREVIEW:
            attention_cost = max(request.user_attention_cost, self.policy.preview_attention_cost)
        else:
            attention_cost = request.user_attention_cost if decision is Decision.FREEZE else 0

        return InteractionDecision(
            decision=decision,
            reasons=stable_reasons(reasons),
            attention_cost=attention_cost,
            hard_gate=hard_gate,
            action_id=request.action_id,
        )

# ===== budget.py =====

from dataclasses import dataclass
from typing import Iterable



@dataclass
class AttentionBudget:
    capacity: int
    consumed: int = 0

    def __post_init__(self) -> None:
        if self.capacity < 0 or self.consumed < 0:
            raise ValueError("attention budget values must be non-negative")
        if self.consumed > self.capacity:
            raise ValueError("consumed attention cannot exceed capacity")

    @property
    def remaining(self) -> int:
        return self.capacity - self.consumed

    def reserve(self, amount: int) -> bool:
        if amount < 0:
            raise ValueError("amount must be non-negative")
        if amount > self.remaining:
            return False
        self.consumed += amount
        return True


def apply_attention_budget(
    decision: InteractionDecision, budget: AttentionBudget
) -> InteractionDecision:
    """Applies attention economics without weakening a hard gate.

    Hard CONFIRM/FREEZE decisions stay intact even when the user attention budget
    is exhausted. A soft PREVIEW can become a no-interruption PROCEED only when
    the budget is exhausted, while preserving an explicit reason code in the
    machine record. This makes the optimization visible and testable.
    """
    if decision.decision in (Decision.FREEZE, Decision.CONFIRM) or decision.hard_gate:
        budget.reserve(min(decision.attention_cost, budget.remaining))
        return decision

    if decision.decision is Decision.PREVIEW:
        if budget.reserve(decision.attention_cost):
            return decision
        return InteractionDecision(
            decision=Decision.PROCEED,
            reasons=stable_reasons(
                (*decision.reasons, ReasonCode.ATTENTION_BUDGET_CONSTRAINED)
            ),
            attention_cost=0,
            hard_gate=False,
            action_id=decision.action_id,
        )

    return decision


def batch_interruptions(
    decisions: Iterable[InteractionDecision],
) -> list[InteractionDecision]:
    """Return only interactions that should surface to a human, stable-sorted."""
    visible = [
        d for d in decisions if d.decision in (Decision.PREVIEW, Decision.CONFIRM, Decision.FREEZE)
    ]
    return sorted(visible, key=lambda d: (d.decision.value, d.action_id))

# ===== recovery.py =====

from dataclasses import dataclass
from enum import Enum
from typing import Iterable



class RecoveryLevel(str, Enum):
    NONE_REQUIRED = "NONE_REQUIRED"
    CHECKPOINT = "CHECKPOINT"
    ROLLBACK_REQUIRED = "ROLLBACK_REQUIRED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class RecoveryPlan:
    action_id: str
    level: RecoveryLevel
    required_steps: tuple[str, ...]


def plan_recovery(request: RequestProfile) -> RecoveryPlan:
    if request.destructive and not request.rollback_available:
        return RecoveryPlan(
            request.action_id,
            RecoveryLevel.BLOCKED,
            ("obtain-or-design-rollback", "re-evaluate-action"),
        )

    if request.destructive or request.reversibility <= 0.30:
        return RecoveryPlan(
            request.action_id,
            RecoveryLevel.ROLLBACK_REQUIRED,
            ("capture-pre-state", "define-rollback", "verify-post-state"),
        )

    if request.external_side_effect or request.scope_breadth >= 0.70:
        return RecoveryPlan(
            request.action_id,
            RecoveryLevel.CHECKPOINT,
            ("capture-pre-state", "verify-post-state"),
        )

    return RecoveryPlan(request.action_id, RecoveryLevel.NONE_REQUIRED, tuple())


def recovery_coverage(plans: Iterable[RecoveryPlan]) -> float:
    plans = list(plans)
    if not plans:
        return 1.0
    covered = sum(plan.level is not RecoveryLevel.BLOCKED for plan in plans)
    return covered / len(plans)

# ===== metrics.py =====

from collections import Counter
from dataclasses import dataclass
from typing import Iterable



@dataclass(frozen=True)
class InteractionMetrics:
    total: int
    distribution: dict[str, int]
    human_interruptions: int
    hard_gates: int
    attention_cost: int
    autonomy_rate: float


def summarize(decisions: Iterable[InteractionDecision]) -> InteractionMetrics:
    items = list(decisions)
    total = len(items)
    counts = Counter(item.decision.value for item in items)
    interruptions = sum(
        item.decision in (Decision.PREVIEW, Decision.CONFIRM, Decision.FREEZE)
        for item in items
    )
    hard_gates = sum(item.hard_gate for item in items)
    attention_cost = sum(item.attention_cost for item in items)
    autonomous = sum(item.decision is Decision.PROCEED for item in items)
    return InteractionMetrics(
        total=total,
        distribution=dict(sorted(counts.items())),
        human_interruptions=interruptions,
        hard_gates=hard_gates,
        attention_cost=attention_cost,
        autonomy_rate=(autonomous / total) if total else 1.0,
    )

# ===== simulator.py =====

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Iterable



@dataclass(frozen=True)
class ScenarioResult:
    name: str
    expected: Decision
    observed: InteractionDecision

    @property
    def passed(self) -> bool:
        return self.expected is self.observed.decision


def load_scenarios(path: str | Path) -> list[dict[str, Any]]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("scenario file must contain a JSON array")
    return raw


def run_scenarios(
    scenarios: Iterable[dict[str, Any]], engine: AgencyDecisionEngine | None = None
) -> list[ScenarioResult]:
    engine = engine or AgencyDecisionEngine()
    out: list[ScenarioResult] = []
    for raw in scenarios:
        name = str(raw["name"])
        expected = Decision(str(raw["expected"]))
        request = RequestProfile(**dict(raw["request"]))
        out.append(ScenarioResult(name, expected, engine.evaluate(request)))
    return out

# ===== explain.py =====



_PREFIX = {
    Decision.PROCEED: "ดำเนินการได้โดยไม่ต้องขัดจังหวะผู้ใช้",
    Decision.PREVIEW: "ควรแสดงตัวอย่างก่อนดำเนินการ",
    Decision.CONFIRM: "ต้องขอการยืนยันจากผู้ใช้",
    Decision.FREEZE: "หยุดการดำเนินการจนกว่าจะมีเงื่อนไขที่ปลอดภัยและชัดเจน",
}


def human_summary(decision: InteractionDecision) -> str:
    reasons = ", ".join(reason.value for reason in decision.reasons)
    return f"{_PREFIX[decision.decision]} | action={decision.action_id} | reasons={reasons}"

# ===== cli.py =====

import argparse
import json
from pathlib import Path
import sys



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NEXY Human Agency Lab prototype")
    sub = parser.add_subparsers(dest="command", required=True)
    sim = sub.add_parser("simulate", help="run scenario corpus")
    sim.add_argument("scenario_file", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "simulate":
        results = run_scenarios(load_scenarios(args.scenario_file), AgencyDecisionEngine())
        decisions = [result.observed for result in results]
        payload = {
            "passed": sum(result.passed for result in results),
            "failed": sum(not result.passed for result in results),
            "total": len(results),
            "metrics": summarize(decisions).__dict__,
            "results": [
                {
                    "name": result.name,
                    "expected": result.expected.value,
                    "observed": result.observed.canonical_dict(),
                    "digest": result.observed.digest(),
                    "passed": result.passed,
                }
                for result in results
            ],
        }
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))
        return 0 if payload["failed"] == 0 else 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
