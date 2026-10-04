from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class ContextItem:
    item_id: str
    tokens: int
    relevance: float
    authority: int
    freshness: float
    dependencies: tuple[str, ...] = ()
    mandatory: bool = False


@dataclass(frozen=True)
class ContextSelection:
    status: str
    selected: tuple[str, ...]
    used_tokens: int
    score: float
    omitted: tuple[tuple[str, str], ...]
    reason: str | None = None


def _validate(items: tuple[ContextItem, ...], budget: int) -> dict[str, ContextItem]:
    if budget < 0:
        raise ValueError('budget must be >= 0')
    index: dict[str, ContextItem] = {}
    for item in items:
        if not item.item_id or item.item_id in index:
            raise ValueError('item ids must be unique and non-empty')
        if item.tokens <= 0:
            raise ValueError('tokens must be > 0')
        if not 0.0 <= item.relevance <= 1.0:
            raise ValueError('relevance must be within [0,1]')
        if not 0.0 <= item.freshness <= 1.0:
            raise ValueError('freshness must be within [0,1]')
        if not 0 <= item.authority <= 10:
            raise ValueError('authority must be within [0,10]')
        index[item.item_id] = item
    for item in items:
        missing = [d for d in item.dependencies if d not in index]
        if missing:
            raise ValueError(f'{item.item_id} has unknown dependencies: {missing}')
    return index


def _closure(item_id: str, index: dict[str, ContextItem]) -> set[str]:
    seen: set[str] = set()
    active: set[str] = set()

    def walk(current: str) -> None:
        if current in active:
            raise ValueError(f'dependency cycle detected at {current}')
        if current in seen:
            return
        active.add(current)
        for dep in index[current].dependencies:
            walk(dep)
        active.remove(current)
        seen.add(current)

    walk(item_id)
    return seen


def _value(item: ContextItem) -> float:
    return (0.45 * item.relevance) + (0.35 * (item.authority / 10.0)) + (0.20 * item.freshness)


def optimize_context(items: Iterable[ContextItem], budget: int) -> ContextSelection:
    data = tuple(items)
    try:
        index = _validate(data, budget)
        closures = {item.item_id: _closure(item.item_id, index) for item in data}
    except ValueError as exc:
        return ContextSelection('FREEZE', (), 0, 0.0, (), str(exc))

    selected: set[str] = set()
    mandatory_roots = sorted(i.item_id for i in data if i.mandatory)
    for root in mandatory_roots:
        selected.update(closures[root])

    used = sum(index[i].tokens for i in selected)
    if used > budget:
        return ContextSelection('FREEZE', tuple(sorted(selected)), used, 0.0, (), 'mandatory dependency closure exceeds budget')

    candidates = [i for i in data if i.item_id not in selected]
    while candidates:
        ranked: list[tuple[float, float, str, set[str], int]] = []
        for item in candidates:
            incremental = closures[item.item_id] - selected
            inc_tokens = sum(index[i].tokens for i in incremental)
            if inc_tokens == 0:
                density = float('inf')
                utility = 0.0
            else:
                utility = sum(_value(index[i]) for i in incremental)
                density = utility / inc_tokens
            ranked.append((density, utility, item.item_id, incremental, inc_tokens))
        ranked.sort(key=lambda x: (-x[0], -x[1], x[2]))
        chosen = None
        for entry in ranked:
            if used + entry[4] <= budget:
                chosen = entry
                break
        if chosen is None:
            break
        selected.update(chosen[3])
        used += chosen[4]
        candidates = [i for i in candidates if i.item_id not in selected]

    selected_order = tuple(sorted(selected))
    score = round(sum(_value(index[i]) for i in selected), 6)
    omitted = tuple((i.item_id, 'budget_or_lower_priority') for i in sorted(data, key=lambda x: x.item_id) if i.item_id not in selected)
    return ContextSelection('PASS', selected_order, used, score, omitted)
