from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nexy_prism import (
    Action, DetailLevel, EvidenceStatus, RiskLevel, Role,
    SurfaceInput, SystemState, compile_surface,
)

SCENARIOS = {
    "verified_result": SurfaceInput(
        system_state=SystemState.STABLE,
        role=Role.OPERATOR,
        evidence_status=EvidenceStatus.PASS,
        requested_action=Action.VIEW_RESULT,
        risk=RiskLevel.LOW,
        preferred_detail=DetailLevel.COMPACT,
        backend_authorized=True,
        release_authorized=True,
        recoverable=False,
    ),
    "freeze_owner_recovery": SurfaceInput(
        system_state=SystemState.FREEZE,
        role=Role.OWNER,
        evidence_status=EvidenceStatus.FAIL,
        requested_action=Action.RECOVER_FREEZE,
        risk=RiskLevel.HIGH,
        preferred_detail=DetailLevel.COMPACT,
        backend_authorized=True,
        release_authorized=False,
        recoverable=True,
        incident_code="FREEZE-DEMO-001",
        blocking_layer="LAW",
    ),
}

for name, inp in SCENARIOS.items():
    plan = compile_surface(inp)
    print(json.dumps({"scenario": name, **plan.to_primitive()}, ensure_ascii=False, indent=2))
