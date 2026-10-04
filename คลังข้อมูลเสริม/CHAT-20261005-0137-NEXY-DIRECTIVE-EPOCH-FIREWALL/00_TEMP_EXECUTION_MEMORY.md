# Temporary Execution Memory — NEXY Directive Epoch Firewall

Status: IN_PROGRESS
Session reference: CHAT-20261005-0137-NEXY-DEF
Session reference type: local durable project tag; NOT the ChatGPT platform conversation ID
Created: 2026-10-05T01:37+07:00
Storage repository: goif74945-crypto/AI-CONTEXT
Protected repositories: any repository whose name contains `NEXY.AI`
Mutation boundary: additive files under this project folder only

## Objective
Design, implement, test, and preserve an AI-proposed reference system that prevents stale autonomous actions from being committed after a newer user directive supersedes, narrows, revokes, or replaces the directive under which those actions were prepared.

## Source-grounded alignment
FACT_PROJECT:
- NEXY is a deterministic AI control hub; workers/models are not final authority.
- USER LAW / explicit human control is a governing authority surface.
- One legal verified output or FREEZE is preferred over guessing.
- Current build design includes directive execution, queue/idempotency, auditability, FREEZE/STOP semantics, and mutating-route idempotency.
- FREEZE purges pending output; old queue jobs are not resumed after recovery.
- Human/operator mutation is intended to be explicit, finite, replayable, and auditable.

Source references:
- projects/NEXY.AI/overview.md
- projects/NEXY.AI/deep/human-control-surface.md
- projects/NEXY.AI/deep/constitutional-locks.md
- projects/NEXY.AI/deep/doc-c-vnext-build-spec.md
- rules/SECURITY.md
- rules/VERIFICATION.md

## AI-proposed system
PROPOSAL: Directive Epoch / Instruction Supersession Firewall (DEF)

Core mechanism:
1. Every accepted user directive advances or confirms a logical directive epoch.
2. Every prepared side effect binds to the exact epoch, active directive hash, and authority-lineage hash.
3. A commit gate rechecks those bindings immediately before mutation.
4. Any stale or tampered prepared action FREEZEs instead of silently rebasing itself.
5. Narrowing a directive may only reduce capability; attempts to expand scope through a NARROW event FREEZE.
6. Irreversible actions require an explicit approval binding tied to the exact action digest and directive epoch.
7. Event replay must deterministically reproduce the same state and lineage hash.

## Non-goals
- No natural-language intent inference.
- No modification of NEXY.AI repositories.
- No claim that this is current NEXY implementation.
- No cryptographic identity/authentication implementation; approval signatures belong to the surrounding AUTH/CORE layer.
- No background execution.

## Required deliverables
- Task contract
- Architecture
- Protocol/state model
- Threat/failure model
- Requirement ledger
- NEXY integration map
- Reference implementation
- Tests and fixtures
- Executed validation evidence
- AI-proposed future extensions
- Final audit

## Verification target
E1: Python compile/static validity.
E2: executed unit tests for state transitions, stale-action rejection, idempotency, tamper detection, approval binding, and deterministic replay.
E3: local fixture-driven integration/smoke flow across event apply → prepare → supersede → commit gate.

## Current state
COMPLETED:
- AI-CONTEXT boot/kernel/router/rules read.
- NEXY project overview/current matrix/deep human-control/constitutional/build-spec context read.
- Existing supplemental tree inspected (685 paths) to avoid obvious duplication.
- New project path checked and confirmed absent.
- Project topic selected.

IN_PROGRESS:
- Design and reference implementation.

NEXT:
- Build code + tests locally.
- Execute validation.
- Fix any failures.
- Publish verified artifacts and evidence into this folder.
- Re-read written paths and final-audit.

## Stop conditions
- Any action would mutate a repository whose name contains NEXY.AI.
- A design claim is presented as current implementation truth.
- Test evidence is unavailable for a PASS claim.
- Required project path collides with pre-existing work.
