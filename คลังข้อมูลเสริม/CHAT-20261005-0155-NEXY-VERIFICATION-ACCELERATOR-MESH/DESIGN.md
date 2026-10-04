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

## 1 — CEF: Correlated Evidence Firewall
Problem: multiple agents may repeat the same upstream source and create fake consensus.
Design: evidence carries provenance roots. Any shared root merges evidence into one independence cluster. Cluster weight is max(member confidence), not sum.
Failure semantics: missing/insufficient proof => FREEZE; malformed provenance/claim IDs => hard error.

## 2 — MVF: Metamorphic Verification Forge
Problem: exact expected outputs are often unavailable even though invariant relations are known.
Design: run the SUT on base + transformed inputs and test declared relations.
Failure semantics: base exception, transform exception, relation exception, or false relation => FAIL.

## 3 — CME: Counterexample Minimization Engine
Problem: large failing traces are expensive to reason about and preserve.
Design: deterministic ddmin followed by a one-element-removal pass.
Failure semantics: non-failing seed rejected; evaluation-budget exhaustion aborts rather than claiming minimality.

## 4 — ALP: Assumption Liquidation Planner
Problem: UNKNOWN/ASSUMPTION states accumulate and are resolved in poor order.
Design: assumption risk = impact × uncertainty. Experiment utility = marginal risk retired × confidence / cost adjusted by execution risk.
Failure semantics: invalid/duplicate IDs, invalid ranges, or unknown assumption targets => hard error.

## 5 — BCC: Behavioral Canary Compiler/Runner
Problem: providers/tools/models can drift while APIs remain syntactically present.
Design: canonical JSON-compatible behavior signatures for a small versioned canary suite.
Failure semantics: signature mismatch => DRIFT; baseline/case identity mismatch => hard error.

## Mesh flow
BCC detects drift -> MVF finds relation failures without exact oracle -> CME shrinks a reproducer -> CEF rejects correlated confirmation -> ALP ranks the next independent experiment -> new evidence returns to the gate.

No module owns release authority. A future NEXY::LAW/NEXY::JUDGE integration remains authoritative.

## Global invariants
- no assumption silently becomes fact;
- no low-class proof is promoted to runtime/deployment proof;
- deterministic tie-breaking where order matters;
- prototype core has no network/repository/credential side effects;
- exceptions do not silently become PASS;
- stale evidence is invalid after semantic code/config change.

## Residual risks
CEF depends on trustworthy upstream provenance.
MVF depends on correct metamorphic relations.
CME proves 1-minimality, not global cardinality minimum.
ALP is a deterministic greedy heuristic, not a globally optimal stochastic solver.
BCC hash equality proves canonical serialized equality, not semantic correctness.

## Verification result
- E1 compileall: PASS
- E2 unit: 20/20 PASS
- E3 local integration: PASS
- property/stress: 1002 PASS
- deterministic wheel reproducibility: PASS, 2 matching builds with SOURCE_DATE_EPOCH=1704067200
- wheel SHA-256: 8518f646fc6f8689584f68c66ed9386aa7e52a15881dbd20cae40c13fcafc755
- ruff/mypy: NOT_VERIFIED because unavailable

## Adoption gate
Promotion requires authoritative requirement mapping, real repository interface review, threat/security review, performance budget, authorized E3/E4 integration evidence, and explicit project-owner decision.

## Status
Design: PASS for supplemental prototype.
Implementation: PASS for local prototype.
NEXY runtime/deployment adoption: NOT_VERIFIED.
