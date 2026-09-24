---
name: nexy-recovery
description: Recover NEXY from FREEZE only through authorized, evidence-backed recovery gates without converting damaged or unknown state into success.
---

# NEXY Skill

## Identity
- Formal ID: `CORE-006`
- Name: `nexy-recovery`
- Family: CORE
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Manage recovery after FREEZE without converting a freeze into success without evidence.

## Authority
Recovery requires source-defined actor/conditions and cannot bypass human/security/state gates.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current freeze reason, state, incident/audit and recovery implementation at pinned HEAD.

## Scope
### In Scope
Recoverability classification, authorized actor, prerequisites, state repair/validation, recovery transition, audit/evidence.
### Out of Scope
Auto-unfreeze, restart-as-recovery, suppressing incidents, assuming corruption repaired.

## Inputs
Universal inputs plus freeze reason, authoritative current state, actor, incident, repair evidence and recovery policy.

## Outputs
Universal outputs plus recovery verdict, prerequisites, transition, audit/evidence, remaining risk and rollback.

## Workflow
Context → Authority → Freeze Reason → Recoverability/Actor Check → Verify Repair → Authorized Transition → Post-Recovery Validation → Evidence.

## Required Behavior
Restart != Continue; damaged/unknown state stays blocked; successful recovery requires evidence.

## Forbidden Behavior
No direct state reset, no recovery on nonrecoverable reason, no actor bypass, no fake “healthy” state.

## Architecture Constraints
Respect state owner, persistence, incident/audit and service recovery boundaries.

## Security Constraints
Security incidents may require human/security gate before recovery.

## Compatibility Constraints
Recovery must preserve contracts/state version/lineage.

## Data Integrity
Validate authoritative state integrity, transaction/replay/idempotency and lineage as applicable.

## Failure Handling
Failed/insufficient repair evidence => remain FREEZE/BLOCKED.

## Freeze Conditions
Unknown/corrupted state, unauthorized actor, nonrecoverable reason, unresolved root cause or integrity/security risk.

## Validation
Negative recovery, unauthorized actor, restart/replay, state/persistence integrity, integration/regression.

## Completion Criteria
Recovery only completes when prerequisites, transition and post-recovery evidence all pass.

## Stop Conditions
Nonrecoverable reason, missing authority, corrupted state, human gate or insufficient evidence.

## Checkpoint
Persist freeze reason, actor, repair proof, transition and validation.

## Resume
Reload authoritative state/incident before further action.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Process restart does not prove a frozen pipeline may continue from prior in-memory state.

## Non-Goals
This Skill does not implement deployment-level recovery; REL-006 is a distinct formal identity.

## Version
1.0.0
