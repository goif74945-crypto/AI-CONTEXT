from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any

from .canonical import sha256_hex
from .constants import (
    CRITICAL_TIMEOUT_MS,
    MAX_TIMEOUT_MS,
    MIN_TIMEOUT_MS,
    REQUIRED_OPERATIONS,
    RULES,
    SUPPORTED_MODES,
    SUPPORTED_SCHEMA_VERSION,
)

_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,63}$")
_SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    code: str
    path: str
    classification: str
    message: str


@dataclass(frozen=True, slots=True)
class ValidationReport:
    status: str
    manifest_digest: str
    issues: tuple[ValidationIssue, ...]
    required_evidence: tuple[str, ...]
    scope_statement: str
    report_digest: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "manifest_digest": self.manifest_digest,
            "issues": [asdict(issue) for issue in self.issues],
            "required_evidence": list(self.required_evidence),
            "scope_statement": self.scope_statement,
            "report_digest": self.report_digest,
        }


def _issue(code: str, path: str, classification: str, message: str) -> ValidationIssue:
    return ValidationIssue(code=code, path=path, classification=classification, message=message)


def _is_bool(value: Any) -> bool:
    return isinstance(value, bool)


def validate_manifest(manifest: Any) -> ValidationReport:
    """Validate a proposed NEXY AgentAdapter manifest.

    PASS means the candidate satisfies this standalone preflight contract only.
    It is not evidence of implementation, runtime behavior, deployment, or approval
    inside NEXY.AI.
    """
    issues: list[ValidationIssue] = []

    if not isinstance(manifest, dict):
        issues.append(_issue(RULES["schema_version"], "$", "PROPOSED_GUARD", "Manifest must be a JSON object."))
        return _build_report(manifest, issues)

    if manifest.get("schema_version") != SUPPORTED_SCHEMA_VERSION:
        issues.append(_issue(
            RULES["schema_version"],
            "$.schema_version",
            "PROPOSED_GUARD",
            f"schema_version must equal {SUPPORTED_SCHEMA_VERSION!r}.",
        ))

    adapter = manifest.get("adapter")
    if not isinstance(adapter, dict):
        issues.append(_issue("LAB.ADAPTER_OBJECT", "$.adapter", "PROPOSED_GUARD", "adapter must be an object."))
        return _build_report(manifest, issues)

    adapter_id = adapter.get("id")
    if not isinstance(adapter_id, str) or not _ID_RE.fullmatch(adapter_id):
        issues.append(_issue(
            RULES["adapter_id"],
            "$.adapter.id",
            "PROPOSED_GUARD",
            "id must be 3-64 lowercase characters using a-z, 0-9, dot, underscore, or hyphen.",
        ))

    provider = adapter.get("provider")
    if not isinstance(provider, str) or not provider.strip():
        issues.append(_issue(RULES["provider"], "$.adapter.provider", "PROPOSED_GUARD", "provider must be a non-empty string."))

    version = adapter.get("version")
    if not isinstance(version, str) or not _SEMVER_RE.fullmatch(version):
        issues.append(_issue(RULES["adapter_version"], "$.adapter.version", "PROPOSED_GUARD", "version must be valid SemVer."))

    modes = adapter.get("supported_modes")
    if not isinstance(modes, list) or not modes or any(not isinstance(mode, str) for mode in modes):
        issues.append(_issue(RULES["modes"], "$.adapter.supported_modes", "SOURCE_FACT", "supported_modes must be a non-empty string list."))
    else:
        mode_set = set(modes)
        unknown = sorted(mode_set - SUPPORTED_MODES)
        if unknown:
            issues.append(_issue(
                RULES["modes"],
                "$.adapter.supported_modes",
                "SOURCE_FACT",
                f"Unsupported NEXY mode(s): {', '.join(unknown)}; allowed: {', '.join(sorted(SUPPORTED_MODES))}.",
            ))
        if len(mode_set) != len(modes):
            issues.append(_issue("LAB.DUPLICATE_MODE", "$.adapter.supported_modes", "PROPOSED_GUARD", "supported_modes must not contain duplicates."))

    deterministic_capable = adapter.get("deterministic_capable")
    if not _is_bool(deterministic_capable):
        issues.append(_issue("DOC-C.DETERMINISTIC_CAPABILITY_DECLARED", "$.adapter.deterministic_capable", "SOURCE_FACT", "deterministic_capable must be boolean."))

    critical = adapter.get("critical")
    if not _is_bool(critical):
        issues.append(_issue("DOC-C.CRITICAL_FLAG_DECLARED", "$.adapter.critical", "SOURCE_FACT", "critical must be boolean."))

    timeout_ms = adapter.get("timeout_ms")
    if isinstance(timeout_ms, bool) or not isinstance(timeout_ms, int) or not (MIN_TIMEOUT_MS <= timeout_ms <= MAX_TIMEOUT_MS):
        issues.append(_issue(
            RULES["timeout_range"],
            "$.adapter.timeout_ms",
            "SOURCE_FACT",
            f"timeout_ms must be an integer in [{MIN_TIMEOUT_MS}, {MAX_TIMEOUT_MS}].",
        ))
    elif critical is True and timeout_ms != CRITICAL_TIMEOUT_MS:
        issues.append(_issue(
            RULES["critical_timeout"],
            "$.adapter.timeout_ms",
            "SOURCE_FACT",
            f"critical adapters must use the canonical {CRITICAL_TIMEOUT_MS} ms timeout.",
        ))

    capacity = adapter.get("context_capacity")
    if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity <= 0:
        issues.append(_issue(RULES["context_capacity"], "$.adapter.context_capacity", "SOURCE_FACT", "context_capacity must be a positive integer."))

    operations = adapter.get("operations")
    if not isinstance(operations, list) or any(not isinstance(op, str) for op in operations):
        issues.append(_issue(RULES["operations"], "$.adapter.operations", "SOURCE_FACT", "operations must be a string list."))
    else:
        missing = sorted(REQUIRED_OPERATIONS - set(operations))
        if missing:
            issues.append(_issue(
                RULES["operations"],
                "$.adapter.operations",
                "SOURCE_FACT",
                f"Missing required AgentAdapter operation(s): {', '.join(missing)}.",
            ))

    authority = manifest.get("authority")
    if not isinstance(authority, dict):
        issues.append(_issue("LAB.AUTHORITY_OBJECT", "$.authority", "PROPOSED_GUARD", "authority must be an object."))
    else:
        _require_exact_bool(authority, "candidate_only", True, RULES["candidate_only"], "SOURCE_FACT", issues)
        _require_exact_bool(authority, "direct_release", False, RULES["direct_release"], "SOURCE_FACT", issues)
        _require_exact_bool(authority, "direct_vault_write", False, RULES["direct_vault_write"], "SOURCE_FACT", issues)
        _require_exact_bool(authority, "mutates_core_state", False, RULES["mutates_core_state"], "SOURCE_FACT", issues)
        _require_exact_bool(authority, "automatic_retry", False, RULES["automatic_retry"], "SOURCE_FACT", issues)

    security = manifest.get("security")
    if not isinstance(security, dict):
        issues.append(_issue("LAB.SECURITY_OBJECT", "$.security", "PROPOSED_GUARD", "security must be an object."))
    else:
        if security.get("secret_delivery") != "runtime_injection":
            issues.append(_issue(
                RULES["secret_delivery"],
                "$.security.secret_delivery",
                "SOURCE_FACT",
                "secret_delivery must be 'runtime_injection'; provider secrets must not be embedded in adapter artifacts.",
            ))
        _require_exact_bool(security, "persists_secrets", False, RULES["secret_persistence"], "SOURCE_FACT", issues)

    return _build_report(manifest, issues)


