REVIEW_ID: R-CHAT-1713-TASK-DOC-C5-STATE-MATRIX-001
TASK_ID: TASK-DOC-C5-STATE-MATRIX-001
REVIEWER: CHAT-20261005-1713-GPT56SOL-CONTRACT-AUDIT
ROLE: INDEPENDENT_SPEC_REVIEW
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SCOPE:
- packages/core/vnext-state-matrix.ts
- core-kernel/src/kernel/vnext_matrix.rs
- tests/contract/state-matrix.test.ts
- tests/contract/core-kernel-vnext-parity.test.ts
- scripts/check-doc-c.ts

FACT:
- Final DOC-C §5.1 includes timeout and cancel in SystemEvent.
- Final DOC-C §5.2 permits error -> FREEZE from RUNNING and VERIFYING only.
- Final DOC-C §5.2 permits fatal -> STOP from ANY except STOP.
- Final DOC-C §5.4 defines OWNER hard kill from RUNNING/VERIFYING/CONSENSUS -> FREEZE.
- TypeScript source contains five extra error -> FREEZE rows from INIT, READY, CONSENSUS, STABLE, FREEZE.
- Rust source contains only the two final-DOC-C error rows.
- tests/contract/state-matrix.test.ts incorrectly labels timeout/cancel as compatibility extensions and requires error -> FREEZE from every non-STOP state.
- tests/contract/core-kernel-vnext-parity.test.ts compares Rust transition triples to TypeScript transition triples, so the current checked-in sources are statically inconsistent.
- scripts/check-doc-c.ts validates the exact event set but does not validate the exact transition set, so this transition drift is not covered by that static gate.

COUNTEREXAMPLES:
- vnextTransition("INIT","error","CORE",{not_in_stop:true}) is represented as legal by the TS table, but no final DOC-C §5.2 row authorizes INIT/error.
- vnextTransition("STABLE","error","CORE",{not_in_stop:true}) is represented as legal by the TS table, but final DOC-C allows STABLE -> FREEZE only through OWNER revoke release before emission.
- The contract oracle calls timeout/cancel non-DOC-C extensions even though final DOC-C §5.1 explicitly lists both.

DESIGN_REVIEW:
- Remove the five unauthorized TypeScript error rows.
- Reclassify timeout and cancel as final DOC-C events.
- Keep RUNNING/VERIFYING error rows and all non-STOP fatal rows.
- Keep OWNER hard-kill semantics for RUNNING/VERIFYING/CONSENSUS.
- Add an exact transition-set oracle to either the contract test or scripts/check-doc-c.ts so future extra/missing rows fail closed.
- Do not weaken the Rust/TS parity test.

EXECUTION_EVIDENCE:
- NONE for a repaired candidate. INC-BRANCH-NAMESPACE-001 blocks V7-compliant worker source mutation and therefore exact-candidate test execution.

RESULT: CHANGES_REQUIRED
SEVERITY: P0
REVIEW_COMPLETED: 1
BLOCKER: INC-BRANCH-NAMESPACE-001
NOTE:
This review does not mutate source and does not claim test PASS. It independently confirms the current mismatch and the narrow repair direction.