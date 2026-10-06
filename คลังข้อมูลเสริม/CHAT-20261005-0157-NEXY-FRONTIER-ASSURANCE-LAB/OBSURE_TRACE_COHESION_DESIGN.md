# OBSURE Cross-Effect Trace Cohesion Design

Status: `AI_PROPOSED_EXPERIMENTAL_NOT_CANON`

## Purpose

Deepen the existing OBSURE runtime-witness assurance at a previously unverified
boundary: whether individually valid effect histories belong to one declared
multi-effect action and obey that action's causal dependencies.

This is not a sixth assurance concept. It is a standalone fail-closed extension
to the experimental OBSURE runtime adapter and is also wired into the existing
five-gate composed reference pipeline.

## Confirmed Gap

`ObsureRuntimeAssurance` validates event phases and correlation within each
effect. Before this extension, a valid `write` history under one trace/action and
a valid `notify` history under another trace/action could be spliced together
and receive `CERTIFIED`. It also had no cross-effect dependency contract, so a
child effect could begin before its declared parent completed.

Generic evidence-freshness, mutation-idempotency, and side-effect-ordering work
elsewhere in the supplemental repository does not bind OBSURE's concrete
runtime events, effect expectations, trace identity, action identity, and
compensation completion into one witness.

## Contract

`TraceCohesionContract` declares:

- one non-empty `trace_id` shared by every event;
- one non-empty `action_id` shared by every event;
- exact coverage of the assessed effect set; and
- an acyclic dependency graph whose values are finite tuples.

The dependency input must be a built-in dictionary. Construction validates it
and snapshots it behind an immutable mapping so post-construction caller
mutation cannot change the graph that was admitted.

`ObsureTraceCohesionAssurance.assess` first delegates every per-effect and event
invariant to `ObsureRuntimeAssurance`. Only a base `CERTIFIED` witness proceeds
to cross-effect checks. Each direct parent must complete before the child's
`INTENT`. Normal parent completion is its expected terminal phase. A parent
requiring compensation completes only at `COMPENSATION_RESULT`, not at its
preceding failure event.

## Evidence Binding

The result binds:

- the canonical trace contract as `contract_hash`;
- the complete canonical runtime event witness as `witness_hash`;
- the original OBSURE result, including its `result_hash`; and
- the complete cohesion decision as `result_hash`.

Order-insensitive inputs are normalized deterministically. Potentially
unbounded collections must be built-in lists or tuples with project-defined
members before sorting or delegation. Non-canonical witness values fail closed.

## Failure Semantics

- Invalid finite-input boundaries or contracts raise the mission's
  `FreezeError` before evaluation.
- A rejected base runtime witness returns `FREEZE / BASE_RUNTIME_INVALID` and
  preserves the complete base decision.
- Trace/action mismatch or dependency inversion returns
  `FREEZE / TRACE_COHESION_INVALID` with deterministic issues.
- The composed pipeline maps a base OBSURE rejection back to its original
  reason while retaining the new cohesion evidence envelope.

The adapter performs no effects, compensation, telemetry emission, identity
authentication, or clock synchronization.

## Verification Plan

- Positive: dependent effects certify; independent effects may interleave.
- Negative: spliced action IDs, dependency inversion, cycles, unknown parents,
  duplicate parents, incomplete coverage, and compensated-parent early start.
- Adversarial: duplicate global sequence, foreign elements, generators,
  post-construction graph mutation, shuffled input order, and identity changes.
- Integration: preserve both base and cohesion hashes; require cohesion in the
  five-gate composed pipeline.
- Regression: compile every mission Python file and execute the full mission
  test suite from the committed bytes.

## Authority and Limitations

This is a standalone reference artifact inside the supplemental mission root.
It does not establish NEXY.AI adoption, compatibility, runtime integration,
deployment, production readiness, or canonical status. Trace/action identifiers
and sequence numbers are caller-supplied assertions; this experiment checks
cohesion, not their external authenticity. Claims are limited to the exact
committed bytes and fresh verification recorded in the evidence artifact.