def _require_exact_bool(
    obj: dict[str, Any],
    field: str,
    expected: bool,
    code: str,
    classification: str,
    issues: list[ValidationIssue],
) -> None:
    value = obj.get(field)
    if not _is_bool(value) or value is not expected:
        issues.append(_issue(code, f"$.authority.{field}" if field != "persists_secrets" else f"$.security.{field}", classification, f"{field} must be {str(expected).lower()}."))


def _build_report(manifest: Any, issues: list[ValidationIssue]) -> ValidationReport:
    ordered_issues = tuple(sorted(issues, key=lambda i: (i.code, i.path, i.message)))
    status = "PASS" if not ordered_issues else "FAIL"
    required_evidence = (
        "E1: schema/static validation of the real adapter implementation",
        "E2: unit tests for execute/cancel/healthcheck and result parsing",
        "E3: integration tests through the real NEXY SWARM adapter boundary",
        "E5: runtime timeout/health/failure evidence before operational claims",
    )
    scope_statement = (
        "Standalone preflight only. PASS does not prove NEXY.AI implementation, runtime integration, "
        "release eligibility, deployment readiness, or provider correctness."
    )
    manifest_digest = sha256_hex(manifest)
    digest_payload = {
        "status": status,
        "manifest_digest": manifest_digest,
        "issues": [asdict(issue) for issue in ordered_issues],
        "required_evidence": list(required_evidence),
        "scope_statement": scope_statement,
    }
    return ValidationReport(
        status=status,
        manifest_digest=manifest_digest,
        issues=ordered_issues,
        required_evidence=required_evidence,
        scope_statement=scope_statement,
        report_digest=sha256_hex(digest_payload),
    )
