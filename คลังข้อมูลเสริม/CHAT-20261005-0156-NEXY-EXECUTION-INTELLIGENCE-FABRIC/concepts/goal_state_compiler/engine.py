from __future__ import annotations

from copy import deepcopy
from typing import Any

from common import ContractError, require_dict, sorted_unique_strings, stable_hash


SET_FIELDS = ("required_capabilities", "forbidden_effects", "required_outputs")


def _normalize_spec(spec: dict[str, Any]) -> dict[str, Any]:
    spec = deepcopy(require_dict(spec, "spec"))
    allowed = {
        "required_facts",
        "forbidden_facts",
        "required_capabilities",
        "forbidden_effects",
        "required_outputs",
    }
    unknown = sorted(set(spec) - allowed)
    if unknown:
        raise ContractError(f"unknown goal fields: {unknown}")

    normalized: dict[str, Any] = {
        "required_facts": deepcopy(require_dict(spec.get("required_facts", {}), "required_facts")),
        "forbidden_facts": deepcopy(require_dict(spec.get("forbidden_facts", {}), "forbidden_facts")),
    }
    for field in SET_FIELDS:
        normalized[field] = sorted_unique_strings(spec.get(field, []), field)

    overlap = sorted(set(normalized["required_facts"]) & set(normalized["forbidden_facts"]))
    for key in overlap:
        if normalized["required_facts"][key] == normalized["forbidden_facts"][key]:
            raise ContractError(f"fact {key!r} cannot be both required and forbidden with the same value")
    return normalized


def compile_goal(spec: dict[str, Any]) -> dict[str, Any]:
    normalized = _normalize_spec(spec)
    return {
        "kind": "NEXY_GOAL_CONTRACT_V1",
        "contract_id": stable_hash(normalized, prefix="goal"),
        "spec": normalized,
    }


def evaluate_goal(contract: dict[str, Any], observed: dict[str, Any]) -> dict[str, Any]:
    contract = require_dict(contract, "contract")
    if contract.get("kind") != "NEXY_GOAL_CONTRACT_V1":
        raise ContractError("unsupported goal contract kind")
    spec = _normalize_spec(require_dict(contract.get("spec"), "contract.spec"))
    if contract.get("contract_id") != stable_hash(spec, prefix="goal"):
        raise ContractError("goal contract hash mismatch")

    observed = require_dict(observed, "observed")
    facts = require_dict(observed.get("facts", {}), "observed.facts")
    capabilities = set(sorted_unique_strings(observed.get("capabilities", []), "observed.capabilities"))
    effects = set(sorted_unique_strings(observed.get("effects", []), "observed.effects"))
    outputs = require_dict(observed.get("outputs", {}), "observed.outputs")

    missing: list[str] = []
    mismatches: list[dict[str, Any]] = []
    violations: list[dict[str, Any]] = []

    for key in sorted(spec["required_facts"]):
        if key not in facts:
            missing.append(f"fact:{key}")
        elif facts[key] != spec["required_facts"][key]:
            mismatches.append({"field": f"fact:{key}", "expected": spec["required_facts"][key], "observed": facts[key]})

    for key in sorted(spec["forbidden_facts"]):
        if key in facts and facts[key] == spec["forbidden_facts"][key]:
            violations.append({"field": f"fact:{key}", "forbidden": spec["forbidden_facts"][key]})

    for capability in spec["required_capabilities"]:
        if capability not in capabilities:
            missing.append(f"capability:{capability}")

    for effect in spec["forbidden_effects"]:
        if effect in effects:
            violations.append({"field": f"effect:{effect}", "forbidden": True})

    for output_key in spec["required_outputs"]:
        if output_key not in outputs:
            missing.append(f"output:{output_key}")

    if violations:
        status = "FREEZE"
    elif mismatches:
        status = "FAIL"
    elif missing:
        status = "NOT_VERIFIED"
    else:
        status = "PASS"

    result = {
        "status": status,
        "contract_id": contract["contract_id"],
        "missing": sorted(missing),
        "mismatches": mismatches,
        "violations": violations,
    }
    result["evaluation_id"] = stable_hash(result, prefix="goal-eval")
    return result
