---
name: nexy-determinism-verify
description: Verify NEXY deterministic obligations and declared exceptions using source-defined semantics and reproducible evidence.
---

# NEXY Skill

## Identity
- Formal ID: `VER-003`
- Name: `nexy-determinism-verify`
- Family: VERIFICATION
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Verify deterministic requirement. Verify NEXY deterministic obligations and declared exceptions using source-defined semantics and reproducible evidence.

## Authority
Verification adjudicates evidence against authoritative requirements; it does not rewrite source, lower acceptance criteria, mutate implementation by default, or convert uncertainty into PASS.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Applicable authoritative project source, pinned repository state, executed tests and current evidence.

## Scope
### In Scope
random/time/env inputs; ordering; concurrency; canonical serialization; state transitions; replay; deterministic output rules; source-authorized exceptions.
### Out of Scope
Declaring deterministic because one run passed, banning allowed randomness outside critical path, or ignoring hidden time/random/env dependencies.

## Inputs
Universal inputs plus exact verification target/version, governing requirements, dependencies, test/evidence records and unresolved findings.

## Outputs
Universal outputs plus gate-by-gate verdicts, proof references, failed/missing conditions, residual risk and next required proof/action.

## Workflow
Context → Determinism Requirement → Critical Path → Static Scan → Replay/Repeat Evidence → Ordering/State Review → Exception Check → Verdict.

## Required Behavior
Separate allowed non-authoritative entropy from critical decision determinism; require repeatability where the source demands it.

## Forbidden Behavior
Declaring deterministic because one run passed, banning allowed randomness outside critical path, or ignoring hidden time/random/env dependencies.

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
Unresolved nondeterministic authority path, unreproducible result, stale target or ambiguous source exception affecting correctness.

## Validation
Validate the verifier itself against positive, negative, stale-evidence, contradiction and incomplete-proof cases; preserve V0–V9 distinctions.

## Completion Criteria
Applicable deterministic properties are proven or explicitly classified with source-backed exceptions and current evidence.

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
