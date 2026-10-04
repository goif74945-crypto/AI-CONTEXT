# 20 CourtScript-Q64 Mechanisms

All 20 are implemented as source modules. They are one compositional candidate, not 20 independent claims of Canon authority.

1. **Bounded Attack-Surface Lexer** — strict token space, comment stripping, NUL rejection, source/token budgets, punctuation rejection.
2. **Deterministic Court Policy Parser** — accepts only explicit advisory policy constructs and rejects hidden statements.
3. **Canonical AST Seal** — structural SHA-256 identity for policy review/replay.
4. **Exact Q64 Literal Compiler** — decimal text to checked signed Q64.64 without floating-point decision arithmetic.
5. **Closed Metric Type Registry** — policies cannot invent unreviewed metric names.
6. **Static Court Type Checker** — rejects duplicate fields/codes, nonpositive weights, invalid thresholds and duplicate proof/guard declarations.
7. **Authority Effect Type Firewall** — fixes authority to `ADVISORY_ONLY` and rejects mutation/promotion effects.
8. **Revision-Pin Contract Checker** — requires SPEC_HASH, NEXY_COMMIT_SHA and AI_CONTEXT_COMMIT_SHA.
9. **Tri-State Epistemic Logic** — TRUE/FALSE/UNKNOWN prevents missing evidence from becoming false certainty.
10. **WIP Immunity Guard Compiler** — CUT_REVIEW is ill-formed without WIP immunity; WIP-only basis DEFERs.
11. **Burden-of-Proof Declaration Compiler** — KEEP_REVIEW requires executed-test proof; CUT_REVIEW substantive-basis proof; both pinned evidence.
12. **Non-Compensatory Requirement Gate Compiler** — hard constraints are separate from weighted score.
13. **Q64 Weighted Advisory Score Compiler** — fixed-point weighted score with positive-weight validation.
14. **Review-Only Recommendation Compiler** — deliberately lacks KEEP/CUT vote or promotion opcodes.
15. **Canonical Bytecode Sealer** — digest-bound instruction stream.
16. **Bounded Side-Effect-Free Court VM** — ≤512 instructions, explicit checks, UNKNOWN-to-DEFER.
17. **Deterministic Trace Proof Hasher** — canonical digest for evaluation replay.
18. **Policy Loosening/Compatibility Analyzer** — detects tightened/loosened/removed/added constraints.
19. **Conformance Vector Runner** — binds policies to expected advisory outcomes and detects regression.
20. **Admission Compiler** — fail-closed front door composing all static gates.

## Distinct axis
Existing EPC candidates cover proposal capsules, counterfactual replay, semantic-overlap proof, impact lattices, evidence entropy, adversarial promotion, utility frontiers, invariant witnesses, dependency graphs, capability escalation, reversibility, adapters, freshness, resources, contradiction cores, lineage, value evidence, shadow integration and the two-round ledger. CourtScript instead makes **the court policy itself** a typed/replayable/effect-bounded artifact.
