# Task Contract — NEXY Multi-FSM Formal Consistency Lab

## Identity
- mission_id: NMFFCL-20261005-0122
- chat_code: CHAT-20261005-0122-NEXY-MULTIFSM-FORMAL-LAB
- persistence_mode: DURABLE_RESUMABLE
- execution_mode: ACTIVE_SYNC + LOGICAL_ISOLATION role court
- target: goif74945-crypto/AI-CONTEXT@main

## Objective
Design, implement, test, verify, and document a standalone deterministic reference engine for formal consistency analysis of one or more FSM definitions relevant to future NEXY engineering.

## Authority order
1. current explicit user directive;
2. AI-CONTEXT AI-EXECUTION-KERNEL and global/security/verification laws;
3. current NEXY project authority boundaries;
4. current AI-CONTEXT FSM registry as observed data;
5. this lab's AI-proposed design.

## IN SCOPE
- new files only under this workstream directory;
- read-only use of current AI-CONTEXT NEXY context/FSM registry;
- local isolated execution of the new reference prototype and tests;
- deterministic analysis of declared machine models;
- counterexample traces for violated modeled invariants;
- documentation of possible future NEXY adoption.

## PROTECTED / OUT OF SCOPE
- any write to any repository whose name contains NEXY.AI;
- any write to pre-existing AI-CONTEXT paths;
- claiming this lab changes current DOC-B/DOC-C/DOC-D/DOC-E;
- claiming runtime/deployment behavior of NEXY.AI;
- inventing guard satisfiability semantics when guards are free-form text;
- treating historical/deprecated requirement counts as current truth;
- destructive Git/history operations;
- secrets or credentials.

## Immutable requirements
R1. Unknown semantics remain UNKNOWN/NOT_VERIFIED; the checker must not pretend free-form guards are formally solved.
R2. Output ordering must be deterministic for equal normalized input.
R3. Local machine checks must include invalid references, duplicate/ambiguous transition routing, reachability, unexpected dead ends, and terminal/absorbing-state violations.
R4. Multi-machine mode must preserve namespaces and never merge same-named states across machines.
R5. Cross-FSM invariants must be explicit data, never inferred from label similarity.
R6. When a modeled invariant is violated in explored state space, the engine should emit a shortest discovered counterexample trace.
R7. State-space explosion must fail closed with an explicit bounded-analysis status, not pretend exhaustive verification.
R8. Partial/source-design FSMs must be analyzable without falsely upgrading partial semantics to complete semantics.
R9. No mutation outside authorized scope.
R10. Every PASS claim must bind to fresh evidence of the matching class.

## Acceptance criteria
A1. Reference package exists and imports under Python 3 stdlib only.
A2. Unit tests demonstrate RED before implementation and GREEN after implementation.
A3. Tests cover deterministic normalization, pipe-expansion endpoints, reachability, ambiguous routing, terminal-state rules, dead-end detection, product exploration, cross-invariant violation, shortest trace, and state-cap behavior.
A4. A source-derived DOC-C execution example is analyzed without modifying source registry files.
A5. Verification report distinguishes reference-prototype proof from NEXY runtime proof.
A6. All committed artifacts are read back from GitHub after final mutation.
A7. Final audit shows protected scope untouched by this workstream's writes.

## Required evidence
- E0: GitHub create/read receipts
- E1: compileall/import plus deterministic serialization checks
- E2: unittest execution with zero failures for the final exact source
- E2 negative/adversarial cases proving the checker catches intentionally bad models

## Stop / freeze conditions
- required mutation would touch NEXY.AI;
- target workstream path collides with pre-existing non-owned content;
- higher authority invalidates the concept;
- inability to obtain required E1/E2 evidence for a claimed PASS;
- secret exposure or irreversible external action.

## Deliverables
Architecture, formal semantics, requirement ledger, code, tests, fixtures, example, verification report, integration proposal, research backlog, final audit, resume capsule.
