from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .core import (
    ContractError,
    Finding,
    GuardDecision,
    Severity,
    _decision,
    _indexed_objects,
    _require_mapping,
    _require_str_list,
    semantic_digest,
    validate_contract_shape,
)


@dataclass(frozen=True, slots=True)
class TransitionReport:
    decision: GuardDecision
    base_digest: str
    candidate_digest: str
    change_ids: tuple[str, ...]
    findings: tuple[Finding, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision.value,
            "base_digest": self.base_digest,
            "candidate_digest": self.candidate_digest,
            "change_ids": list(self.change_ids),
            "findings": [
                {
                    "code": f.code,
                    "severity": f.severity.value,
                    "message": f.message,
                    "subject": f.subject,
                    "expected": f.expected,
                    "observed": f.observed,
                }
                for f in self.findings
            ],
        }


def _change_id(kind: str, subject: str) -> str:
    return f"{kind}:{subject}"


def _changed_keys(base: Mapping[str, Any], candidate: Mapping[str, Any]) -> list[str]:
    return sorted(set(base) | set(candidate), key=str)


def compare_contracts(
    base: Mapping[str, Any],
    candidate: Mapping[str, Any],
    approval: Mapping[str, Any] | None = None,
) -> TransitionReport:
    validate_contract_shape(base)
    validate_contract_shape(candidate)

    approved_changes: set[str] = set()
    approver = None
    if approval is not None:
        approval = _require_mapping(approval, "approval")
        approver = approval.get("approver")
        if approver not in {"user", "authorized_spec_owner"}:
            raise ContractError("approval.approver must be user or authorized_spec_owner")
        approved_changes = set(_require_str_list(approval.get("approved_change_ids", []), "approval.approved_change_ids"))

    findings: list[Finding] = []
    changes: list[str] = []

    def register(change_id: str, message: str, *, immutable: bool = False, observed: Any = None, expected: Any = None) -> None:
        changes.append(change_id)
        if change_id in approved_changes:
            findings.append(Finding(
                code="AUTHORIZED_INTENT_CHANGE",
                severity=Severity.INFO,
                message=message + " Explicit approval covers this change.",
                subject=change_id,
                expected=expected,
                observed=observed,
            ))
            return
        findings.append(Finding(
            code="IMMUTABLE_INTENT_DRIFT" if immutable else "UNAUTHORIZED_INTENT_DRIFT",
            severity=Severity.BLOCK,
            message=message,
            subject=change_id,
            expected=expected,
            observed=observed,
        ))

    if semantic_digest({"objective": base.get("objective")}) != semantic_digest({"objective": candidate.get("objective")}):
        register(
            _change_id("objective", "main"),
            "Objective changed without explicit authority.",
            observed=candidate.get("objective"),
            expected=base.get("objective"),
        )

    base_scope = _require_mapping(base.get("scope"), "scope")
    cand_scope = _require_mapping(candidate.get("scope"), "scope")
    for scope_key in ("in_scope", "out_of_scope", "protected", "allowed_repositories", "protected_repositories"):
        b = set(_require_str_list(base_scope.get(scope_key, []), f"scope.{scope_key}"))
        c = set(_require_str_list(cand_scope.get(scope_key, []), f"scope.{scope_key}"))
        for removed in sorted(b - c):
            register(
                _change_id(f"scope.{scope_key}.remove", removed),
                f"Scope constraint {removed!r} was removed.",
                immutable=scope_key in {"protected", "protected_repositories"},
                expected=removed,
                observed=None,
            )
        for added in sorted(c - b):
            register(
                _change_id(f"scope.{scope_key}.add", added),
                f"Scope constraint {added!r} was added.",
                observed=added,
                expected=None,
            )

    base_req = _indexed_objects(base.get("requirements", []), "requirements")
    cand_req = _indexed_objects(candidate.get("requirements", []), "requirements")
    for req_id in sorted(set(base_req) | set(cand_req)):
        b = base_req.get(req_id)
        c = cand_req.get(req_id)
        if b is None:
            register(
                _change_id("requirement.add", req_id),
                f"Requirement {req_id!r} was added.",
                observed=c,
            )
            continue
        if c is None:
            register(
                _change_id("requirement.remove", req_id),
                f"Requirement {req_id!r} was removed.",
                immutable=bool(b.get("immutable", False)),
                expected=b,
            )
            continue
        if semantic_digest(b) != semantic_digest(c):
            register(
                _change_id("requirement.modify", req_id),
                f"Requirement {req_id!r} was modified.",
                immutable=bool(b.get("immutable", False)),
                expected=b,
                observed=c,
            )

    base_criteria = _indexed_objects(base.get("acceptance_criteria", []), "acceptance_criteria")
    cand_criteria = _indexed_objects(candidate.get("acceptance_criteria", []), "acceptance_criteria")
    for crit_id in sorted(set(base_criteria) | set(cand_criteria)):
        b = base_criteria.get(crit_id)
        c = cand_criteria.get(crit_id)
        if b is None:
            register(_change_id("criterion.add", crit_id), f"Acceptance criterion {crit_id!r} was added.", observed=c)
        elif c is None:
            register(_change_id("criterion.remove", crit_id), f"Acceptance criterion {crit_id!r} was removed.", expected=b)
        elif semantic_digest(b) != semantic_digest(c):
            register(_change_id("criterion.modify", crit_id), f"Acceptance criterion {crit_id!r} was modified.", expected=b, observed=c)

    for key in ("stop_conditions", "unknowns", "assumptions"):
        b = set(_require_str_list(base.get(key, []), key))
        c = set(_require_str_list(candidate.get(key, []), key))
        for removed in sorted(b - c):
            register(_change_id(f"{key}.remove", removed), f"{key} entry was removed.", expected=removed)
        for added in sorted(c - b):
            register(_change_id(f"{key}.add", added), f"{key} entry was added.", observed=added)

    unrecognized_approvals = sorted(approved_changes - set(changes))
    if unrecognized_approvals:
        findings.append(Finding(
            code="STALE_OR_UNKNOWN_APPROVAL",
            severity=Severity.REVIEW,
            message="Approval references change IDs that are not present in this transition.",
            observed=unrecognized_approvals,
        ))

    if not changes:
        findings.append(Finding(
            code="NO_SEMANTIC_DRIFT",
            severity=Severity.INFO,
            message="Candidate contract is semantically identical to the base contract.",
        ))

    return TransitionReport(
        decision=_decision(findings),
        base_digest=semantic_digest(base),
        candidate_digest=semantic_digest(candidate),
        change_ids=tuple(sorted(set(changes))),
        findings=tuple(findings),
    )
