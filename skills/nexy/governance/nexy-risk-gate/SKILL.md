---
name: nexy-risk-gate
description: Assess data-loss, security, compatibility, architecture, determinism, and release risks; critical unknown freezes.
---

# NEXY Skill

## Identity
- Formal ID: `GOV-004`
- Name: `nexy-risk-gate`
- Family: GOVERNANCE
- Version: `1.0.0`
- Status: `MATERIALIZED`


## Objective
Assess data-loss, security, compatibility, architecture, determinism, and release risks; critical unknown freezes.

## Authority
Operate only within current authoritative source and task scope. This Skill cannot invent missing requirements, expand permissions, weaken gates, or promote inference into project truth.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Applicable current project source, pinned repository state, tests/evidence and control state.

## Scope
### In Scope
risk inputs across data, security, compatibility, architecture, determinism, operations/release; severity, proof and mitigation/rollback.
### Out of Scope
Optimistic risk scoring without proof, suppressing critical unknowns, treating absence of evidence as safety, or bypassing a required gate.

## Inputs
Universal inputs plus the exact target/requirement/context needed by this Skill, authoritative constraints, dependencies and available evidence.

## Outputs
Universal outputs plus structured findings/result, proof refs, gaps/risks, validation state and next action.

## Workflow
Context → Scope → Hazard Inventory → Evidence → Severity/Impact → Mitigation/Rollback → Gate Decision → Record.

## Required Behavior
Critical unknown or unacceptable proven risk blocks the affected path until resolved or explicitly human-gated.

## Forbidden Behavior
Optimistic risk scoring without proof, suppressing critical unknowns, treating absence of evidence as safety, or bypassing a required gate.

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
Critical risk/unknown cannot be bounded, mitigation is unverified, or required authority is absent.

## Validation
Use structural, source/spec, functional, security, architecture, integration, regression and evidence validation as applicable.

## Completion Criteria
Gate decision is evidence-backed, risk-specific and records residual risk without hiding unknowns.

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
