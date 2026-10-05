# Independent Review — TASK-DOC-C3-API-HANDLER-STATE-INTEGRITY-001

CHAT_ID: C-SOL-20261005-1912-V8
ROLE: Reviewer / Spec Auditor / Red Team
EPOCH_ID: EPOCH-20261005-b35ee1bf-608426cb
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_BRANCH: NEXY.AI-Test-AI
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SOURCE_TREE: e7f603d06db6475a4d72f5d0aed752213d17eb16
TASK_ID: TASK-DOC-C3-API-HANDLER-STATE-INTEGRITY-001
FINDING_ID: FIND-DOC-C3-API-HANDLER-FALSE-FREEZE-001
SOURCE_MUTATION: NONE
REVIEW_VERDICT: FINDING_CONFIRMED
REPAIR_ELIGIBILITY: BLOCKED_BY_INC-BRANCH-NAMESPACE-001

## Authority checked

Primary DOCX final verdict states build obligation comes from DOC-C only.
Final DOC-C §3.2 requires SystemEnvelope<T>.state: SystemState.
Final DOC-C §4.1 requires all responses to use SystemEnvelope<T> and each route to retain its declared error-matrix authority.

Verified control packets:
- REQ-DOC-C-3-2-SYSTEM-ENVELOPE
- REQ-DOC-C-4-1-GLOBAL-API-LAW

## Source facts at exact SHA

apps/web/lib/api-handler.ts generic catch currently:
- logs a redacted API_UNHANDLED_EXCEPTION record;
- returns HTTP 500;
- serializes status=DEGRADED;
- hardcodes state=FREEZE;
- serializes DEPENDENCY_FAILURE;
- does not call transitionSystemState;
- does not call currentSystemState.

packages/orch-core/system-state.ts exposes currentSystemState() as the process-global canonical runtime state boundary. Legitimate transitions persist through transitionSystemState/transitionSystemStateTransactionally and emit the associated durable transition evidence.

tests/contract/api-handler.test.ts currently encodes the wrong oracle by requiring state=FREEZE for an arbitrary thrown handler exception.

## Why this is a defect

The wrapper reports a legal canonical SystemState value that was neither observed from the state boundary nor produced by a legal FSM transition. This turns a transport/error fallback into fabricated authoritative state.

The defect is not that FREEZE is an invalid SystemState. The defect is that the wrapper claims FREEZE regardless of actual runtime state.

## Minimal semantics-preserving repair design

1. Import currentSystemState from packages/orch-core/system-state.js.
2. In the catch path, snapshot currentSystemState() and use that value as SystemEnvelope.state.
3. Do not invoke transitionSystemState from this generic wrapper.
4. Do not create EventLog/incident/FSM evidence from this generic wrapper.
5. Preserve redaction and non-successful HTTP behavior.
6. Do not broaden or rewrite route-specific error semantics in this task.

## Required oracle repair

Replace the current test expectation that hardcodes FREEZE.

Required mutation-killing case:
- reset runtime state to READY (or another non-FREEZE canonical state);
- execute runApiHandler with a handler that throws;
- assert HTTP 500;
- assert envelope.state equals the actual currentSystemState value, not FREEZE;
- assert currentSystemState remains unchanged after the exception;
- assert thrown secret/error text remains absent from logs and response.

A second parameterized state case is recommended to prevent a one-off READY hardcode.

## Red-team checks

- Do not "repair" by transitioning to FREEZE in the catch. A real FREEZE transition has persistence/incident/audit requirements and would grant the web transport wrapper authority it does not have.
- Do not omit state from the envelope. DOC-C §3.2 requires it.
- Do not weaken error redaction.
- Do not mutate protected upstream NEXY.ai.
- Do not mutate NEXY.AI-Test-AI directly to bypass worker isolation.

## Blocker

INC-BRANCH-NAMESPACE-001 remains OPEN. refs/heads/NEXY.AI-Test-AI conflicts structurally with required worker refs refs/heads/NEXY.AI-Test-AI/work/<TASK_ID>. Under V8 branch law, source repair remains frozen until the worker namespace policy is changed explicitly.

## Closure effect

- ACTIONABLE_CODE_GAP: CONFIRMED
- GAP_FIXED: NO
- VERIFIED_CLEAN: NO
- REVERIFY_REQUIRED: YES
- CODE_CLOSURE_ELIGIBLE: NO
