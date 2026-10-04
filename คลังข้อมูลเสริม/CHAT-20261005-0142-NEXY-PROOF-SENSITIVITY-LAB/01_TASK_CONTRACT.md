# Task Contract — NEXY Proof Sensitivity Lab

## Objective
Create a self-contained, testable reference tool in AI-CONTEXT that detects proof-suite blind spots by applying **explicitly declared semantic mutants** to a baseline contract and checking whether **explicitly declared proofs** reject those mutants.

## Required output
A new mission folder containing:
1. durable execution memory;
2. concept/specification clearly labeled AI proposal;
3. architecture and interfaces;
4. requirement ledger;
5. threat/failure model;
6. Python 3.11+ standard-library implementation;
7. CLI;
8. example contract;
9. tests;
10. executed test evidence;
11. repository read-back evidence;
12. final execution record/completion certificate.

## Target
- Repository: `goif74945-crypto/AI-CONTEXT`
- Branch: `main`
- Write root: `คลังข้อมูลเสริม/CHAT-20261005-0142-NEXY-PROOF-SENSITIVITY-LAB/`

## Authorized scope
Only new files under the target write root.

## Protected scope
- Every repository whose name contains `NEXY.AI`.
- Every path outside the target write root.
- Existing supplemental projects and shared indexes.
- Production systems, deployments, secrets, credentials.

## Authoritative sources
- Current user directive.
- `INDEX.md`
- `AI-BOOTSTRAP.md`
- `AI-EXECUTION-KERNEL.md`
- `WORK-ROUTER.md`
- `rules/GLOBAL.md`
- `rules/SECURITY.md`
- `rules/VERIFICATION.md`
- `projects/NEXY.AI/overview.md`
- `projects/NEXY.AI/source-normalization/CURRENT-SYSTEM-FEATURE-BUILD-MATRIX.md`
- `workflows/system-design.md`
- `workflows/implementation.md`
- `workflows/verification.md`

## Immutable requirements
- No guessing of material missing semantics.
- No shell/network/model execution from input specifications.
- Deterministic core behavior.
- Explicit distinction between proposal, code presence, executed proof, and NEXY integration status.
- Fail closed when baseline proofs do not pass.
- Fail closed on malformed/invalid mutation definitions.
- Preserve JSON value types exactly.
- Support deterministic JSON Pointer path resolution including RFC-6901 escape semantics for `~0` and `~1`.
- Mutation result identity must be content-derived.
- No random UUIDs/timestamps in canonical core output.
- Duplicate proof or mutant IDs are invalid.
- Equivalent mutants must not inflate sensitivity score.
- Surviving mutants must be reported with the proofs that still passed, never hidden.
- Score denominator and exclusions must be explicit.

## Initial functional contract
### Proof operators
At minimum:
- `exists`
- `equals`
- `not_equals`
- `contains`
- `not_contains`
- `min`
- `max`
- `type`
- `evidence_class_at_least`

### Mutation operators
At minimum:
- `set`
- `delete`
- `add_item`
- `remove_item`
- `numeric_delta`

### Mutant states
- `KILLED`
- `SURVIVED`
- `EQUIVALENT`
- `INVALID_MUTANT`

### Analysis states
- `PASS` — baseline valid and every declared eligible mutant is killed.
- `FAIL` — baseline valid and at least one declared eligible mutant survives.
- `FREEZE` — baseline invalid, malformed corpus, or another fail-closed precondition failure.

## Acceptance criteria
AC01 — baseline proofs are executed before mutation scoring.
AC02 — a failing baseline proof returns analysis `FREEZE`.
AC03 — a protected-value `set` mutant is killed when an equality proof guards it.
AC04 — an uncovered non-equivalent mutant survives and produces a proof-gap record.
AC05 — equivalent mutant is classified `EQUIVALENT` and excluded from score denominator.
AC06 — invalid mutation path/operator is `INVALID_MUTANT` and overall analysis `FREEZE`.
AC07 — numeric boundary proofs kill violating `numeric_delta` mutants.
AC08 — collection proofs detect `add_item`/`remove_item` regressions when declared.
AC09 — E0..E7 evidence-class ordering is enforced without inventing unknown classes.
AC10 — JSON Pointer escaped tokens resolve correctly.
AC11 — duplicate IDs are rejected.
AC12 — normalized result is byte-stable across repeated runs.
AC13 — proof/mutant input ordering does not change canonical result semantics.
AC14 — CLI reads a spec and emits deterministic JSON.
AC15 — no production code is accepted without prior failing tests for new behavior.
AC16 — full local test suite passes after implementation.
AC17 — exact authored repository files are read back after write.
AC18 — protected scope remains unchanged by this mission.

## Required evidence
- E0: repository file presence/read-back.
- E1: Python bytecode/static import/compile validation.
- E2: executed unit tests.
- E3: executed CLI integration test.
- Diff/scope verification: GitHub target-folder and commit/read-back inspection.

## Stop/freeze conditions
- Target repository identity differs from `goif74945-crypto/AI-CONTEXT`.
- Any requested next step requires writing to a repository whose name contains `NEXY.AI`.
- A material requirement conflict cannot be resolved by authority.
- Exact tested content cannot be matched to persisted content.
- Required test/runtime evidence is unavailable.
- A repair would require editing outside the mission folder.

## Explicit non-goals
- No automatic mutation generation from vague prose.
- No claim of universal test adequacy.
- No source-code mutation engine in v1.
- No arbitrary subprocess runner in v1.
- No NEXY production integration.
- No deployment.
