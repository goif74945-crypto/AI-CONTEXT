from __future__ import annotations

import copy
from collections import deque
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from .model import (
    Action,
    ExecutionModelError,
    ModelError,
    Plan,
    apply_effect,
    canonical_json,
    evaluate_predicate,
    parse_plan,
    pointer_overlap,
    sha256_json,
)

JSON = Any


@dataclass(frozen=True)
class Node:
    done: frozenset[str]
    state: dict[str, JSON]
    path: tuple[str, ...]

    @property
    def key(self) -> tuple[tuple[str, ...], str]:
        return tuple(sorted(self.done)), canonical_json(self.state)


def _base_report() -> dict[str, JSON]:
    return {
        "report_version": "1.0",
        "verification_status": "NOT_VERIFIED",
        "decision": "FREEZE_INVALID_INPUT",
        "plan_fingerprint": None,
        "exploration_complete": False,
        "states_explored": 0,
        "transitions_explored": 0,
        "terminal_state_count": 0,
        "terminal_fingerprints": [],
        "static_conflicts": [],
        "witnesses": [],
        "diagnostics": [],
    }


def _finalize(report: dict[str, JSON]) -> dict[str, JSON]:
    body = copy.deepcopy(report)
    body.pop("report_fingerprint", None)
    report["report_fingerprint"] = sha256_json(body)
    return report


def _transitive_predecessors(plan: Plan) -> dict[str, set[str]]:
    mapping = plan.action_map()
    memo: dict[str, set[str]] = {}

    def resolve(action_id: str) -> set[str]:
        if action_id in memo:
            return memo[action_id]
        result: set[str] = set(mapping[action_id].depends_on)
        for dep in mapping[action_id].depends_on:
            result.update(resolve(dep))
        memo[action_id] = result
        return result

    for action_id in sorted(mapping):
        resolve(action_id)
    return memo


