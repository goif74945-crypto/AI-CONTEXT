# Five Proposed Systems

Every item is **PROPOSAL BY AI / NOT A NEXY REQUIREMENT / NOT A NEXY IMPLEMENTATION CLAIM**.

1. **Metamorphic Relation Engine (MRE):** transform an input under an authorized semantic rule, re-run the executor, then verify an explicit invariant. Catches silent behavior drift across serializers, providers, queues and wrappers.
2. **Deterministic Counterexample Minimizer (DCM):** shrink a failing structured fixture while preserving the failure, producing a small witness. Bounded and deterministic; never claims mathematical global minimality.
3. **Oracle Independence Auditor (OIA):** flag shared source labels or identical declared logic fingerprints between SUT and oracle, reducing circular verification where the test copies the same bug.
4. **Proof-Weighted Deterministic Test Scheduler (PWTS):** mandatory proofs run first; optional tests are chosen by risk, new invariant coverage, novelty and cost. If mandatory proofs exceed budget, the scheduler returns `freeze_required=true` rather than silently skipping them.
5. **Semantic Failure Fingerprint (SFF):** canonical incident identity over invariant, phase, relation, root-cause code and normalized witness; explicitly configured volatile fields can be excluded.

Composite flow:
`Fixture -> MRE -> executor -> invariant -> DCM on failure -> OIA provenance check -> PWTS next-test planning -> SFF dedup/incident identity`

NMAF does not become authority. NEXY::LAW/JUDGE/release policy remains the release/freeze authority.
