# Task Contract — Cross-FSM Integrity Lab

## OBJECTIVE
Build and verify a standalone reference toolkit that models multiple independent FSMs without flattening them, checks their cross-event contracts, audits freeze/stop propagation, explores bounded composite state space, and rejects stale cross-epoch events.

## TARGET
`คลังข้อมูลเสริม/CHAT-20261005-0156-NEXY-CROSS-FSM-INTEGRITY-LAB/` inside `goif74945-crypto/AI-CONTEXT` on the default branch.

## AUTHORIZED SCOPE
Create only new files under the target namespace; read AI-CONTEXT elsewhere for source grounding and collision avoidance; execute authored code/tests in an isolated local workspace.

## PROTECTED SCOPE
- Any repository whose name contains `NEXY.AI`.
- Existing sibling supplemental projects.
- Canonical NEXY source/spec files.
- Production/deployment systems.
- Credentials, secrets, private keys, session tokens.
- Hidden chain-of-thought.

## SOURCE FACTS DRIVING THE DESIGN
- NEXY has multiple independent FSMs; source explicitly warns that collapsing them destroys semantics.
- DOC-C execution states include INIT, READY, RUNNING, VERIFYING, CONSENSUS, STABLE, FREEZE, STOP.
- Queue states include QUEUED, RUNNING, SUCCEEDED, FAILED, CANCELLED, EXPIRED.
- FREEZE blocks release and new non-owner execution and cancels pending release work.
- STOP is irreversible in current build model and cancels all queue jobs.
- Recovery starts a new execution cycle; an old queue job must never be resumed.
These are source-derived requirements/design facts, not claims about current runtime implementation.

## FIVE SYSTEMS
### CFCC — Cross-FSM Contract Compiler
Compile machine-local transitions plus explicit routed-event contracts into deterministic canonical form. Reject duplicate IDs, unknown states/events, illegal transition endpoints, ambiguous ownership, and malformed routing.

### HCV — Handshake Compatibility Verifier
Validate that every routed event has a legal producer state/transition and a legal consumer transition/guard shape, with compatible schema/version and no owner inversion.

### FPA — Freeze Propagation Auditor
Given propagation requirements and machine capabilities, compute closure of FREEZE/STOP signals and identify any affected machine that can still perform forbidden mutation/release transitions after propagation.

### CSE — Composite State Explorer
Boundedly explore the product of independent FSM states plus an explicit FIFO event queue. Detect reachable forbidden composite states, deadlocks with pending obligations, illegal routed transitions, and bounded livelock witnesses.

### EESG — Event Epoch & Staleness Guard
Bind routed events to execution epoch/run lineage. Reject stale events, cross-run release tokens, and pre-recovery queue events that attempt to affect a newer execution cycle.

## IMMUTABLE REQUIREMENTS
- No engine executes real actions.
- No network or subprocess invocation in library core.
- Python standard library only.
- Canonical output for semantically equivalent normalized inputs.
- Fail closed on malformed/ambiguous contracts.
- Each engine must have positive + negative tests.
- Integration fixture must demonstrate current-source-inspired execution/queue freeze + recovery behavior without claiming NEXY runtime integration.
- All AI-generated design extensions must be labeled non-authoritative.
- Completion claims require executed evidence against the exact published content.

## REQUIRED EVIDENCE
- E0: repository file presence and read-back.
- E1: Python compilation/import/static sanity.
- E2: unit, adversarial, determinism and model-check behavior tests.
- E3-like standalone integration: five engines composed on synthetic/source-inspired fixtures.
- Exact-byte or cryptographic manifest binding published executable/test artifacts to verified local bytes.

## ACCEPTANCE CRITERIA
1. Five engines exist as independently callable modules.
2. Contract compiler rejects structurally invalid models.
3. Handshake verifier finds producer/consumer/schema mismatches.
4. Freeze auditor proves safe closure for a safe fixture and finds at least one unsafe residual path in an unsafe fixture.
5. Composite explorer finds a modeled deadlock/forbidden state and accepts a safe bounded model.
6. Epoch guard rejects stale pre-recovery events and accepts same-epoch events.
7. Full suite passes after any remediation.
8. Published source/test bytes match the tested manifest.
9. No protected path is mutated.

## STOP / FREEZE CONDITIONS
Freeze this mission if target identity becomes ambiguous, safe additive publication is impossible, a required write would touch NEXY.AI, authoritative sources conflict materially, or verification cannot be bound to published bytes.
