# Verification Portfolio Optimizer (VPO) — Design

Status: **AI-PROPOSED / EXPERIMENTAL / NON-CANONICAL**

## Objective
Choose the lowest-cost set of available checks that satisfies every explicit evidence obligation without silently substituting the wrong evidence class.

## Authority and scope
VPO is a planning optimizer. It MUST NOT redefine which evidence class a claim requires. Required classes come from an upstream authority such as the AI-CONTEXT Verification Law or a project contract. VPO only chooses among already-described checks.

## Inputs and outputs
- `Claim`: claim ID + explicit accepted evidence-class set.
- `Check`: check ID + nonnegative cost units + claim-to-evidence-class mapping.
- `Portfolio`: deterministic selected checks, total cost, and one qualifying coverage witness per claim.

## Invariants
1. Evidence-class matching is set membership, not ordinal guessing. E1 never satisfies E2 merely because the labels look ordered.
2. Every returned claim is covered by at least one selected check using an accepted class.
3. Objective is exact minimum total cost, then minimum check count, then lexical check-ID tie-break.
4. Duplicate IDs and negative costs are invalid.
5. If no legal portfolio exists, the optimizer fails explicitly.

## Algorithm
Each claim is assigned one bit. Every check is converted into the mask of claims it legally covers. Dynamic programming retains the best tuple `(cost, count, sorted check IDs)` for each reachable coverage mask.

Complexity is `O(number_of_checks * reachable_masks)`, bounded by `O(C * 2^R)` for C checks and R claims. The reference implementation therefore applies an explicit `max_exact_claims` guard to bound exponential state growth.

## Failure model
- More claims than exact bound: `PortfolioTooLarge`.
- No satisfying portfolio: `NoValidPortfolio`.
- Duplicate claim/check IDs, negative cost, or claim with no accepted evidence class: `ValueError`.

## NEXY integration proposal
A future NEXY verification planner could translate required proof obligations into `Claim` records and registered verification commands into `Check` records. VPO may suggest the cheapest legal plan, while NEXY remains responsible for authorization, execution, freshness binding, and final PASS adjudication.

## Evidence plan
E2 unit tests cover exact minimum cost, evidence-class non-substitution, deterministic ties, empty claims, state-space guard, and invalid input. E3 lab integration couples NSCA-discovered negative-space debt to VPO and verifies the optimizer chooses E2 behavior evidence instead of a cheaper E1 static check.

## Known limitations
- Exact optimizer is intentionally bounded by claim count.
- Costs are caller-provided abstract units; VPO does not predict real wall-clock cost.
- It does not model check dependencies, flaky probabilities, or shared setup cost in v0.1.
