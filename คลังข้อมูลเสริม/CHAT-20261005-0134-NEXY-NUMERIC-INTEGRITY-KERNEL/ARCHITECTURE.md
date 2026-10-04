# NNIK Architecture

**Classification:** AI_PROPOSED / NOT_CURRENT_NEXY_REQUIREMENT

## Objective

Provide an inspectable deterministic primitive for numeric decisions whose correctness depends on units, exact comparison semantics, rounding policy, or uncertainty.

## Non-goals

NNIK is not a symbolic algebra system, statistics package, currency exchange service, physical calibration authority, or replacement for domain-specific safety validation. It does not infer units, aliases, tolerances, or acceptable risk.

## Pipeline

`RAW CONTRACT + RAW OBSERVATION -> STRICT PARSE -> DIMENSION CHECK -> EXACT UNIT CONVERSION -> OPTIONAL QUANTIZATION -> UNCERTAINTY INTERVAL -> BOUND CLASSIFICATION -> CANONICAL VERDICT + DIGEST`

## Modules

- `rational.py`: finite exact numeric parser and deterministic quantization.
- `units.py`: closed unit registry and exact affine conversions.
- `evaluator.py`: contract validation, observation normalization, interval classification, structured freeze semantics.
- `canonical.py`: deterministic JSON normalization and SHA-256 identities.
- `fixed128.py`: exact projection into signed-128 fixed-point integer representation.
- `cli.py`: file boundary and process behavior.

## Authority model

The contract is the authority for dimension, canonical unit, accepted bounds, and rounding. The unit registry is the authority for conversion semantics. The observation supplies a value, source unit, and optional absolute uncertainty. NNIK never guesses missing semantics.

## State/verdict model

`ACCEPT` means the complete uncertainty interval is a subset of the accepted numeric set.

`REJECT` means the complete uncertainty interval is disjoint from the accepted numeric set on one side.

`FREEZE` means a legal deterministic accept/reject conclusion cannot be made under the supplied contract, including malformed/unsupported semantics or an interval that crosses a boundary.

## Exact arithmetic law

Finite decimal text is converted to an exact rational number. Unit scale and offsets are exact rationals. Threshold comparisons are exact. Display formatting is not used as evidence for numeric equality.

## Unit model

Each unit has:

`base_value = input_value * scale_to_base + offset_to_base`

and conversion to a target unit is:

`target = (base_value - target_offset) / target_scale`

Absolute uncertainty is a delta and therefore uses scale only, never affine offsets.

## Failure semantics

Unknown units, dimension mismatch, non-finite/invalid values, Python float inputs, unsupported contract fields, invalid bound order, empty acceptance sets, unsupported rounding modes, and unsupported uncertainty policies produce deterministic `FREEZE` results rather than fallback behavior.

## Security/trust boundaries

The implementation has no dynamic code execution, plugin loading, network access, shell execution, or arbitrary unit aliases. Inputs are treated as data. Unit symbols are exact and case-sensitive.

## Evolution law

Registry or schema changes require versioning and new evidence. Reusing a prior `registry_digest` after unit definitions change is forbidden. External-rate dimensions such as currency must use a separately versioned, time/provenance-bearing adapter if ever proposed.
