# Q64.64 Contract

Classification: `AI_PROPOSED_LO4_ONLY / NUMERIC_REFERENCE_CONTRACT`

## Representation
A value `x` is encoded as an integer raw value `r` with:
`x = r / 2^64`.

The implementation constrains `r` to the signed 128-bit interval:
`[-2^127, 2^127 - 1]`.

## Authoritative inputs
Accepted domain forms:
- decimal strings such as `"0.75"`, `"-12.125"`;
- integer `BigInt` values for exact integers;
- already-validated Q64 objects.

Ordinary JavaScript `Number` values are not accepted by `Q64.parse` as authoritative domain numbers.

## Rounding
Decimal parsing, multiplication, and division use round-to-nearest, ties-to-even. The algorithm compares twice the remainder against the denominator and resolves exact halves by the parity of the quotient.

## Overflow
Every value entering the stored Q64 domain is range checked. Arbitrary-width `BigInt` intermediates may temporarily exceed 128 bits during exact multiplication/division, but the rescaled result must fit the signed Q64.64 raw interval or the operation fails.

## Serialization
A Q64 value serializes with both:
- exact raw integer string;
- deterministic decimal rendering to 18 fractional places for human inspection.

The raw integer is the exact machine identity. The decimal field is a deterministic rendering, not a replacement for raw identity.

## Independent oracle
`scripts/q64-oracle.py` uses Python `fractions.Fraction` and `decimal.Decimal` as an independently implemented oracle for selected vectors. It compares expected raw Q64 results against the Node implementation. Current evidence: 16/16 vectors PASS.

## Deliberate exclusions
This core does not claim:
- arbitrary precision beyond Q64.64 output range;
- transcendental functions;
- physical unit conversion;
- probability calibration validity merely because a number is within [0,1];
- statistical meaning without a separate model contract.

Those concerns require explicit higher-level authority and validation.
