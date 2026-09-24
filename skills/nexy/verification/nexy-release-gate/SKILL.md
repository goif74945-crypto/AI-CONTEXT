---
name: nexy-release-gate
description: Decide whether a NEXY build may advance through release gates using current implementation/test/security/evidence state without performing deployment itself unless separately authorized.
---

# NEXY Skill

## Identity
- Formal ID: `VER-005`
- Name: `nexy-release-gate`
- Family: VERIFICATION
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Gate release. Decide whether a NEXY build may advance through release gates using current implementation/test/security/evidence state without performing deployment itself unless separately authorized.

## Authority
Verification adjudicates evidence against authoritative requirements; it does not rewrite source, lower acceptance criteria, mutate implementation by default, or convert uncertainty into PASS.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Applicable authoritative project source, pinned repository state, executed tests and current evidence.

## Scope
### In Scope
build state; tests; security; determinism; DOC-E/evidence freshness; release policy; staging/canary/prod prerequisites; rollback and human gates.
### Out of Scope
Approving deployment on stale evidence, bypassing failed tests/security, ignoring rollback/human gate, or treating build PASS as release readiness.

## Inputs
Universal inputs plus exact verification target/version, governing requirements, dependencies, test/evidence records and unresolved findings.

## Outputs
Universal outputs plus gate-by-gate verdicts, proof references, failed/missing conditions, residual risk and next required proof/action.

## Workflow
Context → Target/Release Stage → Required Gates → Test/Security/Determinism → Evidence/DOC-E → Rollback/Human Gate → Release Policy → ALLOW/BLOCK.

## Required Behavior
Fail closed: any mandatory failed/missing/stale gate blocks promotion; release decision is bound to exact target and environment.

## Forbidden Behavior
Approving deployment on stale evidence, bypassing failed tests/security, ignoring rollback/human gate, or treating build PASS as release readiness.

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
Production/destructive/human-gated operation without approval, stale release evidence, unresolved S4/S5 issue or absent rollback where mandatory.

## Validation
Validate the verifier itself against positive, negative, stale-evidence, contradiction and incomplete-proof cases; preserve V0–V9 distinctions.

## Completion Criteria
All mandatory release gates are current and satisfied for the exact target/stage, with rollback and approvals present where required.

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
