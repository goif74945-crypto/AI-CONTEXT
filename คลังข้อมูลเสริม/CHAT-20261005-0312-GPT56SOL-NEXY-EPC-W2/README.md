# NEXY Lo4 CCDF-20 — Constitutional Constraint Diagnostics Fabric

CHAT_ID: `CHAT-20261005-0312-GPT56SOL-NEXY-EPC-W2`  
CLASS: `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING`  
STATUS: `STANDALONE_VERIFIED / NEXY_INTEGRATION_NOT_VERIFIED / EPC_VOTE_DEFERRED`

CCDF-20 is a deterministic C++20 reference fabric for diagnosing conflicting proposal/spec/law constraints before a future authorized NEXY promotion review. It implements a bounded Boolean CNF solver, minimal unsatisfiable cores, legal soft-only correction sets, logical implication/redundancy analysis, delta/pair conflict diagnostics, deterministic legal alternatives, and Q64.64 repair ranking.

It deliberately cannot promote anything, mutate Canon, change CORE/JUDGE/SWARM state, alter a vote, or relax a hard constraint because a score looks attractive.

## 20 implemented systems
1. **Constraint Canonicalizer**
2. **Authority-Stratified Constraint Binder**
3. **Deterministic SAT Kernel**
4. **Minimal Unsat Core Extractor**
5. **Minimal Correction Set Enumerator**
6. **Conflict Hypergraph Compiler**
7. **Conflict Witness Minimizer**
8. **Implication Closure Engine**
9. **Redundant Constraint Detector**
10. **Shadowed Soft Constraint Detector**
11. **Assumption Sensitivity Analyzer**
12. **Delta Conflict Predictor**
13. **Conditional Conflict Matrix**
14. **Constraint Dependency Slice**
15. **Legal Alternative Enumerator**
16. **Q64 Relaxation Cost Estimator**
17. **Repair Dominance Filter**
18. **Freeze Explanation Compiler**
19. **Canon Compatibility Certificate**
20. **Promotion Constraint Dossier**

## Numeric law
- signed Q64.64 raw carrier: `__int128_t`;
- 256-bit checked intermediate via Boost.Multiprecision for multiply/divide;
- no IEEE-754 decision math in authoritative package source;
- overflow/divide-by-zero fail closed;
- hard constraints cannot be passed to the relaxation-cost path.

## Solver safety
- deterministic unit propagation + occurrence-count branch heuristic with stable variable-index tie break;
- false-first deterministic branching;
- default search-node budget: 1,000,000;
- variable ceiling: 4,096;
- soft correction enumeration has explicit `max_soft_search` bound;
- model enumeration has explicit output limit.

## Evidence summary
- GCC 14.2 exact-source build/test: PASS 22/22.
- Clang 17 exact-source build/test: PASS 22/22.
- ASan+UBSan: PASS 22/22.
- CTest: PASS 1/1.
- property oracle: 250 deterministic generated small CNF formulas matched brute-force satisfiability.
- benchmark (GCC Release, this sandbox): 5,000 solves × 64-variable all-unit SAT workload = 196,764 µs total. This is only that workload, not a universal performance claim.
- tested source root SHA-256: `f5161190675df4d4c25f4536933c7661e62407afdf4729a88037cb2ad2ed88a2`.
- sealed archive SHA-256: `17cd0fc0905b8b30199f891291596ff5967fdd46e6798e16e5de065bf5443396`.

The exact tested bundle is preserved under `BUNDLE/`. Reconstruct it with `BUNDLE/RESTORE.md`.
