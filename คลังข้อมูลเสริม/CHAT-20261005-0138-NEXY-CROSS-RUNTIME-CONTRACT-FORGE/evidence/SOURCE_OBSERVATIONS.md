# Source Observations

## AI-CONTEXT authority inspected

Repository: `goif74945-crypto/AI-CONTEXT`, branch `main`.

Read during this task:

- `AI-BOOTSTRAP.md`
- `AI-EXECUTION-KERNEL.md`
- `INDEX.md`
- `WORK-ROUTER.md`
- `rules/GLOBAL.md`
- `rules/SECURITY.md`
- `rules/VERIFICATION.md`
- `projects/NEXY.AI/overview.md`
- `projects/NEXY.AI/deep/INDEX.md`
- `projects/NEXY.AI/source-normalization/CURRENT-SYSTEM-FEATURE-BUILD-MATRIX.md`
- `workflows/system-design.md`
- `workflows/implementation.md`
- `workflows/verification.md`
- `คลังข้อมูลเสริม/00_INDEX.md`

Relevant rule facts applied:

- no silent guessing;
- current state before mutation;
- evidence before status;
- design/implementation/runtime/deployment are distinct truth classes;
- read permission is not write authority;
- protected repositories may not be mutated merely because they are readable;
- the 215-entry NEXY registry is deprecated/unreliable for current counts;
- current normalized source matrix records 837 normalized requirement rows and explicit authority/scope classes.

## NEXY.AI read-only source inspected

Repository: `goif74945-crypto/NEXY.AI-`  
Exact immutable commit: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`

Read/searched material included:

- `package.json`
- `tsconfig.json`
- `vitest.config.ts`
- `packages/contracts/state.ts`
- `packages/contracts/errors.ts`
- `packages/contracts/envelope.ts`
- `packages/core/vnext-state-matrix.ts`
- `core-kernel/src/kernel/fsm_state.rs`
- `core-kernel/src/kernel/vnext_matrix.rs`
- `core-kernel/src/kernel/incident_playbook.rs`
- repository searches for Zod, serde, SystemState, contract, JSON schema terminology.

## Key observed facts

1. TypeScript uses strict settings and Zod contracts in multiple `packages/contracts/*` modules.
2. The product VNext lifecycle has 8 states in the observed TypeScript source.
3. Rust `vnext_matrix.rs` explicitly labels itself a mirror of the TypeScript VNext matrix.
4. Rust also has a separate 5-state hardware/safety FSM that must not be conflated with the product lifecycle.
5. The incident playbook composes the two domains.
6. The observed source contains hand-maintained parallel representations, which creates a plausible drift risk. The claim that drift **will** occur is not made.

## Mutation statement

No write-capable GitHub action was invoked against `goif74945-crypto/NEXY.AI-` during this work.
