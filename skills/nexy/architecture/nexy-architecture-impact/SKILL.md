---
name: nexy-architecture-impact
description: Determine the architecture impact of a proposed NEXY change across modules, contracts, state, persistence, security, tests, evidence and release while preventing hidden scope expansion.
---

# NEXY Skill

## Identity
- Formal ID: `ARC-004`
- Name: `nexy-architecture-impact`
- Family: ARCHITECTURE
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Report the proven and candidate impact of a proposed NEXY change across affected modules, contracts, state, tests, security and release surfaces before mutation.

## Authority
This Skill analyzes impact within established authority and scope. It cannot authorize a change, expand the allowed change surface, redefine architecture, or convert an indirect dependency into permission to modify it.

## Source of Truth
- Primary skill specification: `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source named by that specification: `NEXY สกิว.pdf`
- Secondary project context named by that specification: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Exact current repository/branch/HEAD evidence is required for current implementation impact.
- Derived dependency/change-impact registries are navigation aids and must be refreshed or verified when revision-sensitive.

## Scope
### In Scope
- compute direct and transitive task-relevant impact;
- identify affected modules/files/symbols, contracts, state/FSM, persistence, events, config, security boundaries, tests, evidence and release gates;
- classify impact certainty;
- detect path, schema, state, migration, dependency and integration collisions;
- produce the minimum safe validation/regression surface.

### Out of Scope
- modifying affected files;
- treating affected scope as authorized write scope;
- inventing hidden dependencies;
- approving migrations, production actions or security-boundary expansion;
- weakening tests because impact is large.

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
- proposed_change

### Optional
- normalized requirements
- allowed_change_surface
- forbidden_change_surface
- architecture_model
- dependency graph
- contracts
- FSM/state records
- persistence map
- events/config
- security/trust boundaries
- implementation map
- test/evidence indices
- release gates
- prior findings/incidents

## Preconditions
- `nexy-context` has pinned target state;
- `nexy-authority` and `nexy-requirement` have resolved the task contract;
- `nexy-scope-guard` has established allowed/forbidden mutation surface;
- `nexy-architecture` provides a current enough architecture model for the affected area;
- exact implementation-sensitive edges are inspected with `nexy-source-inspector` or equivalent evidence.

## Outputs
- status
- objective
- scope
- proposed_change
- direct_impact
- transitive_impact
- affected_modules
- affected_contracts
- affected_state
- affected_persistence
- affected_events
- affected_config
- affected_security
- affected_tests
- affected_evidence
- affected_release_gates
- collisions
- compatibility_risk
- data_integrity_risk
- security_risk
- required_validation
- rollback_considerations
- out_of_scope_impacts
- unknowns
- evidence
- next_action

## Workflow
### Phase 1 — Context
Pin exact target revision and proposed change.

### Phase 2 — Authority
Confirm governing requirement/scope and protected/human-gated boundaries.

### Phase 3 — Requirement
Bind the change to exact acceptance and non-goals.

### Phase 4 — Inspection
Traverse direct dependencies first, then only the transitive closure needed to establish correctness, compatibility, security, persistence and regression impact.

### Phase 5 — Execution
Classify each impact as EXACT, CANDIDATE, UNKNOWN or NOT_APPLICABLE and separate impact from mutation permission.

### Phase 6 — Validation
Check contract consumers/producers, state transitions/owners, persistence/migrations, security boundaries, events/config, test coverage, release evidence and path/resource collision.

### Phase 7 — Evidence
Return a traceable impact package with exact revision/source references.

## Required Behavior
- Distinguish AFFECTED from ALLOWED_TO_CHANGE.
- Include transitive consumers when contract/state semantics change.
- Expand regression scope when evidence proves broader coupling.
- Report candidate impacts as candidates, not facts.
- Preserve explicit forbidden/protected surfaces even if impacted.
- Surface human gates instead of working around them.

## Forbidden Behavior
- Do not edit code.
- Do not automatically add impacted files to allowed scope.
- Do not call an unmapped entity missing after one search.
- Do not infer a migration is safe from schema compatibility alone.
- Do not hide security/release impacts to keep a change small.
- Do not treat tests as optional because implementation appears local.

## Architecture Constraints
- Impact traversal respects declared boundaries and ownership.
- Any architecture-boundary crossing must identify producer, consumer and contract/state authority.
- Cycles or ambiguous dependency ownership that affect correctness remain explicit.

## Security Constraints
- Analyze authn/authz/RBAC, tenant, secret/logging, input/output validation and audit consequences when affected.
- Security-boundary expansion requires the applicable human/authority gate.
- Encountered secrets are redacted and never copied into evidence.

## Compatibility Constraints
- Identify public/internal contract compatibility, event/schema compatibility, state/recovery compatibility and dependency version effects.
- A rename/move is not assumed compatible without consumer proof.

## Data Integrity
- Analyze destructive write, migration, concurrency, atomicity, rollback and recovery effects where applicable.
- Unknown authoritative data owner or irreversible impact is BLOCKED/HUMAN_GATE according to governing policy.

## Failure Handling
Return PARTIAL/BLOCKED when critical impact edges cannot be proven. Keep proven independent impacts and identify exactly what additional evidence is required.

## Freeze Conditions
- unknown critical architecture/security/data impact;
- proposed change crosses forbidden or human-gated scope without authority;
- unresolved contract/state/persistence conflict;
- target HEAD changes before mutation decision;
- safe impact analysis would require invented dependency/mechanism.

## Validation
### Structural
Output covers all applicable impact classes and distinguishes direct/transitive, exact/candidate/unknown and affected/authorized.

### Functional
Known consumers and state/security dependencies are included for representative changes.

### Security
Protected boundaries cannot be silently converted to modifiable scope.

### Integration
Output is consumable by `nexy-code`, `nexy-modify`, `nexy-debug`, `nexy-code-review`, migration, test, verify and release-gate workflows.

### Regression
The required regression set changes when proven dependency/contract/state impact changes.

### Evidence
Every exact impact links to current source/repository evidence and the pinned revision.

## Completion Criteria
Complete when the minimum safe change and validation surface is known, critical indirect impacts are resolved, and all blocked/gated/out-of-scope impacts are explicit.

## Stop Conditions
Stale/unknown target revision, unresolved critical impact, security/data human gate required, protected-scope conflict, or inaccessible critical dependency evidence.

## Checkpoint
Persist target revision, proposed change, exact/candidate impact sets, required tests/evidence, gates and unresolved edges.

## Resume
Refresh target HEAD, architecture model and dependency/contract/state registries; re-evaluate stale impact edges.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Changing an API response schema impacts route, schema producer, UI/API consumers, contract tests, integration tests and release evidence even if only one source file is edited.
- Changing a state transition impacts state owner, guards, persistence/recovery, event/audit records and regression tests; those impacts do not automatically authorize edits to every affected file.

## Non-Goals
This Skill does not perform the mutation, approve release, or replace task-specific security/test verification.

## Version
1.0.0
