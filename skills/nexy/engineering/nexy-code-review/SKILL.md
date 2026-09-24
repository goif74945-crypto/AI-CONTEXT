---
name: nexy-code-review
description: Review NEXY code for correctness, architecture, security, performance, maintainability, tests and scope using evidence-bound findings without mutating source.
---

# NEXY Skill

## Identity
- Formal ID: `ENG-005`
- Name: `nexy-code-review`
- Family: ENGINEERING
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Review correctness, architecture, security, performance, maintainability, tests and scope and produce evidence-backed findings without equating style preference with defect.

## Authority
Read/review authority does not grant mutation or release approval.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Exact source and applicable specification/contract/test evidence govern findings.

## Scope
### In Scope
- review requested diff/files/system;
- verify requirements/contracts/state/security/scope alignment;
- identify defects, test gaps and maintainability/performance risks supported by evidence.

### Out of Scope
- mutation;
- arbitrary stylistic rewrites;
- release verdict outside required gate;
- unbounded full-project review unless requested.

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
- review_target

### Optional
- diff
- requirements/contracts
- architecture/impact
- tests/results
- performance/security evidence

## Preconditions
Pinned review revision/diff and governing requirements are available or explicitly UNKNOWN.

## Outputs
- status
- review_scope
- findings
- severity
- source
- claim
- proof
- affected_requirements
- architecture_impact
- security_impact
- performance_impact
- test_gaps
- scope_violations
- unknowns
- validation
- evidence
- next_action

## Workflow
Context → Authority → Requirement → Inspect → Adversarial Review → Validate Findings → Evidence.

## Required Behavior
- Review correctness before style.
- Distinguish proven defect, risk, suggestion and unknown.
- Consider architecture/security/performance/maintainability/tests/scope.
- Validate findings against exact code and source requirements.

## Forbidden Behavior
- Do not invent bugs.
- Do not mark preference as correctness defect.
- Do not accept passing tests as complete proof.
- Do not review stale diff as current.
- Do not mutate.

## Architecture Constraints
Flag illegal dependency/boundary/state ownership changes.

## Security Constraints
Review auth/authz/input/secret/logging/tenant/audit implications where applicable.

## Compatibility Constraints
Review API/schema/event/state/dependency compatibility.

## Data Integrity
Review persistence/migration/concurrency risks when relevant.

## Failure Handling
If required context is missing, narrow verdict to NOT_VERIFIED/PARTIAL and identify missing evidence.

## Freeze Conditions
Critical security/data issue, authority/scope conflict or stale/unknown target that prevents a safe review conclusion.

## Validation
Findings must be reproducible from source/evidence; severity and scope must match demonstrated impact.

## Completion Criteria
Review complete when requested surface is covered and every material finding has proof or is explicitly labeled risk/unknown.

## Stop Conditions
Target unavailable, critical authority conflict, or requested conclusion requires unavailable evidence.

## Checkpoint
Persist review target revision, findings, proof gaps and next review edge.

## Resume
Refresh diff/HEAD and invalidate stale findings as needed.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A source file using an allowed clock is not a determinism defect unless the governing requirement forbids that usage.

## Non-Goals
This Skill does not edit, merge, deploy or release code.

## Version
1.0.0
