from __future__ import annotations

import unittest

from nexy_wire import Direction, EventType, WireBoundary

from helpers import event


class NegativePathTests(unittest.TestCase):
    def assertFrozen(self, events, code: str) -> None:
        result = WireBoundary().validate(events)
        self.assertFalse(result.accepted)
        self.assertTrue(result.frozen)
        self.assertEqual(result.error_code, code)

    def test_empty_transcript_freezes(self) -> None:
        self.assertFrozen([], "EMPTY_TRANSCRIPT")

    def test_rejects_missing_open(self) -> None:
        self.assertFrozen([event(0, EventType.STREAM_CLOSE)], "OPEN_REQUIRED")

    def test_rejects_sequence_gap(self) -> None:
        self.assertFrozen([event(0, EventType.STREAM_OPEN), event(2, EventType.STREAM_CLOSE)], "SEQUENCE_GAP")

    def test_rejects_event_after_close(self) -> None:
        self.assertFrozen(
            [event(0, EventType.STREAM_OPEN), event(1, EventType.STREAM_CLOSE), event(2, EventType.STREAM_CLOSE)],
            "EVENT_AFTER_CLOSE",
        )

    def test_rejects_open_message_at_close(self) -> None:
        self.assertFrozen(
            [event(0, EventType.STREAM_OPEN), event(1, EventType.MESSAGE_START, message_id="m1"), event(2, EventType.STREAM_CLOSE)],
            "OPEN_MESSAGE_AT_CLOSE",
        )

    def test_rejects_invalid_tool_json(self) -> None:
        self.assertFrozen(
            [
                event(0, EventType.STREAM_OPEN),
                event(1, EventType.TOOL_CALL_START, tool_call_id="tc1", payload={"name": "x"}),
                event(2, EventType.TOOL_ARGUMENT_DELTA, tool_call_id="tc1", payload={"fragment": "{"}),
                event(3, EventType.TOOL_CALL_END, tool_call_id="tc1"),
            ],
            "INVALID_TOOL_JSON",
        )

    def test_rejects_tool_result_wrong_direction(self) -> None:
        self.assertFrozen(
            [
                event(0, EventType.STREAM_OPEN),
                event(1, EventType.TOOL_CALL_START, tool_call_id="tc1", payload={"name": "x"}),
                event(2, EventType.TOOL_CALL_END, tool_call_id="tc1"),
                event(3, EventType.TOOL_RESULT, tool_call_id="tc1", payload={"result": 1}),
            ],
            "DIRECTION_MISMATCH",
        )

    def test_refusal_must_close_immediately(self) -> None:
        self.assertFrozen(
            [
                event(0, EventType.STREAM_OPEN),
                event(1, EventType.REFUSAL, payload={"reason": "policy"}),
                event(2, EventType.USAGE, payload={"input_tokens": 1, "output_tokens": 0}),
            ],
            "TERMINAL_EVENT_REQUIRES_CLOSE",
        )

    def test_unclosed_stream_freezes(self) -> None:
        self.assertFrozen([event(0, EventType.STREAM_OPEN)], "STREAM_NOT_CLOSED")


if __name__ == "__main__":
    unittest.main()
