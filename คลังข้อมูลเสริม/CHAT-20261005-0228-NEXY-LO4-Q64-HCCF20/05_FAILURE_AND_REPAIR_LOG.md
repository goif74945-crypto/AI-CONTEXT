# Failure and Repair Log

## F-001 — Decimal weight normalization lost one raw ULP
Initial test `test_14_drm` failed: expected raw ONE `18446744073709551616`, observed `18446744073709551615`.

Root cause: decimal strings such as 0.45, 0.35 and 0.20 are not all exactly representable in binary Q64.64. Constructing and multiplying each independently truncates each term before addition.

Repair: composite score formulas now use integer weights in `_weighted_mean`, such as `45:35:20`; Q64 division occurs once after the weighted numerator and exact integer-weight denominator are formed.

Verification: full unit suite and property sweep rerun after repair. Prior pre-repair result is not reused as PASS evidence.
