from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class Mutant:
    mutant_id: str
    path: str
    operator: str
    document: Any


@dataclass(frozen=True)
class MutationReport:
    total: int
    killed: int
    survived: int
    score: float
    killed_ids: tuple[str, ...]
    survivor_ids: tuple[str, ...]


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def _mutant_id(path: str, operator: str, document: Any) -> str:
    payload = f"{path}|{operator}|{_canonical(document)}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]


def _walk(value: Any, path=()):
    yield path, value
    if isinstance(value, dict):
        for key in sorted(value, key=str):
            yield from _walk(value[key], path + (key,))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, path + (index,))


def _fmt(path) -> str:
    if not path:
        return "$"
    return "$" + "".join(f"[{p}]" if isinstance(p, int) else f".{p}" for p in path)


def _replace(root: Any, path, value) -> Any:
    if not path:
        return deepcopy(value)
    out = deepcopy(root)
    cursor = out
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value
    return out


def _delete(root: Any, path) -> Any:
    out = deepcopy(root)
    cursor = out
    for key in path[:-1]:
        cursor = cursor[key]
    del cursor[path[-1]]
    return out


def generate_mutants(document: Any, *, max_mutants: int = 1_000) -> tuple[Mutant, ...]:
    if not isinstance(max_mutants, int) or isinstance(max_mutants, bool) or max_mutants <= 0:
        raise ValueError("max_mutants must be a positive integer")
    candidates: list[tuple[str, str, Any]] = []
    for path, node in _walk(document):
        p = _fmt(path)
        if isinstance(node, dict):
            for key in sorted(node, key=str):
                child_path = path + (key,)
                candidates.append((_fmt(child_path), "delete-key", _delete(document, child_path)))
        elif isinstance(node, list):
            for index in range(len(node)):
                child_path = path + (index,)
                candidates.append((_fmt(child_path), "delete-item", _delete(document, child_path)))
        elif isinstance(node, bool):
            candidates.append((p, "flip-bool", _replace(document, path, not node)))
        elif isinstance(node, int) and not isinstance(node, bool):
            candidates.append((p, "boundary-minus-one", _replace(document, path, node - 1)))
            candidates.append((p, "boundary-plus-one", _replace(document, path, node + 1)))
        elif isinstance(node, str):
            candidates.append((p, "replace-string", _replace(document, path, "__MUTANT__")))

    original = _canonical(document)
    seen = set()
    result = []
    for path, operator, mutated in candidates:
        canonical = _canonical(mutated)
        if canonical == original or canonical in seen:
            continue
        seen.add(canonical)
        result.append(
            Mutant(
                mutant_id=_mutant_id(path, operator, mutated),
                path=path,
                operator=operator,
                document=mutated,
            )
        )
        if len(result) >= max_mutants:
            break
    return tuple(result)


def evaluate_mutation_adequacy(
    document: Any,
    oracle: Callable[[Any], bool],
    *,
    max_mutants: int = 1_000,
) -> MutationReport:
    """
    Measure whether an oracle rejects deterministic semantic mutants.

    Oracle contract: return True when the candidate is accepted as valid. A raised exception is
    treated as rejection/killed, which matches strict validator behavior. The baseline MUST pass.
    """
    try:
        baseline = bool(oracle(deepcopy(document)))
    except Exception as exc:  # baseline validator failure is not useful evidence
        raise ValueError(f"baseline oracle raised: {type(exc).__name__}: {exc}") from exc
    if not baseline:
        raise ValueError("baseline document is not accepted by the oracle")

    mutants = generate_mutants(document, max_mutants=max_mutants)
    if not mutants:
        raise ValueError("no mutants generated; mutation adequacy is undefined")
    killed = []
    survived = []
    for mutant in mutants:
        try:
            accepted = bool(oracle(deepcopy(mutant.document)))
        except Exception:
            accepted = False
        if accepted:
            survived.append(mutant.mutant_id)
        else:
            killed.append(mutant.mutant_id)
    total = len(mutants)
    score = len(killed) / total
    return MutationReport(
        total=total,
        killed=len(killed),
        survived=len(survived),
        score=score,
        killed_ids=tuple(killed),
        survivor_ids=tuple(survived),
    )
