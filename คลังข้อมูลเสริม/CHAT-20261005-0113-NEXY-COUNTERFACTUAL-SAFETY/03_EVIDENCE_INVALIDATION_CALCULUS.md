# Evidence Invalidation Calculus

Status: AI-PROPOSED CONCEPT — NOT CURRENT NEXY REQUIREMENT

## Problem
Evidence is revision-sensitive. A PASS against revision A is not automatically proof for revision B.

## Evidence tuple
E = (claim, target, target_hash, environment, class, procedure_hash, dependencies, result, timestamp)

## Invalidation predicates
Evidence becomes STALE when any material predicate is true:
- target_hash changed in a claim-relevant region;
- test/procedure semantics changed;
- environment changed materially;
- dependency changed across an unproven compatibility boundary;
- authority changed the claim itself;
- evidence exceeded an explicit freshness window;
- provenance can no longer be resolved.

Evidence becomes INVALID when:
- artifact identity cannot be established;
- procedure was not actually executed;
- result provenance is broken;
- target differs from claimed target;
- evidence class cannot prove the claim.

## Reuse rule
Reuse is allowed only when a machine-checkable non-impact proof exists or when the claim is independent of the changed dimension by contract.

## Invalidation levels
I0 NONE: proven unaffected.
I1 REVIEW: informational change, human/machine review required.
I2 RECHECK_STATIC: rerun E1.
I3 RETEST_LOCAL: rerun E2.
I4 RETEST_INTEGRATION: rerun E3.
I5 RETEST_FLOW: rerun E4.
I6 REQUALIFY_RUNTIME: rerun E5.
I7 REDEPLOY_PROOF: rerun E6.
I8 PHYSICAL_REQUALIFICATION: rerun E7.

## Conservative law
UNKNOWN dependency impact escalates to the minimum evidence class capable of resolving the uncertainty. It never silently downgrades.

## Benefit
This prevents "green by inheritance", where old successful evidence remains attached after the system it proved has materially changed.
