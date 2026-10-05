# Independent Shadow Review: T-D4A71C2E

REVIEWER_CHAT: C-D1CB1B5B
TASK_ID: T-D4A71C2E
ROLE: SHADOW_REVIEWER
STATUS: CHANGES_REQUESTED
REVIEWED_BRANCH: NEXY.AI-Test-AI
REVIEWED_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
TREE_SHA: e7f603d06db6475a4d72f5d0aed752213d17eb16
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

SOURCE_BLOBS:
- packages/core/vnext-state-matrix.ts: a5ac7d5e97c9fca19b68557fa7012b607cb1ec0e
- core-kernel/src/kernel/vnext_matrix.rs: 2e5a0a1f9109175ede8884e76bddab2f46c79f77
- tests/contract/state-matrix.test.ts: 2c1c4e1a1ffc62993b6774f5dafcf4f8fafa56ba
- tests/contract/core-kernel-vnext-parity.test.ts: a391b2029fc13c3e38a9037c8adf3f10638f0086

SCOPE:
Final DOC-C executable state/event authority and cross-language transition parity only.

AUTHORITY_EVIDENCE:
- FINAL VERDICT paragraphs 9834-9845: DOC-C is BUILD SPEC; build obligation comes from DOC-C only.
- Final DOC-C state/event authority paragraphs 10353-10499.
- Canonical requirement records REQ-DOC-C-5-STATE-EVENT-MATRIX and REQ-DOC-C-STATE-MATRIX-ERROR-001 bind the locked primary source.

EXECUTED_EVIDENCE:
- Exact-blob transition parser counted canonical DOC-C §5.2 plus §5.4 owner hard-kill mapping: 21 triples.
- Rust transition set: 21 triples, extra=0, missing=0 versus the canonical set.
- TypeScript transition set: 26 triples, missing=0, with five non-authoritative extra edges:
  - INIT|error|FREEZE
  - READY|error|FREEZE
  - CONSENSUS|error|FREEZE
  - STABLE|error|FREEZE
  - FREEZE|error|FREEZE
- tests/contract/state-matrix.test.ts defines DOC_C_FINAL_EVENTS without timeout and cancel even though final DOC-C SystemEvent includes both.
- tests/contract/core-kernel-vnext-parity.test.ts derives its expected event and transition sets from the TypeScript implementation via Object.values(VNEXT_EVENT) and VNEXT_TRANSITIONS.map(...). It therefore proves implementation parity, not independent Spec compliance; identical TS/Rust drift could pass this oracle.

DUPLICATE_SUPPRESSION:
No new finding created. This independently confirms existing FINDING-DOC-C5-STATE-ORACLE-001, F-STATE-MATRIX-PARITY-001, and F-A6D4F129-STATE-PARITY-CONFLICT.

DEPENDENCY / UNKNOWN:
Bootstrap failure from INIT/READY remains an authority gap: DOC-B requires fail-closed FREEZE while final DOC-C has no INIT/READY error->FREEZE row. DEP-E4C19A73-STATE-ERROR-AUTHORITY already freezes unilateral mutation of that semantic scope.

LIMITATIONS:
- No full repository CI/test suite was executed in this review.
- Review is exact-blob/static executable evidence for the pinned integration SHA only.
- Source mutation is globally blocked by INC-BRANCH-NAMESPACE-001 for V7-compliant worker branches.

REVIEW_RESULT:
CHANGES_REQUESTED. Current integration SHA cannot be promoted as VERIFIED for this requirement.
