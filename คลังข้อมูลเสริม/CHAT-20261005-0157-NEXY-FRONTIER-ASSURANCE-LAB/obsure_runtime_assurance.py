"""Runtime witness certification extension for experimental OBSURE.

AI-PROPOSED / EXPERIMENTAL / NOT CANON / NOT NEXY.AI IMPLEMENTATION.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from frontier_assurance_lab import (
    EffectSpec,
    FreezeError,
    ObservabilityGate,
    TelemetryEventSpec,
    stable_hash,
)

_TERMINALS = frozenset({"SUCCESS", "FAILURE"})
_COMPENSATION = ("COMPENSATION_START", "COMPENSATION_RESULT")


@dataclass(frozen=True)
class RuntimeEvent:
    """One observed event with caller-supplied logical sequence."""

    name: str
    effect_id: str
    sequence: int
    fields: Mapping[str, Any]

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.effect_id.strip():
            raise FreezeError("runtime event name/effect_id must be non-empty")
        if isinstance(self.sequence, bool) or not isinstance(self.sequence, int):
            raise FreezeError("runtime event sequence must be an integer")
        if self.sequence < 0:
            raise FreezeError("runtime event sequence must be non-negative")
        if not isinstance(self.fields, Mapping):
            raise FreezeError("runtime event fields must be a mapping")


@dataclass(frozen=True)
class EffectRunExpectation:
    """Declared outcome contract for one completed effect run."""

    effect_id: str
    terminal: str
    require_compensation: bool = False

    def __post_init__(self) -> None:
        if not self.effect_id.strip() or self.terminal not in _TERMINALS:
            raise FreezeError("invalid effect run expectation")
        if not isinstance(self.require_compensation, bool):
            raise FreezeError("require_compensation must be boolean")
        if self.require_compensation and self.terminal != "FAILURE":
            raise FreezeError("compensation is legal only for FAILURE")


class RuntimeWitnessCertifier:
    """Fail-closed conformance check for completed side-effect witnesses."""

    @staticmethod
    def _issue(effect_id: str, code: str, **details: Any) -> dict[str, Any]:
        return {"effect_id": effect_id, "code": code, **details}

    def certify(
        self,
        effects: Iterable[EffectSpec],
        schemas: Iterable[TelemetryEventSpec],
        expectations: Iterable[EffectRunExpectation],
        events: Iterable[RuntimeEvent],
    ) -> dict[str, Any]:
        effect_items = tuple(sorted(effects, key=lambda item: item.effect_id))
        schema_items = tuple(sorted(schemas, key=lambda item: item.name))
        expectation_items = tuple(
            sorted(expectations, key=lambda item: item.effect_id)
        )
        event_items = tuple(
            sorted(events, key=lambda item: (item.sequence, item.effect_id, item.name))
        )

        if not effect_items or not expectation_items or not event_items:
            raise FreezeError("effects, expectations, and runtime events are required")
        if len({item.effect_id for item in effect_items}) != len(effect_items):
            raise FreezeError("effect ids must be unique")
        if len({item.name for item in schema_items}) != len(schema_items):
            raise FreezeError("telemetry schema names must be unique")
        if len({item.effect_id for item in expectation_items}) != len(
            expectation_items
        ):
            raise FreezeError("expectation effect ids must be unique")

        effect_by_id = {item.effect_id: item for item in effect_items}
        schema_by_name = {item.name: item for item in schema_items}
        expected_by_id = {item.effect_id: item for item in expectation_items}

        if set(expected_by_id) != set(effect_by_id):
            raise FreezeError("expectations must cover exactly all effects")

        issues: list[dict[str, Any]] = []
        seen_sequences: set[tuple[str, str, int]] = set()
        event_rows: dict[str, list[tuple[RuntimeEvent, TelemetryEventSpec]]] = {
            effect_id: [] for effect_id in effect_by_id
        }

        for event in event_items:
            schema = schema_by_name.get(event.name)
            if event.effect_id not in effect_by_id:
                issues.append(
                    self._issue(event.effect_id, "UNKNOWN_EFFECT", event=event.name)
                )
                continue
            if schema is None or schema.effect_id != event.effect_id:
                issues.append(
                    self._issue(event.effect_id, "UNADMITTED_EVENT", event=event.name)
                )
                continue

            missing = sorted(
                field
                for field in schema.fields
                if field not in event.fields
                or event.fields[field] is None
                or (isinstance(event.fields[field], str) and not event.fields[field].strip())
            )
            if missing:
                issues.append(
                    self._issue(
                        event.effect_id,
                        "MISSING_FIELD_VALUES",
                        event=event.name,
                        fields=missing,
                    )
                )

            actual_effect = event.fields.get("effect_id")
            if actual_effect != event.effect_id:
                issues.append(
                    self._issue(
                        event.effect_id,
                        "EFFECT_CORRELATION_MISMATCH",
                        event=event.name,
                    )
                )

            trace = event.fields.get("trace_id")
            action = event.fields.get("action_id")
            sequence_key = (str(trace), str(action), event.sequence)
            if sequence_key in seen_sequences:
                issues.append(
                    self._issue(
                        event.effect_id,
                        "DUPLICATE_SEQUENCE",
                        sequence=event.sequence,
                    )
                )
            seen_sequences.add(sequence_key)
            event_rows[event.effect_id].append((event, schema))

        for effect_id, effect in sorted(effect_by_id.items()):
            rows = event_rows[effect_id]
            expectation = expected_by_id[effect_id]
            phases = [schema.phase for _, schema in rows]
            phase_counts = {phase: phases.count(phase) for phase in sorted(set(phases))}

            correlations = {
                (
                    event.fields.get("trace_id"),
                    event.fields.get("action_id"),
                    event.fields.get("effect_id"),
                )
                for event, _ in rows
            }
            if len(correlations) != 1:
                issues.append(self._issue(effect_id, "CORRELATION_DRIFT"))

            required = ["INTENT", "START", expectation.terminal]
            if expectation.require_compensation:
                if not effect.reversible:
                    issues.append(
                        self._issue(effect_id, "COMPENSATION_FOR_IRREVERSIBLE_EFFECT")
                    )
                required.extend(_COMPENSATION)

            allowed = set(required)
            for phase in sorted(allowed):
                if phase_counts.get(phase, 0) != 1:
                    issues.append(
                        self._issue(
                            effect_id,
                            "PHASE_CARDINALITY",
                            phase=phase,
                            observed=phase_counts.get(phase, 0),
                            expected=1,
                        )
                    )

            forbidden_terminal = "FAILURE" if expectation.terminal == "SUCCESS" else "SUCCESS"
            if phase_counts.get(forbidden_terminal, 0):
                issues.append(
                    self._issue(
                        effect_id,
                        "TERMINAL_CONTRADICTION",
                        phase=forbidden_terminal,
                    )
                )

            observed_compensation = any(phase in _COMPENSATION for phase in phases)
            if observed_compensation and not expectation.require_compensation:
                issues.append(self._issue(effect_id, "UNEXPECTED_COMPENSATION"))

            extra_phases = sorted(set(phases) - allowed - {forbidden_terminal})
            for phase in extra_phases:
                issues.append(
                    self._issue(effect_id, "UNEXPECTED_PHASE", phase=phase)
                )

            ordered_phases = [schema.phase for _, schema in rows]
            required_positions: list[int] = []
            complete_order = True
            for phase in required:
                positions = [i for i, observed in enumerate(ordered_phases) if observed == phase]
                if len(positions) != 1:
                    complete_order = False
                    break
                required_positions.append(positions[0])
            if complete_order and required_positions != sorted(required_positions):
                issues.append(self._issue(effect_id, "LIFECYCLE_ORDER_VIOLATION"))

        issues = sorted(
            issues,
            key=lambda item: (
                item["effect_id"],
                item["code"],
                str(item.get("phase", "")),
                str(item.get("event", "")),
                str(item.get("sequence", "")),
            ),
        )
        result: dict[str, Any] = {
            "status": "CERTIFIED" if not issues else "FREEZE",
            "issues": issues,
        }
        result["result_hash"] = stable_hash(result)
        return result


class ObsureRuntimeAssurance:
    """Composition adapter: specification sufficiency, then runtime witness."""

    def __init__(self) -> None:
        self.specification_gate = ObservabilityGate()
        self.runtime_certifier = RuntimeWitnessCertifier()

    def assess(
        self,
        effects: Iterable[EffectSpec],
        schemas: Iterable[TelemetryEventSpec],
        expectations: Iterable[EffectRunExpectation],
        events: Iterable[RuntimeEvent],
    ) -> dict[str, Any]:
        effect_items = tuple(effects)
        schema_items = tuple(schemas)
        expectation_items = tuple(expectations)
        event_items = tuple(events)

        specification = self.specification_gate.evaluate(effect_items, schema_items)
        if specification["status"] != "PASS":
            result: dict[str, Any] = {
                "status": "FREEZE",
                "reason": "SPECIFICATION_INSUFFICIENT",
                "specification": specification,
                "runtime": None,
            }
        else:
            runtime = self.runtime_certifier.certify(
                effect_items, schema_items, expectation_items, event_items
            )
            result = {
                "status": "CERTIFIED" if runtime["status"] == "CERTIFIED" else "FREEZE",
                "reason": "RUNTIME_CERTIFIED"
                if runtime["status"] == "CERTIFIED"
                else "RUNTIME_WITNESS_INVALID",
                "specification": specification,
                "runtime": runtime,
            }
        result["result_hash"] = stable_hash(result)
        return result
