# Task Contract — NEXY Runtime Failure Topology Lab

Classification: **AI_PROPOSAL / EXPERIMENTAL / NON_GOVERNING**

## Objective
Create five deterministic reference systems that help future NEXY runtime orchestration detect and contain failure topologies without weakening canonical authority, evidence requirements, or protected-scope boundaries.

## Target
- Repository: `goif74945-crypto/AI-CONTEXT`
- Branch: `main`
- Write root: `คลังข้อมูลเสริม/CHAT-20261005-0222-NEXY-RUNTIME-FAILURE-TOPOLOGY-LAB/**`

## Authority order
1. Explicit current user directive.
2. AI-CONTEXT execution/security/verification/memory rules.
3. Current source-derived NEXY context in AI-CONTEXT.
4. Read-only current NEXY repository contracts at observed exact SHA.
5. Runtime evidence from this isolated lab.
6. AI proposal/inference.

## In scope
- New artifacts only under the task write root.
- Read-only analysis of NEXY current contracts for compatibility.
- Deterministic Python reference implementation using standard library only.
- TDD RED/GREEN evidence, static compile, unit, adversarial, integration, deterministic replay checks.
- Design, failure semantics, compatibility boundary, evidence record, manifest and final audit.

## Out of scope / forbidden
- Any mutation to a repository whose name contains `NEXY.AI`.
- Any claim that this proposal is current NEXY law or production implementation.
- Deployment, production runtime mutation, secret access, provider calls, network I/O, subprocess use inside production library code, or automatic canonical promotion.
- Weakening NEXY evidence, authorization, release, freeze, or deterministic requirements.

## Immutable invariants
1. Malformed identity-sensitive input fails explicitly.
2. Equivalent unordered inputs produce deterministic canonical outputs.
3. Runtime containment diagnostics remain advisory; CORE/JUDGE authority is not replaced.
4. Retry decisions never mint idempotency or retryability.
5. Poison quarantine is revision-scoped so a fixed revision is not condemned by stale failures.
6. Salvaged partial results must be individually verified and dependency-closed; partial must never masquerade as whole-task completion.
7. Deadlock and livelock detection must distinguish structural blocking from mere slowness/idle waiting.
8. No implementation code performs network, file, environment, shell, database, or model I/O.
9. NEXY.AI remains read-only throughout this mission.

## Required evidence
- E0 Presence: persisted files and remote read-back.
- E1 Static: Python compile plus static forbidden-I/O scan.
- E2 Unit: executed deterministic unit/adversarial tests.
- E3 Integration: executed composition across all five modules.
- E4-E7: NOT_VERIFIED / not claimed.

## Acceptance criteria
- Five distinct modules implemented.
- Every public production function has focused tests.
- RED evidence exists before implementation.
- Full unit/adversarial/integration suite passes after repairs.
- Determinism tests pass under input permutations where order is semantically irrelevant.
- Static scan finds no forbidden production calls/imports.
- Remote persisted bytes for all authored files match the tested local bytes at the publication commit.
- No changed path at the publication commit falls outside the authorized task root.

## Stop / freeze conditions
- Required action would mutate NEXY.AI.
- Target root collides with existing work.
- Authority conflict cannot be resolved.
- Required runtime evidence cannot be executed.
- Persistence cannot be proven at exact commit identity.
- A critical test remains failing after bounded repair attempts.
