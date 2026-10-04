from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from .canon import normalize_text

EvidenceRole = Literal[
    "AUTHORITY",
    "DUPLICATE_CHECK",
    "USER_VALUE",
    "RISK",
    "ASSUMPTION",
    "OTHER",
]

ALLOWED_EVIDENCE_ROLES = {
    "AUTHORITY",
    "DUPLICATE_CHECK",
    "USER_VALUE",
    "RISK",
    "ASSUMPTION",
    "OTHER",
}

TruthClass = Literal[
    "SOURCE_FACT",
    "REPO_FACT",
    "RUNTIME_FACT",
    "EXTERNAL_FACT",
    "INFERENCE",
    "ASSUMPTION",
    "UNKNOWN",
    "NOT_VERIFIED",
]

EVIDENCE_KEYS = {"ref_id", "role", "truth_class", "claim", "locator"}
PROPOSAL_KEYS = {
    "proposal_id", "version", "status", "title", "summary", "problem",
    "intended_users", "user_outcomes", "proposed_capabilities",
    "integration_surfaces", "non_goals", "risks", "assumptions",
    "authority_references", "evidence", "authority_conflicts",
}

ALLOWED_TRUTH_CLASSES = {
    "SOURCE_FACT",
    "REPO_FACT",
    "RUNTIME_FACT",
    "EXTERNAL_FACT",
    "INFERENCE",
    "ASSUMPTION",
    "UNKNOWN",
    "NOT_VERIFIED",
}

PROPOSAL_STATUS = "AI_PROPOSED_CONCEPT"


class ProposalValidationError(ValueError):
    def __init__(self, errors: list[str]):
        self.errors = tuple(errors)
        super().__init__("; ".join(errors))


def _nonempty_str(data: dict[str, Any], key: str, errors: list[str]) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not normalize_text(value):
        errors.append(f"{key}: required non-empty string")
        return ""
    return normalize_text(value)


def _str_list(data: dict[str, Any], key: str, errors: list[str], *, min_items: int = 0) -> tuple[str, ...]:
    value = data.get(key)
    if not isinstance(value, list):
        errors.append(f"{key}: required list")
        return ()
    out: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not normalize_text(item):
            errors.append(f"{key}[{index}]: required non-empty string")
            continue
        normalized = normalize_text(item)
        if normalized not in out:
            out.append(normalized)
    if len(out) < min_items:
        errors.append(f"{key}: requires at least {min_items} item(s)")
    return tuple(out)


@dataclass(frozen=True, slots=True)
class EvidenceRef:
    ref_id: str
    role: EvidenceRole
    truth_class: TruthClass
    claim: str
    locator: str

    @classmethod
    def from_dict(cls, data: Any, *, index: int, errors: list[str]) -> "EvidenceRef | None":
        if not isinstance(data, dict):
            errors.append(f"evidence[{index}]: required object")
            return None
        local: list[str] = []
        unknown = sorted(set(data) - EVIDENCE_KEYS)
        if unknown:
            local.append(f"unknown field(s): {', '.join(unknown)}")
        ref_id = _nonempty_str(data, "ref_id", local)
        claim = _nonempty_str(data, "claim", local)
        locator = _nonempty_str(data, "locator", local)
        role = data.get("role")
        if role not in ALLOWED_EVIDENCE_ROLES:
            local.append(
                f"role: must be one of {', '.join(sorted(ALLOWED_EVIDENCE_ROLES))}"
            )
            role = "OTHER"
        truth_class = data.get("truth_class")
        if truth_class not in ALLOWED_TRUTH_CLASSES:
            local.append(
                f"truth_class: must be one of {', '.join(sorted(ALLOWED_TRUTH_CLASSES))}"
            )
            truth_class = "UNKNOWN"
        errors.extend(f"evidence[{index}].{message}" for message in local)
        if local:
            return None
        return cls(
            ref_id=ref_id,
            role=role,
            truth_class=truth_class,
            claim=claim,
            locator=locator,
        )

    def to_dict(self) -> dict[str, str]:
        return {
            "ref_id": self.ref_id,
            "role": self.role,
            "truth_class": self.truth_class,
            "claim": self.claim,
            "locator": self.locator,
        }


