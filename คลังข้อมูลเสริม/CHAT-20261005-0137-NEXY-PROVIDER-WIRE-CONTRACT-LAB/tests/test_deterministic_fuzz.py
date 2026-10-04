from __future__ import annotations

import random
import unittest

from nexy_wire import EventType, WireBoundary

from helpers import event


class DeterministicFuzzTests(unittest.TestCase):
    def test_random_sequence_corruption_never_false_accepts(self) -> None:
        rng = random.Random(20261005)
        for _ in range(500):
            gap = rng.randint(1, 50)
            events = [event(0, EventType.STREAM_OPEN), event(gap, EventType.STREAM_CLOSE)]
            if gap == 1:
                self.assertTrue(WireBoundary().validate(events).accepted)
            else:
                result = WireBoundary().validate(events)
                self.assertFalse(result.accepted)
                self.assertTrue(result.frozen)
                self.assertEqual(result.error_code, "SEQUENCE_GAP")

    def test_random_invalid_tool_fragments_never_false_accept(self) -> None:
        rng = random.Random(74945)
        alphabet = "{[,:xyz"
        for _ in range(300):
            fragment = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 24)))
            events = [
                event(0, EventType.STREAM_OPEN),
                event(1, EventType.TOOL_CALL_START, tool_call_id="tc1", payload={"name": "tool"}),
                event(2, EventType.TOOL_ARGUMENT_DELTA, tool_call_id="tc1", payload={"fragment": fragment}),
                event(3, EventType.TOOL_CALL_END, tool_call_id="tc1"),
                event(4, EventType.STREAM_CLOSE),
            ]
            result = WireBoundary().validate(events)
            if result.accepted:
                # Acceptance is allowed only if the random fragment happens to be a JSON object.
                import json
                parsed = json.loads(fragment)
                self.assertIsInstance(parsed, dict)
            else:
                self.assertTrue(result.frozen)


if __name__ == "__main__":
    unittest.main()
