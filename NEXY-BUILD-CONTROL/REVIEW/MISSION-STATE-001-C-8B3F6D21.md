MISSION_ID: MISSION-STATE-001
REVIEWER_CHAT: C-8B3F6D21
ROLE: SHADOW_REVIEWER / TEST_DESIGNER / RED_TEAM
SOURCE_REPOSITORY: goif74945-crypto/NEXY.AI-
SOURCE_BRANCH: NEXY.AI-Test-AI
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
REQ_ID: REQ-DOC-C-STATE-MATRIX-ERROR-001
SCOPE:
- final DOC-C event set and transition relation
- TS/Rust parity
- §5.4 revoke-release ambiguity
- executable oracle design
MUTATION: NONE
EVIDENCE:
- TS blob a5ac7d5e97c9fca19b68557fa7012b607cb1ec0e contains 26 transition triples.
- Rust blob 2e5a0a1f9109175ede8884e76bddab2f46c79f77 contains 21 transition triples.
- Executed static extraction finds exactly five TS-only triples: INIT|error|FREEZE, READY|error|FREEZE, CONSENSUS|error|FREEZE, STABLE|error|FREEZE, FREEZE|error|FREEZE. Rust has no Rust-only triples.
- Final DOC-C §5.1 includes timeout and cancel in SystemEvent; treating them as non-DOC-C compatibility rails is a wrong test oracle.
- Final DOC-C §5.2 authorizes error->FREEZE for RUNNING and VERIFYING only; fatal->STOP is ANY except STOP.
- §5.4 revoke release is implemented separately in packages/queue/run-state.ts blob e162efc8b2a45014bcefbd60dc67a95d8a1e1003 by revokeStableRelease(): expectedStates=[STABLE], requireOutputNotEmitted=true, clearOutput=true, action=OWNER_REVOKED_RELEASE. Therefore no speculative STABLE+cancel edge is required in VNEXT_TRANSITIONS.
RED_TEST_DESIGN:
- exact final event set contains 11 events including timeout and cancel.
- RUNNING error -> FREEZE and VERIFYING error -> FREEZE are allowed with valid owner/guards.
- INIT/READY/CONSENSUS/STABLE/FREEZE error must throw STATE_TRANSITION_DENIED.
- fatal from each non-STOP state -> STOP; STOP has no outgoing transitions.
- Rust and TS transition triples must be exact-set equal.
CURRENT_RESULT: FAIL_CURRENT_HEAD
REASON: Current TypeScript source and current contract oracle contradict locked final DOC-C and current Rust implementation.
EXECUTION_LIMIT: No source candidate can be produced under literal V7 worker prefix because INC-BRANCH-NAMESPACE-001 is OPEN. No test PASS is claimed.
NEXT_ACTION: Once branch namespace policy is reconciled, implement test-oracle correction first (red), remove the five TS-only error edges (green), run state-matrix + Rust parity + DOC-C static gates at exact worker SHA, then independent exact-SHA review before integration.
