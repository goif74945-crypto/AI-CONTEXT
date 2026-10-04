from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Mapping, Sequence


class ConformanceInputError(ValueError):
    pass


class Severity(str, Enum):
    ERROR = "ERROR"
    WARN = "WARN"


VALID_STATUS = {"OK", "DEGRADED", "FREEZE", "STOP"}
VALID_STATE = {"INIT", "READY", "RUNNING", "VERIFYING", "CONSENSUS", "STABLE", "FREEZE", "STOP"}
VALID_ROLE = {"OWNER", "OPERATOR", "AUDITOR", "SYSTEM", "PUBLIC_USER"}
PENDING_STATES = {"INIT", "RUNNING", "VERIFYING", "CONSENSUS"}
SUCCESS_TOKENS = ("success", "successful", "completed", "verified result", "สำเร็จ", "ผ่านแล้ว")
STOP_RETRY_TOKENS = ("retry", "try again", "ลองอีกครั้ง", "recover")


@dataclass(frozen=True)
class Violation:
    code: str
    severity: str
    path: str
    message: str


@dataclass(frozen=True)
class AuditReport:
    schema_version: str
    conformant: bool
    violations: tuple[Violation, ...]
    request_id: str
    trace_id: str
    backend_status: str
    backend_state: str
    role: str
    certificate_fingerprint: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConformanceInputError(f"{field} must be non-empty text")
    return value.strip()


def _enum(value: Any, allowed: set[str], field: str) -> str:
    value = _text(value, field)
    if value not in allowed:
        raise ConformanceInputError(f"{field} is invalid: {value}")
    return value


