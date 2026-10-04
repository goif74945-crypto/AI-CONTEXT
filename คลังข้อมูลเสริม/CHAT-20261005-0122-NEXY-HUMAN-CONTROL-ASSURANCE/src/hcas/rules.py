from __future__ import annotations

from dataclasses import dataclass


READ_ONLY = "READ_ONLY"
REVERSIBLE_WRITE = "REVERSIBLE_WRITE"
DURABLE_WRITE = "DURABLE_WRITE"
EXTERNAL_COMMUNICATION = "EXTERNAL_COMMUNICATION"
PRIVILEGE_CHANGE = "PRIVILEGE_CHANGE"
DESTRUCTIVE = "DESTRUCTIVE"
FINANCIAL_OR_LEGAL = "FINANCIAL_OR_LEGAL"

SIDE_EFFECT_CLASSES = frozenset(
    {
        READ_ONLY,
        REVERSIBLE_WRITE,
        DURABLE_WRITE,
        EXTERNAL_COMMUNICATION,
        PRIVILEGE_CHANGE,
        DESTRUCTIVE,
        FINANCIAL_OR_LEGAL,
    }
)

MUTATING_CLASSES = SIDE_EFFECT_CLASSES - {READ_ONLY}
HIGH_IMPACT_CLASSES = frozenset({PRIVILEGE_CHANGE, DESTRUCTIVE, FINANCIAL_OR_LEGAL})
CONFIRMATION_VALUES = frozenset({"NONE", "EXPLICIT", "EXPLICIT_TYPED", "DUAL_APPROVAL"})
EVIDENCE_CLASSES = frozenset({"E0", "E1", "E2", "E3", "E4", "E5", "E6", "E7"})
FAILURE_MODES = frozenset({"BLOCK", "FREEZE", "FREEZE_OR_BLOCK"})
REQUIRED_VISIBLE_OUTCOMES = frozenset({"SUCCESS", "BLOCKED"})


@dataclass(frozen=True, slots=True)
class ProfilePolicy:
    name: str
    high_impact_confirmation: frozenset[str]
    require_dual_approval_for: frozenset[str]
    require_freeze_surface: bool = True
    require_pending_not_evidence: bool = True


PROFILES: dict[str, ProfilePolicy] = {
    "current_vnext": ProfilePolicy(
        name="current_vnext",
        high_impact_confirmation=frozenset({"EXPLICIT", "EXPLICIT_TYPED", "DUAL_APPROVAL"}),
        require_dual_approval_for=frozenset(),
    ),
    "strict_future": ProfilePolicy(
        name="strict_future",
        high_impact_confirmation=frozenset({"EXPLICIT_TYPED", "DUAL_APPROVAL"}),
        require_dual_approval_for=frozenset({DESTRUCTIVE, PRIVILEGE_CHANGE}),
    ),
}
