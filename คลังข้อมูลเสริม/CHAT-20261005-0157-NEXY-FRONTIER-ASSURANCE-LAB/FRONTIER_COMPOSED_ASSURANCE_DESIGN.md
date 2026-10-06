# Frontier Composed Assurance Design

Status: `AI_PROPOSED_EXPERIMENTAL_NOT_CANON`

## Purpose

Close a composition bypass inside the existing five-concept lab. The original
`FrontierAssurancePipeline` invokes the first-generation engines, while the five
later continuation slices expose stricter adapters. A caller can therefore use
the nominal integrated pipeline and bypass the verified input, campaign,
path-integrity, and runtime-witness checks.

This slice adds no sixth assurance concept. It is a fail-closed composition
adapter over the existing hardened MUSCLE, PAREX, GHOSTEDGE, RECERT, and OBSURE
interfaces.

## Confirmed Gap

The original pipeline returns `READY` for a `NEQ("saef")` constraint even though
`"saef"` is outside the `mode` domain. The MUSCLE input-assurance adapter rejects
that same request. The original pipeline also has no inputs for the controlled
GHOSTEDGE campaign, pointer-safe RECERT policy, or OBSURE runtime witness.

## Contract

`ComposedFrontierAssurancePipeline.assess` executes the gates in this fixed order:

1. MUSCLE input and search-budget assurance;
2. PAREX metric-integrity admission;
3. GHOSTEDGE controlled campaign assurance;
4. RECERT original plus pointer-safe certification;
5. OBSURE specification plus runtime-witness certification.

The result is `READY` only when every gate reaches its admitted success state.
The first non-success or rejected input returns `FREEZE`, records exactly the
attempted gates, and does not claim unexecuted gates. Every result receives a
canonical `result_hash` over the complete returned record.

## Input Boundary

Potentially unbounded candidate/event collections must be built-in `list` or
`tuple` values and every member must have the expected adapter type. This check
occurs before adapter materialization or sorting. It prevents infinite generators
and converts foreign elements into structured `FREEZE` results. MUSCLE retains
its own stricter finite-collection admission.

Only project-defined `FreezeError` validation failures are converted into
structured input rejections. Unexpected programming defects are not mislabeled
as user-input failures.

## Failure Semantics

- MUSCLE: unknown/malformed input, budget overflow, or `UNSAT` freezes.
- PAREX: malformed/unbound metrics or an empty eligible frontier freezes.
- GHOSTEDGE: insufficient/invalid campaign, uncontrolled signal, or controlled
  undeclared dependency candidate freezes.
- RECERT: either certifier failing or the certifiers disagreeing freezes.
- OBSURE: insufficient telemetry specification, malformed runtime input, or an
  invalid runtime witness freezes.

The adapter performs no external action, state repair, telemetry emission,
dependency declaration, plan selection, or recovery.

## Verification Plan

- Positive: all five hardened gates pass and preserve their evidence bindings.
- Negative: independently stop at each gate.
- Adversarial: reproduce the original-pipeline vocabulary bypass; exercise NaN,
  empty campaign, dotted-path aliasing, foreign members, and generator inputs.
- Determinism: shuffle all order-insensitive collections across 50 seeded runs.
- Integration: prove short-circuit accounting and structured adapter rejection.
- Regression: execute the complete mission test suite after the focused suite.

## Authority and Limitations

This is a standalone reference artifact inside the supplemental mission root.
It does not establish NEXY.AI adoption, compatibility, runtime integration,
deployment, production readiness, or canonical status. Its executed evidence is
limited to the local Python reference implementation and committed tested bytes.
