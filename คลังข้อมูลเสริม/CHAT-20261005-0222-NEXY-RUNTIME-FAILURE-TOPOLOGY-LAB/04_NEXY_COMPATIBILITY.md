# NEXY Compatibility Boundary

Status: **READ-ONLY COMPATIBILITY PROPOSAL / NOT_INTEGRATED**

## Observed NEXY snapshot
- repository: `goif74945-crypto/NEXY.AI-`
- branch: `NEXY.ai`
- exact read-only SHA: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
- mutation performed by this mission: **NONE**

Observed exact contract blobs:
- `packages/contracts/directive.ts` -> `29cc017aeff76ebaf5a253dc6831ebcf3f7c86c4`
- `packages/contracts/evidence.ts` -> `6b50f4cf9c0ca7e4c056fc546976e6e5a52d5895`
- `packages/contracts/state.ts` -> `04efcc7161c5415922e11e16174013d1d4ea40a3`
- `packages/contracts/envelope.ts` -> `daf1156b3431150e667b5e18727d8abe9bdc9b75`
- `packages/contracts/release-policy.ts` -> `a52354b950c268f2c8fd07d95475d72e7fa26191`
- root `package.json` -> `972cd03ed7878ff6eb0cb4813e459cb0c29cd1e7`

## Observed compatibility anchors
- Directive requests carry stable request/project identity, explicit mode/priority/constraints, operator role, schema version, and `idempotency_key`.
- Evidence items carry content hash, confidence, verification flag, collection identity, contradiction status, anchors, and normalization version.
- Canonical `SystemState` is `INIT | READY | RUNNING | VERIFYING | CONSENSUS | STABLE | FREEZE | STOP`.
- Wire envelopes can carry warnings and canonical freeze reasons while preserving canonical status/state.
- ReleasePolicy remains NEXY-owned and cannot be replaced by this lab.

## Proposed adapter rules
1. **Deadlock Sentinel** should consume NEXY-owned wait/lease telemetry through a versioned adapter. It must not infer wait edges from free-form model prose.
2. **Livelock Detector** should consume authoritative state fingerprints/progress counters. A future adapter must define what counts as progress; the detector must not invent that ontology.
3. **Retry Governor** may use the directive idempotency identity as one input, but existence of an idempotency key alone is not proof that an arbitrary side effect is safe to retry. Retryability/idempotency must remain explicit authoritative facts.
4. **Poison Quarantine** should bind to input identity + executor/adapter revision + normalized failure signature. It must not globally quarantine a provider from one bad input.
5. **Partial Salvage** may reference canonical NEXY Evidence IDs/hashes, but it must not create fake EvidenceItem verification or overwrite the Vault/evidence store.
6. Diagnostic outputs may eventually be translated into an `EnvelopeWarning` or a candidate canonical `FreezeReason` only by NEXY-owned policy. This lab itself cannot add a new SystemState.

## Compatibility claim
`PASS` for this document means only that an isolated advisory adapter boundary can be described without changing the observed canonical contracts. Runtime integration, release behavior, telemetry completeness, and production recovery remain `NOT_VERIFIED`.
