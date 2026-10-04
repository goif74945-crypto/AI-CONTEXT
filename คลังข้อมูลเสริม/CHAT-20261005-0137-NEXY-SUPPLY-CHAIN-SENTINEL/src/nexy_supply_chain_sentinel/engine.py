from __future__ import annotations

from pathlib import Path
from typing import Any

from .canonical import sha256_bytes, sha256_file, sha256_json
from .diffing import diff_snapshots
from .parsers import parse_dependency_file
from .policy import Policy

SNAPSHOT_SCHEMA = "nscs.snapshot.v1"
VERIFY_SCHEMA = "nscs.verify.v1"
_PACKAGE_FIELDS = ("ecosystem", "name", "version", "source", "integrity")


def _package_sort_key(pkg: dict[str, str]) -> tuple[str, ...]:
    return tuple(pkg.get(name, "") for name in _PACKAGE_FIELDS)


def _sort_violations(violations: list[dict[str, str]]) -> list[dict[str, str]]:
    return sorted(violations, key=lambda item: (item.get("code", ""), item.get("subject", ""), item.get("message", "")))


def _sealable(snapshot: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in snapshot.items() if key != "snapshot_sha256"}


def build_snapshot(path: str | Path, policy: Policy | None = None) -> dict[str, Any]:
    policy = policy or Policy()
    source = Path(path)
    source_size = source.stat().st_size
    if source_size > policy.max_input_bytes:
        raw = None
        source_kind = "unparsed"
        packages = []
        violations = [{
            "code": "INPUT_SIZE_LIMIT_EXCEEDED",
            "subject": source.name,
            "message": f"input size {source_size} exceeds policy limit {policy.max_input_bytes}",
        }]
        source_sha256 = sha256_file(source)
    else:
        raw = source.read_bytes()
        source_kind, packages, violations = parse_dependency_file(source, policy)
        source_sha256 = sha256_bytes(raw)
    packages = sorted(packages, key=_package_sort_key)
    if len(packages) > policy.max_packages:
        violations.append({
            "code": "PACKAGE_LIMIT_EXCEEDED",
            "subject": source.name,
            "message": f"inventory contains {len(packages)} packages; limit is {policy.max_packages}",
        })
    violations = _sort_violations(violations)
    snapshot: dict[str, Any] = {
        "schema_version": SNAPSHOT_SCHEMA,
        "source_kind": source_kind,
        "source_file": source.name,
        "source_sha256": source_sha256,
        "policy_sha256": sha256_json(policy.to_dict()),
        "decision": "FREEZE" if violations else "ALLOW",
        "packages": packages,
        "inventory_sha256": sha256_json(packages),
        "violations": violations,
    }
    snapshot["snapshot_sha256"] = sha256_json(snapshot)
    return snapshot


