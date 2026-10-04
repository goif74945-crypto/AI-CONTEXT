from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .model import Finding, JSONMapping, Severity, ValidationReport
from .rules import (
    CONFIRMATION_VALUES,
    EVIDENCE_CLASSES,
    FAILURE_MODES,
    HIGH_IMPACT_CLASSES,
    MUTATING_CLASSES,
    PROFILES,
    READ_ONLY,
    REQUIRED_VISIBLE_OUTCOMES,
    SIDE_EFFECT_CLASSES,
)


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _add(
    findings: list[Finding],
    severity: Severity,
    rule_id: str,
    path: str,
    message: str,
) -> None:
    findings.append(Finding(severity=severity, rule_id=rule_id, path=path, message=message))


def _as_string_set(value: Any) -> frozenset[str]:
    if not isinstance(value, list):
        return frozenset()
    return frozenset(item for item in value if isinstance(item, str))


def _validate_root(manifest: JSONMapping, findings: list[Finding]) -> tuple[str, str]:
    surface_id = manifest.get("surface_id")
    if not _is_nonempty_string(surface_id):
        _add(findings, Severity.ERROR, "HCAS-001", "$.surface_id", "surface_id must be a non-empty string")
        surface_id = "<unknown>"

    schema_version = manifest.get("schema_version")
    if schema_version != "1.0":
        _add(findings, Severity.ERROR, "HCAS-002", "$.schema_version", "schema_version must equal '1.0'")

    profile = manifest.get("profile", "current_vnext")
    if profile not in PROFILES:
        _add(
            findings,
            Severity.ERROR,
            "HCAS-003",
            "$.profile",
            f"unknown profile {profile!r}; supported profiles: {', '.join(sorted(PROFILES))}",
        )
        profile = "current_vnext"

    source_refs = manifest.get("source_refs")
    if not isinstance(source_refs, list) or not source_refs or not all(_is_nonempty_string(x) for x in source_refs):
        _add(
            findings,
            Severity.WARNING,
            "HCAS-004",
            "$.source_refs",
            "source_refs should contain at least one provenance reference",
        )

    return str(surface_id), str(profile)


def _validate_freeze_surface(manifest: JSONMapping, findings: list[Finding], profile: str) -> None:
    policy = PROFILES[profile]
    freeze = manifest.get("freeze_surface")
    if not isinstance(freeze, Mapping):
        if policy.require_freeze_surface:
            _add(findings, Severity.ERROR, "HCAS-110", "$.freeze_surface", "freeze_surface is required")
        return

    required_truths = {
        "visible": True,
        "sticky": True,
        "maskable": False,
        "authoritative": True,
    }
    for field, expected in required_truths.items():
        actual = freeze.get(field)
        if actual is not expected:
            _add(
                findings,
                Severity.ERROR,
                "HCAS-111",
                f"$.freeze_surface.{field}",
                f"freeze surface invariant requires {field}={expected!r}",
            )


def _validate_pending_state(manifest: JSONMapping, findings: list[Finding], profile: str) -> None:
    policy = PROFILES[profile]
    pending = manifest.get("pending_state")
    if not isinstance(pending, Mapping):
        if policy.require_pending_not_evidence:
            _add(findings, Severity.ERROR, "HCAS-120", "$.pending_state", "pending_state contract is required")
        return

    if pending.get("is_evidence") is not False:
        _add(
            findings,
            Severity.ERROR,
            "HCAS-121",
            "$.pending_state.is_evidence",
            "pending/loading state must never be classified as evidence",
        )
    if pending.get("success_claim") is not False:
        _add(
            findings,
            Severity.ERROR,
            "HCAS-122",
            "$.pending_state.success_claim",
            "pending/loading state must not claim success",
        )


