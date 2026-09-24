---
name: nexy-debug
description: Debug NEXY failures by reproducing, observing, evidencing, localizing, testing hypotheses and proving root cause before any fix.
---

# NEXY Skill

## Identity
- Formal ID: `ENG-003`
- Name: `nexy-debug`
- Family: ENGINEERING
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Use the source-specified chain Failure → Reproduce → Observe → Evidence → Localize → Hypothesis → Verify → Root Cause → Fix → Regression, with root cause claimed only when proven.

## Authority
Debugging may inspect and test within authorized scope. Mutation is delegated to an authorized modification path; diagnosis does not itself grant write permission.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Exact runtime/test/repository evidence is required for defect/root-cause claims.

## Scope
### In Scope
- reproduce reported failure;
- collect source/runtime/test evidence;
- localize fault;
- form and falsify hypotheses;
- prove root cause;
- define minimal fix/regression surface.

### Out of Scope
- guessing root cause;
- broad refactor;
- fixing unproven symptoms;
- rewriting tests/spec to fit implementation;
- release approval.

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
- failure_description

### Optional
- reproduction steps
- logs/traces
- failing tests
- prior incidents
- recent diff
- architecture/impact context

## Preconditions
Target revision/environment identity is known enough to reproduce or explicitly classify reproduction as unavailable.

## Outputs
- status
- failure
- reproduction
- observations
- evidence
- localization
- hypotheses
- disproven_hypotheses
- root_cause
- confidence
- impact
- proposed_fix_surface
- regression_surface
- errors
- unknowns
- remaining
- next_action

## Workflow
### Phase 1 — Context
Pin failing target revision/environment.
### Phase 2 — Authority
Confirm inspection/test scope and protected boundaries.
### Phase 3 — Requirement
Identify expected behavior and acceptance.
### Phase 4 — Inspection
Reproduce and collect evidence; inspect relevant source/dependency edges.
### Phase 5 — Execution
Generate multiple plausible hypotheses, prioritize falsification and verify causality.
### Phase 6 — Validation
Reproduce the cause and demonstrate that alternate explanations do not fit the evidence sufficiently.
### Phase 7 — Evidence
Record exact reproduction, observations, source locations and proof chain.

## Required Behavior
- Root cause requires proof, not plausibility.
- Prefer reproducible evidence over logs without context.
- Preserve multiple hypotheses until falsified.
- Distinguish symptom, trigger, contributing factor and root cause.
- Define regression needed to prevent recurrence.

## Forbidden Behavior
- Do not call correlation causation.
- Do not patch before establishing enough causal evidence for safe repair.
- Do not fabricate reproduction.
- Do not ignore contradictory evidence.
- Do not claim fixed without post-fix regression evidence.

## Architecture Constraints
Debugging must include boundary/state/contract ownership when the failure crosses systems.

## Security Constraints
Redact secrets; security failures may require immediate freeze/containment before ordinary debugging.

## Compatibility Constraints
Proposed fix must identify compatibility risk and consumers.

## Data Integrity
If reproduction risks destructive data, use non-destructive evidence/sandbox or require human gate.

## Failure Handling
If reproduction is impossible, return NOT_REPRODUCED/PARTIAL and identify missing environment/evidence; do not invent root cause.

## Freeze Conditions
Critical security/data-integrity risk, destructive reproduction without gate, unknown target revision, evidence contradiction that blocks safe repair.

## Validation
### Structural
Reproduction/observation/hypothesis/root-cause fields are explicit.
### Functional
Root cause is causally supported.
### Security
No unsafe secret/destructive evidence handling.
### Architecture
Cross-boundary failures identify relevant owners/contracts.
### Integration
Output can drive architecture-impact and modify Skills.
### Regression
A concrete regression test/surface is defined when a fix is proposed.
### Evidence
Proof chain is current and reproducible where possible.

## Completion Criteria
Diagnosis complete only when root cause is proven or explicitly remains UNKNOWN with next proof required.

## Stop Conditions
Unsafe reproduction, missing critical target identity, destructive action requires gate, or evidence is insufficient for causal conclusion.

## Checkpoint
Persist reproduction state, observations, hypotheses, falsifications and next proof.

## Resume
Refresh target/environment and re-run the minimal reproduction.

## Error Reporting
Return ERROR, LOCATION, IMPACT, ROOT_CAUSE only if proven, RECOVERY and CURRENT_STATUS.

## Examples
- A failing queue job is not “Redis bug” until queue state, persistence, worker source and reproduction establish the causal mechanism.

## Non-Goals
This Skill does not approve or implement a fix unless separately authorized.

## Version
1.0.0
