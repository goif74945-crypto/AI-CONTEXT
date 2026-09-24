---
name: nexy-state-machine
description: Manage NEXY state transitions so every transition is valid, authorized, deterministic, auditable and recovery-safe.
---

# NEXY Skill

## Identity
- Formal ID: `CORE-002`
- Name: `nexy-state-machine`
- Family: CORE
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Manage state transitions; each transition must be valid, authorized, deterministic and auditable.

## Authority
State mutation requires explicit legal event/actor authority and cannot be forced around guards or recovery gates.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current FSM/state owner/transition code at pinned HEAD.

## Scope
### In Scope
States, initial/terminal states, events, owners, guards, actions, legal/illegal transitions, persistence, recovery, tests/evidence.
### Out of Scope
Merging unrelated FSMs, inventing transitions/events, bypassing ownership.

## Inputs
Universal inputs plus FSM/state owner, event, actor, current state and requested transition.

## Outputs
Universal outputs plus transition verdict, guards, resulting state, audit/persistence requirements, tests/evidence.

## Workflow
Context → Authority → FSM Requirement → Inspect State/Event/Owner → Validate Transition → Persist/Audit if authorized → Evidence.

## Required Behavior
Reject illegal transition; reject wrong actor; distinguish restart from continue; preserve recovery rules.

## Forbidden Behavior
No implicit state jump, no guessed actor ownership, no in-memory-only authority where durable state is required.

## Architecture Constraints
Do not collapse distinct state machines without source authority.

## Security Constraints
Recovery/protected transitions must enforce authorization and audit.

## Compatibility Constraints
State/event semantics and consumers remain version-compatible.

## Data Integrity
Durable state transitions must follow required atomicity/transaction semantics.

## Failure Handling
Illegal/unknown transition is explicit DENIED/BLOCKED/FREEZE as required.

## Freeze Conditions
Invalid critical transition, corrupted state, unknown owner/guard, recovery ambiguity or security violation.

## Validation
Positive/negative transitions, actor ownership, persistence/restart/recovery, race/replay and regression as applicable.

## Completion Criteria
Transition/state model is fully source-backed and required tests/evidence pass.

## Stop Conditions
Unknown current state, owner, event, guard or authority affecting safety.

## Checkpoint
Persist state/event/actor/guard/result and evidence.

## Resume
Reload authoritative state and revision before further transition.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- FREEZE → READY requires the source-defined recovery path and actor; it is not a generic “set state”.

## Non-Goals
This Skill does not invent FSMs or approve release.

## Version
1.0.0
