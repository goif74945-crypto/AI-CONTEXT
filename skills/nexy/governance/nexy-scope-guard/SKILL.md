---
name: nexy-scope-guard
description: Enforce NEXY task scope and stop feature creep, unrelated refactors, unauthorized rename/delete, architecture changes and dependency additions.
---

# NEXY Skill

## Identity
- Formal ID: `GOV-002`
- Name: `nexy-scope-guard`
- Family: GOVERNANCE
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Prevent feature creep, out-of-scope refactor, rename/delete, architecture change, and unauthorized dependency additions.

## Authority
This Skill enforces authorized scope. It cannot broaden scope or approve a protected/human-gated mutation.

## Source of Truth
- Primary skill specification: `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source named by that specification: `NEXY สกิว.pdf`
- Secondary project context named by that specification: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current repository/runtime evidence is required for implementation-state claims.

## Scope
### In Scope
- compare proposed/read/write/test actions against authorized and protected scope;
- classify action as ALLOWED, FORBIDDEN, HUMAN_GATE, or UNKNOWN;
- detect ancestor/descendant path expansion and indirect dependency impact.

### Out of Scope
- generating new product requirements;
- overriding explicit user/canonical restrictions;
- executing mutations.

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
- proposed_actions
- allowed_scope
- forbidden_scope

### Optional
- change-impact set
- dependency closure
- human-gate policy

## Preconditions
- `nexy-context`, `nexy-authority`, and `nexy-requirement` outputs are current enough for the decision.

## Outputs
- status
- action_classification
- violations
- required_gates
- allowed_actions
- blocked_actions
- evidence
- next_action

## Workflow
### Phase 1 — Context
Load exact target and proposed actions.

### Phase 2 — Authority
Confirm the scope source and any protected/human-gated boundary.

### Phase 3 — Requirement
Bind allowed and forbidden surfaces to the task contract.

### Phase 4 — Inspection
Expand path/dependency impact enough to detect indirect scope escape.

### Phase 5 — Execution
Classify every proposed action before mutation.

### Phase 6 — Validation
Check for hidden rename/delete, dependency addition, unrelated refactor, architecture expansion and protected operations.

### Phase 7 — Evidence
Return exact action/path and governing scope rule.

## Required Behavior
- Default critical unresolved scope to BLOCKED/FREEZE.
- Require explicit authorization for expansion.
- Preserve allowed work when an unrelated path is blocked.

## Forbidden Behavior
- Do not treat adjacency as authorization.
- Do not approve destructive/human-gated work by implication.
- Do not hide out-of-scope files inside a larger patch.

## Architecture Constraints
Architecture changes require explicit task authority and impact analysis.

## Security Constraints
Security authority expansion, secrets, production, irreversible data, branch rewrite and cross-tenant operations remain human-gated when specified by current policy.

## Compatibility Constraints
Scope enforcement must preserve existing contracts and protected surfaces.

## Data Integrity
Deletion/migration/data mutation outside explicit scope is blocked.

## Failure Handling
Report the exact violating action/path and the authority needed to proceed.

## Freeze Conditions
Critical scope ambiguity, protected operation without gate, unauthorized architecture/data/security expansion.

## Validation
### Structural
All proposed actions are classified.

### Functional
Known out-of-scope action is blocked; in-scope action is not blocked merely because another action fails.

### Integration
Can gate Builder plans and Auditor command generation.

### Regression
New path patterns cannot weaken existing protected-scope checks.

### Evidence
Each classification identifies the scope rule and affected action.

## Completion Criteria
Complete when every proposed action is either permitted, blocked, human-gated or explicitly UNKNOWN.

## Stop Conditions
Required authorization absent; ambiguity materially affects mutation safety.

## Checkpoint
Persist scope decision and blocked/gated actions for handoff.

## Resume
Refresh task scope and target HEAD before reusing a previous classification.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A command authorizes three test files: editing a production deployment file is FORBIDDEN.
- A destructive migration request without the human gate is HUMAN_GATE/BLOCKED.

## Non-Goals
This Skill does not create or execute code changes.

## Version
1.0.0
