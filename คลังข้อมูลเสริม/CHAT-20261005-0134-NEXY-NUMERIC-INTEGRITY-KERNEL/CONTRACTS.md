# NNIK Data Contracts

**Status:** AI_PROPOSED

## Contract v1

Required semantic fields:

- `schema_version`: exactly `"1"`.
- `name`: non-empty trace label.
- `dimension`: explicit dimension name.
- `canonical_unit`: exact registered unit symbol for the dimension.
- `lower`: null or `{value, inclusive}`.
- `upper`: null or `{value, inclusive}`.
- `normalization`: exactly `{quantum, rounding_mode}`; both null or both supplied.
- `uncertainty_policy`: only `FREEZE_ON_BOUNDARY_OVERLAP`.

At least one numeric bound is required. Equal bounds are legal only when both are inclusive.

## Observation v1

- `value`: exact numeric input.
- `unit`: exact registered symbol.
- `uncertainty_abs`: optional exact non-negative absolute uncertainty in the same source unit, default `0`.

## Exact numeric inputs

Accepted by the library:

- integers;
- finite `Decimal`;
- `Fraction`;
- exact numeric strings such as `"1.25"`, `"1e-3"`, `"5/9"`.

Python binary `float` is forbidden by the library API. The CLI asks the JSON decoder to return number tokens as strings, preserving the source decimal text before exact parsing and safety-limit checks.

## Quantization

If a contract supplies `normalization.quantum`, the canonical center value is quantized before the uncertainty interval is built. Uncertainty is not quantized. Supported modes:

`FLOOR`, `CEILING`, `TOWARD_ZERO`, `AWAY_ZERO`, `HALF_UP`, `HALF_EVEN`.

This policy is explicit because silent rounding is forbidden.

## Canonical output

Authoritative numeric values are serialized as reduced integer or rational text, for example `"3/2"`. Canonical JSON uses sorted keys and compact separators. Every result contains stable digests for input, normalized contract when available, unit registry, and complete result.

## Digests

`input_digest` is a forensic fingerprint of the raw supplied structure, including tagged invalid binary floats. `result_digest` intentionally excludes that raw fingerprint and hashes normalized decision semantics, so numerically equivalent exact representations can share a result identity while retaining distinct raw-input provenance.
