# Temporary Execution Memory — NEXY Operator Contract Compiler

Execution/work ID: CHAT-20261005-0121-NEXY-OPERATOR-CONTRACT-COMPILER
Created: 2026-10-05 Asia/Bangkok
Status: EXECUTING
Classification: AI_PROPOSAL + supplemental implementation; NOT current NEXY.AI runtime truth.

## Objective
Create a divergent, high-value supplemental system for NEXY.AI without modifying any repository whose name contains NEXY.AI.

The system will deterministically compile authoritative Core/API state into a machine-checkable operator-facing contract that:
- reflects real state without inventing success;
- preserves visible/editable/executable distinctions;
- derives only legal next actions from role/state/risk;
- exposes explicit FREEZE/STOP semantics;
- emits structured reason/evidence summaries without exposing hidden model reasoning;
- supports progressive disclosure and safe redaction;
- is testable and provider/model independent.

## Authority sources loaded
1. User directive in current conversation.
2. AI-CONTEXT/AI-EXECUTION-KERNEL.md
3. AI-CONTEXT/rules/GLOBAL.md
4. AI-CONTEXT/rules/AI-BEHAVIOR.md
5. AI-CONTEXT/rules/SECURITY.md
6. AI-CONTEXT/rules/VERIFICATION.md
7. AI-CONTEXT/projects/NEXY.AI/overview.md
8. AI-CONTEXT/projects/NEXY.AI/deep/doc-c-vnext-build-spec.md
9. AI-CONTEXT/projects/NEXY.AI/deep/doc-d-product-design.md
10. AI-CONTEXT/projects/NEXY.AI/deep/human-control-surface.md
11. AI-CONTEXT current 837-row source-normalization matrix metadata.

## Source facts
- NEXY identity is deterministic control infrastructure; one verified output or freeze.
- Current build state enum includes INIT, READY, RUNNING, VERIFYING, CONSENSUS, STABLE, FREEZE, STOP.
- Roles include OWNER, OPERATOR, AUDITOR, SYSTEM, PUBLIC_USER.
- UI must reflect real state and must not substitute visibility for authorization.
- FREEZE blocks release and new non-owner execution; STOP is irreversible in current build model.
- DOC-D requires freeze UI to expose primary incident code, trigger, blocking layer and recoverability.
- Current normalized source denominator is 837 requirement rows; legacy 215 registry is deprecated/unreliable for current counting.

## Protected scope
- DO NOT modify, commit, push, merge, branch, configure, or otherwise mutate any repository whose name contains "NEXY.AI".
- DO NOT claim this proposal is implemented in NEXY.AI.
- DO NOT store secrets.
- DO NOT silently extend NEXY current build scope.

## Authorized scope
Only new files under:
คลังข้อมูลเสริม/CHAT-20261005-0121-NEXY-OPERATOR-CONTRACT-COMPILER/
inside goif74945-crypto/AI-CONTEXT.

## Planned deliverables
- task contract and design specification
- machine-readable input/output schemas
- Python reference implementation using standard library only
- deterministic policy/action compiler
- reason/evidence summary compiler
- redaction/progressive-disclosure layer
- CLI
- unit + negative-path + determinism tests
- fixtures
- requirement/evidence ledger
- future integration/adoption proposal
- final audit and resumable checkpoint

## Verification target
E0 presence + E1 syntax/schema/static validation + E2 executed unit/negative/determinism tests.
No claim of E3/E4/E5/E6 because this implementation is supplemental and not integrated with NEXY.AI runtime.

## Stop conditions
Freeze if writing would touch a protected repository/path, authority conflict materially changes semantics, or required evidence cannot be honestly obtained.

## Current state
COMPLETED:
- AI-CONTEXT boot/kernel/router/rules read.
- NEXY overview, human control surface, DOC-C and DOC-D read.
- Supplemental tree inspected (350 paths at observation time).
- Existing reliability/spec/counterfactual/capacity projects reviewed to avoid direct duplication.

IN PROGRESS:
- architecture + implementation.

NEXT:
- build local reference package and tests;
- run tests/fix/re-run;
- publish only verified artifacts here;
- re-read committed files and record evidence.