def validate_snapshot(snapshot: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if not isinstance(snapshot, dict):
        return False, ["SNAPSHOT_NOT_OBJECT"]
    required = {
        "schema_version",
        "source_kind",
        "source_file",
        "source_sha256",
        "policy_sha256",
        "decision",
        "packages",
        "inventory_sha256",
        "violations",
        "snapshot_sha256",
    }
    missing = sorted(required - set(snapshot))
    if missing:
        reasons.extend(f"SNAPSHOT_MISSING_FIELD:{name}" for name in missing)
        return False, reasons
    unknown = sorted(set(snapshot) - required)
    reasons.extend(f"SNAPSHOT_UNKNOWN_FIELD:{name}" for name in unknown)
    if snapshot.get("schema_version") != SNAPSHOT_SCHEMA:
        reasons.append("SNAPSHOT_SCHEMA_UNSUPPORTED")

    violations = snapshot.get("violations")
    if not isinstance(violations, list):
        reasons.append("SNAPSHOT_VIOLATIONS_INVALID")
        violations = []
    else:
        for violation in violations:
            if (
                not isinstance(violation, dict)
                or set(violation) != {"code", "subject", "message"}
                or any(not isinstance(violation.get(field), str) for field in ("code", "subject", "message"))
            ):
                reasons.append("VIOLATION_SCHEMA_INVALID")
                break

    decision = snapshot.get("decision")
    if decision not in {"ALLOW", "FREEZE"}:
        reasons.append("SNAPSHOT_DECISION_INVALID")
    elif decision != ("FREEZE" if violations else "ALLOW"):
        reasons.append("SNAPSHOT_DECISION_INCONSISTENT")

    packages = snapshot.get("packages")
    if not isinstance(packages, list):
        reasons.append("SNAPSHOT_PACKAGES_INVALID")
    else:
        expected_package_fields = set(_PACKAGE_FIELDS)
        for package in packages:
            if (
                not isinstance(package, dict)
                or set(package) != expected_package_fields
                or any(not isinstance(package.get(field), str) for field in _PACKAGE_FIELDS)
            ):
                reasons.append("PACKAGE_SCHEMA_INVALID")
                break
        if sha256_json(packages) != snapshot.get("inventory_sha256"):
            reasons.append("INVENTORY_HASH_MISMATCH")
        if all(isinstance(package, dict) for package in packages) and packages != sorted(packages, key=_package_sort_key):
            reasons.append("PACKAGES_NOT_CANONICAL_ORDER")
    if sha256_json(_sealable(snapshot)) != snapshot.get("snapshot_sha256"):
        reasons.append("SNAPSHOT_HASH_MISMATCH")
    return not reasons, sorted(set(reasons))


def verify_drift(baseline: dict[str, Any], candidate: dict[str, Any], policy: Policy | None = None) -> dict[str, Any]:
    policy = policy or Policy()
    reason_codes: list[str] = []
    baseline_valid, baseline_reasons = validate_snapshot(baseline)
    candidate_valid, candidate_reasons = validate_snapshot(candidate)
    reason_codes.extend(f"BASELINE_{reason}" for reason in baseline_reasons)
    reason_codes.extend(f"CANDIDATE_{reason}" for reason in candidate_reasons)
    expected_policy_sha = sha256_json(policy.to_dict())
    if baseline_valid and baseline.get("policy_sha256") != expected_policy_sha:
        reason_codes.append("BASELINE_POLICY_MISMATCH")
    if candidate_valid and candidate.get("policy_sha256") != expected_policy_sha:
        reason_codes.append("CANDIDATE_POLICY_MISMATCH")
    if baseline_valid and baseline.get("decision") != "ALLOW":
        reason_codes.append("BASELINE_NOT_ALLOW")
    if candidate_valid and candidate.get("decision") != "ALLOW":
        reason_codes.append("CANDIDATE_NOT_ALLOW")

    events = diff_snapshots(baseline, candidate) if baseline_valid and candidate_valid else []
    permissions = {
        "ADDITION": (policy.allow_additions, "DRIFT_ADDITION_DENIED"),
        "REMOVAL": (policy.allow_removals, "DRIFT_REMOVAL_DENIED"),
        "VERSION_CHANGE": (policy.allow_version_changes, "DRIFT_VERSION_CHANGE_DENIED"),
        "SOURCE_CHANGE": (policy.allow_source_changes, "DRIFT_SOURCE_CHANGE_DENIED"),
        "INTEGRITY_CHANGE": (policy.allow_integrity_changes, "DRIFT_INTEGRITY_CHANGE_DENIED"),
    }
    for event in events:
        allowed, code = permissions[event["type"]]
        if not allowed:
            reason_codes.append(code)
    reason_codes = sorted(set(reason_codes))
    return {
        "schema_version": VERIFY_SCHEMA,
        "decision": "FREEZE" if reason_codes else "ALLOW",
        "baseline_snapshot_sha256": baseline.get("snapshot_sha256"),
        "candidate_snapshot_sha256": candidate.get("snapshot_sha256"),
        "events": events,
        "reason_codes": reason_codes,
    }
