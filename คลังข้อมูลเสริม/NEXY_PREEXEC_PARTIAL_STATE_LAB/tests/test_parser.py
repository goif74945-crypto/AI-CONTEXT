from __future__ import annotations

import unittest

from nexy_pepsa.models import StepKind
from nexy_pepsa.parser import InputValidationError, parse_plan, parse_policy


class ParserTests(unittest.TestCase):
    def test_parse_minimal_read_plan(self) -> None:
        plan = parse_plan(
            {
                "plan_id": "read-only",
                "steps": [
                    {
                        "id": "read",
                        "kind": "READ",
                        "resource": "repo:AI-CONTEXT/README.md",
                        "boundary": "AI_CONTEXT",
                    }
                ],
            }
        )
        self.assertEqual(plan.steps[0].kind, StepKind.READ)
        self.assertEqual(plan.steps[0].depends_on, ())

    def test_unknown_step_field_is_rejected(self) -> None:
        with self.assertRaisesRegex(InputValidationError, "unknown fields"):
            parse_plan(
                {
                    "plan_id": "bad",
                    "steps": [
                        {
                            "id": "x",
                            "kind": "READ",
                            "resource": "r",
                            "boundary": "b",
                            "surprise": True,
                        }
                    ],
                }
            )

    def test_duplicate_dependency_is_rejected(self) -> None:
        with self.assertRaisesRegex(InputValidationError, "duplicates"):
            parse_plan(
                {
                    "plan_id": "bad",
                    "steps": [
                        {
                            "id": "x",
                            "kind": "READ",
                            "resource": "r",
                            "boundary": "b",
                            "depends_on": ["a", "a"],
                        }
                    ],
                }
            )

    def test_policy_requires_nonempty_allowed_boundaries(self) -> None:
        with self.assertRaisesRegex(InputValidationError, "must not be empty"):
            parse_policy(
                {
                    "policy_id": "p",
                    "allowed_boundaries": [],
                    "protected_resources": [],
                }
            )

    def test_bool_is_not_accepted_as_positive_integer(self) -> None:
        with self.assertRaisesRegex(InputValidationError, "positive integer"):
            parse_policy(
                {
                    "policy_id": "p",
                    "allowed_boundaries": ["AI_CONTEXT"],
                    "protected_resources": [],
                    "max_steps": True,
                }
            )

    def test_non_nfc_string_is_rejected(self) -> None:
        decomposed = "é"
        with self.assertRaisesRegex(InputValidationError, "NFC normalized"):
            parse_plan(
                {
                    "plan_id": decomposed,
                    "steps": [{"id": "x", "kind": "READ", "resource": "r", "boundary": "b"}],
                }
            )

    def test_control_character_is_rejected(self) -> None:
        with self.assertRaisesRegex(InputValidationError, "control characters"):
            parse_plan(
                {
                    "plan_id": "bad\nline",
                    "steps": [{"id": "x", "kind": "READ", "resource": "r", "boundary": "b"}],
                }
            )


if __name__ == "__main__":
    unittest.main()
