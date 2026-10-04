from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from .canonical import ZERO_HASH, sha256_hex
from .errors import IntegrityError, ReplayError
from .model import Capsule, EventKind, TerminalState, authority_fingerprint


class ReplayPhase(str, Enum):
    INIT = "INIT"
    REQUESTED = "REQUESTED"
    CONTEXT_READY = "CONTEXT_READY"
    AUTHORITY_READY = "AUTHORITY_READY"
    ALLOWED = "ALLOWED"
    FROZEN = "FROZEN"
    EXECUTING = "EXECUTING"
    VERIFIED = "VERIFIED"
    TERMINAL = "TERMINAL"


@dataclass(frozen=True, slots=True)
class ReplayReport:
    capsule_id: str
    terminal_state: TerminalState
    final_phase: ReplayPhase
    event_count: int
    verification_statuses: tuple[str, ...]
    tool_actions: tuple[str, ...]
    freeze_reason: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "capsule_id": self.capsule_id,
            "terminal_state": self.terminal_state.value,
            "final_phase": self.final_phase.value,
            "event_count": self.event_count,
            "verification_statuses": list(self.verification_statuses),
            "tool_actions": list(self.tool_actions),
            "freeze_reason": self.freeze_reason,
        }


def _expect(condition: bool, message: str) -> None:
    if not condition:
        raise ReplayError(message)


def verify_integrity(capsule: Capsule) -> None:
    computed_authority = authority_fingerprint(capsule.authority_refs)
    if computed_authority != capsule.authority_fingerprint:
        raise IntegrityError("authority fingerprint mismatch")

    previous = ZERO_HASH
    for expected_sequence, event in enumerate(capsule.events):
        if event.sequence != expected_sequence:
            raise IntegrityError(
                f"non-contiguous sequence at index {expected_sequence}: got {event.sequence}"
            )
        if event.prev_hash != previous:
            raise IntegrityError(
                f"hash-chain mismatch at sequence {event.sequence}: prev_hash does not match"
            )
        if event.recompute_hash() != event.event_hash:
            raise IntegrityError(f"event hash mismatch at sequence {event.sequence}")
        previous = event.event_hash


