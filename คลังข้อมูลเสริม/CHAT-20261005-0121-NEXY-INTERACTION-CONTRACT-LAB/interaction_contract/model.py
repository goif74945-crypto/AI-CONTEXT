from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


class ValidationError(ValueError):
    """Raised when the structured interaction contract is invalid."""


_ALLOWED_DIRECTIVE_KINDS = {"requirement", "constraint", "forbidden", "preference", "acceptance"}
_ALLOWED_CRITICALITY = {"critical", "high", "normal", "low"}
_ALLOWED_EVENT_TYPES = {"clarification", "action", "evidence", "completion", "note"}
_ALLOWED_OUTCOMES = {"pass", "fail", "blocked", "unknown", "not_verified"}


@dataclass(frozen=True)
class Directive:
    id: str
    text: str
    kind: str
    criticality: str
    scopes: tuple[str, ...]
    conflicts_with: tuple[str, ...]
    resolved: bool


@dataclass(frozen=True)
class Event:
    seq: int
    actor: str
    type: str
    directive_ids: tuple[str, ...]
    scopes: tuple[str, ...]
    assumptions: tuple[str, ...]
    outcome: str | None
    evidence_ref: str | None
    completion_status: str | None


@dataclass(frozen=True)
class Contract:
    contract_id: str
    authorized_scopes: tuple[str, ...]
    protected_scopes: tuple[str, ...]
    directives: tuple[Directive, ...]
    events: tuple[Event, ...]


def _as_str(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field} must be a non-empty string")
    return value.strip()


def _as_str_tuple(value: Any, field: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ValidationError(f"{field} must be a list of strings")
    result: list[str] = []
    for index, item in enumerate(value):
        result.append(_as_str(item, f"{field}[{index}]"))
    if len(result) != len(set(result)):
        raise ValidationError(f"{field} must not contain duplicates")
    return tuple(result)


def _require_choice(value: Any, field: str, allowed: Iterable[str]) -> str:
    normalized = _as_str(value, field)
    allowed_set = set(allowed)
    if normalized not in allowed_set:
        raise ValidationError(f"{field} must be one of {sorted(allowed_set)}")
    return normalized


def parse_contract(raw: dict[str, Any]) -> Contract:
    if not isinstance(raw, dict):
        raise ValidationError("contract must be a JSON object")

    contract_id = _as_str(raw.get("contract_id"), "contract_id")
    authorized_scopes = _as_str_tuple(raw.get("authorized_scopes", []), "authorized_scopes")
    protected_scopes = _as_str_tuple(raw.get("protected_scopes", []), "protected_scopes")

    overlap = sorted(set(authorized_scopes) & set(protected_scopes))
    if overlap:
        raise ValidationError(f"authorized_scopes and protected_scopes overlap: {overlap}")

    directives_raw = raw.get("directives")
    if not isinstance(directives_raw, list) or not directives_raw:
        raise ValidationError("directives must be a non-empty list")

    directives: list[Directive] = []
    seen_ids: set[str] = set()
    for index, item in enumerate(directives_raw):
        if not isinstance(item, dict):
            raise ValidationError(f"directives[{index}] must be an object")
        did = _as_str(item.get("id"), f"directives[{index}].id")
        if did in seen_ids:
            raise ValidationError(f"duplicate directive id: {did}")
        seen_ids.add(did)
        directive = Directive(
            id=did,
            text=_as_str(item.get("text"), f"directives[{index}].text"),
            kind=_require_choice(item.get("kind"), f"directives[{index}].kind", _ALLOWED_DIRECTIVE_KINDS),
            criticality=_require_choice(
                item.get("criticality", "normal"),
                f"directives[{index}].criticality",
                _ALLOWED_CRITICALITY,
            ),
            scopes=_as_str_tuple(item.get("scopes", []), f"directives[{index}].scopes"),
            conflicts_with=_as_str_tuple(
                item.get("conflicts_with", []), f"directives[{index}].conflicts_with"
            ),
            resolved=bool(item.get("resolved", True)),
        )
        directives.append(directive)

    unknown_conflict_targets = sorted(
        {
            target
            for directive in directives
            for target in directive.conflicts_with
            if target not in seen_ids
        }
    )
    if unknown_conflict_targets:
        raise ValidationError(f"conflicts_with references unknown directives: {unknown_conflict_targets}")

    events_raw = raw.get("events", [])
    if not isinstance(events_raw, list):
        raise ValidationError("events must be a list")

    events: list[Event] = []
    previous_seq = -1
    for index, item in enumerate(events_raw):
        if not isinstance(item, dict):
            raise ValidationError(f"events[{index}] must be an object")
        seq = item.get("seq")
        if not isinstance(seq, int) or seq < 0:
            raise ValidationError(f"events[{index}].seq must be a non-negative integer")
        if seq <= previous_seq:
            raise ValidationError("event seq values must be strictly increasing")
        previous_seq = seq

        directive_ids = _as_str_tuple(item.get("directive_ids", []), f"events[{index}].directive_ids")
        unknown_refs = sorted(set(directive_ids) - seen_ids)
        if unknown_refs:
            raise ValidationError(f"events[{index}] references unknown directives: {unknown_refs}")

        outcome = item.get("outcome")
        if outcome is not None:
            outcome = _require_choice(outcome, f"events[{index}].outcome", _ALLOWED_OUTCOMES)

        completion_status = item.get("completion_status")
        if completion_status is not None:
            completion_status = _require_choice(
                completion_status,
                f"events[{index}].completion_status",
                {"complete", "incomplete", "blocked", "not_verified"},
            )

        events.append(
            Event(
                seq=seq,
                actor=_as_str(item.get("actor"), f"events[{index}].actor"),
                type=_require_choice(item.get("type"), f"events[{index}].type", _ALLOWED_EVENT_TYPES),
                directive_ids=directive_ids,
                scopes=_as_str_tuple(item.get("scopes", []), f"events[{index}].scopes"),
                assumptions=_as_str_tuple(item.get("assumptions", []), f"events[{index}].assumptions"),
                outcome=outcome,
                evidence_ref=(
                    _as_str(item.get("evidence_ref"), f"events[{index}].evidence_ref")
                    if item.get("evidence_ref") is not None
                    else None
                ),
                completion_status=completion_status,
            )
        )

    return Contract(
        contract_id=contract_id,
        authorized_scopes=authorized_scopes,
        protected_scopes=protected_scopes,
        directives=tuple(directives),
        events=tuple(events),
    )
