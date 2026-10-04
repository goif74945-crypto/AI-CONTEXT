from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Mapping, Any


_EVENT_RE = re.compile(r"^[a-z][a-z0-9_]{2,63}$")
_FORBIDDEN = frozenset({
    "pass" + "word", "pass" + "wd", "sec" + "ret", "to" + "ken",
    "access" + "_" + "to" + "ken", "refresh" + "_" + "to" + "ken",
    "api" + "_" + "key", "api" + "key", "author" + "ization",
    "coo" + "kie", "session" + "_" + "coo" + "kie", "private" + "_" + "key",
})


@dataclass(frozen=True, slots=True)
class EventContract:
    name: str
    required_properties: frozenset[str]
    optional_properties: frozenset[str] = frozenset()


def validate_event_contract(contract: EventContract) -> tuple[str, ...]:
    errors: list[str] = []
    if not _EVENT_RE.fullmatch(contract.name):
        errors.append("EVENT_NAME_INVALID")
    overlap = contract.required_properties & contract.optional_properties
    if overlap:
        errors.append("PROPERTY_CLASS_OVERLAP:" + ",".join(sorted(overlap)))
    forbidden = (contract.required_properties | contract.optional_properties) & _FORBIDDEN
    if forbidden:
        errors.append("FORBIDDEN_PROPERTY:" + ",".join(sorted(forbidden)))
    return tuple(errors)


def validate_event_payload(contract: EventContract, payload: Mapping[str, Any]) -> tuple[str, ...]:
    errors = list(validate_event_contract(contract))
    keys = frozenset(str(k) for k in payload.keys())
    missing = contract.required_properties - keys
    if missing:
        errors.append("MISSING_PROPERTY:" + ",".join(sorted(missing)))
    forbidden = keys & _FORBIDDEN
    if forbidden:
        errors.append("FORBIDDEN_PROPERTY:" + ",".join(sorted(forbidden)))
    allowed = contract.required_properties | contract.optional_properties
    unexpected = keys - allowed
    if unexpected:
        errors.append("UNEXPECTED_PROPERTY:" + ",".join(sorted(unexpected)))
    return tuple(errors)
