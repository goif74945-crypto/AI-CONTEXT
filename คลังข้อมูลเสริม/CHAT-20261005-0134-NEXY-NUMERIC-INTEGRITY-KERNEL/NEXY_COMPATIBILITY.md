# NEXY Compatibility Analysis

**Status:** SOURCE-GROUNDED COMPATIBILITY DESIGN + AI_PROPOSED ADOPTION PATH

## Source facts observed in AI-CONTEXT

Current DOC-C/vNEXT context defines numeric configuration values including:

- `confidence_min = 0.85`;
- `deterministic_match_min = 0.90`;
- finite pipeline stage timeouts and a 120-second pipeline cap;
- OTAC/session/cooldown/lock limits;
- queue TTL and concurrency limits;
- coverage targets.

The broader constitutional deterministic-lock context separately states a stricter numeric law for canonical Core execution:

- floating point forbidden in Core;
- fixed-point/integer math only;
- signed 128-bit canonical arithmetic in that locked source branch;
- overflow causes immediate FREEZE.

That constitutional context is broader than the narrower current DOC-C/vNEXT build scope and must not be silently promoted into current build law where authority differs.

## Compatibility decision

NNIK's exact-rational arithmetic is suitable as an **external/boundary verification representation**, not as a direct replacement for the constitutional Core's signed-128 fixed/integer representation.

### Mode A — boundary verifier

Use exact rational arithmetic to parse explicit decimal text, normalize units, prove threshold relations, and detect uncertainty overlap. The output remains an advisory/verifier result until an authorized NEXY integration consumes it.

### Mode B — signed-128 projection gate

Before a numeric value enters a Core path governed by the signed-128 fixed-point law, choose an explicit fixed-point quantum and require:

1. value / quantum is exactly an integer;
2. integer is within `[-2^127, 2^127-1]`;
3. reconstruction equals the original rational exactly.

If any condition fails, FREEZE. No rounding is permitted by this projection gate.

The reference implementation provides `nnik.fixed128.project_exact` and CLI command `project-fixed128` for this proof.

## Source-derived demonstration

DOC-C's `0.85` and `0.90` thresholds are exactly representable at quantum `0.01`:

- `0.85 -> integer 85 -> exact 17/20`;
- `0.90 -> integer 90 -> exact 9/10`.

This demonstrates representability only. It does not prove a NEXY implementation currently uses NNIK or any specific fixed-point quantum.

## Required future integration evidence

Actual integration would require at least:

- explicit ownership of numeric normalization boundary;
- approved unit and quantum contracts;
- tests against current NEXY implementation language/runtime;
- release-law integration tests proving FREEZE propagation;
- overflow/nonrepresentability abuse tests;
- versioned registry and config identity in evidence/audit records.
