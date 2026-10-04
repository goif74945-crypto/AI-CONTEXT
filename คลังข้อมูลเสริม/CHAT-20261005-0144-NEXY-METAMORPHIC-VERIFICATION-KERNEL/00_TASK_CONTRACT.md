# Task Contract — CHAT-20261005-0144-NEXY-METAMORPHIC-VERIFICATION-KERNEL

## Objective
Create a new, non-colliding, high-value standalone verification project in `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม` that can later integrate with NEXY.AI without modifying the separate NEXY.AI repository.

## Authority
1. Current user directive in this conversation.
2. `AI-EXECUTION-KERNEL.md`.
3. `rules/GLOBAL.md`, `rules/SECURITY.md`, `rules/VERIFICATION.md`.
4. `projects/NEXY.AI/overview.md` for integration principles only.
5. This project's AI-proposed design, never promoted above NEXY authority.

## Authorized scope
- Create a new isolated folder under `AI-CONTEXT/คลังข้อมูลเสริม`.
- Create design, source code, tests, examples, temporary memory, and evidence inside that folder.
- Read NEXY.AI context from AI-CONTEXT for compatibility reasoning.

## Protected scope
- Every repository whose name contains `NEXY.AI`.
- Existing sibling projects under `คลังข้อมูลเสริม`.
- Secrets, credentials, production systems, deployments.

## Success invariants
- No mutation to NEXY.AI repository.
- AI-originated proposal is explicitly labeled.
- Standalone library is importable and testable.
- Failures are classified rather than hidden.
- Hashes are deterministic for supported canonical data.
- Critical monotonicity relations fail closed.
- Tests include positive and negative paths.
- Evidence records exact commands and observed results.

## Required evidence
- E0: created artifact tree exists.
- E1: Python compile check passes.
- E2: unit tests pass.
- Local integration evidence: installed/entrypoint fixture validation and multi-relation harness.
- NEXY.AI E3+ integration: explicitly NOT VERIFIED because NEXY.AI may not be modified by this task.

## Stop conditions
- Any required action would mutate NEXY.AI.
- Repository target becomes ambiguous.
- Required write permission to AI-CONTEXT is absent.
- Verification reveals unresolved critical defect.
