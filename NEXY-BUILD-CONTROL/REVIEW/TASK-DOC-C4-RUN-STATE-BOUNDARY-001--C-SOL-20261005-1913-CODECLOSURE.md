TASK_ID: TASK-DOC-C4-RUN-STATE-BOUNDARY-001
REVIEWER_CHAT: C-SOL-20261005-1913-CODECLOSURE
ROLE: INDEPENDENT_BOUNDARY_CONTRACT_REVIEWER
STATUS: REVIEW_CONFIRMS_ACTIONABLE_GAP
PRIORITY: P1
RISK: HIGH_CANONICAL_API_BOUNDARY
SOURCE_REPOSITORY: goif74945-crypto/NEXY.AI-
SOURCE_BRANCH: NEXY.AI-Test-AI
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SOURCE_TREE_SHA: e7f603d06db6475a4d72f5d0aed752213d17eb16
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
CONTROL_HEAD_OBSERVED: 32643861485733527733a478438607ece860ceeb

SPEC_EVIDENCE:
- Final DOC-C paragraphs 9955-9963 define SystemState exactly as INIT | READY | RUNNING | VERIFYING | CONSENSUS | STABLE | FREEZE | STOP.
- Final DOC-C paragraphs 10222-10242 define GET /api/runs/:id and require response data.state: SystemState.

SOURCE_EVIDENCE:
- packages/api/directives.ts blob 8cd214c87e5aa55561e52347802ec8172feadc36 reads PipelineRun.runState from persistence.
- handleGetRun computes an envelopeState fallback for unknown values, but serializes data.state = run.runState unchanged.
- prisma/schema.prisma blob 0c557a1bb9b02859bb479655575c3566e201eb6f defines PipelineRun.runState as unconstrained String @db.VarChar(16).
- tests/integration/directives/read-auth.spec.ts blob 560bc7a5bdc99211395faf5fd46c826e6312fd5e covers valid READY/STABLE values but contains no malformed persisted-state rejection case.

COUNTEREXAMPLE:
A persisted PipelineRun with runState = "BROKEN_STATE" can reach HTTP 200 and serialize data.state = "BROKEN_STATE", violating the final-DOC-C SystemState wire contract.

VERDICT:
CONFIRMED: BOUNDARY_VALIDATION_DEFECT + CANONICAL_RESPONSE_CONTRACT_DRIFT + MISSING_REQUIRED_TEST.

REPAIR_CONSTRAINTS:
- Validate persisted runState before constructing a successful canonical response.
- Do not invent a new SystemState or silently coerce malformed data into a valid state.
- Derive the exact failure envelope/status from active authority or an already-established canonical fail-closed boundary before implementation.
- Add red-first malformed persisted-state coverage and rerun all run-read auth/audit/shape tests on exact candidate SHA and integrated SHA.
- Do not mutate NEXY.ai.

BLOCKER:
INC-BRANCH-NAMESPACE-001 prevents Constitution-compliant isolated source mutation.

SOURCE_MUTATION: NONE
CONTROL_MUTATION: APPEND_ONLY_REVIEW
