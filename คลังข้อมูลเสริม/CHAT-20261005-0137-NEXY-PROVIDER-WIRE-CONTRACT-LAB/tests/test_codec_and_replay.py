from __future__ import annotations

import math
import unittest

from nexy_wire import CanonicalEvent, Direction, EventType, SourceRef, WireContractError, canonical_json

from helpers import event


class CodecReplayTests(unittest.TestCase):
    def test_canonical_json_is_key_order_independent(self) -> None:
        self.assertEqual(canonical_json({"b": 2, "a": 1}), canonical_json({"a": 1, "b": 2}))

    def test_non_finite_numbers_are_rejected(self) -> None:
        with self.assertRaises(WireContractError) as ctx:
            canonical_json({"x": math.nan})
        self.assertEqual(ctx.exception.code, "NON_FINITE_NUMBER")

    def test_event_payload_is_deeply_defensively_frozen(self) -> None:
        payload = {"nested": {"items": [1, 2]}}
        e = event(0, EventType.STREAM_OPEN, payload=payload)
        baseline = e.fingerprint()
        payload["nested"]["items"].append(3)
        payload["nested"]["new"] = "mutated"
        self.assertEqual(tuple(e.payload["nested"]["items"]), (1, 2))
        self.assertEqual(e.fingerprint(), baseline)
        with self.assertRaises(TypeError):
            e.payload["nested"]["blocked"] = True

    def test_invalid_identifier_rejected(self) -> None:
        with self.assertRaises(WireContractError) as ctx:
            CanonicalEvent(
                stream_id="contains spaces",
                sequence=0,
                event_type=EventType.STREAM_OPEN,
                direction=Direction.PROVIDER_TO_CORE,
                source=SourceRef(provider="fixture"),
            )
        self.assertEqual(ctx.exception.code, "INVALID_ID")


if __name__ == "__main__":
    unittest.main()
