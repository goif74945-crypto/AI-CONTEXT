from __future__ import annotations

import fnmatch
import hashlib
import json
import unicodedata
from dataclasses import dataclass, field
from enum import Enum
from pathlib import PurePosixPath
from typing import Any, Iterable, Mapping, Sequence


class GuardDecision(str, Enum):
    PASS = "PASS"
    REVIEW = "REVIEW"
    FREEZE = "FREEZE"


class Severity(str, Enum):
    INFO = "INFO"
    REVIEW = "REVIEW"
    BLOCK = "BLOCK"


class EvidenceClass(str, Enum):
    NONE = "none"
    INSPECTION = "inspection"
    STATIC = "static"
    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"
    RUNTIME = "runtime"
    DEPLOYMENT = "deployment"
    PHYSICAL = "physical"


_EVIDENCE_RANK: dict[EvidenceClass, int] = {
    EvidenceClass.NONE: 0,
    EvidenceClass.INSPECTION: 10,
    EvidenceClass.STATIC: 20,
    EvidenceClass.UNIT: 30,
    EvidenceClass.INTEGRATION: 40,
    EvidenceClass.E2E: 50,
    EvidenceClass.RUNTIME: 60,
    EvidenceClass.DEPLOYMENT: 70,
    EvidenceClass.PHYSICAL: 80,
}


@dataclass(frozen=True, slots=True)
class Finding:
    code: str
    severity: Severity
    message: str
    subject: str | None = None
    expected: Any = None
    observed: Any = None


@dataclass(frozen=True, slots=True)
class GuardReport:
    decision: GuardDecision
    contract_digest: str
    proposal_digest: str
    findings: tuple[Finding, ...] = field(default_factory=tuple)

    @property
    def blocked(self) -> bool:
        return self.decision is GuardDecision.FREEZE

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision.value,
            "contract_digest": self.contract_digest,
            "proposal_digest": self.proposal_digest,
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


class ContractError(ValueError):
    pass


def _normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFC", value)
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip() for line in value.split("\n")).strip()


def _canonicalize(value: Any) -> Any:
    if isinstance(value, str):
        return _normalize_text(value)
    if isinstance(value, Mapping):
        return {str(k): _canonicalize(value[k]) for k in sorted(value, key=str)}
    if isinstance(value, (list, tuple)):
        items = [_canonicalize(v) for v in value]
        if all(isinstance(v, Mapping) and "id" in v for v in items):
            return sorted(items, key=lambda v: str(v["id"]))
        if all(isinstance(v, str) for v in items):
            return sorted(items)
        return items
    if value is None or isinstance(value, (bool, int, float)):
        return value
    raise TypeError(f"Unsupported canonical value: {type(value).__name__}")


