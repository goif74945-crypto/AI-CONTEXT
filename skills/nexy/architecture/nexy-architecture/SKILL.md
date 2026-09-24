---
name: nexy-architecture
description: Inspect and model the actual NEXY architecture at a pinned revision, preserving declared boundaries, contracts, state ownership, security and deployment context without inventing missing architecture.
---

# NEXY Skill

## Identity
- Formal ID: `ARC-001`
- Name: `nexy-architecture`
- Family: ARCHITECTURE
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Understand the actual NEXY architecture relevant to the task, including applicable core-kernel, packages, apps, contracts, auth, API, web, tests, state/persistence, security and deployment surfaces, without treating design intent as implementation proof.

## Authority
This Skill models architecture from authoritative source plus exact repository/runtime evidence. It cannot redefine product law, broaden task scope, approve protected mutations, or turn a candidate mapping into an architectural fact.

## Source of Truth
- Primary skill specification: `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source named by that specification: `NEXY สกิว.pdf`
- Secondary project context named by that specification: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current architecture/state claims require exact repository/branch/HEAD evidence.
- AI-CONTEXT architecture, ontology, contracts, state, security and implementation maps are navigation/derived evidence unless independently bound to current truth.

## Scope
### In Scope
- identify architecture layers, modules, services, packages, apps and boundaries relevant to the task;
- map declared dependencies, contracts, state owners, data stores, security boundaries and integration edges;
- distinguish source-required, implementation-observed, candidate, historical, future and unknown architecture;
- identify architecture constraints that downstream engineering must preserve;
- surface conflicts, missing mappings and stale architectural evidence.

### Out of Scope
- changing architecture;
- inventing modules, services, providers, boundaries or dependencies;
- implementation mutation;
- approving dependency additions;
- declaring runtime/deployment correctness from static structure alone.

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

### Optional
- requirement IDs
- architecture/source registries
- ontology/dependency graph
- contracts
- FSM/state ownership
- security/trust-boundary records
- implementation map
- source-inspector output
- current tests/evidence
- deployment/release context

## Preconditions
- `nexy-context` has pinned the current target and loaded relevant context;
- `nexy-authority` has resolved material authority questions;
- `nexy-requirement` has normalized the task contract;
- `nexy-scope-guard` has established the authorized surface when the architecture result will drive mutation;
- repository-sensitive claims use `nexy-source-inspector` or equivalent exact evidence.

## Outputs
- status
- objective
- scope
- architecture_model
- layers
- modules
- boundaries
- dependencies
- contracts
- state_owners
- persistence
- security_boundaries
- integration_edges
- implementation_evidence
- source_evidence
- conflicts
- unknowns
- constraints
- validation
- evidence
- next_action

## Workflow
### Phase 1 — Context
Pin repository, branch and HEAD; load only task-relevant architecture context.

### Phase 2 — Authority
Separate normative architecture requirements from historical/future design and implementation observations.

### Phase 3 — Requirement
Bind architecture questions to explicit requirements, contracts, invariants and scope.

### Phase 4 — Inspection
Inspect exact task-relevant files/symbols plus required dependency, caller/callee, state, contract and security edges. Use alternate searches before concluding a component is missing.

### Phase 5 — Execution
Build a scoped architecture model using explicit certainty labels such as SOURCE_REQUIRED, IMPLEMENTATION_OBSERVED, CANDIDATE, HISTORICAL, FUTURE, CONFLICT and UNKNOWN.

### Phase 6 — Validation
Check boundary consistency, dependency direction, contract ownership, state ownership, security boundaries, persistence authority and revision freshness.

### Phase 7 — Evidence
Record WHAT → WHERE → HOW → RESULT → EVIDENCE for each material architecture conclusion.

## Required Behavior
- Pin exact HEAD for implementation claims.
- Preserve distinction between source architecture and implemented architecture.
- Trace architecture-critical claims to exact source or repository evidence.
- Keep candidate/unmapped relations explicit.
- Detect architecture conflicts before downstream mutation planning.
- Report only the architecture surface needed for the current task unless full-system architecture is explicitly required.

## Forbidden Behavior
- Do not infer correctness from file/folder presence.
- Do not invent missing providers, components or integration paths.
- Do not use stale repository maps as current-head proof.
- Do not flatten multiple FSM/state domains into one global machine without source authority.
- Do not treat future design as a current-build defect.
- Do not mutate implementation.

## Architecture Constraints
- Preserve declared module/layer boundaries.
- Preserve legal dependency direction.
- Preserve contract producer/consumer boundaries.
- Preserve state ownership and authoritative persistence boundaries.
- Cross-boundary calls must be explicit and traceable.

## Security Constraints
- Include relevant trust boundaries, authn/authz/RBAC, secret handling, tenant boundaries and audit requirements.
- A security boundary must not be widened by architecture inference.
- Secret or credential discovery must be redacted and must not be propagated as evidence content.

## Compatibility Constraints
- Preserve externally consumed contracts, state/event semantics and public interfaces unless explicit authority allows change.
- Distinguish moves/renames from deletion or absence.
- Architecture claims become stale when the pinned HEAD or applicable source revision changes.

## Data Integrity
- State/persistence ownership must be explicit for authoritative data.
- Unknown ownership or destructive data path affecting planned mutation is BLOCKED until resolved.

## Failure Handling
Return PARTIAL/UNKNOWN when required architecture evidence is inaccessible, conflicting or unmapped. Identify the blocked subpath while preserving independent proven architecture facts.

## Freeze Conditions
- unresolved authoritative architecture conflict affecting implementation;
- unknown critical state owner/persistence boundary;
- unresolved security boundary on a proposed mutation path;
- target HEAD unknown or changed for revision-sensitive mutation planning;
- required architecture proof would require inventing a mechanism.

## Validation
### Structural
Architecture output includes target revision, scope, layers/boundaries, dependencies, contracts/state/security where applicable, unknowns and evidence.

### Functional
Each claimed implemented component/boundary resolves to exact source or repository evidence at the pinned revision.

### Security
Relevant trust/security boundaries are represented and no boundary expansion is silently approved.

### Integration
Output is consumable by `nexy-architecture-impact`, engineering, web/API, core, security, test and verification Skills.

### Regression
HEAD/source changes invalidate revision-sensitive architecture facts until refreshed.

### Evidence
Each material conclusion records exact source/path/symbol/registry references and certainty class.

## Completion Criteria
Complete when the task-relevant architecture is sufficiently modeled to support the next authorized action, all critical boundaries are explicit, and unresolved critical architecture uncertainty is absent.

## Stop Conditions
Unknown target revision, inaccessible critical source, unresolved authoritative architecture conflict, critical state/security boundary unknown, or requested action requires architecture invention.

## Checkpoint
Persist target revision, scoped architecture model, evidence references, conflicts, unknowns and next architecture edge.

## Resume
Refresh repository/branch/HEAD and applicable source revision; revalidate stale architecture facts before reuse.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Before changing an API route, model UI/API/schema/auth/core/state/test edges and identify which boundary owns validation and persistence.
- Before changing queue behavior, identify producer/consumer contract, job state owner, persistence, retry/recovery and observability boundaries.

## Non-Goals
This Skill does not implement architecture changes, run deployment, or prove runtime correctness by itself.

## Version
1.0.0
