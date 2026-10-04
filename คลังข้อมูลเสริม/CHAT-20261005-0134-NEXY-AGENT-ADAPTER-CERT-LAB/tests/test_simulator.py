from __future__ import annotations

import json
import unittest
from pathlib import Path

from nexy_adapter_cert.simulator import SimulationEvent, simulate

ROOT = Path(__file__).resolve().parents[1]


def fixture(name: str):
    return json.loads((ROOT / "fixtures" / name).read_text(encoding="utf-8"))


class SimulatorTests(unittest.TestCase):
    def test_valid_result_never_releases_directly(self):
        report = simulate(fixture("valid-noncritical.json"), SimulationEvent.RESULT_VALID)
        self.assertEqual(report.action, "CONTINUE_TO_CROSS_VERIFY")
        self.assertNotEqual(report.action, "RELEASE")

    def test_invalid_result_schema_freezes(self):
        report = simulate(fixture("valid-noncritical.json"), SimulationEvent.RESULT_SCHEMA_INVALID)
        self.assertEqual(report.action, "FREEZE")
        self.assertEqual(report.reason_code, "AGENT_SCHEMA_INVALID")

    def test_critical_timeout_freezes(self):
        report = simulate(fixture("valid-critical.json"), SimulationEvent.TIMEOUT, quorum_possible_after_exclusion=True)
        self.assertEqual(report.action, "FREEZE")
        self.assertEqual(report.reason_code, "AGENT_TIMEOUT_CRITICAL")

    def test_noncritical_timeout_can_exclude_when_quorum_survives(self):
        report = simulate(fixture("valid-noncritical.json"), SimulationEvent.TIMEOUT, quorum_possible_after_exclusion=True)
        self.assertEqual(report.action, "EXCLUDE_AGENT_AND_CONTINUE")

    def test_noncritical_timeout_freezes_when_quorum_would_fail(self):
        report = simulate(fixture("valid-noncritical.json"), SimulationEvent.TIMEOUT, quorum_possible_after_exclusion=False)
        self.assertEqual(report.action, "FREEZE")
        self.assertEqual(report.reason_code, "CONSENSUS_QUORUM_WOULD_FAIL")

    def test_unknown_quorum_freezes_instead_of_guessing(self):
        report = simulate(fixture("valid-noncritical.json"), SimulationEvent.TIMEOUT)
        self.assertEqual(report.action, "FREEZE")
        self.assertEqual(report.reason_code, "QUORUM_STATUS_UNKNOWN_ZERO_GUESS")

    def test_provider_failure_freezes(self):
        report = simulate(fixture("valid-noncritical.json"), SimulationEvent.PROVIDER_FAILURE)
        self.assertEqual(report.action, "FREEZE")
        self.assertEqual(report.reason_code, "DEPENDENCY_FAILURE")

    def test_invalid_manifest_freezes_before_execution(self):
        report = simulate(fixture("invalid-authority-escalation.json"), SimulationEvent.RESULT_VALID)
        self.assertEqual(report.status, "FAIL")
        self.assertEqual(report.action, "FREEZE_PRE_EXEC")


if __name__ == "__main__":
    unittest.main()
