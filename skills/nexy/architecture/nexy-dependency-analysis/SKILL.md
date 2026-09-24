---
name: nexy-dependency-analysis
description: Analyze direct/transitive dependencies, cycles, API compatibility, build impact, and test impact.
---

# NEXY Skill

## Identity
- Formal ID: `ARC-003`
- Name: `nexy-dependency-analysis`
- Family: ARCHITECTURE
- Version: `1.0.0`
- Status: `MATERIALIZED`


## Objective
Analyze direct/transitive dependencies, cycles, API compatibility, build impact, and test impact.

## Authority
Operate only within current authoritative source and task scope. This Skill cannot invent missing requirements, expand permissions, weaken gates, or promote inference into project truth.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Applicable current project source, pinned repository state, tests/evidence and control state.

## Scope
### In Scope
dependency graph, direct/transitive edges, versions, cycles, consumers/producers, build/test/change impact.
### Out of Scope
Analyzing filename proximity only, ignoring transitive impact, inventing dependencies, or approving incompatible version drift.

## Inputs
Universal inputs plus the exact target/requirement/context needed by this Skill, authoritative constraints, dependencies and available evidence.

## Outputs
Universal outputs plus structured findings/result, proof refs, gaps/risks, validation state and next action.

## Workflow
Context → Dependency Sources → Direct Graph → Transitive Closure → Cycle/Compatibility → Change/Test Impact → Evidence.

## Required Behavior
Dependency conclusions distinguish verified edges from inferred candidates and expose cycles/compatibility risks.

## Forbidden Behavior
Analyzing filename proximity only, ignoring transitive impact, inventing dependencies, or approving incompatible version drift.

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
Critical dependency/consumer cannot be established or unresolved cycle/compatibility conflict blocks safe change.

## Validation
Use structural, source/spec, functional, security, architecture, integration, regression and evidence validation as applicable.

## Completion Criteria
Dependency closure and impact are sufficient and traceable for the requested decision/change.

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
