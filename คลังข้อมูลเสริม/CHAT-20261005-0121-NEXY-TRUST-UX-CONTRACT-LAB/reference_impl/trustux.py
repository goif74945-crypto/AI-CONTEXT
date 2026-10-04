from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Mapping, Sequence


class ContractError(ValueError):
    """Raised when an input cannot be rendered without violating truth-surface rules."""


class SystemStatus(str, Enum):
    OK = "OK"
    DEGRADED = "DEGRADED"
    FREEZE = "FREEZE"
    STOP = "STOP"


class SystemState(str, Enum):
    INIT = "INIT"
    READY = "READY"
    RUNNING = "RUNNING"
    VERIFYING = "VERIFYING"
    CONSENSUS = "CONSENSUS"
    STABLE = "STABLE"
    FREEZE = "FREEZE"
    STOP = "STOP"


class Role(str, Enum):
    OWNER = "OWNER"
    OPERATOR = "OPERATOR"
    AUDITOR = "AUDITOR"
    SYSTEM = "SYSTEM"
    PUBLIC_USER = "PUBLIC_USER"


class DisplayMode(str, Enum):
    RESULT = "RESULT"
    PENDING = "PENDING"
    FREEZE = "FREEZE"
    STOP = "STOP"
    HOLD = "HOLD"
    READY = "READY"


@dataclass(frozen=True)
class Action:
    id: str
    label: str
    kind: str
    requires_backend_authorization: bool = True
    requires_confirmation: bool = False


@dataclass(frozen=True)
class TrustCard:
    schema_version: str
    system_status: str
    system_state: str
    display_mode: str
    headline: str
    summary: str
    blocked: bool
    result_visible: bool
    result: Any | None
    primary_action: Action | None
    secondary_actions: tuple[Action, ...]
    request_id: str
    trace_id: str
    incident_code: str | None
    blocking_layer: str | None
    trigger: str | None
    recoverable: bool | None
    evidence_count: int | None
    integrity_hash_present: bool | None
    deterministic_fingerprint: str
    truth_flags: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        return payload


ERROR_COPY: Mapping[str, str] = {
    "INVALID_DIRECTIVE": "Directive rejected by validation.",
    "EMPTY_INPUT": "Input required.",
    "AMBIGUOUS_INPUT": "Directive is materially ambiguous.",
    "UNVERIFIED_OUTPUT": "Output is not verified for release.",
    "CONSENSUS_FAILED": "Consensus requirements were not satisfied.",
    "EVIDENCE_MISSING": "Required evidence is missing.",
    "SCHEMA_VIOLATION": "Schema invalid.",
    "STATE_TRANSITION_DENIED": "Requested state transition is not allowed.",
    "INVALID_STATE": "System state is invalid for this action.",
    "AUTH_INVALID": "Authentication is invalid.",
    "AUTH_EXPIRED": "Authentication has expired.",
    "UNAUTHORIZED": "Permission denied.",
    "FORBIDDEN": "Permission denied.",
    "SESSION_REVOKED": "Session has been revoked.",
    "DEVICE_MISMATCH": "Device verification failed.",
    "CSRF_INVALID": "Request integrity validation failed.",
    "OTAC_LOCKED": "Verification is temporarily locked.",
    "RATE_LIMIT_EXCEEDED": "Rate limit exceeded.",
    "SECURITY_BREACH_DETECTED": "Security breach detected.",
    "SYSTEM_IN_FREEZE": "System frozen.",
    "DEPENDENCY_FAILURE": "A required dependency failed.",
    "DEPENDENCY_UNHEALTHY": "A required dependency is unhealthy.",
    "TIMEOUT": "Execution timed out.",
    "AGENT_TIMEOUT": "An agent timed out.",
    "AGENT_SCHEMA_INVALID": "Agent response schema invalid.",
    "FREEZE_RECOVERY_DENIED": "Recovery is not allowed.",
    "VAULT_COMMIT_CONFLICT": "Vault commit conflict.",
    "REVISION_NOT_FOUND": "Revision not found.",
    "RELEASE_POLICY_FAILED": "Release policy failed.",
}

