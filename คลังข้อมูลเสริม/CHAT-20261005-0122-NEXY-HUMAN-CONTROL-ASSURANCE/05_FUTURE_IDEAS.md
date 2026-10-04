# Future System Ideas

Every item in this file is **AI-PROPOSED CONCEPT ONLY**. None is a current NEXY.AI requirement or implementation claim.

## 1. Control-Surface Trace Binding (CSTB)
Bind each manifest action ID to backend route/action IDs, E2E test IDs and audit-event IDs. A release report could then prove that the control the human saw corresponds to the action the backend executed.

Failure mode: stale bindings create false confidence. Required safeguard: exact revision/hash on every binding and automatic invalidation when either side changes.

## 2. Freeze Visibility Attestation (FVA)
A browser-level verifier could inject FREEZE states at every critical route and assert that the freeze banner remains visible, sticky, unmaskable and higher priority than ordinary success/pending UI.

Failure mode: CSS/portal/z-index differences across viewports. Required evidence: mobile + desktop E4 browser tests, not static HCAS PASS.

## 3. Confirmation Proof Envelope (CPE)
For high-impact actions, serialize the target, action, consequence summary, expected revision and confirmation method into a signed/hashed confirmation envelope that the backend validates before mutation.

Failure mode: confirmation replay or target drift. Required safeguard: one-time nonce, exact target revision and expiration policy if promoted.

## 4. Consequence Preview Engine (CPE-2)
Before an irreversible action, compute a read-only blast-radius preview from current state and show what will become unreachable/deleted/revoked.

Failure mode: preview becomes stale before execution. Required safeguard: execution must compare the preview's state hash/revision and reject on drift.

## 5. Surface-to-Authority Bisimulation Check
Model the UI action graph and backend authorization graph and verify that every visible mutating edge maps to exactly one authorized backend transition, while no hidden UI condition becomes a permission source.

Failure mode: incomplete graph extraction. Promotion requires explicit coverage proof and a machine-readable backend action registry.