def _overlapping_paths(left: Iterable[str], right: Iterable[str]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for a in left:
        for b in right:
            if pointer_overlap(a, b):
                pairs.append((a, b))
    return sorted(set(pairs))


def static_conflicts(plan: Plan) -> list[dict[str, JSON]]:
    preds = _transitive_predecessors(plan)
    actions = sorted(plan.actions, key=lambda a: a.id)
    result: list[dict[str, JSON]] = []
    for i, left in enumerate(actions):
        for right in actions[i + 1 :]:
            if left.id in preds[right.id] or right.id in preds[left.id]:
                continue
            ww = _overlapping_paths(left.writes, right.writes)
            wr = _overlapping_paths(left.writes, right.reads)
            rw = _overlapping_paths(left.reads, right.writes)
            if not (ww or wr or rw):
                continue
            result.append(
                {
                    "actions": [left.id, right.id],
                    "write_write": [[a, b] for a, b in ww],
                    "left_write_right_read": [[a, b] for a, b in wr],
                    "left_read_right_write": [[a, b] for a, b in rw],
                }
            )
    return result


def _state_diff(left: Any, right: Any, path: str = "") -> list[dict[str, JSON]]:
    if isinstance(left, dict) and isinstance(right, dict):
        result: list[dict[str, JSON]] = []
        for key in sorted(set(left) | set(right)):
            pointer = path + "/" + key.replace("~", "~0").replace("/", "~1")
            if key not in left:
                result.append({"path": pointer, "left": "<MISSING>", "right": right[key]})
            elif key not in right:
                result.append({"path": pointer, "left": left[key], "right": "<MISSING>"})
            else:
                result.extend(_state_diff(left[key], right[key], pointer))
        return result
    if isinstance(left, list) and isinstance(right, list):
        if left == right:
            return []
        return [{"path": path or "/", "left": left, "right": right}]
    if left != right:
        return [{"path": path or "/", "left": left, "right": right}]
    return []


def _first_order_disagreement(path_a: tuple[str, ...], path_b: tuple[str, ...], conflicts: list[dict[str, JSON]]) -> list[str] | None:
    index_a = {action: index for index, action in enumerate(path_a)}
    index_b = {action: index for index, action in enumerate(path_b)}
    for item in conflicts:
        left, right = item["actions"]
        if (index_a[left] < index_a[right]) != (index_b[left] < index_b[right]):
            return [left, right]
    return None


def _check_invariants(plan: Plan, state: Mapping[str, JSON]) -> tuple[bool, dict[str, JSON] | None]:
    for index, pred in enumerate(plan.invariants):
        ok, detail = evaluate_predicate(state, pred)
        if not ok:
            return False, {"invariant_index": index, "predicate": copy.deepcopy(pred), "detail": detail}
    return True, None


def _enabled(plan: Plan, done: frozenset[str]) -> list[Action]:
    return [
        action
        for action in sorted(plan.actions, key=lambda a: a.id)
        if action.id not in done and set(action.depends_on).issubset(done)
    ]


def verify_plan(raw_plan: Any) -> dict[str, JSON]:
    report = _base_report()
    try:
        plan = parse_plan(raw_plan)
    except ModelError as exc:
        report["diagnostics"] = [{"code": "INVALID_MODEL", "message": str(exc)}]
        return _finalize(report)

    report["plan_fingerprint"] = sha256_json(plan.normalized())
    conflicts = static_conflicts(plan)
    report["static_conflicts"] = conflicts

    initial = Node(done=frozenset(), state=copy.deepcopy(plan.initial_state), path=())
    queue: deque[Node] = deque([initial])
    seen = {initial.key}
    report["states_explored"] = 1
    terminal_by_state: dict[str, Node] = {}

    initial_ok, initial_failure = _check_invariants(plan, initial.state)
    if not initial_ok:
        report.update({"verification_status": "FAIL", "decision": "INVARIANT_VIOLATION"})
        report["witnesses"] = [{"schedule": [], "failure": initial_failure, "state": initial.state}]
        return _finalize(report)

    while queue:
        node = queue.popleft()
        if len(node.done) == len(plan.actions):
            state_key = canonical_json(node.state)
            if state_key not in terminal_by_state:
                terminal_by_state[state_key] = node
                report["terminal_state_count"] = len(terminal_by_state)
                report["terminal_fingerprints"] = sorted(sha256_json(n.state) for n in terminal_by_state.values())
                if len(terminal_by_state) >= 2:
                    nodes = sorted(terminal_by_state.values(), key=lambda n: canonical_json(n.state))[:2]
                    pair = _first_order_disagreement(nodes[0].path, nodes[1].path, conflicts)
                    report.update({"verification_status": "FAIL", "decision": "DIVERGENT_TERMINAL_STATE"})
                    witness = {
                        "schedule_a": list(nodes[0].path),
                        "schedule_b": list(nodes[1].path),
                        "state_a": nodes[0].state,
                        "state_b": nodes[1].state,
                        "state_diff": _state_diff(nodes[0].state, nodes[1].state),
                    }
                    if pair is not None:
                        witness["candidate_serialization_pair"] = pair
                        witness["candidate_note"] = "Ordering authority is required; the verifier does not choose a direction."
                    report["witnesses"] = [witness]
                    return _finalize(report)
            continue

        for action in _enabled(plan, node.done):
            if report["transitions_explored"] >= plan.limits.max_transitions:
                report.update({"verification_status": "NOT_VERIFIED", "decision": "FREEZE_LIMIT"})
                report["diagnostics"] = [{
                    "code": "MAX_TRANSITIONS_EXCEEDED",
                    "message": f"exact exploration exceeded max_transitions={plan.limits.max_transitions}",
                }]
                return _finalize(report)
            report["transitions_explored"] += 1

            for pred_index, pred in enumerate(action.requires):
                ok, detail = evaluate_predicate(node.state, pred)
                if not ok:
                    report.update({"verification_status": "FAIL", "decision": "PRECONDITION_FAILURE"})
                    report["witnesses"] = [{
                        "schedule_prefix": list(node.path),
                        "blocked_action": action.id,
                        "predicate_index": pred_index,
                        "predicate": copy.deepcopy(pred),
                        "detail": detail,
                        "state": node.state,
                    }]
                    return _finalize(report)

            next_state = copy.deepcopy(node.state)
            try:
                for effect in action.effects:
                    apply_effect(next_state, effect)
            except ExecutionModelError as exc:
                report.update({"verification_status": "FAIL", "decision": "EXECUTION_MODEL_ERROR"})
                report["witnesses"] = [{
                    "schedule_prefix": list(node.path),
                    "action": action.id,
                    "message": str(exc),
                    "state": node.state,
                }]
                return _finalize(report)

            invariant_ok, invariant_failure = _check_invariants(plan, next_state)
            if not invariant_ok:
                report.update({"verification_status": "FAIL", "decision": "INVARIANT_VIOLATION"})
                report["witnesses"] = [{
                    "schedule": list(node.path + (action.id,)),
                    "failure": invariant_failure,
                    "state": next_state,
                }]
                return _finalize(report)

            next_node = Node(done=node.done | {action.id}, state=next_state, path=node.path + (action.id,))
            if next_node.key in seen:
                continue
            if report["states_explored"] >= plan.limits.max_states:
                report.update({"verification_status": "NOT_VERIFIED", "decision": "FREEZE_LIMIT"})
                report["diagnostics"] = [{
                    "code": "MAX_STATES_EXCEEDED",
                    "message": f"exact exploration exceeded max_states={plan.limits.max_states}",
                }]
                return _finalize(report)
            seen.add(next_node.key)
            report["states_explored"] += 1
            queue.append(next_node)

    report["exploration_complete"] = True
    report["terminal_state_count"] = len(terminal_by_state)
    report["terminal_fingerprints"] = sorted(sha256_json(node.state) for node in terminal_by_state.values())
    if len(terminal_by_state) != 1:
        report.update({"verification_status": "FAIL", "decision": "NO_TERMINAL_STATE"})
        report["diagnostics"] = [{"code": "NO_TERMINAL_STATE", "message": "no complete execution reached a terminal state"}]
    else:
        only = next(iter(terminal_by_state.values()))
        report.update({
            "verification_status": "PASS",
            "decision": "CONFLUENT",
            "canonical_terminal_state": only.state,
            "canonical_schedule_witness": list(only.path),
        })
    return _finalize(report)
