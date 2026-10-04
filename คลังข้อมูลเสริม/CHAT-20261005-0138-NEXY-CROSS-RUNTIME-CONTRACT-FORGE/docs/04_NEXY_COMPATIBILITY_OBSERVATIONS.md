# NEXY.AI Compatibility Observations

## Evidence boundary

These are **read-only repository observations**, not new NEXY requirements. Target observed:

- repository: `goif74945-crypto/NEXY.AI-`
- branch context: `NEXY.ai`
- immutable observed commit: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`

No mutation to that repository was performed by this work.

## SOURCE FACT 1: TypeScript contract layer exists

At the observed commit, `packages/contracts/state.ts` defines the product-facing states:

`INIT, READY, RUNNING, VERIFYING, CONSENSUS, STABLE, FREEZE, STOP`.

`packages/contracts/envelope.ts` consumes the corresponding state/status schemas in the system envelope.

## SOURCE FACT 2: Product VNext state matrix exists in TypeScript

`packages/core/vnext-state-matrix.ts` defines:

- the same 8 VNext product states;
- lifecycle events;
- event ownership;
- transition table;
- transition guards;
- a VNext error taxonomy;
- freeze-recovery catalog and validation.

## SOURCE FACT 3: Rust explicitly calls itself a mirror

`core-kernel/src/kernel/vnext_matrix.rs` states that it is the Rust mirror of `packages/core/vnext-state-matrix.ts` and that the two must agree on transitions, ownership, error codes, freeze recovery, and release contract behavior.

That statement is the direct reason a cross-runtime drift detector/compiler is potentially valuable.

## SOURCE FACT 4: Hardware FSM is a separate domain

`core-kernel/src/kernel/fsm_state.rs` defines a separate 5-state hardware/safety FSM:

`Normal, Caution, Uncertain, Critical, Failsafe`.

The forge example deliberately does **not** flatten this hardware FSM into the 8-state product lifecycle. Different state domains remain distinct.

## SOURCE FACT 5: Incident playbook composes domains

`core-kernel/src/kernel/incident_playbook.rs` explicitly composes `FailureMode/SystemState` from the hardware FSM with `VNextState/VNextErrorCode` from the product FSM rather than inventing a parallel taxonomy.

## OBSERVED compatibility fixture

`examples/vnext-product-state.contract.json` captures the observed product lifecycle states, events, actor ownership, transitions, and guard names from `packages/core/vnext-state-matrix.ts` at the immutable commit above.

It is labeled:

> Observed compatibility fixture only. It is not promoted to NEXY.AI authority and must be refreshed against the target commit before integration.

## UNKNOWN / NOT VERIFIED

- Whether the observed commit remains current when a future integration is attempted.
- Whether every runtime-specific behavior in the TypeScript and Rust mirrors is representable by this schema v1.
- Whether DOC-C would authorize generated source to replace either existing implementation.
- Whether the generated Rust source compiles under NEXY's exact Rust toolchain. `rustc` was unavailable in this sandbox.
- Whether adopting this forge would reduce total maintenance cost enough to justify the new compiler/IR surface.

None of these unknowns is silently converted to a FACT.
