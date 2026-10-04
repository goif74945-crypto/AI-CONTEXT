# Requirement Traceability Graph

## Problem
Large AI-built systems often pass local tests while violating the original objective because requirements disappear between prompt, plan, code, and verification.

## Graph model
Node types:
R = Requirement
D = Design decision
W = Work unit
A = Artifact
T = Test
E = Evidence
F = Failure/incident

Required edges:
R->D justification
D->W decomposition
W->A production
A->T validation
T->E result
E->R satisfaction
F->R violated requirement
F->T regression test

## Coverage metrics
Requirement Implementation Coverage = RIDs with at least one A / actionable RIDs.
Requirement Verification Coverage = RIDs with passing E / verifiable RIDs.
Negative Coverage = MUST_NOT RIDs with explicit adversarial tests / MUST_NOT RIDs.
Failure Closure = failures linked to regression tests / resolved failures.

Do not collapse these into one vanity percentage. A project can have 100% implementation coverage and 20% verification coverage.

## Orphan detection
Block release when:
- an actionable RID has no work/artifact edge,
- an artifact has no RID,
- a critical RID has no test,
- a test result has no reproducible evidence,
- a resolved failure has no regression guard where recurrence is plausible.

## Change impact
When a RID changes, traverse descendants and invalidate only affected verification. This avoids both extremes: pretending old evidence still proves new behavior, or retesting the universe because one label changed.
