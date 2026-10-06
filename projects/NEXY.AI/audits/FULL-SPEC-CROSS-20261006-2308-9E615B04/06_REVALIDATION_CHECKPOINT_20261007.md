# FULL-SPEC-CROSS revalidation checkpoint — 2026-10-07

STATUS: IN_PROGRESS
MODE: AUDIT_ONLY / CROSS_CHAT / READ_ONLY_PRODUCT_REPOSITORY
PRODUCT_REPOSITORY: goif74945-crypto/NEXY.AI-
BRANCH: NEXY.ai
HEAD_SHA_REVALIDATED: 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43
TREE_SHA_REVALIDATED: a809bc5f4cc2d8f806e500d1d3a09a4e66450c7c
SPEC_SHA256_REVALIDATED: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
PRODUCT_MUTATION: NONE
BUILDER_EXECUTION_COMMAND: FORBIDDEN_UNTIL_FINAL_GATE

## Source identity revalidation
- Library authoritative DOCX materialized from file_00000000387c82078aecef8cd38fe808.
- Byte size: 2146350.
- SHA-256 independently revalidated to the canonical source SHA above.
- OOXML traversal: 12537 body paragraphs; 10979 non-empty paragraphs; 15044 word/document.xml text nodes.
- Prior cross-chat source coverage map remains exact-source-bound and reports 293/293 pages read. This checkpoint does not replace the authoritative source with the matrix.

## Repository inventory staleness gate
- Current recursive tree: 1084 entries = 881 blobs + 203 trees; truncated=false.
- 02_REPOSITORY_INVENTORY.json re-compared against current Git tree by path/type/SHA.
- missing_in_inventory=0
- extra_in_inventory=0
- sha_mismatch=0
- type_mismatch=0

## Requirement ledger state before this checkpoint
- Explicit current-scope audit rows: 773/773; unique IDs: 773; duplicate IDs: 0.
- PASS_VERIFIED=162
- PARTIAL_VERIFIED=15
- FAIL_VERIFIED=3
- MISSING_PROVEN=1
- SCOPE_VIOLATION=7
- NOT_VERIFIED=585
- All 773 rows are bound to HEAD 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43.
- NOT_VERIFIED is not PASS and not FAIL.

## Fresh finding revalidation

### FIND-P0-0003 / REQ-0207 — still fresh
Claim: Global FREEZE does not atomically close output emission for a previously STABLE/releaseable pipeline run.
Fresh exact-head evidence:
- packages/queue/run-state.ts::emitAuthorizedPipelineOutput locks only pipeline-run:<id>, reads only PipelineRun release/output state, and does not read/lock global SystemState.
- packages/api/directives.ts::_handleGetDirective calls emitAuthorizedPipelineOutput when the run is STABLE+accepted+releaseable without a pre-emission global FREEZE/STOP gate.
- packages/orch-core/system-state.ts global FSM uses a distinct nexy:global-fsm advisory lock.
- The global STOP path explicitly acquires pipeline-run locks and cancels non-terminal dispatches; the FREEZE path does not perform the equivalent global per-run release revocation.
Disposition: FAIL_VERIFIED / P0 remains supported.

### FIND-P1-0002 / REQ-0289 — newly revalidated for ledger update
Claim: The configured 60-second OTAC resend cooldown is advertised but not enforced as a one-resend-per-60s admission law.
Fresh exact-head evidence:
- packages/api/vnext-config.ts: otac_resend_cooldown_ms=60000.
- packages/api/auth.ts uses requestOtacLimiter for admission and returns cooldown_seconds derived from the config after successful issuance.
- packages/api/middleware/rate-limit.ts requestOtacLimiter default is max=3/windowMs=60000.
- Exact repository search for otac_resend_cooldown_ms finds config/evidence/static-value check/response/contract-value test, but no separate durable cooldown admission enforcement.
- cooldown_seconds search finds only response behavior and an integration assertion that it is numeric.
Disposition: FAIL_VERIFIED / P1 is supported for REQ-0289. Durable/race-safe enforcement scope key must follow authoritative spec; do not invent one.

### FIND-P1-0001 / REQ-0164..REQ-0172 — still fresh
Claim: The current FSM preserves event names/ownership/transitions but does not enforce the DOC-C typed lifecycle-event payload contracts at the FSM boundary.
Fresh exact-head evidence:
- packages/core/vnext-state-matrix.ts defines VNextEvent as a string union derived from VNEXT_EVENT.
- transitionSystemState(event, actor, ctx) accepts event name plus independent SetStateContext/guards.
- Broad exact repository searches did not find boundary event payload schemas carrying required results_count/evidence_count/reason/actor_id fields. Some similarly named fields exist elsewhere, but not as the required discriminated event contract.
Disposition: PARTIAL_VERIFIED / P1 remains supported.

### FIND-P0-0001 / REQ-0677..REQ-0682 + REQ-0768 — still fresh
Claim scope: Current SWARM execution imports/uses intelligence layers classified by the canonical source normalization as future/conceptual, while no verified current DOC-C promotion record was found in the checked current authority set.
Fresh exact-head evidence:
- packages/swarm/pipeline.ts imports IRL, CIRL, DSL, RSEL, ECL, CLE, Trinity, certainty, and Lo3 prompt-law functionality directly.
- config/experimental-scope.ts itself states later-era extension tests require explicit spec-extension/version promotion.
- Canonical Source Coverage classifies L1o/Lo3/Lo2 intelligence vision (doc paragraph range 11016–12024) as FUTURE DESIGN unless explicitly promoted.
- Current AI-CONTEXT promotion search returned no verified L1o/Lo3/Lo2 DOC-C promotion record.
Disposition: SCOPE_VIOLATION / P0 remains supported. Absence claim is limited to the current authority set searched and must not be generalized beyond that evidence.

## Exact-head CI revalidation
At HEAD 9e615b04... current GitHub Actions runs remain failed:
- 37222997798 Exact HEAD test evidence — failure
- 37222997784 Six-system exact HEAD evidence — failure
- 37222997743 NEXY CI / Deploy Gate — failure
- 37222997736 Layer8 Cargo lock evidence — failure
Within deploy gate: Contract tests, TypeScript typecheck, Integration tests, Browser E2E, Full test suite, advisory Phase-F validation, Coverage measurement, Production web build, and Static determinism gate failed. DOC-C static gate, release attestation, and deploy were skipped.
Job-log download currently returns GitHub BlobNotFound/404, so assertion-level CI failure causes remain BLOCKED and must not be guessed.

## Remaining gate work
- Reconcile/update REQ-0289 and any other fresh findings into the requirement ledger.
- Inspect all current decisive non-PASS rows and deduplicate structural drift findings.
- Finish negative-claim register and NOT_VERIFIED register.
- Recheck current TASKS/CASES/FAILURES/LEDGER relevant to this exact HEAD.
- Run final head/staleness/dedup/conflict gates and metrics.
- Only after the final audit gate may BUILDER_EXECUTION_COMMAND be generated or emailed.
