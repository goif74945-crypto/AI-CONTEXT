from __future__ import annotations

from nexy_dcr.builder import CapsuleBuilder
from nexy_dcr.canonical import sha256_hex
from nexy_dcr.model import AuthorityRef, EventKind, TerminalState


def authority_refs() -> list[AuthorityRef]:
    return [
        AuthorityRef(
            path="AI-EXECUTION-KERNEL.md",
            sha="1" * 64,
            role="GLOBAL_EXECUTION_KERNEL",
            rank=1,
        ),
        AuthorityRef(
            path="projects/NEXY.AI/overview.md",
            sha="2" * 64,
            role="PROJECT_CONTEXT",
            rank=2,
        ),
    ]


def build_pass_capsule(*, output=None):
    builder = CapsuleBuilder(project_target="goif74945-crypto/NEXY.AI-", authority_refs=authority_refs())
    builder.append(EventKind.REQUEST, {"request_id": "req-001", "objective": "demo"})
    builder.append(EventKind.CONTEXT_SELECTED, {"sources": ["spec", "repo"]})
    builder.append_authority_resolved()
    builder.append(EventKind.DECISION, {"decision": "ALLOW"})
    builder.append(EventKind.VERIFICATION, {"status": "PASS", "claim": "demo invariant"})
    builder.append_final(status=TerminalState.PASS, output={"result": "ok"} if output is None else output)
    return builder.build(terminal_state=TerminalState.PASS)


def build_tool_capsule():
    builder = CapsuleBuilder(project_target="goif74945-crypto/NEXY.AI-", authority_refs=authority_refs())
    builder.append(EventKind.REQUEST, {"request_id": "req-tool", "objective": "tool demo"})
    builder.append(EventKind.CONTEXT_SELECTED, {"sources": ["spec"]})
    builder.append_authority_resolved()
    builder.append(EventKind.DECISION, {"decision": "ALLOW"})
    intent_payload = {"action_id": "a-1", "tool": "READ_ONLY_INSPECT", "args": {"path": "x"}}
    builder.append(EventKind.TOOL_INTENT, intent_payload)
    builder.append(
        EventKind.TOOL_RESULT,
        {"action_id": "a-1", "intent_digest": sha256_hex(intent_payload), "result": {"ok": True}},
    )
    builder.append(EventKind.VERIFICATION, {"status": "PASS", "claim": "tool result consumed"})
    builder.append_final(status=TerminalState.PASS, output={"result": "ok"})
    return builder.build(terminal_state=TerminalState.PASS)
