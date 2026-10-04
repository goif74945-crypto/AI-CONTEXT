# NEXY-REFLEX Mission Contract

## Mission ID
`NXR-20261005-0137-REFLEX`

## Chat ID
`UNKNOWN_NOT_EXPOSED_TO_MODEL`

The ChatGPT platform conversation identifier is not exposed to this execution environment. The mission ID above is the durable operational identifier for this work.

## Objective
Create a standalone, deterministic, fail-closed shadow verification laboratory that can consume exported NEXY requirement/authority/evidence snapshots, detect authority conflicts and stale proof, calculate change-driven invalidation, and produce a replayable advisory gate result without mutating the NEXY.AI repository or runtime.

## Authority sources
1. Current explicit user instruction in this conversation.
2. `AI-CONTEXT/AI-EXECUTION-KERNEL.md`.
3. `AI-CONTEXT/rules/GLOBAL.md`, `SECURITY.md`, `VERIFICATION.md`.
4. `AI-CONTEXT/projects/NEXY.AI/overview.md`.
5. `AI-CONTEXT/projects/NEXY.AI/source-normalization/CURRENT-SYSTEM-FEATURE-BUILD-MATRIX.md`.

## In scope
- New files only under `AI-CONTEXT/คลังข้อมูลเสริม/NEXY-REFLEX/`.
- Design, contracts, standalone Python implementation, unit tests, examples, evidence, and resumable state.
- Compatibility by explicit import/export contract only.

## Protected scope
- Every repository whose name contains `NEXY.AI`.
- Existing NEXY implementation code, branches, settings, workflows, issues, PRs, and deployment/runtime state.
- Existing AI-CONTEXT files outside the new NEXY-REFLEX folder, except read-only inspection.

## Immutable requirements
- No guessing of authority or evidence freshness.
- Deterministic canonical JSON and stable digests.
- Same-highest-authority conflict must fail closed.
- Stale or missing required evidence must never become PASS.
- Evidence class substitution is forbidden unless the requirement explicitly accepts that class.
- Non-current/deferred scope remains traceable but is not treated as a current-build failure.
- The tool is advisory and may not mutate NEXY.
- No secrets or credentials are persisted.

## Acceptance criteria
- Parser rejects malformed/unsupported input.
- Authority resolution is deterministic.
- Same-rank conflicts produce `CONFLICT` + `FREEZE_RECOMMENDED`.
- Missing/stale evidence produces `NOT_VERIFIED` + `FREEZE_RECOMMENDED`.
- Current explicit FAIL evidence produces `FAIL` + `FREEZE_RECOMMENDED`.
- Dependency cycles or structural corruption produce `BLOCKED`.
- Equivalent input ordering yields the same decision digest.
- Snapshot diff propagates invalidation to dependents.
- Static compile and unit tests pass against the delivered source bundle.
- GitHub read-back verifies the delivered source matches the tested source bundle.

## Stop conditions
- Any required mutation would touch protected scope.
- AI-CONTEXT write permission is unavailable.
- Tests reveal an unresolved defect.
- Post-write read-back differs from tested source.
