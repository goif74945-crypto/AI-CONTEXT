from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import unicodedata
from typing import Optional, Tuple


class Effect(str, Enum):
    READ = "READ"
    REVERSIBLE_WRITE = "REVERSIBLE_WRITE"
    IRREVERSIBLE_WRITE = "IRREVERSIBLE_WRITE"
    EXTERNAL_SIDE_EFFECT = "EXTERNAL_SIDE_EFFECT"


class DecisionStatus(str, Enum):
    ALLOW = "ALLOW"
    FREEZE = "FREEZE"


HIGH_IMPACT_EFFECTS = frozenset({
    Effect.IRREVERSIBLE_WRITE,
    Effect.EXTERNAL_SIDE_EFFECT,
})


def _clean_text(value: str, field: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field} must be str")
    value = unicodedata.normalize("NFC", value).strip()
    if not value:
        raise ValueError(f"{field} must not be empty")
    if "\x00" in value:
        raise ValueError(f"{field} must not contain NUL")
    return value


@dataclass(frozen=True, slots=True)
class Action:
    resource: str
    verb: str
    effect: Effect
    destination: Optional[str] = None
    cost_units: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "resource", _clean_text(self.resource, "resource"))
        object.__setattr__(self, "verb", _clean_text(self.verb, "verb").upper())
        if self.destination is not None:
            object.__setattr__(self, "destination", _clean_text(self.destination, "destination"))
        if not isinstance(self.effect, Effect):
            object.__setattr__(self, "effect", Effect(self.effect))
        if not isinstance(self.cost_units, int) or isinstance(self.cost_units, bool):
            raise TypeError("cost_units must be int")
        if self.cost_units < 0:
            raise ValueError("cost_units must be >= 0")

    def to_dict(self) -> dict[str, object]:
        return {
            "resource": self.resource,
            "verb": self.verb,
            "effect": self.effect.value,
            "destination": self.destination,
            "cost_units": self.cost_units,
        }


@dataclass(frozen=True, slots=True)
class Plan:
    actions: Tuple[Action, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.actions, tuple):
            object.__setattr__(self, "actions", tuple(self.actions))
        if not self.actions:
            raise ValueError("plan must contain at least one action")
        for action in self.actions:
            if not isinstance(action, Action):
                raise TypeError("all plan entries must be Action")

    def to_dict(self) -> dict[str, object]:
        return {"actions": [action.to_dict() for action in self.actions]}


@dataclass(frozen=True, slots=True)
class AuthorityLease:
    lease_id: str
    subject: str
    allowed_resource_patterns: Tuple[str, ...]
    allowed_verbs: Tuple[str, ...]
    allowed_effects: Tuple[Effect, ...]
    max_cost_units: int
    max_actions: int
    issued_at_tick: int
    expires_at_tick: int
    plan_hash: str
    policy_version: str
    allow_high_impact: bool = False
    parent_lease_id: Optional[str] = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "lease_id", _clean_text(self.lease_id, "lease_id"))
        object.__setattr__(self, "subject", _clean_text(self.subject, "subject"))
        object.__setattr__(self, "plan_hash", _clean_text(self.plan_hash, "plan_hash"))
        object.__setattr__(self, "policy_version", _clean_text(self.policy_version, "policy_version"))

        patterns = tuple(_clean_text(x, "allowed_resource_pattern") for x in self.allowed_resource_patterns)
        verbs = tuple(_clean_text(x, "allowed_verb").upper() for x in self.allowed_verbs)
        effects = tuple(x if isinstance(x, Effect) else Effect(x) for x in self.allowed_effects)
        if not patterns or not verbs or not effects:
            raise ValueError("lease scope sets must not be empty")
        object.__setattr__(self, "allowed_resource_patterns", patterns)
        object.__setattr__(self, "allowed_verbs", verbs)
        object.__setattr__(self, "allowed_effects", effects)

        for name in ("max_cost_units", "max_actions", "issued_at_tick", "expires_at_tick"):
            value = getattr(self, name)
            if not isinstance(value, int) or isinstance(value, bool):
                raise TypeError(f"{name} must be int")
        if self.max_cost_units < 0:
            raise ValueError("max_cost_units must be >= 0")
        if self.max_actions <= 0:
            raise ValueError("max_actions must be > 0")
        if self.issued_at_tick < 0:
            raise ValueError("issued_at_tick must be >= 0")
        if self.expires_at_tick < self.issued_at_tick:
            raise ValueError("expires_at_tick must be >= issued_at_tick")


@dataclass(frozen=True, slots=True)
class LeaseState:
    used_actions: int = 0
    used_cost_units: int = 0
    revoked: bool = False

    def __post_init__(self) -> None:
        if self.used_actions < 0 or self.used_cost_units < 0:
            raise ValueError("lease counters must be non-negative")


@dataclass(frozen=True, slots=True)
class Decision:
    status: DecisionStatus
    reason_code: str
    lease_id: str
    action_index: int
    plan_hash: str

    @property
    def allowed(self) -> bool:
        return self.status is DecisionStatus.ALLOW


@dataclass(frozen=True, slots=True)
class DriftReport:
    changed: bool
    old_hash: str
    new_hash: str
    categories: Tuple[str, ...]
    details: Tuple[str, ...]
