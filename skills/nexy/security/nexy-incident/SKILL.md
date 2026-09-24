---
name: nexy-incident
description: Manage NEXY security, system and FREEZE incidents with source-backed severity, cause, impact, containment, recovery, prevention and evidence.
---

# NEXY Skill

## Identity
- Formal ID: `SEC-007`
- Name: `nexy-incident`
- Family: SECURITY
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Manage security, system and freeze incidents.

## Authority
Incident handling can contain/freeze affected paths within established policy but cannot invent root cause or bypass recovery/human gates.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Actual incident/state/audit evidence.

## Scope
### In Scope
Detection, classification, severity, containment, cause/evidence, impact, recovery prerequisites, prevention/regression and audit linkage.
### Out of Scope
Hiding incidents, premature root-cause claim, destructive recovery without gate.

## Inputs
Universal inputs plus incident signal/evidence, affected systems, current state and policy.

## Outputs
Universal outputs plus incident_id, severity, containment, cause status, impact, recovery/prevention/regression and evidence.

## Workflow
Detect → Contain/FREEZE if required → Preserve Evidence → Analyze Cause → Impact → Recovery Gate → Prevention/Regression → Close Evidence.

## Required Behavior
Contain critical risk first; separate proven cause from hypothesis; preserve evidence.

## Forbidden Behavior
No incident deletion/hiding, no false closure, no recovery before prerequisites.

## Architecture Constraints
Link incident to affected boundary/state/owner.

## Security Constraints
Sensitive evidence redacted/access-controlled; breach containment has priority.

## Compatibility Constraints
Recovery/prevention changes require normal change-impact analysis.

## Data Integrity
Preserve incident/audit lineage and affected data integrity evidence.

## Failure Handling
Unresolved critical cause/risk keeps incident open/frozen as required.

## Freeze Conditions
Critical security/integrity incident or unresolved unsafe state.

## Validation
Containment, event/audit, recovery prerequisites and regression prevention.

## Completion Criteria
Incident can close only when status/evidence supports containment and required recovery/prevention; unknowns remain explicit.

## Stop Conditions
Human/security gate required or evidence would be destroyed by next action.

## Checkpoint
Persist sanitized incident state, evidence, containment and next action.

## Resume
Reload incident/current system state before recovery.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Secret exposure requires containment and sanitized evidence before ordinary remediation.

## Non-Goals
This Skill does not suppress operational incidents.

## Version
1.0.0
