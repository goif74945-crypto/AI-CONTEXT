# Task Contract

## Objective
Create a large, future-useful NEXY.AI-adjacent project inside `AI-CONTEXT/คลังข้อมูลเสริม/` without modifying any repository whose name contains `NEXY.AI`.

## Target
`goif74945-crypto/AI-CONTEXT` only.

## Authorized scope
Create one new isolated prefix:
`คลังข้อมูลเสริม/NEXY-INTERACTION-ECONOMICS-LAB-20261005/`

## Protected scope
- Every repository whose name contains `NEXY.AI`.
- Existing AI-CONTEXT files outside the new prefix.
- Secrets, credentials, tokens, and private keys.

## Authority sources
1. Current user directive.
2. `AI-BOOTSTRAP.md`.
3. `INDEX.md`.
4. `AI-EXECUTION-KERNEL.md`.
5. `WORK-ROUTER.md`.
6. `rules/GLOBAL.md`, `rules/SECURITY.md`, `rules/VERIFICATION.md`.
7. `projects/NEXY.AI/overview.md` and current source-normalization matrix for product principles only.

## Success invariants
- New work is visibly marked AI-proposed, not current NEXY law/spec.
- Code has deterministic behavior and explicit failure semantics.
- Safety/authority constraints cannot be removed merely to lower friction.
- Full local validation passes before repository mutation.
- No NEXY.AI repository mutation occurs.
- Durable checkpoint and evidence are left for another AI.

## Required evidence
- E0: committed file presence under the authorized prefix.
- E1: Python compile/import validation.
- E2: unit + exhaustive state-space tests.
- E3: CLI subprocess/integration behavior and example runs.
- Exact GitHub commit/tree evidence after mutation.

## Stop conditions
Stop and mark BLOCKED if the target repository identity changes, the authorized prefix already exists unexpectedly, branch update is non-fast-forward and cannot be safely rebased, or mutation would require touching protected scope.