def replay(capsule: Capsule) -> ReplayReport:
    verify_integrity(capsule)
    if not capsule.events:
        raise ReplayError("capsule must contain at least one event")

    phase = ReplayPhase.INIT
    authority_seen = False
    decision: str | None = None
    verification_statuses: list[str] = []
    open_tools: dict[str, dict[str, Any]] = {}
    completed_tools: list[str] = []
    freeze_reason: str | None = None
    final_seen = False

    for event in capsule.events:
        kind = event.kind
        payload = event.payload

        if final_seen:
            raise ReplayError("events after FINAL are forbidden")

        if kind is EventKind.REQUEST:
            _expect(phase is ReplayPhase.INIT, "REQUEST must be the first event")
            _expect(bool(str(payload.get("request_id", "")).strip()), "REQUEST requires request_id")
            phase = ReplayPhase.REQUESTED
            continue

        if kind is EventKind.CONTEXT_SELECTED:
            _expect(phase is ReplayPhase.REQUESTED, "CONTEXT_SELECTED must follow REQUEST")
            _expect(isinstance(payload.get("sources"), list), "CONTEXT_SELECTED requires sources list")
            phase = ReplayPhase.CONTEXT_READY
            continue

        if kind is EventKind.AUTHORITY_RESOLVED:
            _expect(phase is ReplayPhase.CONTEXT_READY, "AUTHORITY_RESOLVED must follow CONTEXT_SELECTED")
            _expect(
                payload.get("fingerprint") == capsule.authority_fingerprint,
                "AUTHORITY_RESOLVED fingerprint must equal capsule authority fingerprint",
            )
            authority_seen = True
            phase = ReplayPhase.AUTHORITY_READY
            continue

        if kind is EventKind.DECISION:
            _expect(phase is ReplayPhase.AUTHORITY_READY, "DECISION must follow AUTHORITY_RESOLVED")
            decision = str(payload.get("decision", ""))
            _expect(decision in {"ALLOW", "FREEZE"}, "DECISION must be ALLOW or FREEZE")
            if decision == "FREEZE":
                freeze_reason = str(payload.get("reason", "")).strip() or "unspecified freeze"
                phase = ReplayPhase.FROZEN
            else:
                phase = ReplayPhase.ALLOWED
            continue

        if kind is EventKind.TOOL_INTENT:
            _expect(decision == "ALLOW", "TOOL_INTENT requires an ALLOW decision")
            _expect(
                phase in {ReplayPhase.ALLOWED, ReplayPhase.EXECUTING},
                "TOOL_INTENT is only legal after ALLOW and before verification",
            )
            action_id = str(payload.get("action_id", "")).strip()
            _expect(bool(action_id), "TOOL_INTENT requires action_id")
            _expect(action_id not in open_tools and action_id not in completed_tools, "action_id must be unique")
            open_tools[action_id] = payload
            phase = ReplayPhase.EXECUTING
            continue

        if kind is EventKind.TOOL_RESULT:
            _expect(phase is ReplayPhase.EXECUTING, "TOOL_RESULT requires an active tool execution")
            action_id = str(payload.get("action_id", "")).strip()
            _expect(action_id in open_tools, "TOOL_RESULT action_id has no matching open intent")
            expected_intent_hash = sha256_hex(open_tools[action_id])
            provided_intent_hash = str(payload.get("intent_digest", ""))
            _expect(
                provided_intent_hash == expected_intent_hash,
                "TOOL_RESULT intent_digest does not match its TOOL_INTENT",
            )
            del open_tools[action_id]
            completed_tools.append(action_id)
            phase = ReplayPhase.ALLOWED if not open_tools else ReplayPhase.EXECUTING
            continue

        if kind is EventKind.VERIFICATION:
            _expect(decision == "ALLOW", "VERIFICATION requires an ALLOW decision")
            _expect(not open_tools, "VERIFICATION cannot run while tool intents are unresolved")
            _expect(
                phase in {ReplayPhase.ALLOWED, ReplayPhase.EXECUTING, ReplayPhase.VERIFIED},
                "VERIFICATION appears in an illegal phase",
            )
            status = str(payload.get("status", ""))
            _expect(
                status in {"PASS", "FAIL", "FREEZE", "BLOCKED", "NOT_VERIFIED"},
                "VERIFICATION has unsupported status",
            )
            verification_statuses.append(status)
            if status == "FREEZE" and freeze_reason is None:
                freeze_reason = str(payload.get("reason", "")).strip() or "verification freeze"
            phase = ReplayPhase.VERIFIED
            continue

        if kind is EventKind.FINAL:
            _expect(authority_seen, "FINAL requires authority resolution")
            _expect(not open_tools, "FINAL cannot close with unresolved tool intents")
            final_status = str(payload.get("status", ""))
            _expect(final_status == capsule.terminal_state.value, "FINAL status must match capsule terminal_state")
            _expect(
                payload.get("output_digest") == sha256_hex(payload.get("output")),
                "FINAL output_digest mismatch",
            )

            if capsule.terminal_state is TerminalState.PASS:
                _expect(decision == "ALLOW", "PASS requires ALLOW decision")
                _expect(bool(verification_statuses), "PASS requires at least one verification event")
                _expect(
                    all(status == "PASS" for status in verification_statuses),
                    "PASS requires every verification status to be PASS",
                )
            elif capsule.terminal_state is TerminalState.FREEZE:
                freeze_signal = decision == "FREEZE" or any(
                    status in {"FREEZE", "FAIL", "NOT_VERIFIED"} for status in verification_statuses
                )
                _expect(freeze_signal, "FREEZE requires a decision or verification freeze signal")
                if freeze_reason is None:
                    freeze_reason = str(payload.get("reason", "")).strip() or "terminal freeze"
            elif capsule.terminal_state is TerminalState.FAIL:
                _expect("FAIL" in verification_statuses, "FAIL requires a FAIL verification")
            elif capsule.terminal_state is TerminalState.BLOCKED:
                _expect("BLOCKED" in verification_statuses, "BLOCKED requires a BLOCKED verification")
            elif capsule.terminal_state is TerminalState.NOT_VERIFIED:
                _expect(
                    not verification_statuses or any(status == "NOT_VERIFIED" for status in verification_statuses),
                    "NOT_VERIFIED requires missing verification or NOT_VERIFIED evidence",
                )

            final_seen = True
            phase = ReplayPhase.TERMINAL
            continue

        raise ReplayError(f"unsupported event kind: {kind}")

    if not final_seen:
        raise ReplayError("capsule has no FINAL event")

    return ReplayReport(
        capsule_id=capsule.capsule_id,
        terminal_state=capsule.terminal_state,
        final_phase=phase,
        event_count=len(capsule.events),
        verification_statuses=tuple(verification_statuses),
        tool_actions=tuple(completed_tools),
        freeze_reason=freeze_reason,
    )
