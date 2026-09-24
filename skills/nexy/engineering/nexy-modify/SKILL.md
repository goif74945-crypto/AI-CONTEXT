---
name: nexy-modify
description: Modify existing NEXY code through inspect, understand, impact, plan, modify, compile, test, diff and evidence gates with strict scope control.
---

# NEXY Skill

## Identity
- Formal ID: `ENG-002`
- Name: `nexy-modify`
- Family: ENGINEERING
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Perform controlled existing-code modification using the required sequence: Inspect → Understand → Impact → Plan → Modify → Compile → Test → Diff → Evidence.

## Authority
Modification requires explicit task authorization and remains bounded by authority, scope, protected surfaces and human gates.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Exact current repository/branch/HEAD is authoritative for implementation state.

## Scope
### In Scope
- authorized repair/change of existing code;
- source inspection and architecture impact;
- minimal coherent patch;
- required compile/test/regression/security validation;
- diff/evidence/rollback.

### Out of Scope
- feature expansion;
- unrelated cleanup;
- opportunistic refactor;
- contract/architecture changes not authorized;
- self-approval of completion/release.

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
- normalized_requirement
- allowed_change_surface
- forbidden_change_surface

### Optional
- finding/root-cause evidence
- architecture model
- architecture-impact output
- tests/evidence baseline
- rollback instructions

## Preconditions
- `nexy-context`, `nexy-authority`, `nexy-scope-guard`, `nexy-architecture` are current enough;
- applicable `nexy-test` capability is available before completion can be claimed;
- exact target revision is pinned.

## Outputs
- status
- objective
- scope
- inputs
- actions
- changed_files
- unchanged_files
- diff
- impact
- tests
- validation
- evidence
- errors
- unknowns
- remaining
- rollback
- next_action

## Workflow
### Phase 1 — Context
Inspect exact target and current behavior.
### Phase 2 — Authority
Verify mutation permission and protected scope.
### Phase 3 — Requirement
Bind change to acceptance/non-goals.
### Phase 4 — Inspection
Understand source, callers/callees, contracts, state, security and tests.
### Phase 5 — Execution
Plan then apply the smallest coherent patch.
### Phase 6 — Validation
Compile/typecheck/build and run applicable focused, negative, integration and regression tests.
### Phase 7 — Evidence
Record START_HEAD/END_HEAD, diff, changed files, commands/results and rollback.

## Required Behavior
- Never modify before inspection and impact analysis.
- Preserve unrelated behavior.
- Keep changes inside allowed surface.
- Stop if actual root cause contradicts the authorized change.
- Test actual changed behavior, not only nearby helpers.

## Forbidden Behavior
- Do not weaken assertions/specification.
- Do not swallow errors to pass tests.
- Do not introduce placeholders/TODO as completion.
- Do not make hidden migrations/dependency changes.
- Do not self-approve release.

## Architecture Constraints
Respect current boundaries and use `nexy-architecture-impact` for nontrivial cross-system impact.

## Security Constraints
Preserve or strengthen security; any security-boundary expansion requires authority/human gate.

## Compatibility Constraints
Preserve public/internal contracts and state/event semantics unless explicitly authorized to change them.

## Data Integrity
Persistent changes require known owner, migration/rollback and recovery semantics as applicable.

## Failure Handling
Return PARTIAL/FAILED with exact failing validation and leave completion false.

## Freeze Conditions
Stale HEAD, out-of-scope path, critical architecture/security/data unknown, destructive/human-gated requirement, test/spec weakening required.

## Validation
### Structural
Diff is confined to authorized surface.
### Functional
Acceptance behavior proven by execution.
### Security
Applicable negative/security checks pass.
### Architecture
No unintended boundary change.
### Integration
Affected consumers remain valid.
### Regression
Affected regression suite passes.
### Evidence
Diff/test/log evidence is exact and current-head bound.

## Completion Criteria
Patch + required tests + regression + evidence + rollback are complete with no critical unknown.

## Stop Conditions
Any forbidden-scope requirement, stale head, unsupported root cause, missing critical dependency/test capability, or human gate.

## Checkpoint
Persist inspected revision, root cause, impact, patch state, validation state and rollback.

## Resume
Refresh HEAD and revalidate whether the partial patch remains applicable.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE, RECOVERY and CURRENT_STATUS.

## Examples
- Repair a proven auth logging defect within the exact allowed source/test files, then run focused negative/security/regression checks.

## Non-Goals
This Skill does not choose requirements, widen scope or approve release.

## Version
1.0.0
