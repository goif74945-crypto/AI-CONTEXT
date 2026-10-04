from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
from typing import Any, Mapping

from .canonical import sha256_json

SCHEMA_VERSION = "0.1.0"
SYSTEM_STATES = frozenset({
    "INIT", "READY", "RUNNING", "VERIFYING", "CONSENSUS", "STABLE", "FREEZE", "STOP"
})
KINDS = frozenset({
    "button", "input", "textarea", "select", "link", "tab", "tablist", "tabpanel",
    "dialog", "banner", "status", "error", "table", "control", "text"
})
SEVERITIES = ("BLOCKER", "ERROR", "WARNING", "MANUAL_REVIEW", "INFO")
STATUS_RANK = {"PASS": 0, "PARTIAL": 1, "FAIL": 2}

TOP_KEYS = frozenset({"schema_version", "surface_id", "route", "system_state", "components", "metadata"})
COMPONENT_KEYS = frozenset({
    "id", "kind", "visible", "interactive", "disabled", "native_semantics", "accessible_name",
    "text", "role", "action", "critical", "keyboard", "pointer", "semantics", "relationships",
    "form", "dialog", "tab", "table"
})


class SurfaceFormatError(ValueError):
    pass


def _expect(condition: bool, message: str) -> None:
    if not condition:
        raise SurfaceFormatError(message)


def _is_bool(value: Any) -> bool:
    return type(value) is bool


def _validate_mapping(value: Any, name: str) -> Mapping[str, Any]:
    _expect(isinstance(value, dict), f"{name} must be an object")
    return value


def _validate_surface_shape(raw: Any) -> dict[str, Any]:
    _expect(isinstance(raw, dict), "surface must be a JSON object")
    unknown = set(raw) - TOP_KEYS
    _expect(not unknown, f"unknown top-level keys: {sorted(unknown)}")
    for key in ("schema_version", "surface_id", "route", "system_state", "components", "metadata"):
        _expect(key in raw, f"missing required key: {key}")
    _expect(raw["schema_version"] == SCHEMA_VERSION, f"unsupported schema_version: {raw['schema_version']!r}")
    _expect(isinstance(raw["surface_id"], str) and raw["surface_id"].strip(), "surface_id must be non-empty string")
    _expect(isinstance(raw["route"], str) and raw["route"].strip(), "route must be non-empty string")
    _expect(raw["system_state"] in SYSTEM_STATES, f"invalid system_state: {raw['system_state']!r}")
    _expect(isinstance(raw["components"], list), "components must be an array")
    _expect(isinstance(raw["metadata"], dict), "metadata must be an object")
    _expect(raw["metadata"].get("classification") == "PROPOSAL_AI", "metadata.classification must equal PROPOSAL_AI")

    ids: set[str] = set()
    for index, component in enumerate(raw["components"]):
        prefix = f"components[{index}]"
        _validate_mapping(component, prefix)
        unknown_component = set(component) - COMPONENT_KEYS
        _expect(not unknown_component, f"{prefix} unknown keys: {sorted(unknown_component)}")
        for key in ("id", "kind", "visible", "interactive", "disabled", "native_semantics", "accessible_name", "text", "role", "action", "critical", "keyboard", "pointer", "semantics", "relationships", "form", "dialog", "tab", "table"):
            _expect(key in component, f"{prefix} missing key: {key}")
        cid = component["id"]
        _expect(isinstance(cid, str) and cid.strip(), f"{prefix}.id must be non-empty string")
        _expect(cid not in ids, f"duplicate component id: {cid}")
        ids.add(cid)
        _expect(component["kind"] in KINDS, f"{prefix}.kind invalid")
        for key in ("visible", "interactive", "disabled", "native_semantics", "critical"):
            _expect(_is_bool(component[key]), f"{prefix}.{key} must be boolean")
        for key in ("accessible_name", "text", "role", "action"):
            _expect(component[key] is None or isinstance(component[key], str), f"{prefix}.{key} must be string or null")
        for key in ("keyboard", "pointer", "semantics", "relationships", "form", "dialog", "tab", "table"):
            _expect(isinstance(component[key], dict), f"{prefix}.{key} must be object")
    return raw


def load_surface(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    try:
        raw = json.loads(source.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SurfaceFormatError(f"invalid JSON: {exc}") from exc
    return _validate_surface_shape(raw)


def validate_surface_shape(raw: Any) -> dict[str, Any]:
    return _validate_surface_shape(raw)


@dataclass(frozen=True, order=True)
class Finding:
    sort_key: tuple[int, str, str]
    rule_id: str
    severity: str
    component_id: str | None
    standard: str
    requirement: str
    message: str
    remediation: str

    @classmethod
    def create(
        cls,
        *,
        rule_id: str,
        severity: str,
        component_id: str | None,
        standard: str,
        requirement: str,
        message: str,
        remediation: str,
    ) -> "Finding":
        severity_order = {name: idx for idx, name in enumerate(SEVERITIES)}
        return cls(
            (severity_order[severity], rule_id, component_id or ""),
            rule_id,
            severity,
            component_id,
            standard,
            requirement,
            message,
            remediation,
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "component_id": self.component_id,
            "standard": self.standard,
            "requirement": self.requirement,
            "message": self.message,
            "remediation": self.remediation,
        }


@dataclass(frozen=True)
class ValidationReport:
    surface_id: str
    surface_digest: str
    status: str
    findings: tuple[Finding, ...]
    rule_count: int
    evaluated_component_count: int
    limits: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        payload = {
            "report_version": "0.1.0",
            "surface_id": self.surface_id,
            "surface_digest": self.surface_digest,
            "status": self.status,
            "rule_count": self.rule_count,
            "evaluated_component_count": self.evaluated_component_count,
            "finding_count": len(self.findings),
            "findings": [finding.as_dict() for finding in self.findings],
            "limits": list(self.limits),
        }
        payload["report_digest"] = sha256_json(payload)
        return payload