@dataclass(frozen=True, slots=True)
class Proposal:
    proposal_id: str
    version: str
    status: str
    title: str
    summary: str
    problem: str
    intended_users: tuple[str, ...]
    user_outcomes: tuple[str, ...]
    proposed_capabilities: tuple[str, ...]
    integration_surfaces: tuple[str, ...]
    non_goals: tuple[str, ...]
    risks: tuple[str, ...]
    assumptions: tuple[str, ...]
    authority_references: tuple[str, ...]
    evidence: tuple[EvidenceRef, ...]
    authority_conflicts: tuple[str, ...]

    @classmethod
    def from_dict(cls, data: Any) -> "Proposal":
        if not isinstance(data, dict):
            raise ProposalValidationError(["proposal: required object"])

        errors: list[str] = []
        unknown = sorted(set(data) - PROPOSAL_KEYS)
        if unknown:
            errors.append(f"proposal: unknown field(s): {', '.join(unknown)}")
        proposal_id = _nonempty_str(data, "proposal_id", errors)
        version = _nonempty_str(data, "version", errors)
        status = _nonempty_str(data, "status", errors)
        title = _nonempty_str(data, "title", errors)
        summary = _nonempty_str(data, "summary", errors)
        problem = _nonempty_str(data, "problem", errors)

        intended_users = _str_list(data, "intended_users", errors, min_items=1)
        user_outcomes = _str_list(data, "user_outcomes", errors, min_items=1)
        proposed_capabilities = _str_list(data, "proposed_capabilities", errors, min_items=1)
        integration_surfaces = _str_list(data, "integration_surfaces", errors, min_items=1)
        non_goals = _str_list(data, "non_goals", errors)
        risks = _str_list(data, "risks", errors, min_items=1)
        assumptions = _str_list(data, "assumptions", errors)
        authority_references = _str_list(data, "authority_references", errors, min_items=1)
        authority_conflicts = _str_list(data, "authority_conflicts", errors)

        raw_evidence = data.get("evidence")
        evidence: list[EvidenceRef] = []
        if not isinstance(raw_evidence, list):
            errors.append("evidence: required list")
        else:
            seen_ref_ids: set[str] = set()
            for index, item in enumerate(raw_evidence):
                parsed = EvidenceRef.from_dict(item, index=index, errors=errors)
                if parsed is not None:
                    if parsed.ref_id in seen_ref_ids:
                        errors.append(f"evidence[{index}].ref_id: duplicate id {parsed.ref_id!r}")
                    else:
                        seen_ref_ids.add(parsed.ref_id)
                        evidence.append(parsed)

        if status and status != PROPOSAL_STATUS:
            errors.append(f"status: must equal {PROPOSAL_STATUS}")

        if proposal_id and any(ch.isspace() for ch in proposal_id):
            errors.append("proposal_id: whitespace is forbidden")

        if errors:
            raise ProposalValidationError(errors)

        return cls(
            proposal_id=proposal_id,
            version=version,
            status=status,
            title=title,
            summary=summary,
            problem=problem,
            intended_users=intended_users,
            user_outcomes=user_outcomes,
            proposed_capabilities=proposed_capabilities,
            integration_surfaces=integration_surfaces,
            non_goals=non_goals,
            risks=risks,
            assumptions=assumptions,
            authority_references=authority_references,
            evidence=tuple(evidence),
            authority_conflicts=authority_conflicts,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "version": self.version,
            "status": self.status,
            "title": self.title,
            "summary": self.summary,
            "problem": self.problem,
            "intended_users": list(self.intended_users),
            "user_outcomes": list(self.user_outcomes),
            "proposed_capabilities": list(self.proposed_capabilities),
            "integration_surfaces": list(self.integration_surfaces),
            "non_goals": list(self.non_goals),
            "risks": list(self.risks),
            "assumptions": list(self.assumptions),
            "authority_references": list(self.authority_references),
            "evidence": [item.to_dict() for item in self.evidence],
            "authority_conflicts": list(self.authority_conflicts),
        }
