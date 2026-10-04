from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .core import (
    ContractError,
    Finding,
    GuardDecision,
    Severity,
    _decision,
    _require_mapping,
    _require_nonempty_str,
    evaluate_proposal,
    semantic_digest,
)


@dataclass(frozen=True, slots=True)
class ExecutionSeal:
    target_repository: str
    target_ref: str
    target_revision: str
    contract_digest: str
    proposal_digest: str
    seal_digest: str

    def to_dict(self) -> dict[str, str]:
        return {
            "target_repository": self.target_repository,
            "target_ref": self.target_ref,
            "target_revision": self.target_revision,
            "contract_digest": self.contract_digest,
            "proposal_digest": self.proposal_digest,
            "seal_digest": self.seal_digest,
        }


@dataclass(frozen=True, slots=True)
class SealVerificationReport:
    decision: GuardDecision
    findings: tuple[Finding, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision.value,
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


def _seal_payload(
    *,
    target_repository: str,
    target_ref: str,
    target_revision: str,
    contract_digest: str,
    proposal_digest: str,
) -> dict[str, str]:
    return {
        "target_repository": target_repository,
        "target_ref": target_ref,
        "target_revision": target_revision,
        "contract_digest": contract_digest,
        "proposal_digest": proposal_digest,
    }


def create_execution_seal(
    contract: Mapping[str, Any],
    proposal: Mapping[str, Any],
    *,
    target_revision: str,
    target_ref: str = "main",
) -> ExecutionSeal:
    """Bind a passing proposal to one exact repository state.

    This is a TOCTOU precondition record, not an authorization token and not a
    cryptographic identity proof. Production use would need authenticated repo
    identity and signed authority envelopes.
    """

    report = evaluate_proposal(contract, proposal)
    if report.decision is not GuardDecision.PASS:
        raise ContractError(
            "Execution seal can only be created from a PASS proposal; "
            f"observed {report.decision.value}"
        )

    target_repository = _require_nonempty_str(
        proposal.get("target_repository"), "proposal.target_repository"
    )
    target_ref = _require_nonempty_str(target_ref, "target_ref")
    target_revision = _require_nonempty_str(target_revision, "target_revision")

    payload = _seal_payload(
        target_repository=target_repository,
        target_ref=target_ref,
        target_revision=target_revision,
        contract_digest=report.contract_digest,
        proposal_digest=report.proposal_digest,
    )
    return ExecutionSeal(**payload, seal_digest=semantic_digest(payload))


def execution_seal_from_mapping(value: Mapping[str, Any]) -> ExecutionSeal:
    value = _require_mapping(value, "seal")
    fields = (
        "target_repository",
        "target_ref",
        "target_revision",
        "contract_digest",
        "proposal_digest",
        "seal_digest",
    )
    parsed = {field: _require_nonempty_str(value.get(field), f"seal.{field}") for field in fields}
    return ExecutionSeal(**parsed)


def verify_execution_seal(
    seal: ExecutionSeal | Mapping[str, Any],
    contract: Mapping[str, Any],
    proposal: Mapping[str, Any],
    *,
    current_repository: str,
    current_ref: str,
    current_revision: str,
) -> SealVerificationReport:
    if not isinstance(seal, ExecutionSeal):
        seal = execution_seal_from_mapping(seal)

    current_repository = _require_nonempty_str(current_repository, "current_repository")
    current_ref = _require_nonempty_str(current_ref, "current_ref")
    current_revision = _require_nonempty_str(current_revision, "current_revision")

    findings: list[Finding] = []

    expected_payload = _seal_payload(
        target_repository=seal.target_repository,
        target_ref=seal.target_ref,
        target_revision=seal.target_revision,
        contract_digest=seal.contract_digest,
        proposal_digest=seal.proposal_digest,
    )
    expected_seal_digest = semantic_digest(expected_payload)
    if seal.seal_digest != expected_seal_digest:
        findings.append(Finding(
            code="SEAL_INTEGRITY_MISMATCH",
            severity=Severity.BLOCK,
            message="Execution seal content does not match its deterministic digest.",
            expected=expected_seal_digest,
            observed=seal.seal_digest,
        ))

    current_contract_digest = semantic_digest(contract)
    if current_contract_digest != seal.contract_digest:
        findings.append(Finding(
            code="STALE_CONTRACT_DIGEST",
            severity=Severity.BLOCK,
            message="The active contract differs from the contract bound to the execution seal.",
            expected=seal.contract_digest,
            observed=current_contract_digest,
        ))

    current_proposal_digest = semantic_digest(proposal)
    if current_proposal_digest != seal.proposal_digest:
        findings.append(Finding(
            code="STALE_PROPOSAL_DIGEST",
            severity=Severity.BLOCK,
            message="The execution proposal differs from the proposal bound to the execution seal.",
            expected=seal.proposal_digest,
            observed=current_proposal_digest,
        ))

    if current_repository.casefold() != seal.target_repository.casefold():
        findings.append(Finding(
            code="REPOSITORY_IDENTITY_CHANGED",
            severity=Severity.BLOCK,
            message="Repository identity changed after precondition validation.",
            expected=seal.target_repository,
            observed=current_repository,
        ))

    if current_ref != seal.target_ref:
        findings.append(Finding(
            code="REPOSITORY_REF_CHANGED",
            severity=Severity.BLOCK,
            message="Repository ref changed after precondition validation.",
            expected=seal.target_ref,
            observed=current_ref,
        ))

    if current_revision != seal.target_revision:
        findings.append(Finding(
            code="REPOSITORY_REVISION_CHANGED",
            severity=Severity.BLOCK,
            message="Repository revision changed after precondition validation; re-validate before mutation.",
            expected=seal.target_revision,
            observed=current_revision,
        ))

    proposal_report = evaluate_proposal(contract, proposal)
    if proposal_report.decision is not GuardDecision.PASS:
        findings.append(Finding(
            code="PROPOSAL_NO_LONGER_PASSES",
            severity=Severity.BLOCK,
            message="The proposal no longer satisfies the active intent contract.",
            expected=GuardDecision.PASS.value,
            observed=proposal_report.decision.value,
        ))

    if not findings:
        findings.append(Finding(
            code="EXECUTION_SEAL_VALID",
            severity=Severity.INFO,
            message="Contract, proposal, repository identity, ref, and revision still match the validated execution state.",
        ))

    return SealVerificationReport(decision=_decision(findings), findings=tuple(findings))
