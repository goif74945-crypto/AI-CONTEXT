# Claim–Evidence Graph

## Purpose
Represent every material completion claim as a typed node linked to evidence whose class is strong enough to prove it.

## Claim tuple
C = {claim_id, subject, predicate, scope, revision, environment, truth_class, required_evidence_class, status}

A claim is invalid for release if revision or scope is missing when the subject can change over time.

## Evidence tuple
E = {evidence_id, type, producer, timestamp, revision, environment, artifact_ref, integrity_ref, result, limitations}

## Edge types
- PROVES: evidence directly establishes claim.
- SUPPORTS: evidence raises confidence but is insufficient alone.
- CONTRADICTS: evidence conflicts with claim.
- SUPERSEDES: newer evidence invalidates older evidence for mutable state.
- DERIVED_FROM: evidence/claim depends on another source.
- REQUIRES: claim cannot be adjudicated without linked evidence.
- BLOCKS: unresolved node prevents release.

## Evidence-class matching
| Claim | Minimum evidence |
|---|---|
| file exists at revision | repository/file observation |
| syntax/type correctness | parser/compiler/typecheck execution |
| unit behavior | executed unit test |
| integration behavior | executed integration test with real boundary or authorized faithful test double |
| browser/UI behavior | browser/E2E evidence |
| security property | threat-specific test + configuration/code evidence; stronger claims may require independent review |
| deployment state | deployment/provider/environment observation |
| performance SLO | measured benchmark under declared workload/environment |
| deterministic behavior | repeated controlled trials + state/input equivalence proof |
| physical safety | physical/HIL evidence; simulation alone is insufficient |

## Freshness
Evidence has a validity window determined by mutability. A changed commit invalidates code-derived PASS evidence unless the evidence is proven unaffected. Deployment evidence must identify environment and deployed revision.

## Aggregation law
A parent PASS requires all mandatory child claims PASS. Optional child failures must be explicitly classified as optional by authority, never silently ignored.

## Contradiction law
If E1 PROVES X and E2 PROVES NOT-X under apparently identical scope/revision/environment, status becomes CONFLICT until identity mismatch or faulty evidence is resolved.

## Release query
A release claim is legal only when:
1. every required claim has at least one valid PROVES edge;
2. no unresolved CONTRADICTS edge exists;
3. evidence revision/environment match;
4. no required node is UNKNOWN/NOT_VERIFIED/CONFLICT;
5. protected-scope and authority checks pass.

## NEXY relevance
This graph operationalizes the NEXY principle “one legal, verified output or freeze/silence” without assuming the implementation already has such a graph.
