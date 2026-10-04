"""Deterministic minimal-cut analysis for alternative support paths."""
from __future__ import annotations

from collections.abc import Iterable, Set


def _normalize_paths(support_paths: Iterable[Set[str]], max_nodes: int) -> tuple[frozenset[str], ...]:
    if not isinstance(max_nodes, int) or max_nodes <= 0:
        raise ValueError("max_nodes must be a positive integer")
    normalized: list[frozenset[str]] = []
    for raw in support_paths:
        path = frozenset(raw)
        if not path:
            raise ValueError("support paths must be non-empty")
        if any(not isinstance(node, str) or not node for node in path):
            raise ValueError("nodes must be non-empty strings")
        normalized.append(path)
    if not normalized:
        raise ValueError("at least one support path is required")
    universe = frozenset().union(*normalized)
    if len(universe) > max_nodes:
        raise ValueError(f"node universe exceeds max_nodes={max_nodes}")
    # Superset support paths are redundant for hitting-set construction.
    unique = sorted(set(normalized), key=lambda p: (len(p), tuple(sorted(p))))
    minimal_paths: list[frozenset[str]] = []
    for path in unique:
        if not any(existing <= path for existing in minimal_paths):
            minimal_paths.append(path)
    return tuple(minimal_paths)


def minimal_failure_cut_sets(
    support_paths: Iterable[Set[str]], *, max_nodes: int = 20
) -> tuple[tuple[str, ...], ...]:
    """Return all inclusion-minimal sets that intersect every support path.

    If each support path is an independent way to justify/operate a decision,
    every returned tuple is a minimal simultaneous-failure set capable of
    breaking every path.  This is exact and intentionally bounded by
    ``max_nodes`` because minimal transversal enumeration is exponential.
    """
    paths = _normalize_paths(support_paths, max_nodes)
    candidates: set[frozenset[str]] = {frozenset()}

    for path in paths:
        next_candidates: set[frozenset[str]] = set()
        for candidate in candidates:
            if candidate & path:
                next_candidates.add(candidate)
            else:
                for node in sorted(path):
                    next_candidates.add(candidate | {node})

        # Keep only inclusion-minimal candidates after each expansion.
        ordered = sorted(next_candidates, key=lambda s: (len(s), tuple(sorted(s))))
        reduced: list[frozenset[str]] = []
        for candidate in ordered:
            if not any(existing <= candidate for existing in reduced):
                reduced.append(candidate)
        candidates = set(reduced)

    # Defensive final minimality and deterministic ordering.
    minimal = [
        candidate
        for candidate in candidates
        if not any(other < candidate for other in candidates)
    ]
    rendered = [tuple(sorted(candidate)) for candidate in minimal]
    return tuple(sorted(rendered, key=lambda item: (len(item), item)))
