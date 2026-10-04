from __future__ import annotations

import json
import unittest

from nexy_dcr.builder import CapsuleBuilder
from nexy_dcr.model import EventKind, TerminalState
from nexy_dcr.receipt import public_receipt

from helpers import authority_refs, build_tool_capsule


class ReceiptTests(unittest.TestCase):
    def test_receipt_contains_structural_proof_not_raw_payloads(self) -> None:
        builder = CapsuleBuilder(project_target="x", authority_refs=authority_refs())
        builder.append(EventKind.REQUEST, {"request_id": "r", "secret": "DO_NOT_LEAK_THIS"})
        builder.append(EventKind.CONTEXT_SELECTED, {"sources": ["x"], "secret": "DO_NOT_LEAK_THIS"})
        builder.append_authority_resolved()
        builder.append(EventKind.DECISION, {"decision": "ALLOW"})
        builder.append(EventKind.VERIFICATION, {"status": "PASS", "secret": "DO_NOT_LEAK_THIS"})
        builder.append_final(status=TerminalState.PASS, output={"secret": "DO_NOT_LEAK_THIS"})
        receipt = public_receipt(builder.build(terminal_state=TerminalState.PASS))
        rendered = json.dumps(receipt.to_dict(), ensure_ascii=False)
        self.assertNotIn("DO_NOT_LEAK_THIS", rendered)
        self.assertEqual(receipt.terminal_state, "PASS")

    def test_receipt_counts_tool_actions(self) -> None:
        receipt = public_receipt(build_tool_capsule())
        self.assertEqual(receipt.tool_action_count, 1)
        self.assertEqual(receipt.verification_status_counts, {"PASS": 1})


if __name__ == "__main__":
    unittest.main()
