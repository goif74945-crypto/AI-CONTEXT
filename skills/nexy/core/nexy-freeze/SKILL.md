---
name: nexy-freeze
description: Enter, represent and preserve NEXY FREEZE on critical failure, contradiction, insufficient evidence, timeout, policy violation or consensus failure without fabricating recovery.
---

# NEXY Skill

## Identity
- Formal ID: `CORE-004`
- Name: `nexy-freeze`
- Family: CORE
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Manage FREEZE triggered by critical failure, contradiction, insufficient evidence, timeout, policy violation or consensus failure.

## Authority
FREEZE follows current law/state authority. This Skill cannot turn FREEZE into success or authorize recovery without the recovery gate.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current state/freeze/incident/audit implementation at pinned HEAD.

## Scope
### In Scope
Freeze trigger classification, state transition, incident/audit obligations, user/system truth representation, recovery preconditions.
### Out of Scope
Silent retry, auto-unfreeze, fake success, policy bypass.

## Inputs
Universal inputs plus freeze trigger, current state, actor, incident context and evidence.

## Outputs
Universal outputs plus freeze reason, state result, recoverability, incident/audit evidence, blocked paths and next proof.

## Workflow
Context → Authority/Law → Trigger Validation → Freeze Transition → Persist Incident/Audit → Validate Representation → Evidence.

## Required Behavior
FREEZE remains explicit; affected path stops; evidence/incident obligations remain mandatory.

## Forbidden Behavior
No warning-only downgrade of mandatory freeze/audit; no automatic success; no recovery without evidence.

## Architecture Constraints
Freeze crosses LAW/state/incident/audit truth boundaries and must preserve ownership.

## Security Constraints
Security breach/secret exposure may require immediate containment and redaction.

## Compatibility Constraints
Freeze/error contract remains consistent for API/UI/worker consumers.

## Data Integrity
Freeze state/incident must be durable where required; corrupted state remains frozen.

## Failure Handling
If freeze persistence/audit itself fails, surface that failure and remain blocked.

## Freeze Conditions
This Skill is the handler for applicable critical triggers; nested freeze-persistence failure remains explicit.

## Validation
State transition, incident/audit persistence, API/UI truth, recovery denial, restart/replay regression as applicable.

## Completion Criteria
Freeze is authoritative, durable as required, visible and evidence-backed.

## Stop Conditions
Unknown state/authority preventing safe transition or recovery requested without gate.

## Checkpoint
Persist freeze reason/state/incident/evidence.

## Resume
Recovery must route through `nexy-recovery` and fresh authoritative state.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Mandatory audit persistence failure must not be reduced to telemetry warning.

## Non-Goals
This Skill does not approve recovery or release.

## Version
1.0.0