def canonical_json(value: Any) -> str:
    return json.dumps(
        _canonicalize(value),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def semantic_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _require_mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ContractError(f"{label} must be an object")
    return value


def _require_nonempty_str(value: Any, label: str) -> str:
    if not isinstance(value, str) or not _normalize_text(value):
        raise ContractError(f"{label} must be a non-empty string")
    return _normalize_text(value)


def _require_str_list(value: Any, label: str) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise ContractError(f"{label} must be an array of strings")
    result: list[str] = []
    for idx, item in enumerate(value):
        result.append(_require_nonempty_str(item, f"{label}[{idx}]"))
    if len(result) != len(set(result)):
        raise ContractError(f"{label} contains duplicate entries")
    return tuple(result)


def _indexed_objects(value: Any, label: str) -> dict[str, Mapping[str, Any]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise ContractError(f"{label} must be an array")
    result: dict[str, Mapping[str, Any]] = {}
    for idx, raw in enumerate(value):
        item = _require_mapping(raw, f"{label}[{idx}]")
        item_id = _require_nonempty_str(item.get("id"), f"{label}[{idx}].id")
        if item_id in result:
            raise ContractError(f"{label} contains duplicate id {item_id!r}")
        result[item_id] = item
    return result


def _normalize_path(path: str) -> str:
    p = _normalize_text(path).replace("\\", "/")
    while "//" in p:
        p = p.replace("//", "/")
    if p.startswith("/"):
        p = p[1:]
    norm = str(PurePosixPath(p))
    if norm == ".":
        return ""
    if norm == ".." or norm.startswith("../"):
        raise ContractError(f"Path escapes root: {path!r}")
    return norm


def _matches(path: str, patterns: Iterable[str]) -> bool:
    normalized = _normalize_path(path)
    for raw_pattern in patterns:
        pattern = _normalize_path(raw_pattern)
        if fnmatch.fnmatchcase(normalized, pattern):
            return True
        if pattern.endswith("/**"):
            prefix = pattern[:-3].rstrip("/")
            if normalized == prefix or normalized.startswith(prefix + "/"):
                return True
    return False


def _decision(findings: Sequence[Finding]) -> GuardDecision:
    if any(f.severity is Severity.BLOCK for f in findings):
        return GuardDecision.FREEZE
    if any(f.severity is Severity.REVIEW for f in findings):
        return GuardDecision.REVIEW
    return GuardDecision.PASS


def _evidence_rank(value: str, label: str) -> int:
    try:
        return _EVIDENCE_RANK[EvidenceClass(value)]
    except ValueError as exc:
        allowed = ", ".join(e.value for e in EvidenceClass)
        raise ContractError(f"{label} has unsupported evidence class {value!r}; allowed: {allowed}") from exc


def validate_contract_shape(contract: Mapping[str, Any]) -> None:
    _require_nonempty_str(contract.get("schema_version"), "schema_version")
    _require_nonempty_str(contract.get("contract_id"), "contract_id")
    _require_nonempty_str(contract.get("objective"), "objective")

    scope = _require_mapping(contract.get("scope"), "scope")
    _require_str_list(scope.get("in_scope", []), "scope.in_scope")
    _require_str_list(scope.get("out_of_scope", []), "scope.out_of_scope")
    _require_str_list(scope.get("protected", []), "scope.protected")
    _require_str_list(scope.get("allowed_repositories", []), "scope.allowed_repositories")
    _require_str_list(scope.get("protected_repositories", []), "scope.protected_repositories")

    requirements = _indexed_objects(contract.get("requirements", []), "requirements")
    for req_id, req in requirements.items():
        _require_nonempty_str(req.get("text"), f"requirements[{req_id}].text")
        kind = _require_nonempty_str(req.get("kind"), f"requirements[{req_id}].kind")
        if kind not in {"must", "must_not", "should"}:
            raise ContractError(f"requirements[{req_id}].kind must be must, must_not, or should")
        if not isinstance(req.get("immutable", False), bool):
            raise ContractError(f"requirements[{req_id}].immutable must be boolean")

    criteria = _indexed_objects(contract.get("acceptance_criteria", []), "acceptance_criteria")
    for crit_id, crit in criteria.items():
        _require_nonempty_str(crit.get("text"), f"acceptance_criteria[{crit_id}].text")
        ev = _require_nonempty_str(crit.get("minimum_evidence"), f"acceptance_criteria[{crit_id}].minimum_evidence")
        _evidence_rank(ev, f"acceptance_criteria[{crit_id}].minimum_evidence")
        linked = _require_str_list(crit.get("requirement_ids", []), f"acceptance_criteria[{crit_id}].requirement_ids")
        missing = [rid for rid in linked if rid not in requirements]
        if missing:
            raise ContractError(f"acceptance_criteria[{crit_id}] references unknown requirements: {missing}")

    _require_str_list(contract.get("stop_conditions", []), "stop_conditions")
    _require_str_list(contract.get("unknowns", []), "unknowns")
    _require_str_list(contract.get("assumptions", []), "assumptions")


def validate_proposal_shape(proposal: Mapping[str, Any]) -> None:
    _require_nonempty_str(proposal.get("proposal_id"), "proposal_id")
    _require_nonempty_str(proposal.get("target_repository"), "target_repository")
    _require_str_list(proposal.get("touch_paths", []), "touch_paths")
    _require_str_list(proposal.get("covered_requirement_ids", []), "covered_requirement_ids")
    _require_str_list(proposal.get("resolved_unknowns", []), "resolved_unknowns")

    evidence = proposal.get("evidence", {})
    evidence = _require_mapping(evidence, "evidence")
    for criterion_id, evidence_class in evidence.items():
        ev = _require_nonempty_str(evidence_class, f"evidence[{criterion_id}]")
        _evidence_rank(ev, f"evidence[{criterion_id}]")

    claims = _indexed_objects(proposal.get("claims", []), "claims")
    for claim_id, claim in claims.items():
        truth = _require_nonempty_str(claim.get("truth_class"), f"claims[{claim_id}].truth_class")
        if truth not in {
            "SOURCE_FACT",
            "REPO_FACT",
            "RUNTIME_FACT",
            "EXTERNAL_FACT",
            "INFERENCE",
            "ASSUMPTION",
            "UNKNOWN",
            "NOT_VERIFIED",
        }:
            raise ContractError(f"claims[{claim_id}].truth_class is unsupported")
        _require_nonempty_str(claim.get("basis"), f"claims[{claim_id}].basis")


def evaluate_proposal(contract: Mapping[str, Any], proposal: Mapping[str, Any]) -> GuardReport:
    validate_contract_shape(contract)
    validate_proposal_shape(proposal)

    contract_digest = semantic_digest(contract)
    proposal_digest = semantic_digest(proposal)
    findings: list[Finding] = []

    requirements = _indexed_objects(contract.get("requirements", []), "requirements")
    criteria = _indexed_objects(contract.get("acceptance_criteria", []), "acceptance_criteria")
    scope = _require_mapping(contract["scope"], "scope")

    in_scope = _require_str_list(scope.get("in_scope", []), "scope.in_scope")
    out_of_scope = _require_str_list(scope.get("out_of_scope", []), "scope.out_of_scope")
    protected = _require_str_list(scope.get("protected", []), "scope.protected")
    allowed_repositories = _require_str_list(scope.get("allowed_repositories", []), "scope.allowed_repositories")
    protected_repositories = _require_str_list(scope.get("protected_repositories", []), "scope.protected_repositories")
    touch_paths = _require_str_list(proposal.get("touch_paths", []), "touch_paths")
    target_repository = _require_nonempty_str(proposal.get("target_repository"), "target_repository")

    def repository_matches(patterns: Iterable[str]) -> bool:
        target = target_repository.casefold()
        return any(fnmatch.fnmatchcase(target, pattern.casefold()) for pattern in patterns)

    if repository_matches(protected_repositories):
        findings.append(Finding(
            code="PROTECTED_REPOSITORY_TARGET",
            severity=Severity.BLOCK,
            message="Proposal targets a protected repository identity.",
            subject=target_repository,
            expected="repository must not match protected repository patterns",
            observed=target_repository,
        ))
    elif allowed_repositories and not repository_matches(allowed_repositories):
        findings.append(Finding(
            code="UNAUTHORIZED_REPOSITORY_TARGET",
            severity=Severity.BLOCK,
            message="Proposal targets a repository not present in the allowed repository boundary.",
            subject=target_repository,
            expected=list(allowed_repositories),
            observed=target_repository,
        ))

    for path in touch_paths:
        normalized = _normalize_path(path)
        if _matches(normalized, protected):
            findings.append(Finding(
                code="PROTECTED_SCOPE_TOUCH",
                severity=Severity.BLOCK,
                message="Proposal touches protected scope.",
                subject=normalized,
                expected="path must not match protected patterns",
                observed=normalized,
            ))
            continue
        if _matches(normalized, out_of_scope):
            findings.append(Finding(
                code="OUT_OF_SCOPE_TOUCH",
                severity=Severity.BLOCK,
                message="Proposal touches explicitly out-of-scope path.",
                subject=normalized,
                expected="path must remain outside proposal touch set",
                observed=normalized,
            ))
            continue
        if in_scope and not _matches(normalized, in_scope):
            findings.append(Finding(
                code="UNAUTHORIZED_SCOPE_EXPANSION",
                severity=Severity.BLOCK,
                message="Proposal touches a path not authorized by in-scope patterns.",
                subject=normalized,
                expected=list(in_scope),
                observed=normalized,
            ))

    covered = set(_require_str_list(proposal.get("covered_requirement_ids", []), "covered_requirement_ids"))
    required_ids = {
        req_id
        for req_id, req in requirements.items()
        if req.get("kind") in {"must", "must_not"}
    }
    unknown_req_ids = sorted(covered - set(requirements))
    if unknown_req_ids:
        findings.append(Finding(
            code="UNKNOWN_REQUIREMENT_REFERENCE",
            severity=Severity.BLOCK,
            message="Proposal claims coverage for unknown requirement identifiers.",
            observed=unknown_req_ids,
        ))

    missing_required = sorted(required_ids - covered)
    if missing_required:
        findings.append(Finding(
            code="REQUIREMENT_COVERAGE_GAP",
            severity=Severity.BLOCK,
            message="Proposal omits one or more mandatory requirements.",
            expected=sorted(required_ids),
            observed=sorted(covered),
        ))

    evidence = _require_mapping(proposal.get("evidence", {}), "evidence")
    for crit_id, criterion in criteria.items():
        minimum = _require_nonempty_str(criterion.get("minimum_evidence"), f"acceptance_criteria[{crit_id}].minimum_evidence")
        observed = evidence.get(crit_id)
        if observed is None:
            findings.append(Finding(
                code="MISSING_ACCEPTANCE_EVIDENCE",
                severity=Severity.BLOCK,
                message="Required acceptance evidence is missing.",
                subject=crit_id,
                expected=minimum,
                observed=None,
            ))
            continue
        observed_str = _require_nonempty_str(observed, f"evidence[{crit_id}]")
        if _evidence_rank(observed_str, f"evidence[{crit_id}]") < _evidence_rank(minimum, f"acceptance_criteria[{crit_id}].minimum_evidence"):
            findings.append(Finding(
                code="EVIDENCE_DOWNGRADE",
                severity=Severity.BLOCK,
                message="Observed evidence class is weaker than the contract requires.",
                subject=crit_id,
                expected=minimum,
                observed=observed_str,
            ))

    unknown_criteria = sorted(set(evidence) - set(criteria))
    if unknown_criteria:
        findings.append(Finding(
            code="UNBOUND_EVIDENCE",
            severity=Severity.REVIEW,
            message="Proposal includes evidence for unknown acceptance criteria.",
            observed=unknown_criteria,
        ))

    unknowns = set(_require_str_list(contract.get("unknowns", []), "unknowns"))
    resolved_unknowns = set(_require_str_list(proposal.get("resolved_unknowns", []), "resolved_unknowns"))
    nonexistent_resolutions = sorted(resolved_unknowns - unknowns)
    if nonexistent_resolutions:
        findings.append(Finding(
            code="UNKNOWN_RESOLUTION_REFERENCE",
            severity=Severity.REVIEW,
            message="Proposal marks unknowns resolved that are not present in the contract.",
            observed=nonexistent_resolutions,
        ))

    claims = _indexed_objects(proposal.get("claims", []), "claims")
    for claim_id, claim in claims.items():
        truth_class = _require_nonempty_str(claim.get("truth_class"), f"claims[{claim_id}].truth_class")
        basis = _require_nonempty_str(claim.get("basis"), f"claims[{claim_id}].basis")
        basis_lower = basis.casefold()
        if truth_class.endswith("FACT") and ("assumption" in basis_lower or "guess" in basis_lower):
            findings.append(Finding(
                code="ASSUMPTION_ESCALATED_TO_FACT",
                severity=Severity.BLOCK,
                message="A claim labeled as fact is explicitly based on an assumption/guess.",
                subject=claim_id,
                expected="fact claim requires non-assumption basis",
                observed={"truth_class": truth_class, "basis": basis},
            ))
        if truth_class == "NOT_VERIFIED" and claim.get("completion_claim") is True:
            findings.append(Finding(
                code="UNVERIFIED_COMPLETION_CLAIM",
                severity=Severity.BLOCK,
                message="A NOT_VERIFIED claim cannot be promoted to completion.",
                subject=claim_id,
            ))

    if not findings:
        findings.append(Finding(
            code="INTENT_INTEGRITY_PRESERVED",
            severity=Severity.INFO,
            message="Proposal preserves mandatory intent, scope, and evidence constraints.",
        ))

    return GuardReport(
        decision=_decision(findings),
        contract_digest=contract_digest,
        proposal_digest=proposal_digest,
        findings=tuple(findings),
    )
