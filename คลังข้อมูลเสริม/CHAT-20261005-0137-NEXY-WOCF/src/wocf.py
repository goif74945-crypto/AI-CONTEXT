from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from enum import Enum
from pathlib import PurePosixPath
from typing import Any, Iterable, Mapping, Sequence


class Decision(str, Enum):
    ALLOW = "ALLOW"
    WARN = "WARN"
    FREEZE = "FREEZE"


class Severity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    BLOCKER = "BLOCKER"


_SEVERITY_ORDER = {
    Severity.BLOCKER: 0,
    Severity.WARNING: 1,
    Severity.INFO: 2,
}

_IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$")
_LIVE_RESOURCE_STATUSES = {"ACTIVE", "IN_PROGRESS"}
_WORD_RE = re.compile(r"\w+", re.UNICODE)


class ManifestError(ValueError):
    pass


@dataclass(frozen=True)
class Policy:
    protected_repository_name_substrings: tuple[str, ...] = ()
    lexical_warn_threshold: float = 0.45
    lexical_freeze_threshold: float = 0.72
    require_namespace_write_containment: bool = True
    minimum_concept_tags: int = 2

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any] | None) -> "Policy":
        raw = raw or {}
        protected = _normalized_unique_strings(
            raw.get("protected_repository_name_substrings", ()),
            field_name="protected_repository_name_substrings",
            allow_empty=True,
        )
        warn = _as_probability(raw.get("lexical_warn_threshold", 0.45), "lexical_warn_threshold")
        freeze = _as_probability(raw.get("lexical_freeze_threshold", 0.72), "lexical_freeze_threshold")
        if warn >= freeze:
            raise ManifestError("lexical_warn_threshold must be lower than lexical_freeze_threshold")
        require_containment = raw.get("require_namespace_write_containment", True)
        if not isinstance(require_containment, bool):
            raise ManifestError("require_namespace_write_containment must be boolean")
        min_tags = raw.get("minimum_concept_tags", 2)
        if not isinstance(min_tags, int) or isinstance(min_tags, bool) or min_tags < 0 or min_tags > 64:
            raise ManifestError("minimum_concept_tags must be an integer from 0 to 64")
        return cls(
            protected_repository_name_substrings=tuple(s.casefold() for s in protected),
            lexical_warn_threshold=warn,
            lexical_freeze_threshold=freeze,
            require_namespace_write_containment=require_containment,
            minimum_concept_tags=min_tags,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "protected_repository_name_substrings": list(self.protected_repository_name_substrings),
            "lexical_warn_threshold": self.lexical_warn_threshold,
            "lexical_freeze_threshold": self.lexical_freeze_threshold,
            "require_namespace_write_containment": self.require_namespace_write_containment,
            "minimum_concept_tags": self.minimum_concept_tags,
        }


