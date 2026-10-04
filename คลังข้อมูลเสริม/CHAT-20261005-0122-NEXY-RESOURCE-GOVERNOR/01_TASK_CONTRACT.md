# Task Contract — Proof-Preserving Resource Governor Lab

## Truth class
AI_PROPOSED_CONCEPT + REFERENCE_IMPLEMENTATION.

## Objective
Create a deterministic, auditable planner that chooses a feasible worker/verifier allocation under hard resource and policy constraints without reducing NEXY authority or verification requirements.

## Authorized scope
Only the isolated `AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0122-NEXY-RESOURCE-GOVERNOR/` namespace.

## Protected scope
- every repository whose name contains `NEXY.AI`;
- canonical NEXY project files;
- sibling supplemental labs;
- current 837-row build matrix;
- runtime/deployment state.

## Source-grounded invariants
1. CORE/JUDGE retain authority; AGENT/SWARM provide labor.
2. Unknown material state is not guessed.
3. Verification/evidence requirements are not downgraded for budget convenience.
4. Failure to produce a legal plan resolves to explicit `FREEZE` in this proposed planner.
5. A planned verifier does not itself prove E0-E7 evidence. Real execution is still required.
6. Design, reference implementation, runtime, and deployment claims remain separate.

## AI-proposed requirements
- R1: candidate workers must satisfy capability, clearance, context, active/quarantine and quality-floor constraints.
- R2: required verifier capability must satisfy the task evidence floor.
- R3: high/critical risk forces verifier independence by provider domain.
- R4: token, cost and latency ceilings are hard budgets.
- R5: no budget exhaustion path may suppress a required verifier.
- R6: ranking is deterministic and stable under input reordering.
- R7: price calculations use integer arithmetic.
- R8: rejected agents/pairs expose reason codes.
- R9: duplicate agent identity is a contract error, not silently merged state.
- R10: a feasible plan reports `NOT_VERIFIED` until downstream proof executes.

## Non-goals
- pricing truth for any real provider;
- automatic purchase/billing;
- dynamic production routing;
- replacement of NEXY LAW/CORE/JUDGE;
- proof that any external model actually meets declared quality/capability metadata;
- promotion into current NEXY build scope.

## Acceptance criteria for this lab
- Python source compiles.
- JSON proposal artifacts parse.
- all unit/adversarial tests pass.
- tests include budget exhaustion, independence, privacy clearance, quarantine, evidence floor, deterministic tie-break and duplicate identity.
- every committed artifact can be re-read from AI-CONTEXT.
- no NEXY.AI-named repository is mutated.
