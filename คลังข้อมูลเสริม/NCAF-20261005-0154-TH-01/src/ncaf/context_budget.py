from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .common import ContractError, require_nonempty


@dataclass(frozen=True)
class ContextItem:
    item_id: str
    tokens: int
    utility: int
    freshness: int
    mandatory: bool = False
    dependencies: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        require_nonempty(self.item_id, "item_id")
        if self.tokens <= 0:
            raise ContractError("tokens must be positive")
        if self.utility < 0 or self.freshness < 0:
            raise ContractError("utility and freshness must be non-negative")
        if self.item_id in self.dependencies:
            raise ContractError("an item cannot depend on itself")


@dataclass(frozen=True)
class ContextSelection:
    selected: tuple[str, ...]
    used_tokens: int
    total_score: int
    omitted: tuple[str, ...]


class ContextBudgetAllocator:
    """Deterministic dependency-aware context packer under a hard token budget."""

    def __init__(self, items: Iterable[ContextItem]):
        items = tuple(items)
        self._items = {item.item_id: item for item in items}
        if len(self._items) != len(items):
            raise ContractError("duplicate context item id")
        for item in self._items.values():
            missing = sorted(set(item.dependencies) - self._items.keys())
            if missing:
                raise ContractError(f"{item.item_id} has missing dependencies: {missing}")
        self._validate_acyclic()

    def _validate_acyclic(self) -> None:
        visiting: set[str] = set()
        visited: set[str] = set()

        def walk(item_id: str) -> None:
            if item_id in visiting:
                raise ContractError("context dependency cycle detected")
            if item_id in visited:
                return
            visiting.add(item_id)
            for dep in self._items[item_id].dependencies:
                walk(dep)
            visiting.remove(item_id)
            visited.add(item_id)

        for item_id in sorted(self._items):
            walk(item_id)

    def _closure(self, item_id: str) -> set[str]:
        out: set[str] = set()

        def add(current: str) -> None:
            if current in out:
                return
            for dep in self._items[current].dependencies:
                add(dep)
            out.add(current)

        add(item_id)
        return out

    @staticmethod
    def _score(item: ContextItem) -> int:
        return item.utility * 1000 + item.freshness

    def allocate(self, token_budget: int) -> ContextSelection:
        if token_budget <= 0:
            raise ContractError("token_budget must be positive")
        selected: set[str] = set()

        mandatory_roots = sorted(i.item_id for i in self._items.values() if i.mandatory)
        for root in mandatory_roots:
            selected |= self._closure(root)

        used = sum(self._items[i].tokens for i in selected)
        if used > token_budget:
            raise ContractError("mandatory dependency closure exceeds token budget")

        candidates = []
        for item_id in sorted(self._items):
            if item_id in selected:
                continue
            closure = self._closure(item_id) - selected
            cost = sum(self._items[i].tokens for i in closure)
            score = sum(self._score(self._items[i]) for i in closure)
            candidates.append((-(score * 1_000_000 // cost), -score, cost, item_id))

        for _, _, _, item_id in sorted(candidates):
            closure = self._closure(item_id) - selected
            cost = sum(self._items[i].tokens for i in closure)
            if used + cost <= token_budget:
                selected |= closure
                used += cost

        ordered = tuple(sorted(selected))
        omitted = tuple(sorted(set(self._items) - selected))
        total_score = sum(self._score(self._items[i]) for i in selected)
        return ContextSelection(ordered, used, total_score, omitted)
