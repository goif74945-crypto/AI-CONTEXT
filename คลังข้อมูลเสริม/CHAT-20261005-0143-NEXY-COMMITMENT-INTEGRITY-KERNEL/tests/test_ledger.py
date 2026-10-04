from __future__ import annotations

import unittest

from ncik.ledger import append_event, tamper_event, verify_ledger
from ncik.model import CommitmentState


class LedgerTests(unittest.TestCase):
    def test_empty_ledger_valid(self):
        self.assertTrue(verify_ledger(()))

    def test_append_and_verify(self):
        ledger = ()
        ledger = append_event(ledger, commitment_id="C1", revision=1, event_type="ACCEPT", state=CommitmentState.ACCEPTED)
        ledger = append_event(ledger, commitment_id="C1", revision=1, event_type="ACTIVATE", state=CommitmentState.ACTIVE)
        self.assertTrue(verify_ledger(ledger))
        self.assertEqual(ledger[1].previous_hash, ledger[0].event_hash)

    def test_tamper_detected(self):
        ledger = append_event((), commitment_id="C1", revision=1, event_type="ACCEPT", state=CommitmentState.ACCEPTED)
        tampered = tamper_event(ledger, 0, event_type="FULFILL")
        self.assertFalse(verify_ledger(tampered))

    def test_reordering_detected(self):
        ledger = ()
        ledger = append_event(ledger, commitment_id="C1", revision=1, event_type="ACCEPT", state=CommitmentState.ACCEPTED)
        ledger = append_event(ledger, commitment_id="C1", revision=1, event_type="ACTIVATE", state=CommitmentState.ACTIVE)
        self.assertFalse(verify_ledger(tuple(reversed(ledger))))

    def test_payload_tamper_detected(self):
        ledger = append_event((), commitment_id="C1", revision=1, event_type="ACCEPT", state=CommitmentState.ACCEPTED, payload={"a":"b"})
        from dataclasses import replace
        tampered = (replace(ledger[0], payload={"a":"c"}),)
        self.assertFalse(verify_ledger(tampered))

    def test_revision_bound_into_hash(self):
        a = append_event((), commitment_id="C1", revision=1, event_type="ACCEPT", state=CommitmentState.ACCEPTED)
        b = append_event((), commitment_id="C1", revision=2, event_type="ACCEPT", state=CommitmentState.ACCEPTED)
        self.assertNotEqual(a[0].event_hash, b[0].event_hash)


if __name__ == "__main__":
    unittest.main()
