from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Mapping

from .canonical import diagnostic_digest, digest
from .errors import ContractError, NumericIntegrityError, ObservationError, UnitError
from .rational import canonical_fraction, parse_rational, quantize
from .units import BUILTIN_REGISTRY, UnitRegistry


@dataclass(frozen=True)
class Bound:
    value: Fraction
    inclusive: bool

    def record(self) -> dict[str, object]:
        return {"value": canonical_fraction(self.value), "inclusive": self.inclusive}


@dataclass(frozen=True)
class NormalizedContract:
    name: str
    dimension: str
    canonical_unit: str
    lower: Bound | None
    upper: Bound | None
    quantum: Fraction | None
    rounding_mode: str | None

    def record(self) -> dict[str, object]:
        return {
            "schema_version": "1",
            "name": self.name,
            "dimension": self.dimension,
            "canonical_unit": self.canonical_unit,
            "lower": self.lower.record() if self.lower else None,
            "upper": self.upper.record() if self.upper else None,
            "normalization": {
                "quantum": canonical_fraction(self.quantum) if self.quantum is not None else None,
                "rounding_mode": self.rounding_mode,
            },
            "uncertainty_policy": "FREEZE_ON_BOUNDARY_OVERLAP",
        }


@dataclass(frozen=True)
class NormalizedObservation:
    source_value: Fraction
    source_unit: str
    canonical_value: Fraction
    uncertainty_abs: Fraction
    interval_low: Fraction
    interval_high: Fraction

    def record(self) -> dict[str, str]:
        return {
            "source_value": canonical_fraction(self.source_value),
            "source_unit": self.source_unit,
            "canonical_value": canonical_fraction(self.canonical_value),
            "uncertainty_abs": canonical_fraction(self.uncertainty_abs),
            "interval_low": canonical_fraction(self.interval_low),
            "interval_high": canonical_fraction(self.interval_high),
        }


def _mapping(value: Any, field: str, error_type: type[NumericIntegrityError]) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise error_type("INVALID_STRUCTURE", f"{field} must be an object")
    bad_keys = [key for key in value if not isinstance(key, str)]
    if bad_keys:
        raise error_type("NON_STRING_FIELD_NAME", f"{field} field names must be strings")
    return value


def _unknown_fields(data: Mapping[str, Any], allowed: set[str]) -> list[str]:
    return sorted(key for key in data if key not in allowed)


def _parse_bound(raw: Any, field: str) -> Bound | None:
    if raw is None:
        return None
    data = _mapping(raw, field, ContractError)
    if set(data) != {"value", "inclusive"}:
        raise ContractError("INVALID_BOUND", f"{field} must contain exactly value and inclusive")
    if not isinstance(data["inclusive"], bool):
        raise ContractError("INVALID_BOUND", f"{field}.inclusive must be boolean")
    try:
        value = parse_rational(data["value"], field=f"{field}.value")
    except NumericIntegrityError as exc:
        raise ContractError(exc.code, exc.message, exc.details) from exc
    return Bound(value=value, inclusive=data["inclusive"])


def normalize_contract(raw: Any, registry: UnitRegistry = BUILTIN_REGISTRY) -> NormalizedContract:
    data = _mapping(raw, "contract", ContractError)
    allowed = {"schema_version", "name", "dimension", "canonical_unit", "lower", "upper", "normalization", "uncertainty_policy"}
    unknown = _unknown_fields(data, allowed)
    if unknown:
        raise ContractError("UNKNOWN_CONTRACT_FIELD", "contract contains unsupported fields", {"fields": unknown})
    if data.get("schema_version") != "1":
        raise ContractError("UNSUPPORTED_SCHEMA", "contract.schema_version must equal '1'")
    name = data.get("name")
    dimension = data.get("dimension")
    canonical_unit = data.get("canonical_unit")
    if not isinstance(name, str) or not name:
        raise ContractError("INVALID_CONTRACT_NAME", "contract.name must be a non-empty string")
    if not isinstance(dimension, str) or not dimension:
        raise ContractError("INVALID_DIMENSION", "contract.dimension must be a non-empty string")
    if not isinstance(canonical_unit, str) or not canonical_unit:
        raise ContractError("INVALID_CANONICAL_UNIT", "contract.canonical_unit must be a non-empty string")
    try:
        registry.require_dimension(canonical_unit, dimension)
    except UnitError as exc:
        raise ContractError(exc.code, exc.message, exc.details) from exc

    lower = _parse_bound(data.get("lower"), "lower")
    upper = _parse_bound(data.get("upper"), "upper")
    if lower is None and upper is None:
        raise ContractError("UNBOUNDED_CONTRACT", "at least one of lower or upper must be defined")
    if lower is not None and upper is not None:
        if lower.value > upper.value:
            raise ContractError("INVALID_BOUND_ORDER", "lower bound must be <= upper bound")
        if lower.value == upper.value and not (lower.inclusive and upper.inclusive):
            raise ContractError("EMPTY_ACCEPTANCE_SET", "equal bounds must both be inclusive")

    normalization = data.get("normalization")
    quantum = None
    rounding_mode = None
    if normalization is not None:
        n = _mapping(normalization, "normalization", ContractError)
        if set(n) != {"quantum", "rounding_mode"}:
            raise ContractError("INVALID_NORMALIZATION", "normalization must contain exactly quantum and rounding_mode")
        if n["quantum"] is None and n["rounding_mode"] is None:
            pass
        elif n["quantum"] is None or n["rounding_mode"] is None:
            raise ContractError("INCOMPLETE_NORMALIZATION", "quantum and rounding_mode must be supplied together")
        else:
            try:
                quantum = parse_rational(n["quantum"], field="normalization.quantum")
            except NumericIntegrityError as exc:
                raise ContractError(exc.code, exc.message, exc.details) from exc
            if quantum <= 0:
                raise ContractError("INVALID_QUANTUM", "normalization.quantum must be > 0")
            rounding_mode = n["rounding_mode"]
            if rounding_mode not in {"FLOOR", "CEILING", "TOWARD_ZERO", "AWAY_ZERO", "HALF_UP", "HALF_EVEN"}:
                raise ContractError("INVALID_ROUNDING_MODE", "unsupported normalization.rounding_mode")

    policy = data.get("uncertainty_policy", "FREEZE_ON_BOUNDARY_OVERLAP")
    if policy != "FREEZE_ON_BOUNDARY_OVERLAP":
        raise ContractError("UNSUPPORTED_UNCERTAINTY_POLICY", "only FREEZE_ON_BOUNDARY_OVERLAP is supported")

    return NormalizedContract(name, dimension, canonical_unit, lower, upper, quantum, rounding_mode)