_PENDING_STATES = {
    SystemState.INIT,
    SystemState.RUNNING,
    SystemState.VERIFYING,
    SystemState.CONSENSUS,
}


def _enum(enum_type: type[Enum], raw: Any, field: str) -> Enum:
    try:
        return enum_type(str(raw))
    except ValueError as exc:
        allowed = ", ".join(member.value for member in enum_type)
        raise ContractError(f"{field} must be one of: {allowed}") from exc


def _required_text(data: Mapping[str, Any], field: str) -> str:
    value = data.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{field} is required and must be non-empty text")
    return value.strip()


def _safe_error_code(error: Any) -> str | None:
    if not isinstance(error, Mapping):
        return None
    code = error.get("code")
    if isinstance(code, str) and code.strip():
        return code.strip()
    return None


def _safe_text(mapping: Mapping[str, Any] | None, key: str) -> str | None:
    if not isinstance(mapping, Mapping):
        return None
    value = mapping.get(key)
    return value.strip() if isinstance(value, str) and value.strip() else None


def _int_or_none(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ContractError("evidence_count must be a non-negative integer when provided")
    return value


def _release_proof(data: Mapping[str, Any]) -> tuple[bool, int | None, bool]:
    accepted = data.get("accepted") is True
    releaseable = data.get("releaseable") is True
    integrity_hash = data.get("integrity_hash")
    integrity_hash_present = isinstance(integrity_hash, str) and bool(integrity_hash.strip())
    evidence_count = _int_or_none(data.get("evidence_count"))
    proof_ok = accepted and releaseable and integrity_hash_present
    return proof_ok, evidence_count, integrity_hash_present


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _fingerprint(payload_without_fingerprint: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(payload_without_fingerprint).encode("utf-8")).hexdigest()


def _primary_for_result(role: Role) -> Action:
    if role in {Role.OWNER, Role.OPERATOR, Role.AUDITOR}:
        return Action("view_result", "View Result", "READ")
    return Action("view_result", "View Result", "READ")


def _freeze_actions(role: Role, recoverable: bool) -> tuple[Action | None, tuple[Action, ...]]:
    inspect = Action("view_trace", "View Trace", "READ")
    if role == Role.OWNER and recoverable:
        recover = Action(
            "recover",
            "Recover",
            "MUTATION_REQUEST",
            requires_backend_authorization=True,
            requires_confirmation=True,
        )
        return recover, (inspect,)
    return inspect, tuple()


def _ready_actions(role: Role) -> tuple[Action | None, tuple[Action, ...]]:
    if role in {Role.OWNER, Role.OPERATOR}:
        return Action("new_directive", "New Directive", "MUTATION_REQUEST"), tuple()
    return Action("view_system", "View System", "READ"), tuple()


def _error_summary(code: str | None) -> str:
    if code is None:
        return "Execution is blocked by the authoritative system state."
    return ERROR_COPY.get(code, f"Execution blocked. Incident code: {code}.")


def compile_trust_card(envelope: Mapping[str, Any], role_raw: str) -> TrustCard:
    """Compile an authoritative backend envelope into a deterministic presentation contract.

    The compiler never upgrades a pending/unverified backend state into success. It also never
    grants authority; actions emitted here are visibility/request hints and still require backend
    authorization.
    """

    if not isinstance(envelope, Mapping):
        raise ContractError("envelope must be an object")

    status = _enum(SystemStatus, envelope.get("status"), "status")
    state = _enum(SystemState, envelope.get("state"), "state")
    role = _enum(Role, role_raw, "role")
    assert isinstance(status, SystemStatus)
    assert isinstance(state, SystemState)
    assert isinstance(role, Role)

    request_id = _required_text(envelope, "request_id")
    trace_id = _required_text(envelope, "trace_id")
    raw_data = envelope.get("data")
    data: Mapping[str, Any] = raw_data if isinstance(raw_data, Mapping) else {}
    error = envelope.get("error")
    error_code = _safe_error_code(error)
    freeze = envelope.get("freeze")
    freeze_obj: Mapping[str, Any] | None = freeze if isinstance(freeze, Mapping) else None

    truth_flags: list[str] = [
        "AUTHORITATIVE_BACKEND_STATE_REFLECTED",
        "UI_DOES_NOT_GRANT_AUTHORITY",
        "NO_INFERRED_SUCCESS",
        "ONE_PRIMARY_ACTION_MAX",
    ]

    incident_code: str | None = None
    blocking_layer: str | None = None
    trigger: str | None = None
    recoverable: bool | None = None
    evidence_count: int | None = None
    integrity_hash_present: bool | None = None
    result: Any | None = None
    result_visible = False

    if state == SystemState.STOP or status == SystemStatus.STOP:
        mode = DisplayMode.STOP
        headline = "System stopped"
        summary = _error_summary(error_code)
        blocked = True
        primary = Action("view_trace", "View Trace", "READ")
        secondary: tuple[Action, ...] = tuple()
        truth_flags.append("STOP_HAS_NO_AUTOMATIC_RECOVERY_ACTION")

    elif state == SystemState.FREEZE or status == SystemStatus.FREEZE:
        mode = DisplayMode.FREEZE
        headline = "System frozen"
        incident_code = _safe_text(freeze_obj, "incident_code") or error_code
        blocking_layer = _safe_text(freeze_obj, "blocking_layer")
        trigger = _safe_text(freeze_obj, "trigger")
        raw_recoverable = freeze_obj.get("recoverable") if freeze_obj else None
        if raw_recoverable is not None and not isinstance(raw_recoverable, bool):
            raise ContractError("freeze.recoverable must be boolean when provided")
        recoverable = bool(raw_recoverable) if raw_recoverable is not None else False
        summary = _error_summary(incident_code or error_code)
        blocked = True
        primary, secondary = _freeze_actions(role, recoverable)
        truth_flags.extend(("FREEZE_ALWAYS_VISIBLE", "RESULT_HIDDEN_DURING_FREEZE"))

    elif state == SystemState.STABLE:
        proof_ok, evidence_count, integrity_hash_present = _release_proof(data)
        if proof_ok and status in {SystemStatus.OK, SystemStatus.DEGRADED}:
            mode = DisplayMode.RESULT
            headline = "Verified result"
            summary = "Release conditions are satisfied by the supplied authoritative envelope."
            blocked = False
            result = data.get("output")
            result_visible = True
            primary = _primary_for_result(role)
            export_action = Action("export", "Export", "READ")
            secondary = (export_action,) if role in {Role.OWNER, Role.OPERATOR, Role.AUDITOR} else tuple()
            truth_flags.append("RESULT_VISIBLE_ONLY_WITH_RELEASE_PROOF")
        else:
            mode = DisplayMode.HOLD
            headline = "Result withheld"
            summary = "The authoritative envelope does not contain sufficient release proof."
            blocked = True
            primary = Action("view_trace", "View Trace", "READ")
            secondary = tuple()
            truth_flags.extend(("UNVERIFIED_RESULT_HIDDEN", "STABLE_DOES_NOT_IMPLY_RELEASEABLE"))

    elif state == SystemState.READY:
        mode = DisplayMode.READY
        headline = "Ready"
        summary = "System is ready for an authorized directive."
        blocked = False
        primary, secondary = _ready_actions(role)

    elif state in _PENDING_STATES:
        mode = DisplayMode.PENDING
        headline = {
            SystemState.INIT: "Initializing",
            SystemState.RUNNING: "Running",
            SystemState.VERIFYING: "Verifying",
            SystemState.CONSENSUS: "Evaluating consensus",
        }[state]
        summary = "No final result is released while this authoritative state is in progress."
        blocked = False
        primary = Action("inspect_run", "Inspect Run", "READ")
        secondary = tuple()
        truth_flags.append("PENDING_NEVER_RENDERED_AS_SUCCESS")

    else:  # pragma: no cover - enum exhaustiveness guard
        raise ContractError(f"Unhandled system state: {state.value}")

    if status == SystemStatus.DEGRADED and mode not in {DisplayMode.FREEZE, DisplayMode.STOP}:
        truth_flags.append("DEGRADED_STATUS_EXPOSED")
        summary = f"Degraded system status. {summary}"

    base = {
        "schema_version": "1.0.0-proposal",
        "system_status": status.value,
        "system_state": state.value,
        "display_mode": mode.value,
        "headline": headline,
        "summary": summary,
        "blocked": blocked,
        "result_visible": result_visible,
        "result": result,
        "primary_action": asdict(primary) if primary else None,
        "secondary_actions": [asdict(a) for a in secondary],
        "request_id": request_id,
        "trace_id": trace_id,
        "incident_code": incident_code,
        "blocking_layer": blocking_layer,
        "trigger": trigger,
        "recoverable": recoverable,
        "evidence_count": evidence_count,
        "integrity_hash_present": integrity_hash_present,
        "truth_flags": tuple(truth_flags),
    }
    fingerprint = _fingerprint(base)

    return TrustCard(
        schema_version="1.0.0-proposal",
        system_status=status.value,
        system_state=state.value,
        display_mode=mode.value,
        headline=headline,
        summary=summary,
        blocked=blocked,
        result_visible=result_visible,
        result=result,
        primary_action=primary,
        secondary_actions=secondary,
        request_id=request_id,
        trace_id=trace_id,
        incident_code=incident_code,
        blocking_layer=blocking_layer,
        trigger=trigger,
        recoverable=recoverable,
        evidence_count=evidence_count,
        integrity_hash_present=integrity_hash_present,
        deterministic_fingerprint=fingerprint,
        truth_flags=tuple(truth_flags),
    )


def validate_card(card: TrustCard) -> None:
    """Validate cross-field invariants after compilation."""

    if len(card.secondary_actions) > 2:
        raise ContractError("trust card may expose at most two secondary actions")
    if card.display_mode == DisplayMode.FREEZE.value:
        if not card.blocked or card.result_visible or card.result is not None:
            raise ContractError("FREEZE must block release and hide result")
    if card.display_mode == DisplayMode.STOP.value:
        action_ids = {a.id for a in card.secondary_actions}
        if card.primary_action:
            action_ids.add(card.primary_action.id)
        if "recover" in action_ids:
            raise ContractError("STOP must not expose automatic recovery")
    if card.display_mode == DisplayMode.RESULT.value:
        if not card.result_visible or card.blocked:
            raise ContractError("RESULT must be visible and non-blocked")
        if card.integrity_hash_present is not True:
            raise ContractError("RESULT requires integrity hash presence")
    if card.display_mode in {DisplayMode.PENDING.value, DisplayMode.HOLD.value} and card.result_visible:
        raise ContractError(f"{card.display_mode} must not expose result")


def compile_and_validate(envelope: Mapping[str, Any], role: str) -> TrustCard:
    card = compile_trust_card(envelope, role)
    validate_card(card)
    return card


def _load_json(path: Path) -> Mapping[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        value = json.load(fh)
    if not isinstance(value, Mapping):
        raise ContractError("input JSON root must be an object")
    return value


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile a NEXY Trust UX presentation contract proposal.")
    parser.add_argument("input", type=Path, help="Path to authoritative SystemEnvelope-like JSON")
    parser.add_argument("--role", required=True, choices=[r.value for r in Role])
    parser.add_argument("--pretty", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    envelope = _load_json(args.input)
    card = compile_and_validate(envelope, args.role)
    print(json.dumps(card.to_dict(), ensure_ascii=False, sort_keys=True, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
