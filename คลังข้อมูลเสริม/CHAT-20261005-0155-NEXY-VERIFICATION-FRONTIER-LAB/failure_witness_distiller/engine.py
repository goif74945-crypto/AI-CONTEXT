from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Iterator, Optional

JsonValue = Any
FailureOracle = Callable[[JsonValue], Optional[str]]


@dataclass(frozen=True)
class ReductionStep:
    operation: str
    before_nodes: int
    after_nodes: int


@dataclass(frozen=True)
class DistillationResult:
    signature: str
    witness: JsonValue
    steps: tuple[ReductionStep, ...]
    original_nodes: int
    final_nodes: int


def _node_count(value: JsonValue) -> int:
    if isinstance(value, dict):
        return 1 + sum(_node_count(v) for v in value.values())
    if isinstance(value, list):
        return 1 + sum(_node_count(v) for v in value)
    return 1


def _replace_at(root: JsonValue, path: tuple[Any, ...], replacement: JsonValue) -> JsonValue:
    if not path:
        return deepcopy(replacement)
    cloned = deepcopy(root)
    cursor = cloned
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement
    return cloned


def _remove_at(root: JsonValue, path: tuple[Any, ...]) -> JsonValue:
    if not path:
        raise ValueError("cannot remove the root object")
    cloned = deepcopy(root)
    cursor = cloned
    for key in path[:-1]:
        cursor = cursor[key]
    leaf = path[-1]
    if isinstance(cursor, dict):
        del cursor[leaf]
    elif isinstance(cursor, list):
        del cursor[leaf]
    else:
        raise TypeError("remove path must target an item in a container")
    return cloned


def _walk(value: JsonValue, path: tuple[Any, ...] = ()) -> Iterator[tuple[tuple[Any, ...], JsonValue]]:
    yield path, value
    if isinstance(value, dict):
        for key in sorted(value, key=lambda x: str(x)):
            yield from _walk(value[key], path + (key,))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _walk(item, path + (index,))


def _candidate_neighbors(value: JsonValue) -> Iterable[tuple[str, JsonValue]]:
    """Yield deterministic, strictly simpler structural candidates."""
    for path, node in _walk(value):
        if isinstance(node, dict):
            for key in sorted(node, key=lambda x: str(x)):
                child_path = path + (key,)
                candidate = _remove_at(value, child_path)
                yield f"remove:{_fmt_path(child_path)}", candidate
        elif isinstance(node, list):
            for index in range(len(node)):
                child_path = path + (index,)
                candidate = _remove_at(value, child_path)
                yield f"remove:{_fmt_path(child_path)}", candidate
        elif path:
            for replacement in _simplifications(node):
                candidate = _replace_at(value, path, replacement)
                if _node_count(candidate) <= _node_count(value):
                    yield f"simplify:{_fmt_path(path)}->{replacement!r}", candidate


def _simplifications(value: JsonValue) -> tuple[JsonValue, ...]:
    if value is None:
        return ()
    if isinstance(value, bool):
        return (False,) if value else ()
    if isinstance(value, int) and not isinstance(value, bool):
        out = []
        for v in (0, 1, -1):
            if v != value:
                out.append(v)
        return tuple(out)
    if isinstance(value, float):
        out = []
        for v in (0.0, 1.0, -1.0):
            if v != value:
                out.append(v)
        return tuple(out)
    if isinstance(value, str):
        out = []
        for v in ("", value[:1]):
            if v != value and v not in out:
                out.append(v)
        return tuple(out)
    return ()


def _fmt_path(path: tuple[Any, ...]) -> str:
    if not path:
        return "$"
    return "$" + "".join(f"[{p}]" if isinstance(p, int) else f".{p}" for p in path)


def distill(value: JsonValue, oracle: FailureOracle, *, max_steps: int = 10_000) -> DistillationResult:
    """
    Deterministically reduce a JSON-like failing input while preserving the exact failure signature.

    This is a greedy local reducer, not a proof of globally minimal size. It is deliberately
    fail-closed: if the source input does not fail, no witness is fabricated.
    """
    source = deepcopy(value)
    signature = oracle(deepcopy(source))
    if not signature:
        raise ValueError("source input does not produce a failure signature")

    current = source
    steps: list[ReductionStep] = []
    original_nodes = _node_count(current)

    for _ in range(max_steps):
        before = _node_count(current)
        accepted = None
        for operation, candidate in _candidate_neighbors(current):
            # Strictly prefer smaller node count; simplifications with equal node count are only
            # accepted if their canonical repr is shorter, preventing oscillation.
            after = _node_count(candidate)
            if after > before:
                continue
            if after == before and len(repr(candidate)) >= len(repr(current)):
                continue
            if oracle(deepcopy(candidate)) == signature:
                accepted = (operation, candidate, after)
                break
        if accepted is None:
            break
        operation, candidate, after = accepted
        steps.append(ReductionStep(operation=operation, before_nodes=before, after_nodes=after))
        current = candidate
    else:
        raise RuntimeError("distillation exceeded max_steps; possible non-converging oracle/candidate space")

    # Final re-check protects against stateful or unstable oracles.
    final_signature = oracle(deepcopy(current))
    if final_signature != signature:
        raise RuntimeError("oracle was unstable: final witness no longer preserves the source signature")

    return DistillationResult(
        signature=signature,
        witness=current,
        steps=tuple(steps),
        original_nodes=original_nodes,
        final_nodes=_node_count(current),
    )
