---
name: nexy-consensus-verify
description: Verify that a NEXY consensus outcome satisfies its governing evidence, quorum, adversarial and release preconditions without equating agreement count with truth.
---

# NEXY Skill

## Identity
- Formal ID: `VER-004`
- Name: `nexy-consensus-verify`
- Family: VERIFICATION
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Verify consensus result. Verify that a NEXY consensus outcome satisfies its governing evidence, quorum, adversarial and release preconditions without equating agreement count with truth.

## Authority
Verification adjudicates evidence against authoritative requirements; it does not rewrite source, lower acceptance criteria, mutate implementation by default, or convert uncertainty into PASS.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Applicable authoritative project source, pinned repository state, executed tests and current evidence.

## Scope
### In Scope
agent outputs; evidence; quorum/threshold; adversarial checks; contradictions; deterministic merge/release rules; consensus contract and final status.
### Out of Scope
Majority-only approval when source requires more, hiding dissent/contradiction, averaging forbidden outputs, or self-declaring consensus without evidence.

## Inputs
Universal inputs plus exact verification target/version, governing requirements, dependencies, test/evidence records and unresolved findings.

## Outputs
Universal outputs plus gate-by-gate verdicts, proof references, failed/missing conditions, residual risk and next required proof/action.

## Workflow
Context → Consensus Contract → Inputs/Evidence → Quorum/Threshold → Adversarial/Contradiction → Merge/Decision Rule → Evidence → Verdict.

## Required Behavior
Consensus must satisfy the exact source-defined acceptance law and preserve unresolved contradiction as explicit failure/freeze where required.

## Forbidden Behavior
Majority-only approval when source requires more, hiding dissent/contradiction, averaging forbidden outputs, or self-declaring consensus without evidence.

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
Missing critical evidence, quorum rule unavailable, contradictory authoritative outputs unresolved, or consensus would bypass LAW/JUDGE gates.

## Validation
Validate the verifier itself against positive, negative, stale-evidence, contradiction and incomplete-proof cases; preserve V0–V9 distinctions.

## Completion Criteria
Consensus result is contract-compliant, evidence-backed and valid for the exact run/version under review.

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
