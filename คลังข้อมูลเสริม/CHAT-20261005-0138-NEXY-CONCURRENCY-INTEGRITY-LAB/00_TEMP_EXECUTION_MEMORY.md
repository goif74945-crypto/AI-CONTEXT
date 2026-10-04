# Temporary Execution Memory — NEXY Concurrency Integrity Lab

Status: IN_PROGRESS
Truth class: REPO_FACT_FOR_THIS_TASK_RECORD
Durable chat/work code: CHAT-20261005-0138-NEXY-CONCURRENCY-INTEGRITY-LAB
Platform-native ChatGPT conversation ID: UNKNOWN_NOT_EXPOSED
Started local: 2026-10-05T01:38:00+07:00

## Objective
Design, implement, test, and document an isolated AI-proposed concurrency-integrity reference system for future NEXY integration without mutating any repository whose name contains NEXY.AI.

The system must detect and explain multi-agent mutation hazards before execution, build deterministic conflict-free execution waves where lawful, and fail closed on unresolved write/read-version/external-side-effect collisions rather than inventing ordering.

## Target
Repository: goif74945-crypto/AI-CONTEXT
Branch: main
Authorized write scope:
- คลังข้อมูลเสริม/CHAT-20261005-0138-NEXY-CONCURRENCY-INTEGRITY-LAB/**

Protected scope:
- every repository whose name contains NEXY.AI;
- every existing sibling path under คลังข้อมูลเสริม;
- canonical NEXY DOC-B/C/D/E context;
- secrets, credentials, production state.

## Authority/context read
- AI-BOOTSTRAP.md
- INDEX.md
- AI-EXECUTION-KERNEL.md
- WORK-ROUTER.md
- rules/GLOBAL.md
- rules/AI-BEHAVIOR.md
- rules/SECURITY.md
- rules/VERIFICATION.md
- workflows/project-start.md
- workflows/system-design.md
- workflows/implementation.md
- workflows/verification.md
- workflows/memory-update.md
- projects/NEXY.AI/overview.md
- projects/NEXY.AI/deep/INDEX.md
- projects/NEXY.AI/deep/doc-c-vnext-build-spec.md
- projects/NEXY.AI/deep/capability-registry-chaos.md
- projects/NEXY.AI/source-normalization/CURRENT-SYSTEM-FEATURE-BUILD-MATRIX.md

## Source-grounded invariants
- NEXY is a deterministic control hub; SWARM/agents are labor, while CORE/JUDGE/LAW retain authority.
- Current DOC-C includes queue + idempotency and optimistic Vault revisioning.
- SWARM -> VAULT is a forbidden direct dependency in current DOC-C.
- Current queue target has max concurrent pipeline runs = 10.
- Mutating routes require idempotency keys unless explicitly exempt.
- Vault revisioning uses optimistic concurrency / previous_version.
- Invalid/ambiguous/unsafe conditions freeze rather than silently patching.
- Design, implementation, runtime, deployment, and physical evidence remain separate truth domains.

## Distinctness inspection
Inspected nearby supplemental work:
- Human Agency Lab: interruption/preview/confirm/freeze policy; rollback is a gate input.
- Delegation Lease Lab: plan-bound temporary restrictive authority; concurrency atomicity explicitly NOT_VERIFIED.
- Resource Governor: token/cost/latency/model-resource allocation, not state-mutation hazards.
- MultiFSM Formal Lab: state-machine reachability/model checking.
- Human Control Surface Assurance: UI/control semantic manifest linting.
- Freeze Bridge: translating already-decided freeze states into recovery guidance.

Selected gap:
Pre-execution concurrency integrity for multiple proposed mutations: read/write hazards, stale expected versions, duplicate/divergent idempotency claims, external side-effect collisions, explicit dependency ordering, and deterministic execution-wave construction.

This is search/inspection-bounded distinctness, not a universal uniqueness claim.

## Architectural position
Proposed only:

SWARM / tools / agents
  -> proposed mutation intents (NO direct write)
  -> NCIL planner under CORE boundary
  -> conflict graph + deterministic schedule OR FREEZE findings
  -> existing LAW/JUDGE/CORE authorization and execution path
  -> target stores/services

NCIL never grants authority and never executes the mutation itself.

## Planned deliverables
1. Task contract / scope lock.
2. Design + architecture.
3. Mutation-intent protocol and JSON schema.
4. Deterministic Python standard-library reference implementation.
5. CLI.
6. Unit / adversarial / bounded property tests.
7. Scenario corpus.
8. Failure and threat model.
9. NEXY compatibility / adoption map marked AI-PROPOSED.
10. Evidence ledger + raw test output.
11. Future ideas explicitly marked AI-PROPOSED.
12. Final audit + read-back verification.
13. Publication manifest/hash binding.

## Required evidence
- E0: committed artifacts exist and re-fetch matches intended content.
- E1: Python compile/static JSON parse.
- E2: executed local unit/adversarial/scenario tests.
- E3-E7: NOT_VERIFIED and not claimed.
- NEXY.AI integration/runtime/deployment: NOT_VERIFIED by design.

## Stop conditions
Freeze if:
- a step would mutate any repository whose name contains NEXY.AI;
- target namespace collides with an existing path;
- correctness requires guessing a canonical NEXY rule;
- a write would overwrite sibling work;
- verification cannot bind published bytes to tested bytes;
- secret/credential material would be persisted.

## Current state
COMPLETED:
- boot/context/authority read;
- target namespace absence observed;
- sibling distinctness inspection;
- concept pivot away from overlapping rollback/human-agency work;
- scope locked to unique folder.

IN PROGRESS:
- protocol/architecture design;
- reference implementation;
- tests.

NEXT ACTION:
Build project in isolated local staging, run verification, repair failures, then publish exact verified files into this folder and re-fetch for final evidence.
