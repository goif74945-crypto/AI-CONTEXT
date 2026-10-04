# Q64.64 Numeric Contract

## Representation
- format: signed Q64.64 fixed point;
- storage: one checked signed 128-bit raw integer;
- scale: `2^64`;
- raw range: `[-2^127, 2^127 - 1]`;
- numeric range: approximately `[-2^63, 2^63)` with 64 fractional bits.

## Construction
Supported constructors:
- exact integer;
- exact rational numerator/denominator;
- canonical decimal text parsed into an exact base-10 rational before one Q64.64 rounding step.

There is intentionally no binary-float constructor.

## Arithmetic
- addition/subtraction: checked raw integer arithmetic;
- multiplication: exact raw product then divide by `2^64` using round-to-nearest, ties-to-even;
- division: multiply numerator raw by `2^64`, divide by denominator raw using the same rounding rule;
- overflow: raises `Q64Overflow`;
- divide by zero: raises `Q64DivisionByZero`.

## Important consequence
Decimal values such as `0.1` are not exactly representable in base-2 fixed point. Therefore:

`parse("0.4")`

is not required to equal

`parse("0.1") * 3 + parse("0.1")`

at the raw-bit level. Tests compare the specified operation sequence, not an unrelated decimal reparse. Two test-oracle defects were found and corrected because of this exactness rule; engine behavior was not weakened.

## Serialization
Q64 values serialize canonically as:

```json
{"format":"Q64.64","raw":123}
```

Fingerprints are SHA-256 over canonical JSON with sorted mapping keys.

## Verification strategy
The final adversarial suite checks:
- signed boundary and overflow behavior;
- no float literals / `float()` calls in decision modules;
- random multiplication and division against independent Python `Fraction` + half-even integer rounding;
- add/subtract round trips;
- deterministic fingerprints under reordered inputs where order should be irrelevant.
