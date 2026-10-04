from __future__ import annotations

from typing import Any

from common import ContractError, require_dict, stable_hash
from concepts.assurance_budget_planner.engine import plan_assurance
from concepts.counterexample_synthesizer.engine import synthesize_counterexamples
from concepts.goal_state_compiler.engine import compile_goal, evaluate_goal
from concepts.reversibility_envelope.engine import plan_reversibility
from concepts.unknown_closure_planner.engine import plan_unknown_closure


def evaluate_execution(payload: dict[str, Any]) -> dict[str, Any]:
    payload = require_dict(payload, "payload")
    required_sections = ["goal_spec", "observed", "uncertainty", "assurance", "actions", "input_schema", "valid_case"]
    missing = [key for key in required_sections if key not in payload]
    if missing:
        raise ContractError(f"missing integration sections: {missing}")

    goal_contract = compile_goal(payload["goal_spec"])
    goal = evaluate_goal(goal_contract, payload["observed"])
    unknowns = plan_unknown_closure(payload["uncertainty"])
    assurance = plan_assurance(payload["assurance"])
    reversibility = plan_reversibility(payload["actions"])
    counterexamples = synthesize_counterexamples(payload["input_schema"], payload["valid_case"])

    freeze_reasons: list[str] = []
    if goal["status"] in {"FREEZE", "FAIL"}:
        freeze_reasons.append(f"goal:{goal['status']}")
    if unknowns["status"] == "FREEZE":
        freeze_reasons.append(f"unknowns:{unknowns.get('reason')}")
    if assurance["status"] == "FREEZE":
        freeze_reasons.append(f"assurance:{assurance.get('reason')}")
    if reversibility["status"] == "FREEZE":
        freeze_reasons.append(f"reversibility:{reversibility.get('reason')}")
    if counterexamples["status"] == "FREEZE":
        freeze_reasons.append(f"counterexamples:{counterexamples.get('reason')}")

    if freeze_reasons:
        status = "FREEZE"
    elif goal["status"] == "NOT_VERIFIED":
        missing_goal = set(goal["missing"])
        planned_unknowns = set(unknowns.get("needed", []))
        if unknowns["status"] == "ASK" and missing_goal.issubset(planned_unknowns):
            status = "ASK"
        else:
            status = "FREEZE"
            freeze_reasons.append("goal:NOT_VERIFIED_WITHOUT_COMPLETE_RESOLUTION_PATH")
    elif unknowns["status"] == "ASK":
        status = "ASK"
    else:
        status = "READY"

    result = {
        "kind": "NEXY_EXECUTION_INTELLIGENCE_FABRIC_V1",
        "status": status,
        "freeze_reasons": freeze_reasons,
        "goal": goal,
        "unknown_closure": unknowns,
        "assurance": assurance,
        "reversibility": reversibility,
        "counterexamples": {
            "status": counterexamples["status"],
            "count": counterexamples.get("count", 0),
            "suite_id": counterexamples["suite_id"],
        },
    }
    result["decision_id"] = stable_hash(result, prefix="eif-decision")
    return result
