# RIPPLE Mission State

- mission_id: AICTX-RIPPLE-20261005T0143+07
- parent_mission: AICTX-PCAC-20261005T0143+07
- platform_chat_id: UNKNOWN_NOT_EXPOSED_TO_ASSISTANT
- persistence_mode: DURABLE_RESUMABLE
- repository: goif74945-crypto/AI-CONTEXT
- branch: main
- writable_scope: คลังข้อมูลเสริม/RIPPLE-Revision-Impact-Proof-Lineage-Engine/** plus supplemental index
- protected_scope: every repository whose name contains NEXY.AI; unrelated existing AI-CONTEXT paths
- current_phase: DESIGN_LOCK
- status: IN_PROGRESS
- concept_authority: AI_PROPOSED_CONCEPT_ONLY

## Objective
Build a deterministic standalone engine that receives a versioned proof/dependency graph plus a change set and computes:
1. transitive impacted nodes;
2. evidence that becomes stale;
3. claims that lose required fresh evidence and must reopen;
4. the smallest deduplicated set of verification producers/tests that must rerun;
5. reason chains for every invalidation;
6. fail-closed freeze escalation for blocking claims/authority-critical changes;
7. an explicit set of unaffected evidence that remains valid.

## Compatibility boundary
RIPPLE complements, rather than replaces, NEXY Evidence/SystemEnvelope/Judge/Vault concepts. It does not approve actions and does not modify NEXY.AI.

## Authority sources
- /AI-EXECUTION-KERNEL.md
- /rules/GLOBAL.md
- /rules/SECURITY.md
- /rules/VERIFICATION.md
- /projects/NEXY.AI/overview.md
- /projects/NEXY.AI/deep/doc-c-vnext-build-spec.md
- /projects/NEXY.AI/deep/doc-e-deployment-evidence.md
- /projects/NEXY.AI/deep/constitutional-locks.md
- /projects/NEXY.AI/deep/final-architecture-cross-system.md

## Evidence-backed gap statement
Within the inspected authoritative context:
- evidence objects and exact build/environment binding exist;
- dependency/test impact review is required for spec extension;
- invalid release tokens/stale jobs are defined in narrower contexts;
- a general transitive proof invalidation/minimal revalidation planner was not found in the inspected files.
This is not an exhaustive absence proof outside the inspected scope.

## Core invariants
- deterministic output for the same graph/change set;
- no global invalidation when a bounded affected closure can be proven;
- no stale evidence may satisfy a blocking claim;
- no missing graph reference may be guessed;
- causal reason chain must exist for every stale/reopened item;
- cyclic hard-dependency graph freezes planning unless explicitly modeled later;
- NEXY remains final authority.

## Planned deliverables
README, DESIGN, REQUIREMENTS, NEXY-INTEGRATION-CONTRACT, schema, TypeScript reference implementation, positive/negative/property tests, benchmark, test evidence, completion certificate, and final durable checkpoint.

- last_checkpoint: CP-0001-RIPPLE-BOOTSTRAP
- next_action: implement graph contracts and deterministic invalidation planner locally; test, audit, persist, read back.
