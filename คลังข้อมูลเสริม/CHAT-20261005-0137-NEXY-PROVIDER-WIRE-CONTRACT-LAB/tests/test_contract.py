from __future__ import annotations

import unittest

from nexy_wire import Direction, EventType, WireBoundary

from helpers import event, valid_text_transcript


class ContractTests(unittest.TestCase):
    def test_valid_text_transcript_passes(self) -> None:
        result = WireBoundary().validate(valid_text_transcript())
        self.assertTrue(result.accepted)
        self.assertFalse(result.frozen)
        self.assertIsNotNone(result.report)
        self.assertTrue(result.report.closed)
        self.assertEqual(result.report.event_count, 7)

    def test_valid_tool_roundtrip_passes(self) -> None:
        events = [
            event(0, EventType.STREAM_OPEN),
            event(1, EventType.TOOL_CALL_START, tool_call_id="tc1", payload={"name": "weather"}),
            event(2, EventType.TOOL_ARGUMENT_DELTA, tool_call_id="tc1", payload={"fragment": '{"city":"'}),
            event(3, EventType.TOOL_ARGUMENT_DELTA, tool_call_id="tc1", payload={"fragment": 'Bangkok"}'}),
            event(4, EventType.TOOL_CALL_END, tool_call_id="tc1"),
            event(
                5,
                EventType.TOOL_RESULT,
                tool_call_id="tc1",
                direction=Direction.CORE_TO_PROVIDER,
                payload={"result": {"temperature_c": 31}},
            ),
            event(6, EventType.STREAM_CLOSE),
        ]
        result = WireBoundary().validate(events)
        self.assertTrue(result.accepted)

    def test_same_transcript_has_same_hash(self) -> None:
        first = WireBoundary().validate(valid_text_transcript())
        second = WireBoundary().validate(valid_text_transcript())
        self.assertEqual(first.report.transcript_hash, second.report.transcript_hash)


if __name__ == "__main__":
    unittest.main()
