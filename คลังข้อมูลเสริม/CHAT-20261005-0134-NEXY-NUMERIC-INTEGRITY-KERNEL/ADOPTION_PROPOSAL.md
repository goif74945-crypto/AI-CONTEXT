# AI-Proposed Future Adoption Path

**This document is a proposal, not a NEXY requirement.**

## Candidate use cases

1. Pre-verification normalization for thresholds expressed in heterogeneous units.
2. Safety/release gates where uncertainty must not be silently collapsed into a point estimate.
3. Test oracle support for inclusive/exclusive numeric boundaries.
4. Deterministic canonicalization of numeric evidence emitted by tools/providers.
5. Regression detection when unit registries or rounding policies change.

## Proposed integration boundary

Future NEXY code could call an adapter with explicit `contract` and `observation` objects and consume only `ACCEPT`, `REJECT`, or `FREEZE` plus reason/digests. The kernel should not own user policy, model routing, or release authority.

## Adoption gates

Before integration, require:

- mapping from actual NEXY numeric decision surfaces to explicit contracts;
- authority review of allowed units/dimensions;
- property-based/exhaustive tests over each adopted dimension;
- independent cross-check against a second exact arithmetic implementation for high-impact conversions;
- performance characterization under expected workloads;
- integration tests proving FREEZE propagation rather than fallback;
- compatibility/version migration plan for registry changes;
- security review for any future external-rate adapter.

## Explicitly deferred

Currency, timezone-dependent quantities, locale-inferred number formats, physical sensor calibration, statistical confidence intervals, significant-figure semantics, and irrational/transcendental unit conversions are not silently added. Each requires a separate authority/data model.
