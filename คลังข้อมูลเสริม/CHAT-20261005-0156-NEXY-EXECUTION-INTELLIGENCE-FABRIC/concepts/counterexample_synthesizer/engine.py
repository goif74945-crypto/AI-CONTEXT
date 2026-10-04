from __future__ import annotations

from copy import deepcopy
from typing import Any

from common import ContractError, canonical_json, require_dict, require_str, stable_hash


def _type_ok(value: Any, kind: str) -> bool:
    if kind == "int":
        return isinstance(value, int) and not isinstance(value, bool)
    if kind == "string":
        return isinstance(value, str)
    if kind == "bool":
        return isinstance(value, bool)
    if kind == "enum":
        return isinstance(value, (str, int, float, bool)) and not isinstance(value, (dict, list))
    raise ContractError(f"unsupported field type: {kind}")


def validate_case(schema: dict[str, Any], case: dict[str, Any]) -> list[str]:
    schema = require_dict(schema, "schema")
    fields = require_dict(schema.get("fields", {}), "schema.fields")
    case = require_dict(case, "case")
    errors: list[str] = []

    for name in sorted(fields):
        rule = require_dict(fields[name], f"schema.fields.{name}")
        kind = require_str(rule.get("type"), f"schema.fields.{name}.type")
        required = rule.get("required", False)
        if not isinstance(required, bool):
            raise ContractError(f"schema.fields.{name}.required must be boolean")
        if name not in case:
            if required:
                errors.append(f"{name}:missing")
            continue
        value = case[name]
        if not _type_ok(value, kind):
            errors.append(f"{name}:wrong_type")
            continue
        if kind == "int":
            min_value = rule.get("min")
            max_value = rule.get("max")
            for label, bound in (("min", min_value), ("max", max_value)):
                if bound is not None and (not isinstance(bound, int) or isinstance(bound, bool)):
                    raise ContractError(f"schema.fields.{name}.{label} must be an integer")
            if min_value is not None and max_value is not None and min_value > max_value:
                raise ContractError(f"schema.fields.{name} has min greater than max")
            if min_value is not None and value < min_value:
                errors.append(f"{name}:below_min")
            if max_value is not None and value > max_value:
                errors.append(f"{name}:above_max")
        elif kind == "string":
            min_length = rule.get("min_length")
            max_length = rule.get("max_length")
            for label, bound in (("min_length", min_length), ("max_length", max_length)):
                if bound is not None and (not isinstance(bound, int) or isinstance(bound, bool) or bound < 0):
                    raise ContractError(f"schema.fields.{name}.{label} must be a non-negative integer")
            if min_length is not None and max_length is not None and min_length > max_length:
                raise ContractError(f"schema.fields.{name} has min_length greater than max_length")
            if min_length is not None and len(value) < min_length:
                errors.append(f"{name}:below_min_length")
            if max_length is not None and len(value) > max_length:
                errors.append(f"{name}:above_max_length")
        elif kind == "enum":
            values = rule.get("values")
            if not isinstance(values, list) or not values:
                raise ContractError(f"schema.fields.{name}.values must be a non-empty array")
            if value not in values:
                errors.append(f"{name}:outside_enum")
    return sorted(errors)


def synthesize_counterexamples(schema: dict[str, Any], valid_case: dict[str, Any]) -> dict[str, Any]:
    schema = require_dict(schema, "schema")
    fields = require_dict(schema.get("fields", {}), "schema.fields")
    valid_case = require_dict(valid_case, "valid_case")
    base_errors = validate_case(schema, valid_case)
    if base_errors:
        result = {"status": "FREEZE", "reason": "BASE_CASE_INVALID", "base_errors": base_errors, "vectors": []}
        result["suite_id"] = stable_hash(result, prefix="counterexample-suite")
        return result

    vectors: list[dict[str, Any]] = []
    seen_cases: set[str] = set()

    def add_vector(vector_id: str, mutation: str, candidate: dict[str, Any]) -> None:
        errors = validate_case(schema, candidate)
        if not errors:
            return
        fingerprint = canonical_json(candidate)
        if fingerprint in seen_cases:
            return
        seen_cases.add(fingerprint)
        vectors.append({"id": vector_id, "mutation": mutation, "input": candidate, "expected_errors": errors})

    for name in sorted(fields):
        rule = require_dict(fields[name], f"schema.fields.{name}")
        kind = require_str(rule.get("type"), f"schema.fields.{name}.type")
        required = rule.get("required", False)
        if required:
            candidate = deepcopy(valid_case)
            candidate.pop(name, None)
            add_vector(f"{name}__missing", f"remove:{name}", candidate)

        candidate = deepcopy(valid_case)
        if kind == "int":
            candidate[name] = "not-an-int"
            add_vector(f"{name}__wrong_type", f"wrong_type:{name}", candidate)
            if "min" in rule:
                candidate = deepcopy(valid_case)
                candidate[name] = int(rule["min"]) - 1
                add_vector(f"{name}__below_min", f"below_min:{name}", candidate)
            if "max" in rule:
                candidate = deepcopy(valid_case)
                candidate[name] = int(rule["max"]) + 1
                add_vector(f"{name}__above_max", f"above_max:{name}", candidate)
        elif kind == "string":
            candidate[name] = 0
            add_vector(f"{name}__wrong_type", f"wrong_type:{name}", candidate)
            if "min_length" in rule and int(rule["min_length"]) > 0:
                candidate = deepcopy(valid_case)
                candidate[name] = "x" * (int(rule["min_length"]) - 1)
                add_vector(f"{name}__below_min_length", f"below_min_length:{name}", candidate)
            if "max_length" in rule:
                candidate = deepcopy(valid_case)
                candidate[name] = "x" * (int(rule["max_length"]) + 1)
                add_vector(f"{name}__above_max_length", f"above_max_length:{name}", candidate)
        elif kind == "bool":
            candidate[name] = "true"
            add_vector(f"{name}__wrong_type", f"wrong_type:{name}", candidate)
        elif kind == "enum":
            candidate[name] = "__NEXY_INVALID_ENUM_SENTINEL__"
            add_vector(f"{name}__outside_enum", f"outside_enum:{name}", candidate)
        else:
            raise ContractError(f"unsupported field type: {kind}")

    vectors.sort(key=lambda v: v["id"])
    result = {"status": "PASS", "vectors": vectors, "count": len(vectors)}
    result["suite_id"] = stable_hash(result, prefix="counterexample-suite")
    return result
