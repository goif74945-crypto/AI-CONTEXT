FINDING_ID: F-V8-QUEUE-RUN-FSM-001
REQ_ID: DOC-C-5-STATE-MATRIX
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SEVERITY: P1
STATUS: REPRODUCED_BY_SOURCE_TRACE

OBSERVED:
packages/queue/run-state.ts recordPipelineRunFailure() writes PipelineRun.runState=FREEZE for any current run state unless a caller explicitly supplies expectedStates.
packages/queue/workers.ts failed handler calls recordPipelineRunFailure() without expectedStates.
processJob() can fail before setPipelineRunState(...,"RUNNING"), while API-created PipelineRun state is READY.
The same generic failed handler can also receive failures after CONSENSUS.

EXPECTED:
Final DOC-C section 5.2 is the executable SystemState matrix. READY has execute->RUNNING only. Error->FREEZE is authorized from RUNNING and VERIFYING. CONSENSUS reaches FREEZE through rejected or timeout. Any run state exposed as SystemState must not bypass these transitions.

REPRODUCTION:
1. packages/api/directives.ts creates PipelineRun with runState READY.
2. packages/queue/workers.ts validates TSA/payload and durable run boundary before READY->RUNNING.
3. A pre-RUNNING exception reaches worker.on("failed").
4. failed handler invokes recordPipelineRunFailure without expectedStates.
5. recordPipelineRunFailure updates runState to FREEZE without a default legal-state guard.
6. tests/contract/pipeline-failure-incident-linkage.test.ts currently mocks READY and expects recordPipelineRunFailure to succeed, encoding the permissive oracle.

IMPACT:
Illegal state transition / contract drift, misleading incident/event evidence, and divergence between canonical DOC-C matrix and durable PipelineRun state.

SAFE_DIRECTION:
Do not invent new DOC-C edges. Enforce legal source-state/event semantics at the durable failure boundary. Pre-admission queue failures must remain fail-closed without manufacturing READY->FREEZE. Update the test oracle accordingly. Exact repair must preserve incident/evidence requirements and validate CONSENSUS failure semantics separately.

SOURCE_MUTATION:
NONE; worker-branch namespace remains blocked by INC-BRANCH-NAMESPACE-001.
