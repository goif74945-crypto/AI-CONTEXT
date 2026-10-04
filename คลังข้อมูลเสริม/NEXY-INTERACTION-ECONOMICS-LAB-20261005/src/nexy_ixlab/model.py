from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable, Mapping


class ValidationError(ValueError):
    """Raised when an interaction contract is malformed."""


class StepKind(str, Enum):
    AUTOMATIC = "automatic"
    INFORMATION = "information"
    CLARIFICATION = "clarification"
    CONFIRMATION = "confirmation"
    SELECTION = "selection"
    WAIT = "wait"
    IRREVERSIBLE_ACTION = "irreversible_action"
    FREEZE = "freeze"


USER_TOUCH_KINDS = {
    StepKind.CLARIFICATION,
    StepKind.CONFIRMATION,
    StepKind.SELECTION,
}


def _as_non_negative_int(value: Any, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValidationError(f"{field_name} must be a non-negative integer")
    return value


def _as_bool(value: Any, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValidationError(f"{field_name} must be a boolean")
    return value


def _as_effort(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValidationError("user_effort must be numeric")
    value = float(value)
    if not 0.0 <= value <= 5.0:
        raise ValidationError("user_effort must be in [0, 5]")
    return value


@dataclass(frozen=True, slots=True)
class InteractionStep:
    id: str
    kind: StepKind
    blocking: bool = False
    required: bool = True
    choice_count: int = 0
    estimated_wait_ms: int = 0
    context_switches: int = 0
    user_effort: float = 0.0
    reversible: bool = True
    preauthorized: bool = False
    required_by_law: bool = False
    guards_step_id: str | None = None
    justification: str = ""
    dependencies: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "InteractionStep":
        try:
            step_id = str(raw["id"]).strip()
            kind = StepKind(str(raw["kind"]))
        except KeyError as exc:
            raise ValidationError(f"missing required step field: {exc.args[0]}") from exc
        except ValueError as exc:
            raise ValidationError(f"unknown step kind: {raw.get('kind')!r}") from exc
        if not step_id:
            raise ValidationError("step id must not be empty")
        deps_raw = raw.get("dependencies", ())
        if not isinstance(deps_raw, (list, tuple)) or not all(isinstance(x, str) and x for x in deps_raw):
            raise ValidationError("dependencies must be a list of non-empty strings")
        choice_count = _as_non_negative_int(raw.get("choice_count", 0), "choice_count")
        if kind is StepKind.SELECTION and choice_count < 2:
            raise ValidationError("selection steps require choice_count >= 2")
        if kind is not StepKind.SELECTION and choice_count == 1:
            raise ValidationError("choice_count=1 is semantically invalid; use 0 or >=2")
        return cls(
            id=step_id,
            kind=kind,
            blocking=_as_bool(raw.get("blocking", False), "blocking"),
            required=_as_bool(raw.get("required", True), "required"),
            choice_count=choice_count,
            estimated_wait_ms=_as_non_negative_int(raw.get("estimated_wait_ms", 0), "estimated_wait_ms"),
            context_switches=_as_non_negative_int(raw.get("context_switches", 0), "context_switches"),
            user_effort=_as_effort(raw.get("user_effort", 0.0)),
            reversible=_as_bool(raw.get("reversible", True), "reversible"),
            preauthorized=_as_bool(raw.get("preauthorized", False), "preauthorized"),
            required_by_law=_as_bool(raw.get("required_by_law", False), "required_by_law"),
            guards_step_id=str(raw["guards_step_id"]) if raw.get("guards_step_id") is not None else None,
            justification=str(raw.get("justification", "")).strip(),
            dependencies=tuple(deps_raw),
        )

    def to_mapping(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind.value,
            "blocking": self.blocking,
            "required": self.required,
            "choice_count": self.choice_count,
            "estimated_wait_ms": self.estimated_wait_ms,
            "context_switches": self.context_switches,
            "user_effort": self.user_effort,
            "reversible": self.reversible,
            "preauthorized": self.preauthorized,
            "required_by_law": self.required_by_law,
            "guards_step_id": self.guards_step_id,
            "justification": self.justification,
            "dependencies": list(self.dependencies),
        }


@dataclass(frozen=True, slots=True)
class InteractionBudget:
    max_friction_score: float = 35.0
    max_blocking_touches: int = 2
    max_choice_bits: float = 4.0
    max_context_switches: int = 2
    max_wait_ms: int = 5_000

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any] | None) -> "InteractionBudget":
        if raw is None:
            return cls()
        values = dict(raw)
        try:
            score = float(values.get("max_friction_score", 35.0))
        except (TypeError, ValueError) as exc:
            raise ValidationError("max_friction_score must be numeric") from exc
        if not 0 <= score <= 100:
            raise ValidationError("max_friction_score must be in [0, 100]")
        try:
            choice_bits = float(values.get("max_choice_bits", 4.0))
        except (TypeError, ValueError) as exc:
            raise ValidationError("max_choice_bits must be numeric") from exc
        if choice_bits < 0:
            raise ValidationError("max_choice_bits must be non-negative")
        return cls(
            max_friction_score=score,
            max_blocking_touches=_as_non_negative_int(values.get("max_blocking_touches", 2), "max_blocking_touches"),
            max_choice_bits=choice_bits,
            max_context_switches=_as_non_negative_int(values.get("max_context_switches", 2), "max_context_switches"),
            max_wait_ms=_as_non_negative_int(values.get("max_wait_ms", 5_000), "max_wait_ms"),
        )


@dataclass(frozen=True, slots=True)
class InteractionPlan:
    name: str
    steps: tuple[InteractionStep, ...]
    budget: InteractionBudget = field(default_factory=InteractionBudget)

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "InteractionPlan":
        name = str(raw.get("name", "unnamed-plan")).strip() or "unnamed-plan"
        steps_raw = raw.get("steps")
        if not isinstance(steps_raw, list):
            raise ValidationError("steps must be a list")
        steps = tuple(InteractionStep.from_mapping(x) for x in steps_raw)
        _validate_step_graph(steps)
        return cls(name=name, steps=steps, budget=InteractionBudget.from_mapping(raw.get("budget")))

    def to_mapping(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "budget": {
                "max_friction_score": self.budget.max_friction_score,
                "max_blocking_touches": self.budget.max_blocking_touches,
                "max_choice_bits": self.budget.max_choice_bits,
                "max_context_switches": self.budget.max_context_switches,
                "max_wait_ms": self.budget.max_wait_ms,
            },
            "steps": [s.to_mapping() for s in self.steps],
        }


def _validate_step_graph(steps: Iterable[InteractionStep]) -> None:
    steps = tuple(steps)
    ids = [s.id for s in steps]
    if len(ids) != len(set(ids)):
        raise ValidationError("step ids must be unique")
    known = set(ids)
    graph: dict[str, tuple[str, ...]] = {}
    for step in steps:
        unknown_deps = set(step.dependencies) - known
        if unknown_deps:
            raise ValidationError(f"step {step.id!r} has unknown dependencies: {sorted(unknown_deps)}")
        if step.id in step.dependencies:
            raise ValidationError(f"step {step.id!r} cannot depend on itself")
        if len(step.dependencies) != len(set(step.dependencies)):
            raise ValidationError(f"step {step.id!r} dependencies must be unique")
        if step.guards_step_id == step.id:
            raise ValidationError(f"step {step.id!r} cannot guard itself")
        graph[step.id] = step.dependencies

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visited:
            return
        if node in visiting:
            raise ValidationError(f"dependency cycle detected at step {node!r}")
        visiting.add(node)
        for dep in graph[node]:
            visit(dep)
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)
