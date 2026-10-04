# Task Contract — NEXY Intent Integrity Lab

Status: ACTIVE
Session code: NEXY-IIL-20261005-0121-TH
Platform chat ID: UNKNOWN (not exposed by available tools)
Created from user directive time: 2026-10-05T01:21+07:00

## OBJECTIVE
Design, implement, test, and document an additive prototype that preserves explicit user intent as a deterministic, inspectable contract before execution. The prototype must detect missing authority, unresolved critical unknowns, protected-scope collisions, and scope drift without guessing.

## TARGET
Repository: goif74945-crypto/AI-CONTEXT
Authorized path only: `คลังข้อมูลเสริม/NEXY-INTENT-INTEGRITY-LAB-20261005-0121/**`

## AUTHORIZED_SCOPE
- Add new files only under the target path.
- Read AI-CONTEXT for governing context.
- Read goif74945-crypto/NEXY.AI- as evidence only.
- Build and test a standalone prototype locally.
- Record verification evidence and a resumable session state.

## PROTECTED_SCOPE
- Entire repository goif74945-crypto/NEXY.AI-: READ-ONLY.
- Existing AI-CONTEXT files outside the target path: NO MUTATION.
- Existing sibling folders under คลังข้อมูลเสริม: NO MUTATION.

## AUTHORITY_SOURCES
1. Current explicit user directive.
2. AI-CONTEXT/AI-EXECUTION-KERNEL.md.
3. AI-CONTEXT/WORK-ROUTER.md and INDEX.md where applicable.
4. Current NEXY.AI repository state for observed compatibility facts only.
5. This prototype's tests for prototype behavior only.

## SOURCE FACTS USED
- NEXY repository orientation states: "One Output. One Truth. Or Freeze."
- README describes Layer 2 Context & Intent Resolution as rejecting ambiguous intent rather than guessing.
- packages/human/dialog-sandbox.ts routes TASK intent away from presentation-only dialog and gives dialog no core mutation authority.
- No code-search hit for the exact phrase "user intent" was observed in the inspected NEXY repository state.

## SUCCESS_INVARIANTS
- No mutation to any repository whose name contains NEXY.AI.
- Prototype uses deterministic canonical serialization and SHA-256 sealing.
- Missing required contract sections cannot silently become defaults.
- Critical UNKNOWN/CONFLICT/protected-scope collision produces FREEZE.
- Comparison between contract revisions reports potentially unsafe scope drift.
- Tests cover admission, freeze, canonicalization, sealing, duplicate handling, and drift classification.
- Documentation labels all new architecture ideas as AI-PROPOSED / ADVISORY ONLY.
- Remote files are fetch-verified after write.

## FORBIDDEN_ACTIONS
- Modifying, committing, merging, branching, pushing, deleting, renaming, or changing settings in NEXY.AI.
- Treating README/descriptive NEXY text as higher authority than actual canonical sources.
- Claiming this prototype is integrated with, required by, or deployed to NEXY.AI.
- Guessing intent from missing fields.
- Hiding failing tests.
- Writing secrets or credentials.

## REQUIRED_EVIDENCE
- TypeScript typecheck result.
- Executed automated test result.
- Determinism/repeatability test.
- Remote GitHub fetch verification of all critical artifacts.
- Final session state with exact status and known limitations.

## STOP_CONDITIONS
Freeze mutation if:
- target repository/path becomes uncertain;
- a required write would touch protected scope;
- authoritative inputs conflict materially;
- local prototype tests cannot be made to pass without weakening the stated invariants;
- repository state changes in a way that makes a planned write unsafe.

## DELIVERABLES
- executable standalone Intent Integrity Engine prototype;
- machine-readable schema/example contracts;
- test suite and fixtures;
- architecture and policy documentation;
- integration blueprint that is explicitly non-authoritative;
- verification report;
- resumable session state.

## SCOPE LABEL
This project is additive research/prototyping only. It does not alter NEXY.AI.