def _validate_action(action: Mapping[str, Any], idx: int, findings: list[Finding], profile: str) -> str | None:
    base = f"$.actions[{idx}]"
    action_id = action.get("id")
    if not _is_nonempty_string(action_id):
        _add(findings, Severity.ERROR, "HCAS-010", f"{base}.id", "action id must be a non-empty string")
        action_id = None

    if not _is_nonempty_string(action.get("label")):
        _add(findings, Severity.ERROR, "HCAS-130", f"{base}.label", "action label must be a non-empty string")
    if not _is_nonempty_string(action.get("accessibility_name")):
        _add(
            findings,
            Severity.ERROR,
            "HCAS-131",
            f"{base}.accessibility_name",
            "interactive action requires an accessibility_name",
        )

    side_effect = action.get("side_effect")
    if side_effect not in SIDE_EFFECT_CLASSES:
        _add(
            findings,
            Severity.ERROR,
            "HCAS-020",
            f"{base}.side_effect",
            f"side_effect must be one of: {', '.join(sorted(SIDE_EFFECT_CLASSES))}",
        )
        return str(action_id) if action_id else None

    mutates = action.get("mutates")
    if not isinstance(mutates, bool):
        _add(findings, Severity.ERROR, "HCAS-021", f"{base}.mutates", "mutates must be boolean")
    elif (side_effect == READ_ONLY and mutates) or (side_effect in MUTATING_CLASSES and not mutates):
        _add(
            findings,
            Severity.ERROR,
            "HCAS-022",
            f"{base}.mutates",
            "mutates is inconsistent with side_effect class",
        )

    if side_effect in MUTATING_CLASSES and action.get("backend_authorization") is not True:
        _add(
            findings,
            Severity.ERROR,
            "HCAS-030",
            f"{base}.backend_authorization",
            "mutating action must require backend authorization; UI visibility is not authorization",
        )

    confirmation = action.get("confirmation")
    if confirmation not in CONFIRMATION_VALUES:
        _add(
            findings,
            Severity.ERROR,
            "HCAS-040",
            f"{base}.confirmation",
            f"confirmation must be one of: {', '.join(sorted(CONFIRMATION_VALUES))}",
        )
    elif side_effect in HIGH_IMPACT_CLASSES and confirmation not in PROFILES[profile].high_impact_confirmation:
        _add(
            findings,
            Severity.ERROR,
            "HCAS-041",
            f"{base}.confirmation",
            f"{side_effect} requires explicit confirmation under profile {profile}",
        )

    if side_effect in PROFILES[profile].require_dual_approval_for and confirmation != "DUAL_APPROVAL":
        _add(
            findings,
            Severity.ERROR,
            "HCAS-042",
            f"{base}.confirmation",
            f"profile {profile} requires DUAL_APPROVAL for {side_effect}",
        )

    if side_effect in MUTATING_CLASSES and not _is_nonempty_string(action.get("audit_event")):
        _add(
            findings,
            Severity.ERROR,
            "HCAS-050",
            f"{base}.audit_event",
            "mutating action requires an explicit audit_event",
        )

    if side_effect in MUTATING_CLASSES and action.get("failure_mode") not in FAILURE_MODES:
        _add(
            findings,
            Severity.ERROR,
            "HCAS-060",
            f"{base}.failure_mode",
            f"mutating action failure_mode must be one of: {', '.join(sorted(FAILURE_MODES))}",
        )

    if action.get("deterministic_result") is not True:
        _add(
            findings,
            Severity.ERROR,
            "HCAS-070",
            f"{base}.deterministic_result",
            "action contract must declare one defined structural result",
        )

    evidence = action.get("evidence_requirement")
    if evidence not in EVIDENCE_CLASSES:
        _add(
            findings,
            Severity.ERROR,
            "HCAS-080",
            f"{base}.evidence_requirement",
            f"evidence_requirement must be one of: {', '.join(sorted(EVIDENCE_CLASSES))}",
        )
    elif side_effect in MUTATING_CLASSES and evidence in {"E0", "E1"}:
        _add(
            findings,
            Severity.WARNING,
            "HCAS-081",
            f"{base}.evidence_requirement",
            "mutating user flow usually needs executed behavioral evidence, not presence/static proof alone",
        )

    outcomes = _as_string_set(action.get("visible_outcomes"))
    missing = REQUIRED_VISIBLE_OUTCOMES - outcomes
    if missing:
        _add(
            findings,
            Severity.ERROR,
            "HCAS-090",
            f"{base}.visible_outcomes",
            f"user-visible outcomes missing: {', '.join(sorted(missing))}",
        )
    if side_effect in MUTATING_CLASSES and not ({"FREEZE", "FAILURE"} & outcomes):
        _add(
            findings,
            Severity.ERROR,
            "HCAS-091",
            f"{base}.visible_outcomes",
            "mutating action must expose a visible FREEZE or FAILURE outcome",
        )

    required_role = action.get("required_role")
    visibility_role = action.get("ui_visibility_role")
    if not _is_nonempty_string(required_role):
        _add(findings, Severity.ERROR, "HCAS-100", f"{base}.required_role", "required_role must be explicit")
    if not _is_nonempty_string(visibility_role):
        _add(findings, Severity.ERROR, "HCAS-101", f"{base}.ui_visibility_role", "ui_visibility_role must be explicit")

    reversible = action.get("reversible")
    if not isinstance(reversible, bool):
        _add(findings, Severity.ERROR, "HCAS-140", f"{base}.reversible", "reversible must be boolean")
    elif reversible and not _is_nonempty_string(action.get("rollback_path")):
        _add(
            findings,
            Severity.ERROR,
            "HCAS-141",
            f"{base}.rollback_path",
            "reversible action must declare rollback_path",
        )
    elif not reversible and side_effect in MUTATING_CLASSES:
        if action.get("irreversible_warning") is not True:
            _add(
                findings,
                Severity.ERROR,
                "HCAS-142",
                f"{base}.irreversible_warning",
                "irreversible mutating action must declare irreversible_warning=true",
            )

    return str(action_id) if action_id else None


def validate_manifest(manifest: JSONMapping) -> ValidationReport:
    """Validate a control-surface manifest deterministically.

    The function performs no I/O and has no time/random/network dependency. Given the
    same manifest object, it returns the same ordered report.
    """

    if not isinstance(manifest, Mapping):
        finding = Finding(
            severity=Severity.ERROR,
            rule_id="HCAS-000",
            path="$",
            message="manifest must be a JSON object",
        )
        return ValidationReport(profile="current_vnext", surface_id="<unknown>", findings=(finding,))

    findings: list[Finding] = []
    surface_id, profile = _validate_root(manifest, findings)
    _validate_freeze_surface(manifest, findings, profile)
    _validate_pending_state(manifest, findings, profile)

    actions = manifest.get("actions")
    if not isinstance(actions, list) or not actions:
        _add(findings, Severity.ERROR, "HCAS-005", "$.actions", "actions must be a non-empty array")
    else:
        ids: list[str] = []
        for idx, action in enumerate(actions):
            if not isinstance(action, Mapping):
                _add(findings, Severity.ERROR, "HCAS-006", f"$.actions[{idx}]", "action must be an object")
                continue
            action_id = _validate_action(action, idx, findings, profile)
            if action_id:
                ids.append(action_id)
        duplicates = sorted({item for item in ids if ids.count(item) > 1})
        for duplicate in duplicates:
            _add(
                findings,
                Severity.ERROR,
                "HCAS-011",
                "$.actions",
                f"duplicate action id: {duplicate}",
            )

    return ValidationReport(profile=profile, surface_id=surface_id, findings=tuple(sorted(findings)))
