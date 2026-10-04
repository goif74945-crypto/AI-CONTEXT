# 00 — Session / Execution Memory

**Work ID:** `CHAT-20261005-0143-NEXY-CONTEXT-FIDELITY-COMPILER`
**Started:** 2026-10-05 01:43 +07:00
**Status:** IN_PROGRESS
**Class:** AI-PROPOSED / AUXILIARY / NON-CANONICAL
**Repository:** goif74945-crypto/AI-CONTEXT
**Protected implementation repository:** any repository whose name contains `NEXY.AI` — READ/ANALYZE ONLY for this work; NO MUTATION.

## Objective
Design, implement, test, and evidence a standalone **NEXY Context Fidelity Compiler (NCFC)** prototype that can compact structured long-context inputs while proving that protected requirements, authority, conflicts, unknowns, evidence status, numeric constants, negation/exception semantics, and provenance are not silently lost.

## Why this is orthogonal
Nearby supplemental systems already cover decision replay, proof/evidence capsules, context delta analysis, knowledge decay, reuse, privacy/release boundaries, and retrieval. NCFC targets a different failure boundary: **loss introduced by summarization/compaction itself**.

## Authoritative basis inspected
- `AI-BOOTSTRAP.md`
- `AI-EXECUTION-KERNEL.md`
- `INDEX.md`
- `WORK-ROUTER.md`
- `rules/GLOBAL.md`
- `rules/MEMORY.md`
- `rules/SECURITY.md`
- `rules/VERIFICATION.md`
- `workflows/system-design.md`
- `workflows/implementation.md`
- `workflows/long-context-ingestion.md`
- `workflows/memory-update.md`
- `projects/NEXY.AI/overview.md`
- `projects/NEXY.AI/context/INDEX.md`
- `projects/NEXY.AI/context-router/INDEX.md`
- `projects/NEXY.AI/invariants/INDEX.md`
- `projects/NEXY.AI/deep/final-architecture-cross-system.md`
- `คลังข้อมูลเสริม/02_CONTEXT_ENGINE.md`
- `FAILURES/2026-09-25/NEXY-L1O-ROLE-OVERCOMPRESSION.json`

## Key source-backed design constraints
1. Context compression must not remove authority, exceptions, unresolved conflicts, or evidence status.
2. Context packs prioritize authority and must never trim S5 invariants or unresolved conflicts to save budget.
3. Material ambiguity must remain UNKNOWN/CONFLICT instead of being guessed away.
4. Advisory AI output cannot become canonical NEXY law.
5. Runtime/design/evidence truth domains must remain distinct.
6. Compression must be deterministic at the authoritative gate; model output can only be an upstream candidate.
7. If the budget cannot carry all protected content, the compiler must FREEZE rather than silently omit it.

## Planned deliverables
- README / problem statement / non-goals
- architecture + contracts + invariants + failure model
- requirement ledger + integration notes
- deterministic TypeScript reference implementation
- CLI
- JSON schemas / fixtures
- focused unit + negative-path + determinism tests
- benchmark / property-style adversarial tests
- evidence report with exact commands and hashes
- session memory / final state / future research backlog

## Current state
- Duplicate scan completed against 963 existing supplemental paths.
- Concept selected: **proof-carrying context compaction / fidelity certification**.
- No NEXY.AI implementation repository mutation performed.
- Implementation/tests not yet written at this checkpoint.

## Next action
Build standalone TypeScript implementation in an isolated local workspace, execute tests, repair failures, then atomically persist tested artifacts into this folder and re-read them from AI-CONTEXT.

## Stop conditions
- Any required action would mutate a repository whose name contains `NEXY.AI`.
- Material authority conflict invalidates the design.
- Runtime evidence cannot be obtained: final status must not claim PASS for unexecuted gates.
- A discovered existing supplemental project is semantically equivalent enough to make this duplicate work.
