from __future__ import annotations

import json
import sys
from typing import Any

from .canonical import canonical_json
from .compiler import compile_contract, contract_from_dict
from .errors import OutcomeFabricError
from .frontier import satisfaction_frontier
from .recovery import plan_recovery
from .regression import benefit_regression_guard
from .verifier import verify_outcome


def dispatch(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise OutcomeFabricError("input must be an object")
    operation = payload.get("operation")
    if operation == "compile":
        contract, digest = compile_contract(payload.get("spec"))
        return {"status": "PASS", "contract": contract.to_dict(), "contract_hash": digest}
    contract = contract_from_dict(payload.get("contract"))
    if operation == "verify":
        return verify_outcome(contract, payload.get("observation"))
    if operation == "frontier":
        return satisfaction_frontier(contract, payload.get("candidates", []))
    if operation == "regression":
        return benefit_regression_guard(contract, payload.get("baseline"), payload.get("candidate"))
    if operation == "recover":
        return plan_recovery(
            contract,
            payload.get("observation"),
            payload.get("actions", []),
            max_cost=payload.get("max_cost"),
            max_risk=payload.get("max_risk"),
            require_reversible=payload.get("require_reversible", True),
        )
    raise OutcomeFabricError(f"unsupported operation: {operation!r}")


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        result = dispatch(payload)
        sys.stdout.write(canonical_json(result) + "
")
        return 0
    except (OutcomeFabricError, json.JSONDecodeError, TypeError) as exc:
        sys.stdout.write(canonical_json({"status": "FREEZE", "error": str(exc)}) + "
")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
