---
name: nexy-concurrency
description: Verify NEXY optimistic concurrency and revision-conflict semantics, preventing stale or duplicate writers from silently overwriting authoritative Vault state.
---

# NEXY Skill

## Identity
- Formal ID: `VLT-006`
- Name: `nexy-concurrency`
- Family: VAULT / STATE
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Verify optimistic concurrency and revision conflicts.

## Authority
Concurrency decisions follow established Vault/revision/commit contracts. This Skill cannot invent a conflict-resolution winner or force an overwrite without explicit authority.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current Vault/revision/commit implementation and pinned test/evidence when applicable.

## Scope
### In Scope
Expected-version checks, optimistic concurrency, duplicate writers, revision/commit conflicts, idempotency interaction, race analysis and conflict evidence.
### Out of Scope
Silent last-write-wins, guessed merges, distributed locking mechanisms not established by source, or destructive force resolution without gate.

## Inputs
Universal inputs plus object/revision identity, expected and observed version/state, competing operation context and applicable idempotency/concurrency evidence.

## Outputs
Universal outputs plus concurrency verdict, conflict classification, winner/loser only when deterministically established by contract, evidence and next action.

## Workflow
Context → Authority → Concurrency Contract → Resolve Expected/Observed State → Model Competing Operations → Validate Preconditions/Idempotency → Detect Conflict → Apply Only Contract-Defined Resolution → Evidence.

## Required Behavior
Stale or incompatible writers are detected explicitly; resolution is deterministic only where the governing contract defines it.

## Forbidden Behavior
No silent overwrite, race-dependent truth, arbitrary winner selection, hidden retry, conflict swallowing or invented lock semantics.

## Architecture Constraints
Concurrency protection spans Vault/Revision/Commit boundaries and must preserve their state ownership.

## Security Constraints
Concurrency controls must not bypass authorization, tenant/ownership boundaries or audit requirements.

## Compatibility Constraints
Concurrency token/version/precondition changes require compatibility review across all producers/consumers.

## Data Integrity
A concurrent operation must not corrupt revision ordering, lineage, commit references or idempotency state.

## Failure Handling
Conflict returns explicit conflict/failure state; retry occurs only if separately authorized and contract-safe.

## Freeze Conditions
Critical race can corrupt authoritative state, conflict semantics are unknown, replay/duplicate can bypass integrity, or a force operation requires human gate.

## Validation
Two-writer stale/version cases, duplicate/replay, idempotency interaction, race ordering, rollback/recovery and regression tests as applicable.

## Completion Criteria
Concurrency behavior is contract-aligned, prevents silent overwrite and is supported by required current evidence.

## Stop Conditions
Conflict resolution is unspecified, target state is stale/unknown, destructive force is requested without gate or required evidence is unavailable.

## Checkpoint
Persist object/version state, competing operations, conflict result, evidence and resume point.

## Resume
Refresh authoritative state and expected-version inputs before re-evaluating a conflict.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Writer B using a stale expected revision must receive an explicit conflict rather than replacing Writer A's newer state.

## Non-Goals
This Skill does not define a new locking or merge protocol.

## Version
1.0.0