@dataclass(frozen=True)
class WorkstreamManifest:
    workstream_id: str
    repository: str
    namespace: str
    objective: str
    concept_tags: tuple[str, ...]
    write_paths: tuple[str, ...]
    read_paths: tuple[str, ...] = ()
    exclusive_resources: tuple[str, ...] = ()
    status: str = "ACTIVE"
    differentiators: tuple[str, ...] = ()

    @classmethod
    def from_mapping(
        cls,
        raw: Mapping[str, Any],
        *,
        policy: Policy,
        role: str,
    ) -> "WorkstreamManifest":
        if not isinstance(raw, Mapping):
            raise ManifestError(f"{role} manifest must be an object")

        workstream_id = _require_string(raw, "workstream_id")
        if not _IDENTIFIER_RE.fullmatch(workstream_id):
            raise ManifestError(
                f"{role}.workstream_id must match {_IDENTIFIER_RE.pattern!r}; got {workstream_id!r}"
            )
        repository = _require_string(raw, "repository")
        if "/" not in repository or repository.startswith("/") or repository.endswith("/"):
            raise ManifestError(f"{role}.repository must use owner/name form")
        namespace = _normalize_relative_path(_require_string(raw, "namespace"), f"{role}.namespace")
        objective = _normalize_human_text(_require_string(raw, "objective"))
        if len(objective) < 20:
            raise ManifestError(f"{role}.objective must be at least 20 normalized characters")

        concept_tags = _normalized_unique_strings(raw.get("concept_tags", ()), f"{role}.concept_tags")
        if len(concept_tags) < policy.minimum_concept_tags:
            raise ManifestError(
                f"{role}.concept_tags requires at least {policy.minimum_concept_tags} unique tags"
            )

        write_paths = _normalized_unique_paths(raw.get("write_paths", ()), f"{role}.write_paths")
        if not write_paths:
            raise ManifestError(f"{role}.write_paths must contain at least one path")

        read_paths = _normalized_unique_paths(raw.get("read_paths", ()), f"{role}.read_paths", allow_empty=True)
        exclusive_resources = _normalized_unique_strings(
            raw.get("exclusive_resources", ()), f"{role}.exclusive_resources", allow_empty=True
        )
        differentiators = _normalized_unique_strings(
            raw.get("differentiators", ()), f"{role}.differentiators", allow_empty=True
        )
        status = _normalize_human_text(str(raw.get("status", "ACTIVE"))).upper()
        if status not in {"ACTIVE", "IN_PROGRESS", "COMPLETE", "ARCHIVED", "REFERENCE"}:
            raise ManifestError(f"{role}.status is unsupported: {status!r}")

        if policy.require_namespace_write_containment:
            outside = [p for p in write_paths if not _path_contains(namespace, p)]
            if outside:
                raise ManifestError(
                    f"{role}.write_paths escape namespace {namespace!r}: {outside!r}"
                )

        return cls(
            workstream_id=workstream_id,
            repository=repository,
            namespace=namespace,
            objective=objective,
            concept_tags=concept_tags,
            write_paths=write_paths,
            read_paths=read_paths,
            exclusive_resources=exclusive_resources,
            status=status,
            differentiators=differentiators,
        )

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "workstream_id": self.workstream_id,
            "repository": self.repository,
            "namespace": self.namespace,
            "objective": self.objective,
            "concept_tags": list(self.concept_tags),
            "write_paths": list(self.write_paths),
            "read_paths": list(self.read_paths),
            "exclusive_resources": list(self.exclusive_resources),
            "status": self.status,
            "differentiators": list(self.differentiators),
        }

    def concept_fingerprint_payload(self) -> dict[str, Any]:
        return {
            "objective": self.objective.casefold(),
            "concept_tags": [t.casefold() for t in self.concept_tags],
            "differentiators": [d.casefold() for d in self.differentiators],
        }


@dataclass(frozen=True)
class Finding:
    code: str
    severity: Severity
    message: str
    other_workstream_id: str | None = None
    evidence: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "code": self.code,
            "severity": self.severity.value,
            "message": self.message,
            "evidence": dict(self.evidence),
        }
        if self.other_workstream_id is not None:
            data["other_workstream_id"] = self.other_workstream_id
        return data


@dataclass(frozen=True)
class EvaluationResult:
    decision: Decision
    proposal_hash: str
    catalog_hash: str
    policy_hash: str
    findings: tuple[Finding, ...]
    compared_workstreams: int
    max_lexical_overlap: float
    max_overlap_workstream_id: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision.value,
            "proposal_hash": self.proposal_hash,
            "catalog_hash": self.catalog_hash,
            "policy_hash": self.policy_hash,
            "compared_workstreams": self.compared_workstreams,
            "max_lexical_overlap": round(self.max_lexical_overlap, 6),
            "max_overlap_workstream_id": self.max_overlap_workstream_id,
            "findings": [f.to_dict() for f in self.findings],
        }


