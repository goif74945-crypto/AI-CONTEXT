---
name: nexy-authority
description: Determine which NEXY source has authority for a decision and classify authoritative, supporting, historical and unknown evidence without averaging conflicts.
---

# NEXY Skill

## Identity
- Formal ID: `GOV-001`
- Name: `nexy-authority`
- Family: GOVERNANCE
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Determine which source has authority over a NEXY decision and distinguish `AUTHORITATIVE`, `SUPPORTING`, `HISTORICAL`, and `UNKNOWN`.

## Authority
This Skill interprets declared source authority. It cannot create new authority, bypass the current user directive, or use implementation behavior to rewrite normative requirements.

## Source of Truth
- Primary skill specification: `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source named by that specification: `NEXY สกิว.pdf`
- Secondary project context named by that specification: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current repository/runtime evidence is required for implementation-state claims.

## Scope
### In Scope
- classify candidate sources by authority role;
- resolve explicit supersession and scope;
- identify material authority conflicts;
- emit the authoritative source set for the specific decision.

### Out of Scope
- editing requirements to make sources agree;
- implementation mutation;
- choosing a side when authoritative conflict is unresolved;
- treating model confidence as authority.

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
- candidate_sources

### Optional
- supersession records
- conflict registry
- prior decision record

## Preconditions
- `nexy-context` has identified the relevant current sources;
- source identity/provenance is available or marked UNKNOWN.

## Outputs
- status
- authority_decision
- authoritative_sources
- supporting_sources
- historical_sources
- unknown_sources
- conflicts
- evidence
- next_action

## Workflow
### Phase 1 — Context
Load the decision scope and candidate sources from `nexy-context`.

### Phase 2 — Authority
Evaluate explicit current user directive, canonical project law/spec, scoped supersession and source role. Do not average conflicting authority.

### Phase 3 — Requirement
Identify which requirements/claims depend on the authority decision.

### Phase 4 — Inspection
Verify source identity, revision and scope.

### Phase 5 — Execution
Classify each source and produce the decision-specific authority set.

### Phase 6 — Validation
Check that no lower-authority source overrides a higher-authority source and that scope/supersession are respected.

### Phase 7 — Evidence
Record exact source references and conflict/supersession evidence.

## Required Behavior
- Separate normative authority from implementation/runtime evidence.
- Preserve unresolved conflicts.
- Keep authority decisions scoped to the decision being made.

## Forbidden Behavior
- Do not invent authority.
- Do not flatten all source eras into one canon.
- Do not use a successful test to change what the specification requires.
- Do not resolve conflict by majority vote or model preference.

## Architecture Constraints
Authority resolution precedes requirement interpretation when a material conflict exists.

## Security Constraints
Authority cannot be expanded to bypass security/human gates.

## Compatibility Constraints
Preserve source identity and supersession history.

## Data Integrity
Do not rewrite historical source meaning.

## Failure Handling
If source identity/scope/supersession cannot be established, return UNKNOWN or CONFLICT.

## Freeze Conditions
Unresolved authoritative conflict affecting implementation, security, data integrity or release.

## Validation
### Structural
All candidate sources are classified or explicitly UNKNOWN.

### Functional
A lower-authority source cannot override a higher-authority source in test cases.

### Integration
Output can be consumed by requirement, scope, architecture, build and audit Skills.

### Regression
Previously scoped authority decisions remain scoped after new sources are added.

### Evidence
Every authority conclusion has source/supersession proof.

## Completion Criteria
Complete when the task-specific authority set is established without unresolved critical conflict.

## Stop Conditions
Missing critical source identity, unresolved authoritative conflict, security/human-gate bypass attempt.

## Checkpoint
Persist the decision scope, source classifications, conflict IDs and evidence references.

## Resume
Refresh candidate source revisions and supersession state before reuse.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Current user directive may constrain a build, while older vision material remains historical/supporting.
- Runtime evidence answers whether behavior works; it does not redefine normative acceptance.

## Non-Goals
This Skill does not implement code or validate runtime behavior.

## Version
1.0.0
