# C3 — Evidence Acquisition Planner (EAP)

Status: `AI_PROPOSED_CONCEPT`

## Objective
Choose the deterministic minimum-cost set of available probes/tests that can satisfy all required claims at or above each required evidence class.

## Model
- `ClaimNeed(claim_id, minimum_class)` uses E0..E7.
- `Probe(probe_id, cost, produces, prerequisites)` declares what class it can produce for each claim.
- Caller supplies currently satisfied prerequisites.

## Optimization law
Among complete legal plans minimize lexicographically:
1. total cost;
2. number of probes;
3. sorted probe-id tuple.

The algorithm uses exact dynamic programming over the satisfied-claim bitmask. A probe that only produces E2 cannot satisfy an E3 claim. Missing prerequisites make a probe ineligible.

## Invariants
1. No evidence-class substitution downward.
2. No fabricated evidence: EAP plans probes; it does not mark them PASS.
3. No partial plan is labeled complete.
4. Equivalent probe/claim input ordering yields the same plan.
5. If no complete plan exists, FREEZE with uncovered claims.

## NEXY value
Verification can become expensive across many systems. EAP minimizes redundant checks while preserving exact proof obligations and deterministic tie-breaking.
