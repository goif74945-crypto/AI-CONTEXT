---
name: nexy-completion-proof
description: Prove whether a task/system/audit may be declared complete by checking denominator, acceptance, tests, evidence, regression, unresolved risk and writeback.
---

# NEXY Skill

## Identity
- Formal ID: `VER-006`
- Name: `nexy-completion-proof`
- Family: VERIFICATION
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Answer what evidence permits a completion declaration; if it cannot, status is NOT COMPLETE. Prove whether a task/system/audit may be declared complete by checking denominator, acceptance, tests, evidence, regression, unresolved risk and writeback.

## Authority
Verification adjudicates evidence against authoritative requirements; it does not rewrite source, lower acceptance criteria, mutate implementation by default, or convert uncertainty into PASS.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Applicable authoritative project source, pinned repository state, executed tests and current evidence.

## Scope
### In Scope
task acceptance; denominator/coverage; required tests; evidence; regression; blockers/conflicts/unknowns; deliverables; durable records and read-back.
### Out of Scope
Declaring complete from progress, confidence, source presence, partial tests, unverified files, stale evidence or optimistic wording.

## Inputs
Universal inputs plus exact verification target/version, governing requirements, dependencies, test/evidence records and unresolved findings.

## Outputs
Universal outputs plus gate-by-gate verdicts, proof references, failed/missing conditions, residual risk and next required proof/action.

## Workflow
Context → Completion Contract → Denominator/Acceptance → Required Outputs → Tests/Regression → Evidence → Unresolved Items → Writeback → COMPLETE/NOT COMPLETE.

## Required Behavior
Completion is a proof obligation; all required terminal states and evidence must close. Missing proof means NOT COMPLETE/PARTIAL.

## Forbidden Behavior
Declaring complete from progress, confidence, source presence, partial tests, unverified files, stale evidence or optimistic wording.

## Architecture Constraints
Verification follows source authority and real dependency boundaries; it cannot make storage/UI/test presence authoritative over CORE/LAW/spec.

## Security Constraints
Security failures and secret/cross-tenant/privilege risks cannot be waived by verification convenience; human gates remain binding.

## Compatibility Constraints
Compatibility obligations are verified where changes affect contracts, schemas, versions, consumers, persisted state or release interfaces.

## Data Integrity
Evidence and state references must bind to the intended object/version/head/environment and must not be fabricated or silently substituted.

## Failure Handling
A failed/missing/stale required gate yields FAIL/PARTIAL/BLOCKED/UNKNOWN as appropriate; no optimistic fallback.

## Freeze Conditions
Any required item is unknown/unverified, count mismatch, stale evidence, writeback failure, unresolved critical finding or human gate.

## Validation
Validate the verifier itself against positive, negative, stale-evidence, contradiction and incomplete-proof cases; preserve V0–V9 distinctions.

## Completion Criteria
Every required acceptance/coverage/evidence/writeback condition is proven and traceable; otherwise completion is denied.

## Stop Conditions
Authority conflict, missing critical source, unsafe required action, stale target that invalidates proof, human gate or inability to establish the required evidence class.

## Checkpoint
Persist target/version, gates checked, verdicts, evidence refs, unresolved conditions, next proof and resume point.

## Resume
Refresh authoritative source, target HEAD/state and evidence freshness before continuing verification.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A historical PASS tied to another HEAD cannot satisfy a current exact-head release/completion gate.

## Non-Goals
This Skill does not manufacture evidence or self-approve unverified behavior.

## Version
1.0.0
