# NEXY Operator Experience Compiler Lab — Task Contract

Status: ACTIVE
Memory class: EXPERIMENTAL
Storage repository: goif74945-crypto/AI-CONTEXT
Authorized write scope: คลังข้อมูลเสริม/CHAT-20261005-0120-NEXY-OXC-LAB/**
Protected scope: every repository whose name contains "NEXY.AI"; all paths outside the folder above unless explicitly required for indexing and separately authorized
Work/session reference: CHAT-20261005-0120-NEXY-OXC-LAB
Platform ChatGPT conversation ID: UNKNOWN / not exposed by the available tool surface

## Objective
Design, implement, test, and document an AI-proposed reference system that converts authoritative NEXY state/role/risk information into a deterministic operator-facing presentation plan without changing Core truth, authority, permissions, release decisions, or project canon.

## Authority sources
1. Current explicit user directive.
2. AI-CONTEXT root Execution Kernel and global rules.
3. projects/NEXY.AI current authority/status/context.
4. DOC-B/DOC-C/DOC-D-derived context according to their recorded authority boundaries.
5. Current read-only NEXY implementation evidence only when directly observed.

## In scope
- proposal architecture;
- deterministic reference implementation;
- static/unit tests in a sandbox;
- failure/security/privacy model;
- requirement ledger;
- integration guidance that does not mutate NEXY;
- research backlog;
- resumable checkpoint/state files.

## Out of scope
- modifying, committing, branching, configuring, or otherwise mutating any repository whose name contains NEXY.AI;
- claiming this proposal is canonical NEXY behavior;
- production deployment;
- replacing Core/JUDGE/LAW authority;
- mood/emotion inference as authority;
- persistent personal profiling;
- hidden permission escalation.

## Immutable invariants
1. Presentation cannot change authoritative truth.
2. Presentation cannot grant permissions.
3. FREEZE/STOP and critical blocking states cannot be hidden.
4. Backend-denied actions can never become enabled by presentation preferences.
5. Preference changes may affect wording/detail/layout only, never eligibility, risk, authority, evidence, or release semantics.
6. Unknown/invalid contract values fail closed.
7. Reference implementation must be deterministic for identical inputs.
8. No time, randomness, network, filesystem, environment, or hidden I/O in the compiler core.

## Required evidence
- E0 presence for all deliverables;
- E1 TypeScript compile/static validation;
- E2 executed unit tests including negative-path and metamorphic invariance tests;
- post-write re-read of committed paths in AI-CONTEXT.

## Acceptance criteria
- unique proposal does not duplicate the dominant verification/context/epistemic packs already present in the supplemental vault;
- reference compiler passes all local E1/E2 checks;
- at least one test proves style preferences cannot alter action authorization/eligibility;
- at least one test proves FREEZE cannot be hidden;
- at least one test proves invalid input fails closed;
- all persisted files are explicitly EXPERIMENTAL / AI-PROPOSED;
- no protected repository mutation occurs.

## Stop conditions
FREEZE mutation if target identity changes, protected scope would be touched, authority conflicts materially, or a requested claim lacks matching evidence.
