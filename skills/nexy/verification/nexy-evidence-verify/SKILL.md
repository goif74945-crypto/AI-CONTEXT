---
name: nexy-evidence-verify
description: Validate NEXY evidence provenance, freshness, binding, integrity and claim fit before it can support a verdict.
---

# NEXY Skill

## Identity
- Formal ID: `VER-002`
- Name: `nexy-evidence-verify`
- Family: VERIFICATION
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Verify evidence itself, not merely file existence. Validate NEXY evidence provenance, freshness, binding, integrity and claim fit before it can support a verdict.

## Authority
Verification adjudicates evidence against authoritative requirements; it does not rewrite source, lower acceptance criteria, mutate implementation by default, or convert uncertainty into PASS.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Applicable authoritative project source, pinned repository state, executed tests and current evidence.

## Scope
### In Scope
source/provenance; repository/branch/HEAD/environment binding; execution identity; result; integrity/hash when available; claim-to-proof relevance; staleness and contradictions.
### Out of Scope
Counting a file, screenshot, test source or historical PASS as current proof without exact binding; fabricated hash; unsupported evidence class.

## Inputs
Universal inputs plus exact verification target/version, governing requirements, dependencies, test/evidence records and unresolved findings.

## Outputs
Universal outputs plus gate-by-gate verdicts, proof references, failed/missing conditions, residual risk and next required proof/action.

## Workflow
Context → Claim → Required Evidence Class → Inspect Provenance/Binding → Integrity/Freshness → Relevance → Contradiction Search → Classify.

## Required Behavior
Evidence is classified VERIFIED, UNVERIFIED, CONTRADICTED or UNKNOWN according to real proof, not presentation quality.

## Forbidden Behavior
Counting a file, screenshot, test source or historical PASS as current proof without exact binding; fabricated hash; unsupported evidence class.

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
Critical evidence cannot be sourced/bound, evidence contradicts authoritative state, secret-sensitive proof cannot be safely handled.

## Validation
Validate the verifier itself against positive, negative, stale-evidence, contradiction and incomplete-proof cases; preserve V0–V9 distinctions.

## Completion Criteria
Evidence classification is reproducible, claim-specific and bound to the correct target/version/environment.

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
