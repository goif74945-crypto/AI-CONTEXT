"""Typed immutable domain models for NEXY-REFLEX."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TruthStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    PARTIAL = "PARTIAL"
    BLOCKED = "BLOCKED"
    NOT_VERIFIED = "NOT_VERIFIED"
    UNKNOWN = "UNKNOWN"
    CONFLICT = "CONFLICT"


class GateAction(str, Enum):
    ACCEPT_ADVISORY = "ACCEPT_ADVISORY"
    FREEZE_RECOMMENDED = "FREEZE_RECOMMENDED"


class Severity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    BLOCKING = "BLOCKING"


VALID_EVIDENCE_CLASSES = frozenset({f"E{i}" for i in range(8)})
VALID_SCOPES = frozenset({
    "CURRENT_GOVERNING_LAW",
    "CURRENT_BUILD",
    "CURRENT_BUILD_SUPPLEMENT",
    "SUPPORTED_PRODUCT_DESIGN",
    "DEPLOYMENT_EVIDENCE",
    "EXCLUDED_CURRENT",
    "DEFERRED_FUTURE",
})
NON_GATING_SCOPES = frozenset({"EXCLUDED_CURRENT", "DEFERRED_FUTURE"})


@dataclass(frozen=True, slots=True)
class TargetIdentity:
    target_id: str
    revision: str
    content_digest: str | None = None

    @staticmethod
    def from_dict(raw: dict[str, Any]) -> "TargetIdentity":
        _require_keys(raw, {"id", "revision"}, "target")
        target_id = _require_nonempty_str(raw.get("id"), "target.id")
        revision = _require_nonempty_str(raw.get("revision"), "target.revision")
        digest = raw.get("content_digest")
        if digest is not None:
            digest = _require_nonempty_str(digest, "target.content_digest")
        return TargetIdentity(target_id=target_id, revision=revision, content_digest=digest)

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.target_id, "revision": self.revision, "content_digest": self.content_digest}


@dataclass(frozen=True, slots=True)
class RequirementClaim:
    claim_id: str
    key: str
    value: Any
    authority: str
    scope: str
    accepted_evidence_classes: tuple[str, ...]
    dependencies: tuple[str, ...] = ()

    @staticmethod
    def from_dict(raw: dict[str, Any]) -> "RequirementClaim":
        _require_keys(raw, {"id", "key", "authority", "scope", "accepted_evidence_classes", "value"}, "requirement")
        claim_id = _require_nonempty_str(raw.get("id"), "requirement.id")
        key = _require_nonempty_str(raw.get("key"), "requirement.key")
        authority = _require_nonempty_str(raw.get("authority"), "requirement.authority")
        scope = _require_nonempty_str(raw.get("scope"), "requirement.scope")
        if scope not in VALID_SCOPES:
            raise ValueError(f"invalid requirement scope: {scope}")
        classes_raw = raw.get("accepted_evidence_classes")
        if not isinstance(classes_raw, list) or not classes_raw:
            raise ValueError("requirement.accepted_evidence_classes must be a non-empty list")
        classes: list[str] = []
        for idx, item in enumerate(classes_raw):
            evidence_class = _require_nonempty_str(item, f"requirement.accepted_evidence_classes[{idx}]")
            if evidence_class not in VALID_EVIDENCE_CLASSES:
                raise ValueError(f"invalid evidence class: {evidence_class}")
            classes.append(evidence_class)
        if len(set(classes)) != len(classes):
            raise ValueError("requirement.accepted_evidence_classes contains duplicates")
        deps_raw = raw.get("dependencies", [])
        if not isinstance(deps_raw, list):
            raise ValueError("requirement.dependencies must be a list")
        dependencies = tuple(_require_nonempty_str(x, "requirement.dependencies[]") for x in deps_raw)
        if len(set(dependencies)) != len(dependencies):
            raise ValueError("requirement.dependencies contains duplicates")
        if claim_id in dependencies:
            raise ValueError(f"requirement {claim_id} cannot depend on itself")
        return RequirementClaim(claim_id,key,raw.get("value"),authority,scope,tuple(classes),dependencies)

    def to_dict(self) -> dict[str, Any]:
        return {"id":self.claim_id,"key":self.key,"value":self.value,"authority":self.authority,"scope":self.scope,"accepted_evidence_classes":list(self.accepted_evidence_classes),"dependencies":list(self.dependencies)}


@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    evidence_id: str
    requirement_id: str
    evidence_class: str
    status: TruthStatus
    target_revision: str
    target_digest: str | None = None
    provenance: str | None = None

    @staticmethod
    def from_dict(raw: dict[str, Any]) -> "EvidenceRecord":
        _require_keys(raw,{"id","requirement_id","class","status","target_revision"},"evidence")
        evidence_id=_require_nonempty_str(raw.get("id"),"evidence.id")
        requirement_id=_require_nonempty_str(raw.get("requirement_id"),"evidence.requirement_id")
        evidence_class=_require_nonempty_str(raw.get("class"),"evidence.class")
        if evidence_class not in VALID_EVIDENCE_CLASSES: raise ValueError(f"invalid evidence class: {evidence_class}")
        status_raw=_require_nonempty_str(raw.get("status"),"evidence.status")
        try: status=TruthStatus(status_raw)
        except ValueError as exc: raise ValueError(f"invalid evidence status: {status_raw}") from exc
        revision=_require_nonempty_str(raw.get("target_revision"),"evidence.target_revision")
        digest=raw.get("target_digest"); provenance=raw.get("provenance")
        if digest is not None: digest=_require_nonempty_str(digest,"evidence.target_digest")
        if provenance is not None: provenance=_require_nonempty_str(provenance,"evidence.provenance")
        return EvidenceRecord(evidence_id,requirement_id,evidence_class,status,revision,digest,provenance)

    def to_dict(self) -> dict[str, Any]:
        return {"id":self.evidence_id,"requirement_id":self.requirement_id,"class":self.evidence_class,"status":self.status.value,"target_revision":self.target_revision,"target_digest":self.target_digest,"provenance":self.provenance}


@dataclass(frozen=True, slots=True)
class Snapshot:
    snapshot_version: str
    target: TargetIdentity
    authority_order: tuple[str, ...]
    requirements: tuple[RequirementClaim, ...]
    evidence: tuple[EvidenceRecord, ...]

    @staticmethod
    def from_dict(raw: dict[str, Any]) -> "Snapshot":
        _require_keys(raw,{"snapshot_version","target","authority_order","requirements","evidence"},"snapshot")
        version=_require_nonempty_str(raw.get("snapshot_version"),"snapshot_version")
        if version!="1.0": raise ValueError(f"unsupported snapshot_version: {version}")
        target_raw=raw.get("target")
        if not isinstance(target_raw,dict): raise ValueError("target must be an object")
        authority_raw=raw.get("authority_order")
        if not isinstance(authority_raw,list) or not authority_raw: raise ValueError("authority_order must be a non-empty list")
        authority_order=tuple(_require_nonempty_str(x,"authority_order[]") for x in authority_raw)
        if len(set(authority_order))!=len(authority_order): raise ValueError("authority_order contains duplicates")
        req_raw=raw.get("requirements"); evidence_raw=raw.get("evidence")
        if not isinstance(req_raw,list): raise ValueError("requirements must be a list")
        if not isinstance(evidence_raw,list): raise ValueError("evidence must be a list")
        return Snapshot(version,TargetIdentity.from_dict(target_raw),authority_order,tuple(RequirementClaim.from_dict(_require_dict(x,"requirements[]")) for x in req_raw),tuple(EvidenceRecord.from_dict(_require_dict(x,"evidence[]")) for x in evidence_raw))

    def to_dict(self) -> dict[str, Any]:
        return {"snapshot_version":self.snapshot_version,"target":self.target.to_dict(),"authority_order":list(self.authority_order),"requirements":[x.to_dict() for x in self.requirements],"evidence":[x.to_dict() for x in self.evidence]}


@dataclass(frozen=True, slots=True)
class Finding:
    code: str
    status: TruthStatus
    severity: Severity
    subject: str
    detail: str
    related_ids: tuple[str, ...] = ()
    def to_dict(self) -> dict[str, Any]:
        return {"code":self.code,"status":self.status.value,"severity":self.severity.value,"subject":self.subject,"detail":self.detail,"related_ids":list(self.related_ids)}


@dataclass(frozen=True, slots=True)
class GateDecision:
    verdict: TruthStatus
    action: GateAction
    input_digest: str
    decision_digest: str
    effective_requirements: tuple[str, ...]
    non_gating_requirements: tuple[str, ...]
    findings: tuple[Finding, ...] = field(default_factory=tuple)
    def to_dict(self) -> dict[str, Any]:
        return {"verdict":self.verdict.value,"action":self.action.value,"input_digest":self.input_digest,"decision_digest":self.decision_digest,"effective_requirements":list(self.effective_requirements),"non_gating_requirements":list(self.non_gating_requirements),"findings":[x.to_dict() for x in self.findings]}


def _require_keys(raw: dict[str, Any], required: set[str], label: str) -> None:
    missing=sorted(required.difference(raw))
    if missing: raise ValueError(f"{label} missing required keys: {', '.join(missing)}")

def _require_nonempty_str(value: Any,label: str)->str:
    if not isinstance(value,str) or not value.strip(): raise ValueError(f"{label} must be a non-empty string")
    return value

def _require_dict(value: Any,label: str)->dict[str,Any]:
    if not isinstance(value,dict): raise ValueError(f"{label} must be an object")
    return value
