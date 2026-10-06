"""Cross-effect trace cohesion extension for experimental OBSURE.

AI-PROPOSED / EXPERIMENTAL / NOT CANON / NOT NEXY.AI IMPLEMENTATION.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from frontier_assurance_lab import (
    EffectSpec,
    FreezeError,
    TelemetryEventSpec,
    stable_hash,
)
from obsure_runtime_assurance import (
    EffectRunExpectation,
    ObsureRuntimeAssurance,
    RuntimeEvent,
)


@dataclass(frozen=True)
class TraceCohesionContract:
    """Expected shared run identity and dependency DAG for all effects."""

    trace_id: str
    action_id: str
    dependencies: Mapping[str, tuple[str, ...]]

    def __post_init__(self) -> None:
        if not isinstance(self.trace_id, str) or not self.trace_id.strip():
            raise FreezeError("trace_id must be a non-empty string")
        if not isinstance(self.action_id, str) or not self.action_id.strip():
            raise FreezeError("action_id must be a non-empty string")
        if type(self.dependencies) is not dict or not self.dependencies:
            raise FreezeError("trace dependencies must be a non-empty built-in dict")
        if any(not isinstance(effect_id, str) or not effect_id.strip() for effect_id in self.dependencies):
            raise FreezeError("trace dependency effect ids must be non-empty strings")

        effect_ids = set(self.dependencies)
        for effect_id, parents in self.dependencies.items():
            if not isinstance(parents, tuple):
                raise FreezeError(f"dependencies for {effect_id!r} must be a tuple")
            if any(not isinstance(parent, str) or not parent.strip() for parent in parents):
                raise FreezeError(f"dependencies for {effect_id!r} contain an invalid parent")
            if len(set(parents)) != len(parents):
                raise FreezeError(f"dependencies for {effect_id!r} contain duplicate parents")
            if effect_id in parents:
                raise FreezeError("an effect cannot depend on itself")
            unknown = sorted(set(parents) - effect_ids)
            if unknown:
                raise FreezeError(f"dependencies for {effect_id!r} contain unknown parents: {unknown}")

        object.__setattr__(
            self,
            "dependencies",
            MappingProxyType(dict(self.dependencies)),
        )

        states: dict[str, int] = {effect_id: 0 for effect_id in effect_ids}

        def visit(effect_id: str) -> None:
            if states[effect_id] == 1:
                raise FreezeError("trace dependency graph must be acyclic")
            if states[effect_id] == 2:
                return
            states[effect_id] = 1
            for parent in self.dependencies[effect_id]:
                visit(parent)
            states[effect_id] = 2

        for effect_id in sorted(effect_ids):
            visit(effect_id)

    def canonical_record(self) -> dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "action_id": self.action_id,
            "dependencies": {
                effect_id: sorted(self.dependencies[effect_id])
                for effect_id in sorted(self.dependencies)
            },
        }


class ObsureTraceCohesionAssurance:
    """Require one trace/action identity and dependency order across effects."""

    def __init__(self) -> None:
        self.base = ObsureRuntimeAssurance()

    @staticmethod
    def _finite_sequence(name: str, value: object, member_type: type) -> tuple:
        if type(value) not in (list, tuple):
            raise FreezeError(f"{name} must be a finite built-in list or tuple")
        if any(not isinstance(item, member_type) for item in value):
            raise FreezeError(f"{name} contains an invalid value")
        return tuple(value)

    @staticmethod
    def _witness_record(events: tuple[RuntimeEvent, ...]) -> list[dict[str, Any]]:
        rows = []
        for event in sorted(events, key=lambda item: (item.sequence, item.effect_id, item.name)):
            rows.append(
                {
                    "name": event.name,
                    "effect_id": event.effect_id,
                    "sequence": event.sequence,
                    "fields": event.fields,
                }
            )
        try:
            stable_hash(rows)
        except (TypeError, ValueError) as error:
            raise FreezeError("runtime witness contains non-canonical values") from error
        return rows

    def assess(
        self,
        contract: TraceCohesionContract,
        effects: list[EffectSpec] | tuple[EffectSpec, ...],
        schemas: list[TelemetryEventSpec] | tuple[TelemetryEventSpec, ...],
        expectations: list[EffectRunExpectation] | tuple[EffectRunExpectation, ...],
        events: list[RuntimeEvent] | tuple[RuntimeEvent, ...],
    ) -> dict[str, Any]:
        if not isinstance(contract, TraceCohesionContract):
            raise FreezeError("invalid trace cohesion contract")
        effect_items = self._finite_sequence("effects", effects, EffectSpec)
        schema_items = self._finite_sequence("schemas", schemas, TelemetryEventSpec)
        expectation_items = self._finite_sequence(
            "expectations", expectations, EffectRunExpectation
        )
        event_items = self._finite_sequence("events", events, RuntimeEvent)

        effect_ids = [effect.effect_id for effect in effect_items]
        if len(set(effect_ids)) != len(effect_ids):
            raise FreezeError("effect ids must be unique")
        if set(effect_ids) != set(contract.dependencies):
            raise FreezeError("trace contract must cover exactly all effects")

        witness_record = self._witness_record(event_items)
        contract_hash = stable_hash(contract.canonical_record())
        witness_hash = stable_hash(witness_record)
        base = self.base.assess(
            effect_items, schema_items, expectation_items, event_items
        )
        if base["status"] != "CERTIFIED":
            result: dict[str, Any] = {
                "status": "FREEZE",
                "reason": "BASE_RUNTIME_INVALID",
                "issues": [],
                "contract_hash": contract_hash,
                "witness_hash": witness_hash,
                "base": base,
            }
            result["result_hash"] = stable_hash(result)
            return result

        schema_by_name = {schema.name: schema for schema in schema_items}
        expectation_by_effect = {
            expectation.effect_id: expectation for expectation in expectation_items
        }
        rows_by_effect: dict[str, list[tuple[RuntimeEvent, TelemetryEventSpec]]] = {
            effect_id: [] for effect_id in effect_ids
        }
        for event in event_items:
            rows_by_effect[event.effect_id].append((event, schema_by_name[event.name]))

        issues: list[dict[str, Any]] = []
        for effect_id in sorted(rows_by_effect):
            effect_events = [event for event, _ in rows_by_effect[effect_id]]
            traces = sorted({str(event.fields.get("trace_id")) for event in effect_events})
            actions = sorted({str(event.fields.get("action_id")) for event in effect_events})
            if traces != [contract.trace_id]:
                issues.append(
                    {"effect_id": effect_id, "code": "TRACE_ID_MISMATCH", "observed": traces}
                )
            if actions != [contract.action_id]:
                issues.append(
                    {"effect_id": effect_id, "code": "ACTION_ID_MISMATCH", "observed": actions}
                )

        for child in sorted(contract.dependencies):
            child_intent = next(
                event.sequence
                for event, schema in rows_by_effect[child]
                if schema.phase == "INTENT"
            )
            for parent in sorted(contract.dependencies[child]):
                parent_expectation = expectation_by_effect[parent]
                completion_phase = (
                    "COMPENSATION_RESULT"
                    if parent_expectation.require_compensation
                    else parent_expectation.terminal
                )
                parent_terminal = next(
                    event.sequence
                    for event, schema in rows_by_effect[parent]
                    if schema.phase == completion_phase
                )
                if parent_terminal >= child_intent:
                    issues.append(
                        {
                            "effect_id": child,
                            "code": "DEPENDENCY_ORDER_VIOLATION",
                            "parent": parent,
                            "parent_completion_phase": completion_phase,
                            "parent_terminal_sequence": parent_terminal,
                            "child_intent_sequence": child_intent,
                        }
                    )

        issues = sorted(
            issues,
            key=lambda issue: (
                issue["effect_id"],
                issue["code"],
                str(issue.get("parent", "")),
            ),
        )
        result = {
            "status": "CERTIFIED" if not issues else "FREEZE",
            "reason": "TRACE_COHESIVE" if not issues else "TRACE_COHESION_INVALID",
            "issues": issues,
            "contract_hash": contract_hash,
            "witness_hash": witness_hash,
            "base": base,
        }
        result["result_hash"] = stable_hash(result)
        return result
