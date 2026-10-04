# NEXY Lo4 Innovation Capital Fabric (ICF)

**Classification:** `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_GOVERNING / NOT_CANON`

ICF is a standalone reference lab for deciding which Lo4 proposals deserve scarce engineering attention when many ideas arrive concurrently. It does not decide NEXY law, does not promote anything into Canon, and does not mutate the NEXY.AI implementation repository.

## Why this exists

The current supplemental ecosystem contains many strong labs for verification, authority, outcomes, interaction integrity, preference sovereignty, convergence and decision stability. What is still useful is a deterministic layer for **innovation capital allocation**: compare uncertain proposal value, discount overlap, price structural complexity, compose a diverse feasible portfolio, and design a bounded reversible pilot.

## Five systems

1. **IURS — Interval Utility Regret Selector**
   Selects among proposal candidates using conservative Q64.64 utility intervals, minimax regret and protected objective minima.
2. **COMET — Concept Overlap Marginal-Erosion Table**
   Discounts marginal value when a candidate overlaps already-selected work and freezes if overlap evidence is missing/conflicting.
3. **SCTE — Structural Complexity Tax Engine**
   Converts persistence, migration, public-contract and rollback burden across change surfaces into an explicit Q64.64 complexity tax.
4. **DCPX — Diversity-Constrained Portfolio Composer**
   Exactly enumerates bounded proposal subsets and selects the highest conservative value subject to cost, complexity, dependency, conflict, diversity and overlap constraints.
5. **RIVP — Reversible Information-Value Pilot Planner**
   Plans only bounded reversible/view-only pilots when expected information option value survives explicit risk, blast-radius, rollback and sample-budget gates.

## Numeric law

Every decision score, interval, weight, ratio, risk, overlap, budget coefficient, penalty and threshold in the reference engines uses signed **Q64.64** fixed point backed by a checked signed 128-bit raw integer. Binary floating-point is prohibited from decision modules and checked by an adversarial AST test.

## Conceptual flow

`Lo4 proposals -> IURS -> COMET -> SCTE -> DCPX -> RIVP -> human/formal promotion process`

The last arrow is deliberately outside this package. A pilot plan is not approval, deployment, adoption or Canon.

## Local verification commands

```bash
python3 -m compileall -f -q aeul tests
PYTHONHASHSEED=1 python3 -m unittest discover -v tests
PYTHONHASHSEED=777 python3 -m unittest discover -v tests
PYTHONPATH=. python3 tests/stress.py
```

No third-party Python dependencies are required.