class WorkstreamCollisionFirewall:
    def __init__(self, policy: Policy) -> None:
        self.policy = policy

    def evaluate(
        self,
        proposal: WorkstreamManifest,
        catalog: Sequence[WorkstreamManifest],
    ) -> EvaluationResult:
        findings: list[Finding] = []

        repo_fold = proposal.repository.casefold()
        for protected in self.policy.protected_repository_name_substrings:
            if protected and protected in repo_fold:
                findings.append(
                    Finding(
                        code="PROTECTED_REPOSITORY",
                        severity=Severity.BLOCKER,
                        message="Proposal targets a repository blocked by current mutation policy.",
                        evidence={"repository": proposal.repository, "matched_substring": protected},
                    )
                )

        proposal_signature = _stable_hash(proposal.concept_fingerprint_payload())
        max_overlap = 0.0
        max_overlap_id: str | None = None

        for existing in sorted(catalog, key=lambda item: item.workstream_id.casefold()):
            if proposal.workstream_id.casefold() == existing.workstream_id.casefold():
                findings.append(
                    Finding(
                        code="WORKSTREAM_ID_COLLISION",
                        severity=Severity.BLOCKER,
                        message="workstream_id is already present in the catalog.",
                        other_workstream_id=existing.workstream_id,
                        evidence={"workstream_id": proposal.workstream_id},
                    )
                )

            if proposal.repository.casefold() == existing.repository.casefold():
                if _paths_overlap(proposal.namespace, existing.namespace):
                    findings.append(
                        Finding(
                            code="NAMESPACE_COLLISION",
                            severity=Severity.BLOCKER,
                            message="Proposal namespace overlaps an existing workstream namespace.",
                            other_workstream_id=existing.workstream_id,
                            evidence={
                                "proposal_namespace": proposal.namespace,
                                "existing_namespace": existing.namespace,
                            },
                        )
                    )

                for proposal_path, existing_path in _write_collisions(
                    proposal.write_paths, existing.write_paths
                ):
                    findings.append(
                        Finding(
                            code="WRITE_PATH_COLLISION",
                            severity=Severity.BLOCKER,
                            message="Proposal write-set overlaps an existing workstream write-set.",
                            other_workstream_id=existing.workstream_id,
                            evidence={
                                "proposal_path": proposal_path,
                                "existing_path": existing_path,
                            },
                        )
                    )

            shared_resources: list[str] = []
            if existing.status in _LIVE_RESOURCE_STATUSES:
                shared_resources = sorted(
                    {r.casefold(): r for r in proposal.exclusive_resources}.keys()
                    & {r.casefold(): r for r in existing.exclusive_resources}.keys()
                )
            for resource in shared_resources:
                findings.append(
                    Finding(
                        code="EXCLUSIVE_RESOURCE_COLLISION",
                        severity=Severity.BLOCKER,
                        message="Proposal claims an exclusive resource already claimed by another workstream.",
                        other_workstream_id=existing.workstream_id,
                        evidence={"resource": resource},
                    )
                )

            existing_signature = _stable_hash(existing.concept_fingerprint_payload())
            if proposal_signature == existing_signature:
                findings.append(
                    Finding(
                        code="DUPLICATE_CONCEPT_SIGNATURE",
                        severity=Severity.BLOCKER,
                        message="Proposal concept fingerprint exactly matches an existing workstream.",
                        other_workstream_id=existing.workstream_id,
                        evidence={"concept_signature": proposal_signature},
                    )
                )

            overlap, components = _lexical_overlap(proposal, existing)
            if overlap > max_overlap or (
                overlap == max_overlap
                and (max_overlap_id is None or existing.workstream_id.casefold() < max_overlap_id.casefold())
            ):
                max_overlap = overlap
                max_overlap_id = existing.workstream_id

            if overlap >= self.policy.lexical_freeze_threshold:
                findings.append(
                    Finding(
                        code="HIGH_LEXICAL_CONCEPT_OVERLAP",
                        severity=Severity.BLOCKER,
                        message="Proposal is too lexically similar to an existing workstream for automatic admission.",
                        other_workstream_id=existing.workstream_id,
                        evidence={
                            "score": round(overlap, 6),
                            **{k: round(v, 6) for k, v in components.items()},
                            "freeze_threshold": self.policy.lexical_freeze_threshold,
                        },
                    )
                )
            elif overlap >= self.policy.lexical_warn_threshold:
                findings.append(
                    Finding(
                        code="MODERATE_LEXICAL_CONCEPT_OVERLAP",
                        severity=Severity.WARNING,
                        message="Proposal has material lexical overlap; review differentiators before execution.",
                        other_workstream_id=existing.workstream_id,
                        evidence={
                            "score": round(overlap, 6),
                            **{k: round(v, 6) for k, v in components.items()},
                            "warn_threshold": self.policy.lexical_warn_threshold,
                        },
                    )
                )

        findings = _deduplicate_findings(findings)
        findings.sort(key=_finding_sort_key)

        decision = Decision.ALLOW
        if any(f.severity is Severity.BLOCKER for f in findings):
            decision = Decision.FREEZE
        elif any(f.severity is Severity.WARNING for f in findings):
            decision = Decision.WARN

        return EvaluationResult(
            decision=decision,
            proposal_hash=_stable_hash(proposal.canonical_dict()),
            catalog_hash=_stable_hash(
                [
                    item.canonical_dict()
                    for item in sorted(
                        catalog,
                        key=lambda x: (x.workstream_id.casefold(), x.namespace.casefold()),
                    )
                ]
            ),
            policy_hash=_stable_hash(self.policy.to_dict()),
            findings=tuple(findings),
            compared_workstreams=len(catalog),
            max_lexical_overlap=max_overlap,
            max_overlap_workstream_id=max_overlap_id,
        )


