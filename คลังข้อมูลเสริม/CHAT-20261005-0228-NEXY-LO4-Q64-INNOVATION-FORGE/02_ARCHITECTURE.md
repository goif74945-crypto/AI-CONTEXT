# Architecture

Classification: `AI_PROPOSED_LO4_ONLY / NON_CANONICAL`

## Structural model
```text
JSON request
  -> registry / concept identity
  -> strict input validation
  -> Q64.64 domain conversion
  -> concept-specific deterministic transform
  -> PASS | FREEZE | REJECT
  -> canonical recursive serialization
  -> SHA-256 result identity
```

## Numeric kernel
`src/q64.js` defines signed Q64.64 using a `BigInt` raw representation:
- 64 integer/sign-side bits and 64 fractional bits;
- scale = `2^64`;
- raw minimum = `-2^127`;
- raw maximum = `2^127 - 1`;
- decimal parsing is exact rational scaling followed by nearest-even rounding;
- multiply/divide use arbitrary-width BigInt intermediates, nearest-even rescaling, then signed-128 range checks.

This avoids binary-float authority in the domain path while preserving deterministic behavior on Node.js implementations with conforming BigInt semantics.

## Shared control components
- `validation.js`: structured fail-closed input contracts.
- `safe.js`: converts declared Q64/input failures into bounded FREEZE responses while not hiding unexpected programmer exceptions.
- `rank.js`: deterministic score ordering with stable ID tie-breaks.
- `result.js`: controlled PASS/FREEZE/REJECT envelopes.
- `canonical.js`: deterministic key ordering and SHA-256 identities.
- `registry.js`: exact concept catalog and dispatch.
- `cli.js`: file/stdin integration surface and policy exit codes.

## Authority architecture
The Forge is intentionally below authority. It can calculate, rank, quantify, or freeze a proposal, but it cannot:
- alter NEXY LAW;
- bypass JUDGE;
- authorize release/deployment;
- modify persistent project truth;
- override a safety stop;
- promote its own Lo4 proposal into Canon.

A future adapter must preserve this one-way boundary:
`verified NEXY inputs -> Lo4 evaluator -> advisory/proof artifact -> canonical NEXY authority decides`.

## Determinism contract
Determinism is scoped to same source, same normalized input, and same declared concept contract. There is no random sampling, wall-clock read, network lookup, hidden model call, unspecified object iteration dependency in serialized output, or environment-derived score.

## Failure semantics
Material invalidity becomes explicit FREEZE. Programmer defects are allowed to surface as hard execution failures so they cannot be laundered into plausible business output. This split is deliberate: user/data ambiguity is a domain state; a broken implementation is an engineering failure.
