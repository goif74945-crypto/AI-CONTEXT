# Design Specification

## Authority label
Everything in this directory is `PROPOSAL_BY_AI` unless explicitly marked as executed evidence. It must never override current user directives, NEXY authoritative specifications, repository truth, sealed evidence, or runtime/deployment proof.

## Objective
Create five orthogonal mechanisms that improve deterministic control, epistemic integrity, adoption safety, evidence freshness and human-facing friction control while remaining external to the protected NEXY.AI repository.

## Immutable requirements
- No mutation to a repository whose name contains `NEXY.AI`.
- No hidden I/O in engine logic.
- Deterministic ordering and canonical JSON fingerprints.
- FREEZE must dominate a local PASS in composition.
- Missing critical authority/evidence/rollback must not silently pass.
- Proposal status must be explicit.
- Negative paths must be executable tests.

## Engine contracts

### ILC
Inputs: objective, authorized/protected scope, invariants, evidence requirements, stop conditions, authority sources, known conflicts.  
Output: compiled contract + findings + deterministic verdict.  
Failure semantics: empty authority, empty evidence, scope collision, unresolved authority conflict => FREEZE.

### CAG
Inputs: proposal benefit, failure scenarios, invariant preservation, rollback, evidence plan, risk budget.  
Output: residual-risk trace and adoption verdict.  
Failure semantics: broken invariant, absent rollback/evidence plan, or over-budget residual risk => FREEZE.

### CDL
Inputs: typed epistemic debt items.  
Output: weighted debt total and release health.  
Failure semantics: explicit release blocker or exhausted debt budget => FREEZE.

### PHS
Inputs: proof nodes, dependency edges, evidence class, freshness budget, observed drift.  
Output: deterministic revalidation plan.  
Failure semantics: invalidated critical E4-E7 proof => FREEZE; lower-class proof invalidation => REVIEW.

### HTBG
Inputs: uncertainty, irreversibility, impact, evidence strength, user effort, scope clarity.  
Output: EXECUTE / EXECUTE_WITH_EXPLANATION / REQUIRE_CONFIRMATION / FREEZE.  
Failure semantics: unclear scope, weak evidence on high-impact action, or extreme aggregate risk => FREEZE.

## Why the combination is stronger than each part
ILC prevents ambiguous work from becoming execution. CAG blocks attractive but fragile features. CDL prevents unverified shortcuts from accumulating invisibly. PHS prevents old proof from surviving relevant change. HTBG prevents the safe system from becoming unusably ceremonial. The suite composes them with a conservative dominance rule: FREEZE > FAIL > REVIEW > PASS.

## Integration boundaries
This package exposes pure Python objects today. A production integration should add a schema-versioned JSON adapter, signed/provenance-tagged evidence references, exact NEXY authority mapping and NEXY-owned acceptance thresholds. Those items are intentionally not claimed here because current canonical integration contracts were not modified or runtime-tested.
