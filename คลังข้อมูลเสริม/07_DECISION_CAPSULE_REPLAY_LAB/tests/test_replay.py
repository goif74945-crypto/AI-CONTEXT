from __future__ import annotations

import unittest

from nexy_dcr.builder import CapsuleBuilder
from nexy_dcr.canonical import sha256_hex
from nexy_dcr.errors import ReplayError
from nexy_dcr.model import EventKind, TerminalState
from nexy_dcr.replay import replay

from helpers import authority_refs, build_pass_capsule, build_tool_capsule


class ReplayTests(unittest.TestCase):
    def test_valid_pass_replays(self) -> None:
        report = replay(build_pass_capsule())
        self.assertEqual(report.terminal_state, TerminalState.PASS)
        self.assertEqual(report.verification_statuses, ("PASS",))

    def test_valid_tool_pair_replays(self) -> None:
        report = replay(build_tool_capsule())
        self.assertEqual(report.tool_actions, ("a-1",))

    def test_pass_without_verification_is_rejected(self) -> None:
        builder = CapsuleBuilder(project_target="x", authority_refs=authority_refs())
        builder.append(EventKind.REQUEST, {"request_id": "r"})
        builder.append(EventKind.CONTEXT_SELECTED, {"sources": []})
        builder.append_authority_resolved()
        builder.append(EventKind.DECISION, {"decision": "ALLOW"})
        builder.append_final(status=TerminalState.PASS, output="bad")
        with self.assertRaisesRegex(ReplayError, "PASS requires at least one verification"):
            replay(builder.build(terminal_state=TerminalState.PASS))

    def test_freeze_decision_can_terminate_without_tool(self) -> None:
        builder = CapsuleBuilder(project_target="x", authority_refs=authority_refs())
        builder.append(EventKind.REQUEST, {"request_id": "r"})
        builder.append(EventKind.CONTEXT_SELECTED, {"sources": ["x"]})
        builder.append_authority_resolved()
        builder.append(EventKind.DECISION, {"decision": "FREEZE", "reason": "authority conflict"})
        builder.append_final(status=TerminalState.FREEZE, output=None, reason="authority conflict")
        report = replay(builder.build(terminal_state=TerminalState.FREEZE))
        self.assertEqual(report.freeze_reason, "authority conflict")

    def test_tool_after_freeze_is_rejected(self) -> None:
        builder = CapsuleBuilder(project_target="x", authority_refs=authority_refs())
        builder.append(EventKind.REQUEST, {"request_id": "r"})
        builder.append(EventKind.CONTEXT_SELECTED, {"sources": ["x"]})
        builder.append_authority_resolved()
        builder.append(EventKind.DECISION, {"decision": "FREEZE", "reason": "no unique output"})
        builder.append(EventKind.TOOL_INTENT, {"action_id": "a", "tool": "WRITE", "args": {}})
        builder.append_final(status=TerminalState.FREEZE, output=None)
        with self.assertRaisesRegex(ReplayError, "TOOL_INTENT requires an ALLOW decision"):
            replay(builder.build(terminal_state=TerminalState.FREEZE))

    def test_tool_result_requires_matching_intent_digest(self) -> None:
        builder = CapsuleBuilder(project_target="x", authority_refs=authority_refs())
        builder.append(EventKind.REQUEST, {"request_id": "r"})
        builder.append(EventKind.CONTEXT_SELECTED, {"sources": ["x"]})
        builder.append_authority_resolved()
        builder.append(EventKind.DECISION, {"decision": "ALLOW"})
        intent = {"action_id": "a", "tool": "READ", "args": {}}
        builder.append(EventKind.TOOL_INTENT, intent)
        builder.append(EventKind.TOOL_RESULT, {"action_id": "a", "intent_digest": "0" * 64})
        builder.append(EventKind.VERIFICATION, {"status": "PASS"})
        builder.append_final(status=TerminalState.PASS, output="x")
        with self.assertRaisesRegex(ReplayError, "intent_digest"):
            replay(builder.build(terminal_state=TerminalState.PASS))

    def test_unresolved_tool_blocks_verification(self) -> None:
        builder = CapsuleBuilder(project_target="x", authority_refs=authority_refs())
        builder.append(EventKind.REQUEST, {"request_id": "r"})
        builder.append(EventKind.CONTEXT_SELECTED, {"sources": ["x"]})
        builder.append_authority_resolved()
        builder.append(EventKind.DECISION, {"decision": "ALLOW"})
        builder.append(EventKind.TOOL_INTENT, {"action_id": "a", "tool": "READ", "args": {}})
        builder.append(EventKind.VERIFICATION, {"status": "PASS"})
        builder.append_final(status=TerminalState.PASS, output="x")
        with self.assertRaisesRegex(ReplayError, "unresolved"):
            replay(builder.build(terminal_state=TerminalState.PASS))

    def test_fail_terminal_requires_fail_verification(self) -> None:
        builder = CapsuleBuilder(project_target="x", authority_refs=authority_refs())
        builder.append(EventKind.REQUEST, {"request_id": "r"})
        builder.append(EventKind.CONTEXT_SELECTED, {"sources": ["x"]})
        builder.append_authority_resolved()
        builder.append(EventKind.DECISION, {"decision": "ALLOW"})
        builder.append(EventKind.VERIFICATION, {"status": "PASS"})
        builder.append_final(status=TerminalState.FAIL, output=None)
        with self.assertRaisesRegex(ReplayError, "FAIL requires a FAIL verification"):
            replay(builder.build(terminal_state=TerminalState.FAIL))

    def test_blocked_terminal_requires_blocked_verification(self) -> None:
        builder = CapsuleBuilder(project_target="x", authority_refs=authority_refs())
        builder.append(EventKind.REQUEST, {"request_id": "r"})
        builder.append(EventKind.CONTEXT_SELECTED, {"sources": ["x"]})
        builder.append_authority_resolved()
        builder.append(EventKind.DECISION, {"decision": "ALLOW"})
        builder.append(EventKind.VERIFICATION, {"status": "BLOCKED", "reason": "dependency unavailable"})
        builder.append_final(status=TerminalState.BLOCKED, output=None)
        report = replay(builder.build(terminal_state=TerminalState.BLOCKED))
        self.assertEqual(report.terminal_state, TerminalState.BLOCKED)

    def test_wrong_authority_fingerprint_event_is_rejected(self) -> None:
        builder = CapsuleBuilder(project_target="x", authority_refs=authority_refs())
        builder.append(EventKind.REQUEST, {"request_id": "r"})
        builder.append(EventKind.CONTEXT_SELECTED, {"sources": ["x"]})
        builder.append(EventKind.AUTHORITY_RESOLVED, {"fingerprint": "0" * 64})
        builder.append(EventKind.DECISION, {"decision": "ALLOW"})
        builder.append(EventKind.VERIFICATION, {"status": "PASS"})
        builder.append_final(status=TerminalState.PASS, output="x")
        with self.assertRaisesRegex(ReplayError, "fingerprint"):
            replay(builder.build(terminal_state=TerminalState.PASS))

    def test_tool_intent_digest_reference_positive(self) -> None:
        builder = CapsuleBuilder(project_target="x", authority_refs=authority_refs())
        builder.append(EventKind.REQUEST, {"request_id": "r"})
        builder.append(EventKind.CONTEXT_SELECTED, {"sources": ["x"]})
        builder.append_authority_resolved()
        builder.append(EventKind.DECISION, {"decision": "ALLOW"})
        intent = {"action_id": "a", "tool": "READ", "args": {"path": "x"}}
        builder.append(EventKind.TOOL_INTENT, intent)
        builder.append(EventKind.TOOL_RESULT, {"action_id": "a", "intent_digest": sha256_hex(intent)})
        builder.append(EventKind.VERIFICATION, {"status": "PASS"})
        builder.append_final(status=TerminalState.PASS, output="x")
        report = replay(builder.build(terminal_state=TerminalState.PASS))
        self.assertEqual(report.tool_actions, ("a",))


if __name__ == "__main__":
    unittest.main()
