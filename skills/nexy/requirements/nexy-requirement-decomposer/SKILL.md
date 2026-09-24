---
name: nexy-requirement-decomposer
description: Decompose requirements into functional, technical, security, data, UI, test, and release aspects.
---

# NEXY Skill

## Identity
- Formal ID: `REQ-002`
- Name: `nexy-requirement-decomposer`
- Family: REQUIREMENTS
- Version: `1.0.0`
- Status: `MATERIALIZED`


## Objective
Decompose requirements into functional, technical, security, data, UI, test, and release aspects.

## Authority
Operate only within current authoritative source and task scope. This Skill cannot invent missing requirements, expand permissions, weaken gates, or promote inference into project truth.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Applicable current project source, pinned repository state, tests/evidence and control state.

## Scope
### In Scope
authoritative requirement text, scope/authority, functional behavior, technical constraints, security/data/UI obligations, test/evidence/release needs.
### Out of Scope
Adding requirements not present in source, dropping qualifiers, converting assumptions into obligations, or flattening future/current scope.

## Inputs
Universal inputs plus the exact target/requirement/context needed by this Skill, authoritative constraints, dependencies and available evidence.

## Outputs
Universal outputs plus structured findings/result, proof refs, gaps/risks, validation state and next action.

## Workflow
Source → Authority/Scope → Atomic Clauses → Domain Decomposition → Dependencies/Acceptance → Traceable Requirement Set.

## Required Behavior
Preserve exact semantics and qualifiers; each derived item traces back to authoritative text and scope.

## Forbidden Behavior
Adding requirements not present in source, dropping qualifiers, converting assumptions into obligations, or flattening future/current scope.

## Architecture Constraints
Respect declared layers, contracts, state ownership, dependency direction and source authority; do not create hidden bypasses.

## Security Constraints
Validate applicable trust boundaries, permissions, secret handling and unsafe side effects; fail closed on critical uncertainty.

## Compatibility Constraints
Assess contract/version/consumer/data compatibility when the task can affect them.

## Data Integrity
Preserve authoritative data/state/provenance and do not mutate or reinterpret protected state without explicit authority.

## Failure Handling
Failure, unknown, conflict, missing proof or unavailable dependency remains explicit; no fabricated fallback success.

## Freeze Conditions
Material ambiguity/conflict prevents safe decomposition or would change architecture/obligation.

## Validation
Use structural, source/spec, functional, security, architecture, integration, regression and evidence validation as applicable.

## Completion Criteria
Atomic decomposed requirements cover the source claim without addition, omission or authority drift.

## Stop Conditions
Stale target, material authority/scope conflict, missing critical proof, unsafe mutation, required human gate or unresolved dependency that affects correctness.

## Checkpoint
Persist exact target/version, inputs, claims/proofs, decisions, validation state, unresolved gaps and resume point.

## Resume
Refresh source authority, target state and evidence freshness before continuing.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Presence or naming similarity alone is never sufficient proof of implementation or compliance.

## Non-Goals
This Skill does not self-approve unsupported completion.

## Version
1.0.0
