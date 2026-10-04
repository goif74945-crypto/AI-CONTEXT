# NEXY Numeric Integrity Kernel (NNIK)

**Status:** AI_PROPOSED / SUPPLEMENTAL / NOT_CURRENT_NEXY_REQUIREMENT

NNIK is a standalone Python 3.11+ reference implementation for deterministic numeric contract evaluation. It exists to make unit, threshold, rounding, and uncertainty semantics explicit before a numeric result is allowed to influence a higher-level decision.

It does **not** modify or integrate with any NEXY.AI repository. Adoption would require a separate authority decision, interface mapping, and integration verification.

## Why this exists

Numeric failures are often silent: binary floating-point representation, wrong units, hidden rounding, affine conversions such as Fahrenheit/Celsius, and uncertain measurements near a threshold can all turn a seemingly simple comparison into an incorrect decision.

NNIK uses exact rational arithmetic for authoritative computation and a closed unit registry. It emits exactly one domain verdict:

- `ACCEPT`: the full uncertainty interval satisfies the contract.
- `REJECT`: the full uncertainty interval is outside the accepted set.
- `FREEZE`: the input/contract is invalid, the unit semantics are unknown/incompatible, or uncertainty overlaps a decision boundary.

## Properties

- exact finite decimal and rational parsing;
- Python `float` rejected by the library API;
- exact rational unit conversion, including affine temperature units;
- exact uncertainty-delta conversion without affine offsets;
- explicit inclusive/exclusive lower and upper bounds;
- optional exact quantization with six deterministic rounding modes;
- deterministic canonical JSON and SHA-256 identities;
- exact signed-128 fixed-point projection proof for NEXY-compatible boundary adaptation;
- no network, model calls, random sampling, `eval`, or external packages;
- CLI input capped at 1 MiB before JSON parsing; numeric magnitude/text safety limits bound exact-arithmetic cost;
- time-dependent currency conversion intentionally excluded.

## Run

```bash
python validate.py
python -m nnik.cli evaluate fixtures/length_accept.json
python -m nnik.cli registry
python -m nnik.cli project-fixed128 --value 0.85 --quantum 0.01
```

A domain-level `FREEZE` is a successful CLI evaluation and returns process exit code 0. File/JSON/usage failures return exit code 2.

## Evidence boundary

Passing local tests proves only the authored standalone reference implementation at the tested artifact revision. It does not prove NEXY.AI integration, runtime behavior, deployment readiness, or product acceptance.
