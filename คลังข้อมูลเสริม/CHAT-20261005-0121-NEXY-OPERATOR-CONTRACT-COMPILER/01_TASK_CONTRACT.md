# Task Contract — NEXY Operator Contract Compiler

Status: LOCKED FOR THIS EXECUTION
Classification: AI_PROPOSED_FUTURE_SYSTEM

## Objective
Design, implement, test, and document a deterministic compiler that translates NEXY system truth into an operator-facing interaction contract while preserving authority, evidence, and legal-action boundaries.

## Target
Repository: goif74945-crypto/AI-CONTEXT
Path: คลังข้อมูลเสริม/CHAT-20261005-0121-NEXY-OPERATOR-CONTRACT-COMPILER/
Branch: default branch (main observed)
Expected write pattern: create-only in the new path.

## In scope
- reference implementation independent of NEXY.AI runtime;
- canonical mapping of current DOC-C state/role names;
- legal-action policy;
- FREEZE/STOP behavior;
- visible/editable/executable separation;
- structured reason/evidence summaries;
- deterministic output hashing;
- progressive disclosure;
- PII/secret-safe redaction for presentation fields;
- CLI and test suite;
- machine-readable schema;
- adoption plan clearly marked proposal.

## Out of scope
- changing NEXY.AI implementation;
- claiming production integration;
- provider calls;
- authentication implementation;
- persistence/database changes;
- deployment;
- changing DOC-B/C/D/E authority;
- adding new current-build obligations.

## Success invariants
1. Same normalized input and policy version => byte-stable canonical JSON output.
2. No action may be executable unless role + state + policy explicitly allow it.
3. FREEZE must never render as success or releaseable.
4. STOP must expose no executable resume/run action.
5. PUBLIC_USER and AUDITOR cannot receive mutating executable actions.
6. OWNER recovery appears only for recoverable FREEZE.
7. Missing mandatory freeze metadata produces an invalid contract, not guessed text.
8. Evidence state and reason codes remain explicit.
9. Hidden/internal reasoning is never required in output.
10. Unknown fields fail closed under strict schema validation.

## Required evidence
- Python compile/import validation.
- JSON schema shape validation via implementation validators.
- executed unit tests;
- negative tests for permissions/state/freeze/stop;
- determinism test;
- stable hash test;
- CLI fixture test.

## Completion condition
All in-scope tests PASS and committed artifacts are re-read from AI-CONTEXT after write. Integration with NEXY.AI remains NOT_VERIFIED/NOT_PERFORMED by design.