def normalize_observation(raw: Any, contract: NormalizedContract, registry: UnitRegistry = BUILTIN_REGISTRY) -> NormalizedObservation:
    data = _mapping(raw, "observation", ObservationError)
    allowed = {"value", "unit", "uncertainty_abs"}
    unknown = _unknown_fields(data, allowed)
    if unknown:
        raise ObservationError("UNKNOWN_OBSERVATION_FIELD", "observation contains unsupported fields", {"fields": unknown})
    if "value" not in data or "unit" not in data:
        raise ObservationError("MISSING_OBSERVATION_FIELD", "observation requires value and unit")
    unit = data["unit"]
    if not isinstance(unit, str) or not unit:
        raise ObservationError("INVALID_UNIT", "observation.unit must be a non-empty string")
    try:
        registry.require_dimension(unit, contract.dimension)
        value = parse_rational(data["value"], field="observation.value")
        uncertainty_source = parse_rational(data.get("uncertainty_abs", "0"), field="observation.uncertainty_abs")
    except UnitError as exc:
        raise ObservationError(exc.code, exc.message, exc.details) from exc
    except NumericIntegrityError as exc:
        raise ObservationError(exc.code, exc.message, exc.details) from exc
    if uncertainty_source < 0:
        raise ObservationError("NEGATIVE_UNCERTAINTY", "observation.uncertainty_abs must be >= 0")

    canonical_value = registry.convert(value, unit, contract.canonical_unit)
    uncertainty = registry.convert_delta(uncertainty_source, unit, contract.canonical_unit)
    if uncertainty < 0:
        uncertainty = -uncertainty
    if contract.quantum is not None:
        assert contract.rounding_mode is not None
        canonical_value = quantize(canonical_value, contract.quantum, contract.rounding_mode)
    low = canonical_value - uncertainty
    high = canonical_value + uncertainty
    return NormalizedObservation(value, unit, canonical_value, uncertainty, low, high)


def _fully_inside(obs: NormalizedObservation, contract: NormalizedContract) -> bool:
    if contract.lower is not None:
        if obs.interval_low < contract.lower.value:
            return False
        if obs.interval_low == contract.lower.value and not contract.lower.inclusive:
            return False
    if contract.upper is not None:
        if obs.interval_high > contract.upper.value:
            return False
        if obs.interval_high == contract.upper.value and not contract.upper.inclusive:
            return False
    return True


def _fully_outside(obs: NormalizedObservation, contract: NormalizedContract) -> tuple[bool, str | None]:
    if contract.lower is not None:
        if obs.interval_high < contract.lower.value:
            return True, "BELOW_LOWER_BOUND"
        if obs.interval_high == contract.lower.value and not contract.lower.inclusive:
            return True, "BELOW_LOWER_BOUND"
    if contract.upper is not None:
        if obs.interval_low > contract.upper.value:
            return True, "ABOVE_UPPER_BOUND"
        if obs.interval_low == contract.upper.value and not contract.upper.inclusive:
            return True, "ABOVE_UPPER_BOUND"
    return False, None


def evaluate(contract_raw: Any, observation_raw: Any, registry: UnitRegistry = BUILTIN_REGISTRY) -> dict[str, Any]:
    input_record = {"contract": contract_raw, "observation": observation_raw}
    try:
        contract = normalize_contract(contract_raw, registry)
        observation = normalize_observation(observation_raw, contract, registry)
    except NumericIntegrityError as exc:
        result: dict[str, Any] = {
            "schema_version": "1",
            "verdict": "FREEZE",
            "reason_code": exc.code,
            "message": exc.message,
            "details": dict(exc.details or {}),
            "registry_digest": registry.digest,
            "input_digest": diagnostic_digest(input_record),
        }
        result["result_digest"] = digest({key: value for key, value in result.items() if key != "input_digest"})
        return result

    if _fully_inside(observation, contract):
        verdict = "ACCEPT"
        reason = "WITHIN_BOUNDS"
    else:
        outside, reason = _fully_outside(observation, contract)
        if outside:
            verdict = "REJECT"
            assert reason is not None
        else:
            verdict = "FREEZE"
            reason = "BOUNDARY_OVERLAP"

    contract_record = contract.record()
    observation_record = observation.record()
    result = {
        "schema_version": "1",
        "verdict": verdict,
        "reason_code": reason,
        "contract": contract_record,
        "contract_digest": digest(contract_record),
        "observation": observation_record,
        "registry_digest": registry.digest,
        "input_digest": diagnostic_digest(input_record),
    }
    result["result_digest"] = digest({key: value for key, value in result.items() if key != "input_digest"})
    return result
