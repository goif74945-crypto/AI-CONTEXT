from __future__ import annotations

import unittest

from nexy_dcr.builder import CapsuleBuilder
from nexy_dcr.diff import diff_capsules
from nexy_dcr.model import AuthorityRef, EventKind, TerminalState

from helpers import authority_refs, build_pass_capsule


class DiffTests(unittest.TestCase):
    def test_identical_capsules_have_no_divergence(self) -> None:
        left = build_pass_capsule()
        right = build_pass_capsule()
        self.assertEqual(diff_capsules(left, right), [])

    def test_output_change_is_detected_as_event_payload_divergence(self) -> None:
        left = build_pass_capsule(output={"answer": 1})
        right = build_pass_capsule(output={"answer": 2})
        categories = [d.category for d in diff_capsules(left, right)]
        self.assertIn("event_payload", categories)

    def test_authority_change_is_detected(self) -> None:
        left = build_pass_capsule()
        changed_refs = authority_refs() + [
            AuthorityRef(path="new-law.md", sha="3" * 64, role="NEW_AUTHORITY", rank=0)
        ]
        builder = CapsuleBuilder(project_target="goif74945-crypto/NEXY.AI-", authority_refs=changed_refs)
        builder.append(EventKind.REQUEST, {"request_id": "req-001", "objective": "demo"})
        builder.append(EventKind.CONTEXT_SELECTED, {"sources": ["spec", "repo"]})
        builder.append_authority_resolved()
        builder.append(EventKind.DECISION, {"decision": "ALLOW"})
        builder.append(EventKind.VERIFICATION, {"status": "PASS", "claim": "demo invariant"})
        builder.append_final(status=TerminalState.PASS, output={"result": "ok"})
        right = builder.build(terminal_state=TerminalState.PASS)
        categories = [d.category for d in diff_capsules(left, right)]
        self.assertIn("authority", categories)


if __name__ == "__main__":
    unittest.main()
