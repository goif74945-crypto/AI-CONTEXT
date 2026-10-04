from __future__ import annotations

import json
from pathlib import Path

from nexy_adapter_cert.simulator import simulate
from nexy_adapter_cert.validator import validate_manifest

ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "fixtures" / name).read_text(encoding="utf-8"))


cases = {
    "valid_noncritical": validate_manifest(load("valid-noncritical.json")).status,
    "valid_critical": validate_manifest(load("valid-critical.json")).status,
    "invalid_critical_timeout": validate_manifest(load("invalid-critical-timeout.json")).status,
    "invalid_authority_escalation": validate_manifest(load("invalid-authority-escalation.json")).status,
    "valid_result": simulate(load("valid-noncritical.json"), "result_valid").action,
    "schema_invalid": simulate(load("valid-noncritical.json"), "result_schema_invalid").action,
    "noncritical_timeout_quorum": simulate(load("valid-noncritical.json"), "timeout", quorum_possible_after_exclusion=True).action,
    "noncritical_timeout_no_quorum": simulate(load("valid-noncritical.json"), "timeout", quorum_possible_after_exclusion=False).action,
    "noncritical_timeout_unknown": simulate(load("valid-noncritical.json"), "timeout").action,
    "critical_timeout": simulate(load("valid-critical.json"), "timeout", quorum_possible_after_exclusion=True).action,
}
print(json.dumps(cases, sort_keys=True, separators=(",", ":")))
