# NEXY Novelty Forge — Design Pack

**Work/session ID:** `CHAT-20261005-0154-NEXY-NOVELTY-FORGE`  
**Classification:** AI-proposed reference systems, not canonical NEXY requirements.

## Collision guard

The supplemental namespace was recursively inspected before design. It already contained 1,389 entries at that scan, including proof/evidence graphs, semantic contracts, context-fidelity systems, directive integrity, privacy firewalls, resource governors, concurrency/partial-order labs, causal merge, shadow execution, deterministic interchange, proof sensitivity and commitment integrity. Exact lexical searches for the selected mechanism terms such as `cross-modal`, `Shapley`, `verification scheduler`, `outcome credit`, and the chosen explicit marker mechanism returned no exact implementation hits in AI-CONTEXT at scan time. This reduces obvious duplication but is **not** proof of global novelty.

## 1. Cross-Modal Truth Lattice (CMTL)

**Problem:** individually valid spec/code/UI/API/test/config/runtime surfaces can contradict one another.  
**Input:** structured assertion `{artifactId, modality, subject, predicate, object, polarity, critical}`.  
**Mechanism:** canonicalize `(subject,predicate)`, group assertions, surface differing variants, and request advisory `FREEZE` for critical conflicts under policy.  
**Invariants:** no free-form semantic guessing; order-invariant report; exact artifact/modalities preserved; missing cross-modal coverage becomes an explicit diagnostic.  
**Failure:** malformed IDs, empty fields, invalid cross-check policy fail closed with `ContractError`.  
**NEXY fit:** pre-JUDGE/verification diagnostic only. It may request freeze but may never call LAW or transition system state itself.

## 2. Counterfactual Outcome Credit Ledger (COCL)

**Problem:** success/failure of a multi-agent run does not show which actions actually added value.  
**Input:** bounded action IDs plus externally supplied value for every action coalition.  
**Mechanism:** exact Shapley-style marginal contribution accounting across the complete coalition table.  
**Invariants:** full coalition table required; unique IDs; bounded action count; canonical output ordering; reported efficiency residual.  
**Failure:** missing coalitions, non-finite values, duplicate IDs or unsafe action count fail closed.  
**Truth boundary:** output explicitly says `COUNTERFACTUAL_CONTRIBUTION_NOT_CAUSAL_PROOF`. It is accounting under supplied counterfactuals, not real-world causal proof.  
**NEXY fit:** OBS/evaluation plane for replay/routing research, never execution authority.

## 3. Verification Value Scheduler (VVS)

**Problem:** verifying every claim maximally wastes resources, but cheapest-first verification can violate evidence law.  
**Input:** claim risk, impact, uncertainty, mandatory flag, candidate evidence options, cost, expected residual uncertainty, and whether an option satisfies the required evidence class.  
**Mechanism:** lock mandatory legal evidence first. Missing legal evidence or mandatory cost above budget returns `BLOCKED`. Optimize only the remaining optional portfolio via deterministic integer-cost dynamic programming.  
**Invariants:** required evidence class is never downgraded; PASS never exceeds budget; one optional evidence choice per claim; tie-breaking deterministic.  
**NEXY fit:** higher-level claim/evidence portfolio planner. It is distinct from current Lo3's cheap-tester/expensive-verifier agent ladder, which chooses verifier agents rather than claim-level evidence investment.

## 4. Semantic Entropy Guard (SEG)

**Problem:** consensus can hide severe worker disagreement after only the winner survives.  
**Input:** independent worker decisions reduced to explicit dimensions plus optional positive weights.  
**Mechanism:** compute coverage and normalized Shannon entropy per dimension; policy marks critical dimensions and review/freeze thresholds.  
**Invariants:** at least two workers; missing decisions reduce coverage; critical low coverage/high disagreement may request FREEZE; input order does not change output.  
**Failure:** duplicate workers, invalid weights or thresholds fail closed.  
**Numeric caveat:** standalone code uses JavaScript floating point. Therefore SEG is advisory. Any future authoritative NEXY threshold should be migrated to NEXY's canonical fixed-point/Q64.64 law before promotion.

## 5. Observed Contract Miner (OCM)

**Problem:** maintaining a large spec↔test crosswalk by inference risks hallucinated requirement mappings.  
**Input:** source/test text containing explicit markers such as `@nexy-observed-contract {"requirementId":"REQ-X","behavior":"...","evidenceClass":"E2"}` plus authoritative expected requirement IDs.  
**Mechanism:** parse only explicit markers; retain source path/line; detect duplicate contradictions; crosswalk observed and missing requirement IDs.  
**Truth discipline:** marker present → `NOT_VERIFIED`; absent → `UNKNOWN`; conflicting markers → `CONFLICT`; malformed marker quarantined; every observation stamped `OBSERVED_NON_AUTHORITY`.  
**NEXY fit:** offline audit tooling that could assist the current 837-row matrix without granting annotations authority.

## Compatibility contract

Current NEXY read-only inspection showed deterministic canonical JSON, request/trace IDs, centralized LAW freeze transition, module-boundary enforcement, and a Lo3 governor with Q64.64 scoring and a verification ladder. A future adapter must therefore:

1. wrap outputs in existing request/trace/evidence envelopes;
2. keep these five systems advisory unless explicitly promoted by authoritative spec;
3. route any real FREEZE through canonical LAW/state transition, never from auxiliary code;
4. use NEXY canonical ordering/hash/numeric utilities where the result becomes authoritative;
5. honor module-boundary rules and exact-head tests;
6. never convert OCM markers or CMTL/SEG scores into release authorization;
7. require fresh exact-head evidence and an explicitly authorized NEXY mutation task before integration.

## Acceptance evidence model

- E0: code/design/test/evidence artifacts exist.
- E1: strict compile succeeds in available local compiler.
- E2: focused/negative/determinism tests execute and pass.
- E3 (standalone only): OCM status output composes with VVS without authority promotion.
- NEXY E3/E4/E5/E6: `NOT_VERIFIED` and intentionally not claimed.
