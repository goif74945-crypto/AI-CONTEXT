from __future__ import annotations

import contextlib
import io
import json
import pathlib
import unittest

from nmdpc.cli import main


class CLITests(unittest.TestCase):
    def test_example_policy_compiles_without_payload_values(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[1]
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = main([str(root / "examples" / "support_case_policy.json")])
        self.assertEqual(rc, 0)
        plan = json.loads(out.getvalue())
        self.assertEqual(plan["decision"], "TRANSFORM")
        actions = {x["field_name"]: x["action"] for x in plan["field_decisions"]}
        self.assertEqual(actions["issue_title"], "INCLUDE_RAW")
        self.assertEqual(actions["customer_name"], "INCLUDE_TRANSFORMED")
        self.assertEqual(actions["provider_token"], "BROKER_OUT_OF_BAND")
        self.assertEqual(actions["full_account_history"], "OMIT_NOT_NEEDED")


if __name__ == "__main__":
    unittest.main()
