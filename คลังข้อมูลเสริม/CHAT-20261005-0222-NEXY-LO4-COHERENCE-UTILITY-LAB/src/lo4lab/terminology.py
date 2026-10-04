from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .canonical import fingerprint


class TerminologyError(ValueError):
    pass


def _parts(scope: str) -> tuple[str, ...]:
    cleaned = scope.strip().strip("/")
    if not cleaned:
        return ()
    parts = tuple(part for part in cleaned.split("/") if part)
    if any(part in {".", ".."} for part in parts):
        raise TerminologyError("scope cannot contain dot path segments")
    return parts


def _is_prefix(prefix: tuple[str, ...], full: tuple[str, ...]) -> bool:
    return len(prefix) <= len(full) and full[: len(prefix)] == prefix


@dataclass(frozen=True, slots=True)
class TermDefinition:
    term: str
    scope: str
    definition: str
    aliases: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.term.strip() or not self.definition.strip():
            raise TerminologyError("term and definition must be non-empty")
        _parts(self.scope)
        normalized_aliases = [alias.strip() for alias in self.aliases]
        if any(not alias for alias in normalized_aliases):
            raise TerminologyError("aliases must be non-empty")
        if len(normalized_aliases) != len(set(normalized_aliases)):
            raise TerminologyError("duplicate alias")
        if self.term in normalized_aliases:
            raise TerminologyError("term cannot alias itself")

    @property
    def scope_parts(self) -> tuple[str, ...]:
        return _parts(self.scope)

    @property
    def definition_fingerprint(self) -> str:
        return fingerprint(self.definition.strip())


@dataclass(frozen=True, slots=True)
class TermResolution:
    status: str
    requested: str
    canonical_term: str | None
    definition: str | None
    scope: str | None
    reason_codes: tuple[str, ...]
    resolution_fingerprint: str


class TerminologyRegistry:
    def __init__(self, definitions: Iterable[TermDefinition]):
        rows = tuple(sorted(definitions, key=lambda d: (d.scope_parts, d.term, d.definition_fingerprint)))
        if not rows:
            raise TerminologyError("registry requires at least one definition")

        exact: dict[tuple[tuple[str, ...], str], TermDefinition] = {}
        alias_exact: dict[tuple[tuple[str, ...], str], str] = {}
        canonical_names_by_scope: dict[tuple[str, ...], set[str]] = {}

        for row in rows:
            key = (row.scope_parts, row.term)
            previous = exact.get(key)
            if previous is not None and previous.definition_fingerprint != row.definition_fingerprint:
                raise TerminologyError(f"conflicting exact definition for {row.term} in {row.scope}")
            exact[key] = row
            canonical_names_by_scope.setdefault(row.scope_parts, set()).add(row.term)

        for row in rows:
            for alias in row.aliases:
                key = (row.scope_parts, alias)
                if alias in canonical_names_by_scope.get(row.scope_parts, set()):
                    raise TerminologyError(f"alias collides with canonical term in same scope: {alias}")
                previous = alias_exact.get(key)
                if previous is not None and previous != row.term:
                    raise TerminologyError(f"ambiguous alias {alias} in {row.scope}")
                alias_exact[key] = row.term

        # Reject direct/indirect alias cycles across same-scope names, even if introduced by future extensions.
        for scope_parts in sorted(canonical_names_by_scope):
            mapping = {alias: target for (scope, alias), target in alias_exact.items() if scope == scope_parts}
            for start in sorted(mapping):
                seen: set[str] = set()
                cursor = start
                while cursor in mapping:
                    if cursor in seen:
                        raise TerminologyError(f"alias cycle detected in scope {'/'.join(scope_parts)}")
                    seen.add(cursor)
                    cursor = mapping[cursor]

        self._definitions = tuple(exact.values())
        self._alias_exact = alias_exact

    def resolve(self, requested: str, context_scope: str) -> TermResolution:
        if not requested.strip():
            raise TerminologyError("requested term must be non-empty")
        context = _parts(context_scope)

        candidates: list[tuple[int, TermDefinition, str]] = []
        for row in self._definitions:
            if not _is_prefix(row.scope_parts, context):
                continue
            if row.term == requested:
                candidates.append((len(row.scope_parts), row, row.term))
                continue
            target = self._alias_exact.get((row.scope_parts, requested))
            if target == row.term:
                candidates.append((len(row.scope_parts), row, row.term))

        if not candidates:
            payload = {
                "status": "UNKNOWN",
                "requested": requested,
                "canonical_term": None,
                "definition": None,
                "scope": None,
                "reason_codes": ["TERM_NOT_DEFINED_FOR_SCOPE"],
            }
            return TermResolution(
                status="UNKNOWN",
                requested=requested,
                canonical_term=None,
                definition=None,
                scope=None,
                reason_codes=("TERM_NOT_DEFINED_FOR_SCOPE",),
                resolution_fingerprint=fingerprint(payload),
            )

        most_specific = max(depth for depth, _, _ in candidates)
        top = [(row, canonical) for depth, row, canonical in candidates if depth == most_specific]
        semantics = {(row.term, row.definition_fingerprint) for row, _ in top}
        if len(semantics) != 1:
            payload = {
                "status": "CONFLICT",
                "requested": requested,
                "canonical_term": None,
                "definition": None,
                "scope": "/".join(top[0][0].scope_parts),
                "reason_codes": ["AMBIGUOUS_TERM_AT_EQUAL_SPECIFICITY"],
            }
            return TermResolution(
                status="CONFLICT",
                requested=requested,
                canonical_term=None,
                definition=None,
                scope="/".join(top[0][0].scope_parts),
                reason_codes=("AMBIGUOUS_TERM_AT_EQUAL_SPECIFICITY",),
                resolution_fingerprint=fingerprint(payload),
            )

        row, canonical = top[0]
        payload = {
            "status": "PASS",
            "requested": requested,
            "canonical_term": canonical,
            "definition": row.definition,
            "scope": "/".join(row.scope_parts),
            "reason_codes": ["MOST_SPECIFIC_DEFINITION_SELECTED"],
        }
        return TermResolution(
            status="PASS",
            requested=requested,
            canonical_term=canonical,
            definition=row.definition,
            scope="/".join(row.scope_parts),
            reason_codes=("MOST_SPECIFIC_DEFINITION_SELECTED",),
            resolution_fingerprint=fingerprint(payload),
        )