def evaluate_payloads(
    proposal_raw: Mapping[str, Any],
    catalog_raw: Sequence[Mapping[str, Any]],
    policy_raw: Mapping[str, Any] | None = None,
) -> EvaluationResult:
    try:
        policy = Policy.from_mapping(policy_raw)
    except ManifestError as exc:
        return _invalid_result("INVALID_POLICY", str(exc), policy_raw or {})

    try:
        proposal = WorkstreamManifest.from_mapping(proposal_raw, policy=policy, role="proposal")
    except ManifestError as exc:
        return _invalid_result("INVALID_PROPOSAL", str(exc), proposal_raw, policy=policy)

    catalog: list[WorkstreamManifest] = []
    if not isinstance(catalog_raw, Sequence) or isinstance(catalog_raw, (str, bytes, bytearray)):
        return _invalid_result("INVALID_CATALOG", "catalog must be an array", catalog_raw, policy=policy)

    seen_catalog_ids: set[str] = set()
    for index, entry in enumerate(catalog_raw):
        try:
            parsed = WorkstreamManifest.from_mapping(entry, policy=policy, role=f"catalog[{index}]")
            folded_id = parsed.workstream_id.casefold()
            if folded_id in seen_catalog_ids:
                raise ManifestError(f"catalog contains duplicate workstream_id: {parsed.workstream_id!r}")
            seen_catalog_ids.add(folded_id)
            catalog.append(parsed)
        except ManifestError as exc:
            return _invalid_result(
                "INVALID_CATALOG_ENTRY",
                str(exc),
                {"index": index, "entry": entry},
                policy=policy,
            )

    return WorkstreamCollisionFirewall(policy).evaluate(proposal, catalog)


def _invalid_result(
    code: str,
    message: str,
    payload: Any,
    *,
    policy: Policy | None = None,
) -> EvaluationResult:
    safe_policy = policy or Policy()
    finding = Finding(
        code=code,
        severity=Severity.BLOCKER,
        message=message,
        evidence={"payload_hash": _stable_hash(_json_safe(payload))},
    )
    return EvaluationResult(
        decision=Decision.FREEZE,
        proposal_hash="UNAVAILABLE",
        catalog_hash="UNAVAILABLE",
        policy_hash=_stable_hash(safe_policy.to_dict()),
        findings=(finding,),
        compared_workstreams=0,
        max_lexical_overlap=0.0,
        max_overlap_workstream_id=None,
    )


def _as_probability(value: Any, field_name: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ManifestError(f"{field_name} must be numeric")
    result = float(value)
    if not 0.0 <= result <= 1.0:
        raise ManifestError(f"{field_name} must be between 0 and 1")
    return result


def _require_string(raw: Mapping[str, Any], key: str) -> str:
    value = raw.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ManifestError(f"{key} must be a non-empty string")
    return value.strip()


def _normalize_human_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value)
    return " ".join(value.split())


def _normalized_unique_strings(
    values: Any,
    field_name: str,
    *,
    allow_empty: bool = False,
) -> tuple[str, ...]:
    if values is None and allow_empty:
        return ()
    if not isinstance(values, Sequence) or isinstance(values, (str, bytes, bytearray)):
        raise ManifestError(f"{field_name} must be an array of strings")
    normalized: dict[str, str] = {}
    for value in values:
        if not isinstance(value, str) or not value.strip():
            raise ManifestError(f"{field_name} contains an empty/non-string value")
        clean = _normalize_human_text(value)
        normalized.setdefault(clean.casefold(), clean)
    if not normalized and not allow_empty:
        raise ManifestError(f"{field_name} must not be empty")
    return tuple(normalized[key] for key in sorted(normalized))


def _normalized_unique_paths(
    values: Any,
    field_name: str,
    *,
    allow_empty: bool = False,
) -> tuple[str, ...]:
    if values is None and allow_empty:
        return ()
    if not isinstance(values, Sequence) or isinstance(values, (str, bytes, bytearray)):
        raise ManifestError(f"{field_name} must be an array of relative paths")
    normalized = {
        _normalize_relative_path(value, field_name)
        for value in values
        if isinstance(value, str)
    }
    if len(normalized) != len(values):
        raise ManifestError(f"{field_name} contains an empty/non-string value")
    if not normalized and not allow_empty:
        raise ManifestError(f"{field_name} must not be empty")
    return tuple(sorted(normalized, key=str.casefold))


