from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from .errors import ValidationError


@dataclass(frozen=True, slots=True)
class Profile:
    schema_version: str
    profile_id: str
    profile_status: str
    transition_kind: str
    execution_start_kind: str
    release_kinds: frozenset[str]
    freeze_state: str
    stop_state: str
    allowed_transitions: frozenset[tuple[str, str]]
    authority_sources: tuple[str, ...]

    @classmethod
    def from_raw(cls, raw: Mapping[str, Any]) -> "Profile":
        if not isinstance(raw, Mapping):
            raise ValidationError("profile must be an object")
        expected = {
            "schema_version",
            "profile_id",
            "profile_status",
            "transition_kind",
            "execution_start_kind",
            "release_kinds",
            "freeze_state",
            "stop_state",
            "allowed_transitions",
            "authority_sources",
        }
        unknown = set(raw) - expected
        if unknown:
            raise ValidationError("unknown profile fields: " + ", ".join(sorted(unknown)))

        def nonempty(key: str) -> str:
            value = raw.get(key)
            if not isinstance(value, str) or not value.strip():
                raise ValidationError(f"profile.{key} must be a non-empty string")
            return value

        schema_version = nonempty("schema_version")
        if schema_version != "nfwm.profile.v1":
            raise ValidationError("profile.schema_version must equal 'nfwm.profile.v1'")

        release = raw.get("release_kinds")
        if not isinstance(release, Sequence) or isinstance(release, (str, bytes)) or not release:
            raise ValidationError("profile.release_kinds must be a non-empty array")
        if any(not isinstance(x, str) or not x for x in release):
            raise ValidationError("profile.release_kinds entries must be non-empty strings")

        transitions = raw.get("allowed_transitions")
        if not isinstance(transitions, Sequence) or isinstance(transitions, (str, bytes)):
            raise ValidationError("profile.allowed_transitions must be an array")
        normalized: list[tuple[str, str]] = []
        for pair in transitions:
            if (
                not isinstance(pair, Sequence)
                or isinstance(pair, (str, bytes))
                or len(pair) != 2
                or any(not isinstance(x, str) or not x for x in pair)
            ):
                raise ValidationError("each allowed transition must be [from, to]")
            normalized.append((pair[0], pair[1]))

        sources = raw.get("authority_sources")
        if not isinstance(sources, Sequence) or isinstance(sources, (str, bytes)) or not sources:
            raise ValidationError("profile.authority_sources must be a non-empty array")
        if any(not isinstance(x, str) or not x for x in sources):
            raise ValidationError("profile.authority_sources entries must be strings")

        return cls(
            schema_version=schema_version,
            profile_id=nonempty("profile_id"),
            profile_status=nonempty("profile_status"),
            transition_kind=nonempty("transition_kind"),
            execution_start_kind=nonempty("execution_start_kind"),
            release_kinds=frozenset(release),
            freeze_state=nonempty("freeze_state"),
            stop_state=nonempty("stop_state"),
            allowed_transitions=frozenset(normalized),
            authority_sources=tuple(sources),
        )

    def to_raw(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "profile_id": self.profile_id,
            "profile_status": self.profile_status,
            "transition_kind": self.transition_kind,
            "execution_start_kind": self.execution_start_kind,
            "release_kinds": sorted(self.release_kinds),
            "freeze_state": self.freeze_state,
            "stop_state": self.stop_state,
            "allowed_transitions": [list(x) for x in sorted(self.allowed_transitions)],
            "authority_sources": list(self.authority_sources),
        }


def load_profile(path: str | Path) -> Profile:
    with Path(path).open("r", encoding="utf-8") as f:
        raw = json.load(f)
    return Profile.from_raw(raw)
