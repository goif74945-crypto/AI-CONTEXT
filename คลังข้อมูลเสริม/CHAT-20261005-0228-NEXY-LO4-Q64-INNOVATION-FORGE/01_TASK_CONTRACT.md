# Task Contract

Classification: `AI_PROPOSED_LO4_ONLY / EXECUTION_CONTRACT`

## Objective
Design, implement, execute, test, audit, and persist twenty novel Lo4 quantitative control concepts that can be evaluated for future NEXY.AI use, all sharing a strict Q64.64 numeric substrate.

## Required output
- one standalone project under AI-CONTEXT `คลังข้อมูลเสริม`;
- twenty actual executable concepts, not twenty prose-only ideas;
- shared Q64.64 library and canonical result envelope;
- tests, negative paths, replay/determinism checks, independent numeric oracle, benchmark workload, CLI fixture;
- design, integration boundary, threat/failure model, novelty/collision audit, evidence ledger, final audit;
- durable temporary execution memory.

## Inputs / authority
1. Explicit current user directive.
2. `AI-EXECUTION-KERNEL.md`.
3. `rules/GLOBAL.md`, `rules/SECURITY.md`, `rules/VERIFICATION.md`.
4. NEXY project context in `projects/NEXY.AI/` as alignment evidence only.
5. Current AI-CONTEXT repository state and executable evidence.
6. This AI-authored design.

## Authorized scope
Only new files below:
`คลังข้อมูลเสริม/CHAT-20261005-0228-NEXY-LO4-Q64-INNOVATION-FORGE/`

## Protected / out of scope
- any mutation to any repository whose name contains `NEXY.AI`;
- editing, deleting, renaming, consolidating, or rewriting sibling supplemental projects;
- changing NEXY Canon, DOC-B, DOC-C, release state, deployment, settings, branch, issue, PR, workflow, or source code;
- claiming this project is already integrated, deployed, promoted, or authoritative;
- secrets, credentials, hidden network dependencies, runtime model calls, or destructive Git history operations.

## Immutable requirements
1. Exactly twenty executable Lo4 concepts in v1.
2. Every concept explicitly marked `AI_PROPOSED_LO4_ONLY`.
3. All authoritative domain numeric input is parsed to Q64.64 from decimal string / integer semantics, never JS binary floating-point.
4. Raw Q64.64 values are constrained to signed 128-bit range.
5. Multiplication/division and decimal parsing use round-to-nearest-even.
6. Arithmetic overflow, divide-by-zero, invalid input, unknown dependencies, cycles, or missing critical evidence fail closed.
7. No concept module may use `Math.*`, `parseFloat`, `parseInt`, `Number(...)`, `eval`, dynamic `Function`, `fetch`, or HTTP(S) paths.
8. No concept has promotion/release/deploy authority.
9. Deterministic ordering and canonical JSON are required for replay identity.
10. Same source + same normalized input must not depend on wall clock, random state, network, environment/provider state, or mutable global decision state.

## Acceptance criteria
- E0: all intended artifacts persist and can be re-read.
- E1: JS syntax, static policy scan, and exact numeric cross-oracle pass.
- E2: complete unit/adversarial/property suite passes.
- E3-local: CLI and multi-concept integration chain execute; replay and workload harnesses complete.
- final committed/source hashes match the locally tested bytes.
- no protected repository mutation is performed.

## Stop conditions
Stop/freeze if persistence requires touching protected repositories, a material authority conflict appears, source read-back differs from tested bytes, verification fails after repair, or a critical concept duplicates an existing sibling responsibility rather than adding a distinct mechanism.
