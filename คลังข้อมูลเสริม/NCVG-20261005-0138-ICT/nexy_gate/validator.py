from __future__ import annotations

from collections import Counter
from fnmatch import fnmatchcase
from typing import Any, Iterable, Mapping

from .model import EVIDENCE_CLASSES, VALID_STATUSES, Finding, expect_mapping


REQUIRED_TOP_LEVEL = (
    "bundle_version",
    "task_contract",
    "requirement_ledger",
    "evidence",
    "execution_record",
    "policy",
)


def _err(code: str, path: str, message: str) -> Finding:
    return Finding(code=code, path=path, message=message, severity="ERROR")


def _warn(code: str, path: str, message: str) -> Finding:
    return Finding(code=code, path=path, message=message, severity="WARNING")


def _nonempty_str(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _list(value: Any) -> list[Any] | None:
    return value if isinstance(value, list) else None


def _path_matches(target: str, patterns: Iterable[str]) -> bool:
    normalized = target.replace("\\", "/")
    for pattern in patterns:
        if not isinstance(pattern, str) or not pattern:
            continue
        p = pattern.replace("\\", "/")
        if normalized == p or normalized.startswith(p.rstrip("/") + "/") or fnmatchcase(normalized, p):
            return True
    return False


def _contains_forbidden_repo(target: str, fragments: Iterable[str]) -> str | None:
    lowered = target.lower()
    for fragment in fragments:
        if isinstance(fragment, str) and fragment and fragment.lower() in lowered:
            return fragment
    return None


def validate_bundle_semantics(bundle: Any) -> tuple[list[Finding], set[str], int]:
    findings: list[Finding] = []
    verified_requirements: set[str] = set()

    root = expect_mapping(bundle)
    if root is None:
        return [_err("BUNDLE_NOT_OBJECT", "$", "Bundle must be a JSON object")], set(), 0

    for key in REQUIRED_TOP_LEVEL:
        if key not in root:
            findings.append(_err("MISSING_TOP_LEVEL", f"$.{key}", f"Required top-level field '{key}' is missing"))

    if findings:
        return sorted(findings), set(), 0

    if root.get("bundle_version") != "1.0":
        findings.append(_err("UNSUPPORTED_BUNDLE_VERSION", "$.bundle_version", "Only bundle_version '1.0' is supported"))

    task = expect_mapping(root.get("task_contract"))
    ledger = expect_mapping(root.get("requirement_ledger"))
    execution = expect_mapping(root.get("execution_record"))
    policy = expect_mapping(root.get("policy"))
    evidence = _list(root.get("evidence"))

    if task is None:
        findings.append(_err("TASK_CONTRACT_NOT_OBJECT", "$.task_contract", "task_contract must be an object"))
    if ledger is None:
        findings.append(_err("LEDGER_NOT_OBJECT", "$.requirement_ledger", "requirement_ledger must be an object"))
    if execution is None:
        findings.append(_err("EXECUTION_NOT_OBJECT", "$.execution_record", "execution_record must be an object"))
    if policy is None:
        findings.append(_err("POLICY_NOT_OBJECT", "$.policy", "policy must be an object"))
    if evidence is None:
        findings.append(_err("EVIDENCE_NOT_ARRAY", "$.evidence", "evidence must be an array"))

    if any(f.code.endswith("NOT_OBJECT") or f.code == "EVIDENCE_NOT_ARRAY" for f in findings):
        return sorted(findings), set(), 0

    assert task is not None and ledger is not None and execution is not None and policy is not None and evidence is not None

    # Task contract checks.
    for field in ("objective", "target"):
        if not _nonempty_str(task.get(field)):
            findings.append(_err("TASK_FIELD_INVALID", f"$.task_contract.{field}", f"{field} must be a non-empty string"))
    for field in ("authorized_scope", "protected_scope", "deliverables"):
        values = _list(task.get(field))
        if values is None or not values:
            findings.append(_err("TASK_SCOPE_INVALID", f"$.task_contract.{field}", f"{field} must be a non-empty array"))
        elif not all(_nonempty_str(x) for x in values):
            findings.append(_err("TASK_SCOPE_ENTRY_INVALID", f"$.task_contract.{field}", f"{field} entries must be non-empty strings"))

    # Evidence indexing + local validity.
    evidence_by_id: dict[str, Mapping[str, Any]] = {}
    evidence_ids: list[str] = []
    for i, raw in enumerate(evidence):
        path = f"$.evidence[{i}]"
        item = expect_mapping(raw)
        if item is None:
            findings.append(_err("EVIDENCE_ITEM_NOT_OBJECT", path, "Evidence entry must be an object"))
            continue
        eid = item.get("id")
        if not _nonempty_str(eid):
            findings.append(_err("EVIDENCE_ID_INVALID", f"{path}.id", "Evidence id must be a non-empty string"))
            continue
        evidence_ids.append(eid)
        evidence_by_id[eid] = item
        status = item.get("status")
        if not isinstance(status, str) or status not in VALID_STATUSES:
            findings.append(_err("EVIDENCE_STATUS_INVALID", f"{path}.status", f"Invalid evidence status: {status!r}"))
        eclass = item.get("evidence_class")
        if not isinstance(eclass, str) or eclass not in EVIDENCE_CLASSES:
            findings.append(_err("EVIDENCE_CLASS_INVALID", f"{path}.evidence_class", f"Invalid evidence class: {eclass!r}"))
        for req_field in ("claim", "target", "method", "observed"):
            if not _nonempty_str(item.get(req_field)):
                findings.append(_err("EVIDENCE_FIELD_INVALID", f"{path}.{req_field}", f"{req_field} must be a non-empty string"))

    dupes = [eid for eid, count in Counter(evidence_ids).items() if count > 1]
    for eid in sorted(dupes):
        findings.append(_err("DUPLICATE_EVIDENCE_ID", "$.evidence", f"Evidence id '{eid}' appears more than once"))

    # Policy checks.
    acceptable = policy.get("acceptable_evidence_classes", {})
    if not isinstance(acceptable, Mapping):
        findings.append(_err("POLICY_EVIDENCE_MAP_INVALID", "$.policy.acceptable_evidence_classes", "Must be an object mapping requirement id to allowed evidence classes"))
        acceptable = {}

    expected_commit = policy.get("expected_commit")
    if expected_commit is not None and not _nonempty_str(expected_commit):
        findings.append(_err("EXPECTED_COMMIT_INVALID", "$.policy.expected_commit", "expected_commit must be null or a non-empty string"))
        expected_commit = None

    protected_patterns = policy.get("protected_target_patterns", [])
    if not isinstance(protected_patterns, list) or not all(isinstance(x, str) for x in protected_patterns):
        findings.append(_err("PROTECTED_PATTERNS_INVALID", "$.policy.protected_target_patterns", "Must be an array of strings"))
        protected_patterns = []

    forbidden_repo_fragments = policy.get("forbidden_mutation_repository_name_fragments", [])
    if not isinstance(forbidden_repo_fragments, list) or not all(isinstance(x, str) for x in forbidden_repo_fragments):
        findings.append(_err("FORBIDDEN_REPO_POLICY_INVALID", "$.policy.forbidden_mutation_repository_name_fragments", "Must be an array of strings"))
        forbidden_repo_fragments = []

    allow_warnings = policy.get("allow_warnings", True)
    if not isinstance(allow_warnings, bool):
        findings.append(_err("ALLOW_WARNINGS_INVALID", "$.policy.allow_warnings", "allow_warnings must be boolean"))
        allow_warnings = True

    # Ledger checks and evidence admission.
    requirements = _list(ledger.get("requirements"))
    mandatory_count = 0
    if requirements is None or not requirements:
        findings.append(_err("NO_REQUIREMENTS", "$.requirement_ledger.requirements", "At least one requirement is required"))
        requirements = []

    requirement_ids: list[str] = []
    for i, raw in enumerate(requirements):
        path = f"$.requirement_ledger.requirements[{i}]"
        req = expect_mapping(raw)
        if req is None:
            findings.append(_err("REQUIREMENT_NOT_OBJECT", path, "Requirement must be an object"))
            continue
        rid = req.get("id")
        if not _nonempty_str(rid):
            findings.append(_err("REQUIREMENT_ID_INVALID", f"{path}.id", "Requirement id must be a non-empty string"))
            continue
        requirement_ids.append(rid)
        mandatory = req.get("mandatory", True)
        if not isinstance(mandatory, bool):
            findings.append(_err("MANDATORY_FLAG_INVALID", f"{path}.mandatory", "mandatory must be boolean"))
            mandatory = True
        if not mandatory:
            continue
        mandatory_count += 1
        status = req.get("status")
        if status != "PASS":
            findings.append(_err("MANDATORY_REQUIREMENT_NOT_PASS", f"{path}.status", f"Mandatory requirement '{rid}' must be PASS, got {status!r}"))
            continue
        refs = req.get("evidence_refs", [])
        if not isinstance(refs, list) or not refs or not all(_nonempty_str(x) for x in refs):
            findings.append(_err("MANDATORY_EVIDENCE_REFS_INVALID", f"{path}.evidence_refs", f"Mandatory requirement '{rid}' must reference at least one evidence id"))
            continue

        allowed_classes = acceptable.get(rid)
        if not isinstance(allowed_classes, list) or not allowed_classes:
            findings.append(_err("EVIDENCE_POLICY_MISSING", f"$.policy.acceptable_evidence_classes.{rid}", f"No acceptable evidence classes declared for mandatory requirement '{rid}'"))
            continue
        invalid_classes = [c for c in allowed_classes if not isinstance(c, str) or c not in EVIDENCE_CLASSES]
        if invalid_classes:
            findings.append(_err("EVIDENCE_POLICY_CLASS_INVALID", f"$.policy.acceptable_evidence_classes.{rid}", f"Invalid evidence classes: {invalid_classes}"))
            continue

        admitted = False
        for ref in refs:
            ev = evidence_by_id.get(ref)
            if ev is None:
                findings.append(_err("UNKNOWN_EVIDENCE_REF", f"{path}.evidence_refs", f"Requirement '{rid}' references missing evidence '{ref}'"))
                continue
            if ev.get("status") != "PASS":
                findings.append(_err("REFERENCED_EVIDENCE_NOT_PASS", f"{path}.evidence_refs", f"Evidence '{ref}' for requirement '{rid}' is not PASS"))
                continue
            if ev.get("evidence_class") not in allowed_classes:
                findings.append(_err("EVIDENCE_CLASS_NOT_ACCEPTED", f"{path}.evidence_refs", f"Evidence '{ref}' class {ev.get('evidence_class')!r} is not accepted for requirement '{rid}'"))
                continue
            if expected_commit is not None:
                ev_commit = ev.get("commit")
                if ev_commit != expected_commit:
                    findings.append(_err("STALE_OR_WRONG_COMMIT_EVIDENCE", f"{path}.evidence_refs", f"Evidence '{ref}' commit {ev_commit!r} does not match expected commit {expected_commit!r}"))
                    continue
            admitted = True

        if admitted:
            verified_requirements.add(rid)

    for rid in sorted([rid for rid, count in Counter(requirement_ids).items() if count > 1]):
        findings.append(_err("DUPLICATE_REQUIREMENT_ID", "$.requirement_ledger.requirements", f"Requirement id '{rid}' appears more than once"))

    # Execution record and mutation boundary.
    if execution.get("final_status") != "PASS":
        findings.append(_err("EXECUTION_NOT_PASS", "$.execution_record.final_status", f"Execution record must be PASS, got {execution.get('final_status')!r}"))

    mutations = _list(execution.get("mutations"))
    if mutations is None:
        findings.append(_err("MUTATIONS_INVALID", "$.execution_record.mutations", "mutations must be an array"))
        mutations = []

    for i, raw in enumerate(mutations):
        path = f"$.execution_record.mutations[{i}]"
        mutation = expect_mapping(raw)
        if mutation is None:
            findings.append(_err("MUTATION_NOT_OBJECT", path, "Mutation entry must be an object"))
            continue
        target = mutation.get("target")
        if not _nonempty_str(target):
            findings.append(_err("MUTATION_TARGET_INVALID", f"{path}.target", "Mutation target must be a non-empty string"))
            continue
        if _path_matches(target, protected_patterns):
            findings.append(_err("PROTECTED_TARGET_MUTATION", f"{path}.target", f"Mutation target '{target}' matches a protected target pattern"))
        fragment = _contains_forbidden_repo(target, forbidden_repo_fragments)
        if fragment is not None:
            findings.append(_err("FORBIDDEN_REPOSITORY_MUTATION", f"{path}.target", f"Mutation target '{target}' contains forbidden repository fragment '{fragment}'"))

    # Warnings for optional requirements not passing.
    for i, raw in enumerate(requirements):
        req = expect_mapping(raw)
        if req is None or req.get("mandatory", True):
            continue
        if req.get("status") != "PASS":
            findings.append(_warn("OPTIONAL_REQUIREMENT_NOT_PASS", f"$.requirement_ledger.requirements[{i}].status", f"Optional requirement '{req.get('id')}' is not PASS"))

    if not allow_warnings and any(f.severity == "WARNING" for f in findings):
        findings.append(_err("WARNINGS_DISALLOWED", "$.policy.allow_warnings", "Policy disallows warnings"))

    return sorted(findings), verified_requirements, mandatory_count