def _normalize_relative_path(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ManifestError(f"{field_name} contains an empty/non-string path")
    raw = unicodedata.normalize("NFKC", value.strip()).replace("\\", "/")
    if raw.startswith("/"):
        raise ManifestError(f"{field_name} paths must be relative: {value!r}")
    parts = PurePosixPath(raw).parts
    if any(part in {"..", "."} for part in parts):
        raise ManifestError(f"{field_name} paths may not contain dot traversal: {value!r}")
    normalized = posixpath.normpath(raw)
    if normalized in {"", ".", ".."} or normalized.startswith("../"):
        raise ManifestError(f"{field_name} path is unsafe: {value!r}")
    return normalized.strip("/")


def _path_contains(parent: str, child: str) -> bool:
    return child == parent or child.startswith(parent + "/")


def _paths_overlap(left: str, right: str) -> bool:
    return _path_contains(left, right) or _path_contains(right, left)


def _write_collisions(
    proposal_paths: Sequence[str],
    existing_paths: Sequence[str],
) -> Iterable[tuple[str, str]]:
    for proposal_path in proposal_paths:
        for existing_path in existing_paths:
            if _paths_overlap(proposal_path, existing_path):
                yield proposal_path, existing_path


def _token_set(text: str) -> set[str]:
    normalized = unicodedata.normalize("NFKC", text).casefold()
    return {token for token in _WORD_RE.findall(normalized) if len(token) >= 2}


def _jaccard(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 1.0
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def _lexical_overlap(
    proposal: WorkstreamManifest,
    existing: WorkstreamManifest,
) -> tuple[float, dict[str, float]]:
    proposal_tags = {tag.casefold() for tag in proposal.concept_tags}
    existing_tags = {tag.casefold() for tag in existing.concept_tags}
    tag_score = _jaccard(proposal_tags, existing_tags)

    objective_score = _jaccard(_token_set(proposal.objective), _token_set(existing.objective))

    proposal_diff = {item.casefold() for item in proposal.differentiators}
    existing_diff = {item.casefold() for item in existing.differentiators}
    differentiator_score = _jaccard(proposal_diff, existing_diff) if proposal_diff and existing_diff else 0.0

    combined = (0.65 * tag_score) + (0.30 * objective_score) + (0.05 * differentiator_score)
    return combined, {
        "tag_jaccard": tag_score,
        "objective_token_jaccard": objective_score,
        "differentiator_jaccard": differentiator_score,
    }


def _stable_hash(value: Any) -> str:
    payload = json.dumps(
        _json_safe(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _json_safe(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return repr(value)


def _finding_sort_key(finding: Finding) -> tuple[Any, ...]:
    return (
        _SEVERITY_ORDER[finding.severity],
        finding.code,
        (finding.other_workstream_id or "").casefold(),
        json.dumps(_json_safe(finding.evidence), ensure_ascii=False, sort_keys=True),
    )


def _deduplicate_findings(findings: Sequence[Finding]) -> list[Finding]:
    result: list[Finding] = []
    seen: set[str] = set()
    for finding in findings:
        key = _stable_hash(
            {
                "code": finding.code,
                "severity": finding.severity.value,
                "other": finding.other_workstream_id,
                "evidence": finding.evidence,
            }
        )
        if key not in seen:
            seen.add(key)
            result.append(finding)
    return result


def _load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="wocf",
        description="Deterministic preflight for concurrent AI workstream collisions.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    evaluate_parser = subparsers.add_parser("evaluate", help="Evaluate a proposal against a catalog")
    evaluate_parser.add_argument("--proposal", required=True)
    evaluate_parser.add_argument("--catalog", required=True)
    evaluate_parser.add_argument("--policy", required=False)
    evaluate_parser.add_argument("--pretty", action="store_true")

    args = parser.parse_args(argv)
    if args.command != "evaluate":
        parser.error("unsupported command")

    proposal_raw = _load_json(args.proposal)
    catalog_raw = _load_json(args.catalog)
    policy_raw = _load_json(args.policy) if args.policy else None

    result = evaluate_payloads(proposal_raw, catalog_raw, policy_raw)
    json.dump(
        result.to_dict(),
        sys.stdout,
        ensure_ascii=False,
        sort_keys=True,
        indent=2 if args.pretty else None,
    )
    sys.stdout.write("\n")
    return 2 if result.decision is Decision.FREEZE else 0


if __name__ == "__main__":
    raise SystemExit(_main())
