---
name: nexy-refactor
description: Refactor NEXY only when scope permits, preserving behavior, APIs, contracts, state semantics, security, tests and compatibility with regression evidence.
---

# NEXY Skill

## Identity
- Formal ID: `ENG-004`
- Name: `nexy-refactor`
- Family: ENGINEERING
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Improve internal structure only when explicitly in scope while preserving externally relevant behavior and all required compatibility/security/state semantics.

## Authority
Refactor is mutation and requires explicit scope. “Cleanup” or maintainability preference is not authorization.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current behavior/contracts/tests are revision-bound evidence.

## Scope
### In Scope
- explicitly authorized structural cleanup;
- behavior-preserving decomposition/renaming/movement when compatibility is proven;
- test/evidence needed to prove preservation.

### Out of Scope
- feature changes;
- architecture redesign;
- contract/state semantics changes;
- opportunistic dependency changes;
- unrequested rename/delete.

## Inputs
### Required
- task
- authority
- scope
- repository
- branch
- head
- source_of_truth
- constraints
- expected_output
- validation_requirements
- refactor_objective
- allowed_change_surface

### Optional
- behavior baseline
- contracts
- architecture-impact output
- tests
- performance baseline

## Preconditions
Explicit refactor authority; pinned target; known behavior/contract surface.

## Outputs
- status
- objective
- scope
- baseline_behavior
- changed_files
- diff
- architecture_impact
- compatibility_check
- tests
- regression
- evidence
- errors
- unknowns
- rollback
- next_action

## Workflow
### Phase 1 — Context
Capture target and baseline.
### Phase 2 — Authority
Confirm refactor itself is in scope.
### Phase 3 — Requirement
Define invariants that must not change.
### Phase 4 — Inspection
Inspect consumers/contracts/state/security/tests.
### Phase 5 — Execution
Apply minimal structural change.
### Phase 6 — Validation
Compare behavior/contracts/state/security/performance where applicable and run regression.
### Phase 7 — Evidence
Record before/after diff and preservation proof.

## Required Behavior
- Preserve behavior/API/contracts/state/security/tests/compatibility.
- Detect semantic drift, not just compile success.
- Keep rename/move traceability.
- Roll back if preservation cannot be proven.

## Forbidden Behavior
- Do not mix feature work into refactor.
- Do not delete tests because internals changed.
- Do not weaken contracts.
- Do not use refactor to bypass scope/architecture gates.

## Architecture Constraints
No boundary redesign without separate architecture authority.

## Security Constraints
Security posture must not be weakened; auth/RBAC/secret/audit paths require regression when touched.

## Compatibility Constraints
All relevant consumers must remain compatible or the task becomes a contract change, not a refactor.

## Data Integrity
State/persistence semantics must remain unchanged unless explicitly authorized otherwise.

## Failure Handling
Any unplanned semantic change = FAIL/PARTIAL; restore or split into a separately authorized change.

## Freeze Conditions
Unknown baseline, hidden contract/state/security change, scope expansion, destructive migration, or inability to prove preservation.

## Validation
Structural, functional, architecture, security, integration, regression and evidence checks are required as applicable.

## Completion Criteria
Refactor complete only when preservation is demonstrated and required regression passes.

## Stop Conditions
Scope does not authorize refactor, semantic drift appears, critical baseline unknown, or human gate required.

## Checkpoint
Persist baseline, invariants, diff, regression and rollback.

## Resume
Refresh target and compare partial change against baseline.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Moving a helper is acceptable only if imports/consumers and behavior remain proven compatible.

## Non-Goals
This Skill does not change product behavior or requirements.

## Version
1.0.0
