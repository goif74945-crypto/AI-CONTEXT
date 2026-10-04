# NEXY Verification Accelerator Mesh — Design

> AI PROPOSAL / NOT CANONICAL NEXY.AI LAW

## Task Contract
Objective: build exactly five isolated, testable prototypes that strengthen verification/evidence/debugging for future NEXY.AI integration evaluation.

Authorized scope: AI-CONTEXT supplemental storage, local sandbox execution, adapter-oriented design, test/evidence capture.
Protected scope: any repository whose name contains NEXY.AI, secrets, production systems, adjacent chat folders, claims of canonical adoption.

Success invariants:
1. five distinct concepts;
2. executable implementation for each;
3. positive + negative tests;
4. cross-module integration test;
5. static compile proof;
6. determinism/minimality stress where relevant;
7. raw evidence preserved;
8. no NEXY.AI mutation.

## System 1 — CEF: Correlated Evidence Firewall
Problem: multiple agents may repeat the same upstream source and create fake consensus.
Design: evidence carries provenance roots. Any shared root merges evidence into one independence cluster. Cluster weight is max(member confidence), not sum. Admission requires minimum independent clusters and effective weight.
Failure semantics: missing/insufficient proof => FREEZE; malformed provenance/claim IDs => hard error.
Why useful: distinguishes many voices from independent observations before final judgment.
Adjacent difference: lineage systems record provenance; CEF consumes lineage to make independence admission decisions.

## System 2 — MVF: Metamorphic Verification Forge
Problem: exact expected outputs are often unavailable even though invariant relations are known.
Design: run the same SUT on base + transformed inputs and test declared relations such as permutation invariance or idempotence.
Failure semantics: base exception, transform exception, relation exception, or false relation => FAIL.
Why useful: expands verify-only coverage without asking an AI to invent an oracle.
Adjacent difference: interleaving verifiers perturb scheduling; MVF perturbs semantic inputs.

## System 3 — CME: Counterexample Minimization Engine
Problem: large failing traces are expensive to reason about and preserve.
Design: deterministic ddmin followed by a one-element-removal pass. Returned witness must reproduce the failure and be 1-minimal if the algorithm completes normally.
Failure semantics: non-failing seed rejected; evaluation-budget exhaustion aborts instead of claiming minimality.
Why useful: turns fuzz/metamorphic/canary/interleaving failures into small regression witnesses.

## System 4 — ALP: Assumption Liquidation Planner
Problem: UNKNOWN/ASSUMPTION states accumulate and are often resolved in poor order.
Design: assumption risk = impact × uncertainty. Experiment utility = marginal risk retired × confidence / cost adjusted by execution risk. Greedy selection is deterministic and budget bounded.
Failure semantics: invalid/duplicate IDs, invalid ranges, or unknown assumption targets => hard error.
Why useful: operationalizes “do not guess” into an explicit evidence-acquisition queue.

## System 5 — BCC: Behavioral Canary Compiler/Runner
Problem: providers/tools/models can drift while APIs remain syntactically present.
Design: record canonical JSON-compatible behavior signatures for a small canary suite. Future runs compare signatures. Explicit top-level nondeterministic fields may be ignored, but nested drift remains visible.
Failure semantics: signature mismatch => DRIFT; baseline/case identity mismatch => hard error.
Why useful: cheap preflight gate before more expensive verification.

## Mesh flow
BCC detects drift -> MVF finds relation failures without exact oracle -> CME shrinks a reproducer -> CEF rejects correlated “confirmation” -> ALP ranks the next independent experiment -> new evidence returns to the gate.

No module owns release authority. A future NEXY::LAW/NEXY::JUDGE integration would remain authoritative.

## Global invariants
- no assumption silently becomes fact;
- no low-class proof is promoted to runtime/deployment proof;
- deterministic tie-breaking where order matters;
- prototype core has no network/repository/credential side effects;
- exceptions do not silently become PASS;
- stale evidence is invalid after semantic code/config change.

## Failure model / residual risks
CEF cannot detect fabricated provenance unless upstream lineage is trustworthy.
MVF is only as good as its declared metamorphic relations.
CME guarantees 1-minimality, not globally minimum cardinality for arbitrary predicates.
ALP uses a heuristic, not a globally optimal stochastic decision solver.
BCC hash equality proves canonical serialized equality, not semantic correctness; bad baselines remain bad.

## Verification plan
E1 static: Python compileall.
E2 unit: all five modules with positive/negative paths.
E3 local integration: BCC -> MVF -> CME -> CEF -> ALP.
Property/stress: CME 1-minimality, CEF permutation invariance, ALP deterministic selection, BCC canonicalization.
Package: wheel build without network/build isolation.

## Evidence result
- compileall PASS
- 20 tests PASS
- 1002 stress/property checks PASS
- wheel build PASS
- wheel SHA-256 56c275d96fcad546daef4b06a2b3e68ef5b84fe184eecc63b9116fad3791f18a
- ruff/mypy unavailable, therefore NOT claimed

## Integration contract
Future adapters must supply authoritative provenance roots, metamorphic relations, deterministic failure predicates, assumption/risk calibration, and versioned canary baselines. The proposal must not be promoted solely because local tests pass.

## Adoption gate
Promotion requires authoritative requirement mapping, real repository interface review, threat/security review, performance budget, authorized E3/E4 integration evidence, and explicit project-owner decision.

## Status
Design: PASS for supplemental prototype.
Implementation: PASS for local prototype.
NEXY runtime/deployment adoption: NOT_VERIFIED.