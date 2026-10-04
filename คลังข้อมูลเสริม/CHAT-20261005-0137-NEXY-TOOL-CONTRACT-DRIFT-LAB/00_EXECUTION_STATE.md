# Execution State — NEXY Tool Contract Drift Lab

Status: IN_PROGRESS
Created: 2026-10-05T01:37+07:00
Project reference: CHAT-20261005-0137-NEXY-TOOL-CONTRACT-DRIFT-LAB
Platform immutable chat/conversation ID: UNKNOWN (not exposed by available toolset; do not invent)

## Objective
Design, implement, test, and preserve an auxiliary prototype that detects semantic drift in external tool/plugin/connector contracts before NEXY-like orchestration relies on them.

## Scope lock
AUTHORIZED WRITE:
- goif74945-crypto/AI-CONTEXT
- only under: คลังข้อมูลเสริม/CHAT-20261005-0137-NEXY-TOOL-CONTRACT-DRIFT-LAB/

READ-ONLY CONTEXT:
- AI-CONTEXT project context for NEXY.AI
- NEXY.AI repositories/spec context when needed for compatibility reasoning

PROTECTED / FORBIDDEN:
- Any repository whose name contains NEXY.AI
- No create/update/delete/move/rename/commit/push/merge/branch/settings/workflow/issue/PR mutation there
- No promotion of this proposal into canonical NEXY requirements
- No secrets, credentials, or private tokens

## Authority baseline
1. Current user directive
2. AI-CONTEXT canonical execution/security/verification rules
3. NEXY.AI authoritative context in AI-CONTEXT
4. This lab's own AI-proposed design

## Verified source facts
- NEXY treats external models/tools as workers/capabilities rather than authority.
- AI-CONTEXT capability registry explicitly warns dynamic external capabilities may become stale and should be refreshed before reliance.
- Existing supplemental Semantic Contract Lab includes generic Interface Drift and Tool Semantics Drift, but no dedicated executable tool-schema drift detector was found by path inspection.

## Current state
COMPLETED:
- AI-CONTEXT repository identity and write permission verified.
- Existing supplemental tree inspected to reduce duplication.
- NEXY overview, current source matrix, capability registry, verification/security rules inspected.
- Candidate project selected: dedicated Tool Contract Drift Sentinel/Lab.

IN PROGRESS:
- Design contract
- Reference implementation
- Test suite
- Evidence capture
- Integration guide
- Final audit

BLOCKED:
- None

NEXT:
1. Define drift semantics and safety policy.
2. Implement canonicalizer, diff classifier, decision engine, CLI.
3. Build unit/property-style scenario tests.
4. Run syntax + unit + negative + regression tests locally.
5. Fix failures until green.
6. Write design/code/tests/evidence into this folder.
7. Read back written files and record final verification.

## Verification status
NOT_VERIFIED until executed tests and read-after-write checks exist.
