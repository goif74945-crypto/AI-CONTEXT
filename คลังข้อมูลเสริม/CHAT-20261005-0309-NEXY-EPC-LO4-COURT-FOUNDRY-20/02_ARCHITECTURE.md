# Architecture — EPC CourtScript-Q64

## Pipeline
```text
CourtScript source
  -> 01 bounded lexer
  -> 02 parser
  -> 03 canonical AST seal
  -> 04 Q64 literal compiler
  -> 05 metric registry
  -> 06 static type checker
  -> 07 authority/effect checker
  -> 08 exact-revision pin contract
  -> 09 tri-state truth semantics
  -> 10 WIP/CUT guard compiler
  -> 11 proof-obligation compiler
  -> 12 hard-requirement compiler
  -> 13 weighted Q64 score compiler
  -> 14 review-only recommendation compiler
  -> 15 canonical bytecode seal
  -> 16 bounded pure VM
  -> 17 trace digest
  -> 18 revision compatibility / loosening analysis
  -> 19 conformance corpus runner
  -> 20 admission compiler
```

## Trust model
CourtScript source is untrusted proposal data. The compiler grants no side effects. The language has no filesystem, network, process, environment, clock, randomness, dynamic loading, eval, FFI, async I/O, persistence, or authority mutation primitive.

## Numeric model
`Q64` stores signed Q64.64 raw values in the signed 128-bit interval `[-2^127, 2^127-1]`. Decimal policy literals are parsed from strings directly to bigint quantized fixed point. Arithmetic performs explicit overflow checks; division by zero fails explicitly.

## Decision model
A policy may declare exact revision pins, proof obligations, guards, hard Q64 constraints, one weighted advisory score, and one review recommendation target.

The VM produces only `REVIEW_ELIGIBLE` + `KEEP_REVIEW`/`CUT_REVIEW`, or `DEFER`. It cannot produce Canon acceptance, runtime transition, deployment, physical deletion, or vote-right consumption.

## Unknown semantics
Any metric may be `UNKNOWN`. A hard requirement over UNKNOWN yields UNKNOWN and forces DEFER. A score containing UNKNOWN is not computed from the remaining values because that would silently reweight the policy.

## CUT law
A `CUT_REVIEW` policy is rejected at compile time unless it declares `GUARD WIP_IMMUNITY` and `PROOF CUT_SUBSTANTIVE_BASIS`. At runtime, a WIP-only or UNKNOWN-only basis fails the guard even if numeric scores are favorable.

## Compatibility law
Policy revision comparison labels requirement changes as TIGHTENED, LOOSENED, ADDED, REMOVED, or TARGET_CHANGED. This exposes security/Canon-impacting loosening as explicit review evidence.

## NX relationship
NEXY's existing NX v0.1 is a broader deterministic language prototype. CourtScript is therefore a **non-canonical EPC policy profile/reference compiler**, not a competing NEXY language. Future integration should use a reviewed adapter or transpilation contract and preserve NX authority constraints.
