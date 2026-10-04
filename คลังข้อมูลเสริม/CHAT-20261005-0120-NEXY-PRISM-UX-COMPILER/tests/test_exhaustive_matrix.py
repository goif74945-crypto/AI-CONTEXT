from __future__ import annotations

import itertools
import unittest

from nexy_prism import (
    Action,
    DetailLevel,
    EvidenceStatus,
    RiskLevel,
    Role,
    SurfaceInput,
    SystemState,
    compile_surface,
    validate_plan,
)


class ExhaustiveInvariantMatrixTests(unittest.TestCase):
    def test_cross_product_invariants(self) -> None:
        checked = 0
        failures: list[str] = []

        # 430,080 deterministic scenarios:
        # 8 states × 5 roles × 7 evidence × 8 actions × 4 risks × 3 details
        # × 2 backend auth × 2 release auth × 2 recoverable × 2 irreversible.
        for (
            state,
            role,
            evidence,
            action,
            risk,
            detail,
            backend_authorized,
            release_authorized,
            recoverable,
            irreversible,
        ) in itertools.product(
            SystemState,
            Role,
            EvidenceStatus,
            Action,
            RiskLevel,
            DetailLevel,
            (False, True),
            (False, True),
            (False, True),
            (False, True),
        ):
            inp = SurfaceInput(
                system_state=state,
                role=role,
                evidence_status=evidence,
                requested_action=action,
                risk=risk,
                preferred_detail=detail,
                backend_authorized=backend_authorized,
                release_authorized=release_authorized,
                recoverable=recoverable,
                irreversible=irreversible,
                incident_code="INC-X" if state is SystemState.FREEZE else None,
                blocking_layer="LAW" if state is SystemState.FREEZE else None,
                backend_reason_code=None,
            )
            plan = compile_surface(inp)
            violations = validate_plan(inp, plan)
            checked += 1
            if violations:
                failures.append(
                    f"{checked}:{state.value}/{role.value}/{evidence.value}/{action.value}/"
                    f"{risk.value}/{detail.value}/ba={backend_authorized}/ra={release_authorized}/"
                    f"rec={recoverable}/irr={irreversible}: {violations}"
                )
                if len(failures) >= 10:
                    break

        self.assertFalse(failures, "\n".join(failures))
        self.assertEqual(checked, 430080)


if __name__ == "__main__":
    unittest.main()
