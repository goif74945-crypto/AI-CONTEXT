from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

JSON = Any


class ModelError(ValueError):
    """Raised when the declarative verification model is invalid."""


class ExecutionModelError(RuntimeError):
    """Raised when a valid action cannot be evaluated on a reachable state."""


def canonical_json(value: JSON) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def sha256_json(value: JSON) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _is_json_scalar(value: Any) -> bool:
    return value is None or isinstance(value, (bool, int, str))


def validate_json_value(value: Any, *, where: str = "value") -> None:
    if isinstance(value, float):
        raise ModelError(f"{where}: floating-point values are forbidden; use scaled integers/fixed-point")
    if _is_json_scalar(value):
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            validate_json_value(item, where=f"{where}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise ModelError(f"{where}: object keys must be strings")
            validate_json_value(item, where=f"{where}.{key}")
        return
    raise ModelError(f"{where}: unsupported non-JSON value {type(value).__name__}")


def parse_pointer(pointer: str) -> tuple[str, ...]:
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise ModelError(f"invalid JSON pointer {pointer!r}; non-root pointers must start with '/'")
    if pointer == "/":
        return ("",)
    out: list[str] = []
    for raw in pointer[1:].split("/"):
        i = 0
        decoded = ""
        while i < len(raw):
            if raw[i] != "~":
                decoded += raw[i]
                i += 1
                continue
            if i + 1 >= len(raw) or raw[i + 1] not in "01":
                raise ModelError(f"invalid JSON pointer escape in {pointer!r}")
            decoded += "~" if raw[i + 1] == "0" else "/"
            i += 2
        out.append(decoded)
    return tuple(out)


def format_pointer(parts: Iterable[str]) -> str:
    encoded = [part.replace("~", "~0").replace("/", "~1") for part in parts]
    return "/" + "/".join(encoded)


def pointer_overlap(a: str, b: str) -> bool:
    pa = parse_pointer(a)
    pb = parse_pointer(b)
    shortest = min(len(pa), len(pb))
    return pa[:shortest] == pb[:shortest]


def _parent_for(state: dict[str, JSON], pointer: str, *, create: bool = False) -> tuple[dict[str, JSON], str]:
    parts = parse_pointer(pointer)
    if not parts:
        raise ModelError("root mutation is forbidden")
    current: dict[str, JSON] = state
    for part in parts[:-1]:
        if part not in current:
            if not create:
                raise ExecutionModelError(f"missing parent at {format_pointer(parts[:-1])}")
            current[part] = {}
        nxt = current[part]
        if not isinstance(nxt, dict):
            raise ExecutionModelError(f"non-object parent at {format_pointer(parts[:-1])}")
        current = nxt
    return current, parts[-1]


def get_path(state: Mapping[str, JSON], pointer: str) -> JSON:
    parts = parse_pointer(pointer)
    current: JSON = state
    for part in parts:
        if not isinstance(current, Mapping) or part not in current:
            raise ExecutionModelError(f"missing path {pointer}")
        current = current[part]
    return current


def path_exists(state: Mapping[str, JSON], pointer: str) -> bool:
    try:
        get_path(state, pointer)
        return True
    except ExecutionModelError:
        return False


def set_path(state: dict[str, JSON], pointer: str, value: JSON) -> None:
    parent, key = _parent_for(state, pointer, create=True)
    parent[key] = copy.deepcopy(value)


def delete_path(state: dict[str, JSON], pointer: str) -> None:
    parent, key = _parent_for(state, pointer, create=False)
    if key not in parent:
        raise ExecutionModelError(f"cannot delete missing path {pointer}")
    del parent[key]


PREDICATE_OPS = {"exists", "not_exists", "eq", "neq", "int_range", "unique"}
EFFECT_OPS = {"set", "add", "copy", "delete", "append_unique"}


@dataclass(frozen=True)
class Limits:
    max_states: int = 50_000
    max_transitions: int = 250_000


@dataclass(frozen=True)
class Action:
    id: str
    depends_on: tuple[str, ...]
    requires: tuple[dict[str, JSON], ...]
    effects: tuple[dict[str, JSON], ...]

    @property
    def reads(self) -> tuple[str, ...]:
        values: set[str] = set()
        for pred in self.requires:
            values.add(pred["path"])
        for effect in self.effects:
            op = effect["op"]
            if op in {"add", "append_unique"}:
                values.add(effect["path"])
            elif op == "copy":
                values.add(effect["from"])
        return tuple(sorted(values))

    @property
    def writes(self) -> tuple[str, ...]:
        values: set[str] = set()
        for effect in self.effects:
            op = effect["op"]
            if op == "copy":
                values.add(effect["to"])
            else:
                values.add(effect["path"])
        return tuple(sorted(values))


@dataclass(frozen=True)
class Plan:
    schema_version: str
    initial_state: dict[str, JSON]
    actions: tuple[Action, ...]
    invariants: tuple[dict[str, JSON], ...]
    limits: Limits

    def action_map(self) -> dict[str, Action]:
        return {action.id: action for action in self.actions}

    def normalized(self) -> dict[str, JSON]:
        return {
            "schema_version": self.schema_version,
            "initial_state": self.initial_state,
            "actions": [
                {
                    "id": a.id,
                    "depends_on": list(a.depends_on),
                    "requires": list(a.requires),
                    "effects": list(a.effects),
                }
                for a in sorted(self.actions, key=lambda item: item.id)
            ],
            "invariants": sorted((copy.deepcopy(x) for x in self.invariants), key=canonical_json),
            "limits": {
                "max_states": self.limits.max_states,
                "max_transitions": self.limits.max_transitions,
            },
        }


def _require_object(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ModelError(f"{where}: expected object")
    return value


def _reject_extra(obj: Mapping[str, Any], allowed: set[str], where: str) -> None:
    extra = sorted(set(obj) - allowed)
    if extra:
        raise ModelError(f"{where}: unknown fields: {', '.join(extra)}")


def _validate_predicate(raw: Any, where: str) -> dict[str, JSON]:
    pred = _require_object(raw, where)
    _reject_extra(pred, {"op", "path", "value", "min", "max"}, where)
    op = pred.get("op")
    if op not in PREDICATE_OPS:
        raise ModelError(f"{where}.op: unsupported predicate {op!r}")
    path = pred.get("path")
    parse_pointer(path)
    if op in {"eq", "neq"}:
        if "value" not in pred:
            raise ModelError(f"{where}: {op} requires value")
        validate_json_value(pred["value"], where=f"{where}.value")
    elif op == "int_range":
        if "min" not in pred and "max" not in pred:
            raise ModelError(f"{where}: int_range requires min and/or max")
        for key in ("min", "max"):
            if key in pred and (not isinstance(pred[key], int) or isinstance(pred[key], bool)):
                raise ModelError(f"{where}.{key}: expected integer")
        if "min" in pred and "max" in pred and pred["min"] > pred["max"]:
            raise ModelError(f"{where}: min cannot exceed max")
    else:
        illegal = {"value", "min", "max"} & set(pred)
        if illegal:
            raise ModelError(f"{where}: {op} forbids {', '.join(sorted(illegal))}")
    return copy.deepcopy(pred)


def _validate_effect(raw: Any, where: str) -> dict[str, JSON]:
    effect = _require_object(raw, where)
    _reject_extra(effect, {"op", "path", "value", "from", "to"}, where)
    op = effect.get("op")
    if op not in EFFECT_OPS:
        raise ModelError(f"{where}.op: unsupported effect {op!r}")
    if op == "copy":
        illegal = {"path", "value"} & set(effect)
        if illegal:
            raise ModelError(f"{where}: copy forbids {', '.join(sorted(illegal))}")
        if "from" not in effect or "to" not in effect:
            raise ModelError(f"{where}: copy requires from and to")
        parse_pointer(effect["from"])
        parse_pointer(effect["to"])
    else:
        illegal = {"from", "to"} & set(effect)
        if illegal:
            raise ModelError(f"{where}: {op} forbids {', '.join(sorted(illegal))}")
        if "path" not in effect:
            raise ModelError(f"{where}: {op} requires path")
        parse_pointer(effect["path"])
        if op in {"set", "add", "append_unique"}:
            if "value" not in effect:
                raise ModelError(f"{where}: {op} requires value")
            validate_json_value(effect["value"], where=f"{where}.value")
            if op == "add" and (not isinstance(effect["value"], int) or isinstance(effect["value"], bool)):
                raise ModelError(f"{where}.value: add requires integer delta")
        if op == "delete" and "value" in effect:
            raise ModelError(f"{where}: delete forbids value")
    return copy.deepcopy(effect)


def _validate_dag(actions: tuple[Action, ...]) -> None:
    ids = {a.id for a in actions}
    for action in actions:
        missing = sorted(set(action.depends_on) - ids)
        if missing:
            raise ModelError(f"action {action.id}: missing dependencies {', '.join(missing)}")
        if action.id in action.depends_on:
            raise ModelError(f"action {action.id}: self dependency")

    visiting: set[str] = set()
    visited: set[str] = set()
    mapping = {a.id: a for a in actions}

    def visit(action_id: str, stack: list[str]) -> None:
        if action_id in visited:
            return
        if action_id in visiting:
            cycle_start = stack.index(action_id)
            cycle = stack[cycle_start:] + [action_id]
            raise ModelError("dependency cycle: " + " -> ".join(cycle))
        visiting.add(action_id)
        stack.append(action_id)
        for dep in mapping[action_id].depends_on:
            visit(dep, stack)
        stack.pop()
        visiting.remove(action_id)
        visited.add(action_id)

    for action_id in sorted(ids):
        visit(action_id, [])


def parse_plan(raw: Any) -> Plan:
    root = _require_object(raw, "plan")
    _reject_extra(root, {"schema_version", "initial_state", "actions", "invariants", "limits"}, "plan")
    version = root.get("schema_version", "1.0")
    if version != "1.0":
        raise ModelError(f"schema_version: unsupported {version!r}")
    initial = _require_object(root.get("initial_state"), "initial_state")
    validate_json_value(initial, where="initial_state")

    raw_actions = root.get("actions")
    if not isinstance(raw_actions, list) or not raw_actions:
        raise ModelError("actions: expected non-empty array")
    actions: list[Action] = []
    seen: set[str] = set()
    for index, item in enumerate(raw_actions):
        where = f"actions[{index}]"
        obj = _require_object(item, where)
        _reject_extra(obj, {"id", "depends_on", "requires", "effects"}, where)
        action_id = obj.get("id")
        if not isinstance(action_id, str) or not action_id.strip():
            raise ModelError(f"{where}.id: expected non-empty string")
        if action_id in seen:
            raise ModelError(f"{where}.id: duplicate action id {action_id!r}")
        seen.add(action_id)
        deps = obj.get("depends_on", [])
        if not isinstance(deps, list) or any(not isinstance(x, str) or not x for x in deps):
            raise ModelError(f"{where}.depends_on: expected array of non-empty strings")
        if len(deps) != len(set(deps)):
            raise ModelError(f"{where}.depends_on: duplicates are forbidden")
        requires = obj.get("requires", [])
        effects = obj.get("effects", [])
        if not isinstance(requires, list):
            raise ModelError(f"{where}.requires: expected array")
        if not isinstance(effects, list) or not effects:
            raise ModelError(f"{where}.effects: expected non-empty array")
        actions.append(
            Action(
                id=action_id,
                depends_on=tuple(sorted(deps)),
                requires=tuple(_validate_predicate(p, f"{where}.requires[{i}]") for i, p in enumerate(requires)),
                effects=tuple(_validate_effect(e, f"{where}.effects[{i}]") for i, e in enumerate(effects)),
            )
        )

    invariants_raw = root.get("invariants", [])
    if not isinstance(invariants_raw, list):
        raise ModelError("invariants: expected array")
    invariants = tuple(_validate_predicate(p, f"invariants[{i}]") for i, p in enumerate(invariants_raw))

    limits_raw = root.get("limits", {})
    limits_obj = _require_object(limits_raw, "limits")
    _reject_extra(limits_obj, {"max_states", "max_transitions"}, "limits")
    max_states = limits_obj.get("max_states", 50_000)
    max_transitions = limits_obj.get("max_transitions", 250_000)
    for name, value in (("max_states", max_states), ("max_transitions", max_transitions)):
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise ModelError(f"limits.{name}: expected positive integer")

    plan = Plan(
        schema_version=version,
        initial_state=copy.deepcopy(initial),
        actions=tuple(actions),
        invariants=invariants,
        limits=Limits(max_states=max_states, max_transitions=max_transitions),
    )
    _validate_dag(plan.actions)
    return plan


def evaluate_predicate(state: Mapping[str, JSON], pred: Mapping[str, JSON]) -> tuple[bool, str]:
    op = pred["op"]
    path = pred["path"]
    exists = path_exists(state, path)
    if op == "exists":
        return exists, f"{path} exists={exists}"
    if op == "not_exists":
        return (not exists), f"{path} exists={exists}"
    if not exists:
        return False, f"{path} is missing"
    value = get_path(state, path)
    if op == "eq":
        ok = value == pred["value"]
        return ok, f"{path}={value!r}, expected {pred['value']!r}"
    if op == "neq":
        ok = value != pred["value"]
        return ok, f"{path}={value!r}, forbidden {pred['value']!r}"
    if op == "int_range":
        if not isinstance(value, int) or isinstance(value, bool):
            return False, f"{path} is not an integer"
        if "min" in pred and value < pred["min"]:
            return False, f"{path}={value} < min {pred['min']}"
        if "max" in pred and value > pred["max"]:
            return False, f"{path}={value} > max {pred['max']}"
        return True, f"{path}={value} within range"
    if op == "unique":
        if not isinstance(value, list):
            return False, f"{path} is not a list"
        encoded = [canonical_json(item) for item in value]
        ok = len(encoded) == len(set(encoded))
        return ok, f"{path} unique={ok}"
    raise AssertionError(f"validated predicate op missing implementation: {op}")


def apply_effect(state: dict[str, JSON], effect: Mapping[str, JSON]) -> None:
    op = effect["op"]
    if op == "set":
        set_path(state, effect["path"], effect["value"])
        return
    if op == "add":
        path = effect["path"]
        current = get_path(state, path)
        if not isinstance(current, int) or isinstance(current, bool):
            raise ExecutionModelError(f"add requires integer at {path}")
        set_path(state, path, current + effect["value"])
        return
    if op == "copy":
        set_path(state, effect["to"], get_path(state, effect["from"]))
        return
    if op == "delete":
        delete_path(state, effect["path"])
        return
    if op == "append_unique":
        path = effect["path"]
        current = get_path(state, path)
        if not isinstance(current, list):
            raise ExecutionModelError(f"append_unique requires list at {path}")
        candidate = copy.deepcopy(effect["value"])
        encoded = canonical_json(candidate)
        if encoded not in {canonical_json(item) for item in current}:
            current = copy.deepcopy(current)
            current.append(candidate)
            set_path(state, path, current)
        return
    raise AssertionError(f"validated effect op missing implementation: {op}")
