# Integration Architecture Proposal

Status: `Lo4_AI_PROPOSAL_ONLY`

## Boundary contract
This package is an advisory optimization layer. It may recommend what to preload, how to distribute latency budget, how to order independent proofs, what context to keep resident, and which optional notices to defer. It must never outrank NEXY LAW/JUDGE or the current authoritative specification.

## Shared invariants
1. Authority before optimization.
2. No speculative side effects.
3. Proof floor is immutable.
4. Proof dependencies are hard edges.
5. Counterevidence is not cache trash.
6. Blocker/security/authority-conflict signals are not notification noise.
7. Decision arithmetic is Q64.64.
8. No Canon self-promotion.

## Suggested adapters
- Context Engine -> WCRC using authority rank, freshness, counterevidence and dependency distance.
- Retrieval/tool planner -> AP3 candidates with explicit side-effect classification.
- Verification graph -> PCPS proof tasks.
- Product SLO/policy -> LEC stage minima and weights.
- PULSE/VIEW/DIALOG -> ABG notices with authoritative mandatory flags.

## Promotion gates
Map adapters to Canon, prove units/range, adversarially test side-effect classification, benchmark latency, run exact-SHA integration/E2E, verify no safety/proof gate bypass, then formal promotion.