def _mapping(value: Any, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ConformanceInputError(f"{field} must be an object")
    return value


def _bool(value: Any, field: str) -> bool:
    if not isinstance(value, bool):
        raise ConformanceInputError(f"{field} must be boolean")
    return value


def _surface_copy(surface: Mapping[str, Any]) -> str:
    parts = []
    for key in ("headline", "summary"):
        value = surface.get(key)
        if isinstance(value, str):
            parts.append(value.casefold())
    return " ".join(parts)


def _release_proof(data: Mapping[str, Any]) -> bool:
    ih = data.get("integrity_hash")
    return data.get("accepted") is True and data.get("releaseable") is True and isinstance(ih, str) and bool(ih.strip())


def _actions(surface: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    raw = surface.get("actions", [])
    if not isinstance(raw, list):
        raise ConformanceInputError("surface.actions must be an array")
    out: list[Mapping[str, Any]] = []
    for idx, item in enumerate(raw):
        if not isinstance(item, Mapping):
            raise ConformanceInputError(f"surface.actions[{idx}] must be an object")
        _text(item.get("id"), f"surface.actions[{idx}].id")
        kind = _text(item.get("kind"), f"surface.actions[{idx}].kind")
        if kind not in {"READ", "MUTATION_REQUEST"}:
            raise ConformanceInputError(f"surface.actions[{idx}].kind is invalid")
        if "requires_backend_authorization" in item and not isinstance(item["requires_backend_authorization"], bool):
            raise ConformanceInputError(f"surface.actions[{idx}].requires_backend_authorization must be boolean")
        if "requires_confirmation" in item and not isinstance(item["requires_confirmation"], bool):
            raise ConformanceInputError(f"surface.actions[{idx}].requires_confirmation must be boolean")
        out.append(item)
    return out


def _add(vs: list[Violation], code: str, path: str, message: str, severity: Severity = Severity.ERROR) -> None:
    vs.append(Violation(code, severity.value, path, message))


def audit_surface(backend: Mapping[str, Any], surface: Mapping[str, Any], role_raw: str) -> AuditReport:
    backend = _mapping(backend, "backend")
    surface = _mapping(surface, "surface")
    role = _enum(role_raw, VALID_ROLE, "role")
    status = _enum(backend.get("status"), VALID_STATUS, "backend.status")
    state = _enum(backend.get("state"), VALID_STATE, "backend.state")
    request_id = _text(backend.get("request_id"), "backend.request_id")
    trace_id = _text(backend.get("trace_id"), "backend.trace_id")
    displayed_status = _enum(surface.get("displayed_status"), VALID_STATUS, "surface.displayed_status")
    displayed_state = _enum(surface.get("displayed_state"), VALID_STATE, "surface.displayed_state")
    result_visible = _bool(surface.get("result_visible"), "surface.result_visible")
    actions = _actions(surface)
    copy = _surface_copy(surface)
    data = backend.get("data") if isinstance(backend.get("data"), Mapping) else {}
    freeze = backend.get("freeze") if isinstance(backend.get("freeze"), Mapping) else {}

    violations: list[Violation] = []

    if displayed_status != status:
        _add(violations, "STATUS_MISMATCH", "surface.displayed_status", "Rendered status differs from authoritative backend status.")
    if displayed_state != state:
        _add(violations, "STATE_MISMATCH", "surface.displayed_state", "Rendered state differs from authoritative backend state.")
    if surface.get("request_id") != request_id:
        _add(violations, "REQUEST_ID_MISMATCH", "surface.request_id", "Rendered request identity does not match the backend request.")
    if surface.get("trace_id") != trace_id:
        _add(violations, "TRACE_ID_MISMATCH", "surface.trace_id", "Rendered trace identity does not match the backend trace.")

    if result_visible and surface.get("result") is None:
        _add(violations, "VISIBLE_RESULT_MISSING", "surface.result", "Surface claims a visible result but no result payload is present.")

    if status == "FREEZE" or state == "FREEZE":
        if result_visible or surface.get("result") is not None:
            _add(violations, "FREEZE_RESULT_LEAK", "surface.result", "FREEZE must not expose a candidate/stale result.")
        if any(token in copy for token in SUCCESS_TOKENS):
            _add(violations, "FREEZE_SUCCESS_COPY", "surface.copy", "FREEZE copy must not imply success.")
        recoverable = freeze.get("recoverable") is True
        for idx, action in enumerate(actions):
            if action["kind"] == "MUTATION_REQUEST":
                if action["id"] != "recover":
                    _add(violations, "FREEZE_ILLEGAL_MUTATION", f"surface.actions[{idx}]", "FREEZE surface exposes an unrelated mutation action.")
                elif role != "OWNER" or not recoverable:
                    _add(violations, "RECOVER_VISIBILITY_VIOLATION", f"surface.actions[{idx}]", "Recover may be shown only to OWNER when the authoritative freeze is recoverable.")

    if status == "STOP" or state == "STOP":
        if result_visible or surface.get("result") is not None:
            _add(violations, "STOP_RESULT_LEAK", "surface.result", "STOP must not expose a result.")
        for idx, action in enumerate(actions):
            if action["kind"] == "MUTATION_REQUEST":
                _add(violations, "STOP_MUTATION_ACTION", f"surface.actions[{idx}]", "STOP surface must not expose ordinary mutation actions.")
        if any(token in copy for token in STOP_RETRY_TOKENS):
            _add(violations, "STOP_RETRY_COPY", "surface.copy", "STOP copy must not imply ordinary retry/recovery.")

    if state in PENDING_STATES:
        if result_visible or surface.get("result") is not None:
            _add(violations, "PENDING_RESULT_LEAK", "surface.result", "Pending states must not expose a final result.")
        if any(token in copy for token in SUCCESS_TOKENS):
            _add(violations, "PENDING_SUCCESS_COPY", "surface.copy", "Pending copy must not imply completion or verified success.")
        for idx, action in enumerate(actions):
            if action["kind"] == "MUTATION_REQUEST":
                _add(violations, "PENDING_MUTATION_ACTION", f"surface.actions[{idx}]", "Pending surface must not expose a new mutation request.")

    if state == "STABLE" and result_visible and not _release_proof(data):
        _add(violations, "RELEASE_PROOF_MISSING", "surface.result_visible", "A STABLE label alone is insufficient to expose a final result.")

    if state == "READY" and role in {"AUDITOR", "PUBLIC_USER"}:
        for idx, action in enumerate(actions):
            if action["kind"] == "MUTATION_REQUEST":
                _add(violations, "ROLE_MUTATION_VISIBILITY", f"surface.actions[{idx}]", f"{role} must not receive a mutation CTA from the truth surface.")

    for idx, action in enumerate(actions):
        if action["kind"] == "MUTATION_REQUEST":
            if action.get("requires_backend_authorization") is not True:
                _add(violations, "BACKEND_AUTH_FLAG_MISSING", f"surface.actions[{idx}].requires_backend_authorization", "Mutation CTA must state that backend authorization is required.")
            if action["id"] == "recover" and action.get("requires_confirmation") is not True:
                _add(violations, "RECOVER_CONFIRMATION_MISSING", f"surface.actions[{idx}].requires_confirmation", "Recover CTA must require explicit confirmation in this proposal.")

    normalized = {
        "schema_version": "1.0.0-proposal",
        "request_id": request_id,
        "trace_id": trace_id,
        "backend_status": status,
        "backend_state": state,
        "role": role,
        "violations": [asdict(v) for v in violations],
    }
    encoded = json.dumps(normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    fp = hashlib.sha256(encoded).hexdigest()
    return AuditReport(
        schema_version="1.0.0-proposal",
        conformant=not violations,
        violations=tuple(violations),
        request_id=request_id,
        trace_id=trace_id,
        backend_status=status,
        backend_state=state,
        role=role,
        certificate_fingerprint=fp,
    )


def assert_conformant(backend: Mapping[str, Any], surface: Mapping[str, Any], role: str) -> AuditReport:
    report = audit_surface(backend, surface, role)
    if not report.conformant:
        codes = ",".join(v.code for v in report.violations)
        raise AssertionError(f"truth surface is non-conformant: {codes}")
    return report
