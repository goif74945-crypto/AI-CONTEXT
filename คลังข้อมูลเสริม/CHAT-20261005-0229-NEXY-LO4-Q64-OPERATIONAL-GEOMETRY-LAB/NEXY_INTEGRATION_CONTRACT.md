# NEXY.AI Read-Only Integration Contract

Status: `CONTRACT_READY / RUNTIME_NOT_INTEGRATED / NOT_CANON`
Work code: `CHAT-20261005-0229-NEXY-LO4-Q64-OPERATIONAL-GEOMETRY-LAB`

This file is a Lo4 proposal. It does not modify, promote, or govern NEXY.AI.

## Read-only target inspected

Repository: `goif74945-crypto/NEXY.AI-`
Default branch observed: `NEXY.ai`

Relevant current surfaces inspected:
- `core-kernel/src/engine/fixed128_math.rs`
- `packages/queue/workers.ts`
- `scripts/check-module-boundaries.ts`
- root `Cargo.toml`
- root `package.json`
- repository orientation `README.md`

## Compatibility facts

### Numeric representation — aligned

Current NEXY Core defines signed Q64.64 as an `i128` raw integer where value = raw / 2^64, with:
- `ONE = 1 << 64`
- signed i128 minimum/maximum bounds
- no wrapping arithmetic
- division-by-zero and overflow fail closed into `freeze()`
- authoritative multiplication/division producing truncation toward zero for signed results.

The Lo4 reference substrate uses the same:
- 64 fractional bits
- signed 128-bit raw bounds
- raw integer canonical value
- default multiplication/division rounding toward zero
- deterministic error/freeze on overflow or zero division
- floating-point input forbidden at authoritative boundaries.

Therefore the **numeric semantic contract is aligned** for default Core-style operations.

### Runtime language boundary — not drop-in

Current NEXY is a Rust workspace with TypeScript runtime packages. This Lo4 laboratory reference implementation is Python. It is therefore **not** legal to claim direct module-import compatibility.

Promotion must use one of these bounded approaches:
1. port the verified algorithms to Rust using the existing NEXY `Fixed128` implementation; or
2. port the orchestration-facing algorithms to TypeScript using canonical BigInt raw-Q64 values while preserving i128 bounds and freeze semantics; or
3. introduce an explicitly authorized external adapter process only if future Canon permits that dependency.

Option 1 is preferred for any authoritative Core path. Option 2 is suitable only for a permitted non-Core/experimental control surface. Option 3 must not be assumed legal.

## Proposed wire contract

All quantitative fields cross the adapter boundary as **decimal strings containing signed raw Q64.64 integers**, never IEEE-754 JSON numbers.

Example envelope:

```json
{
  "schema": "nexy.lo4.operational_geometry.v1",
  "proposal_status": "Lo4_AI_PROPOSAL_ONLY",
  "engine": "queue_stability_margin",
  "request_id": "opaque-caller-id",
  "inputs": {
    "arrival_raw": ["55340232221128654848"],
    "service_raw": ["110680464442257309696"]
  }
}
```

Rules:
- each `*_raw` value parses exactly to signed i128;
- out-of-range, malformed, missing, oversized, or unexpected fields fail closed;
- no float or locale-dependent decimal is admitted;
- list lengths retain the bounded limits in the reference design;
- tie breaking is index-stable and deterministic;
- result objects must include an engine identifier and deterministic state/action, but must not mint Canon authority.

## Queue/runtime placement hypothesis

Current NEXY queue worker resolves durable runtime configuration, validates stale jobs using verified TSA time, applies bounded queue concurrency, and fails closed on dependency loss. The proposed operational-geometry systems are therefore best treated as a **pre-release scheduling/admission advisory layer** during Lo4 experimentation, never as a bypass around LAW/JUDGE/SWARM.

A future promoted adapter may consume only already-authorized/durable metrics such as:
- queue depth/history,
- bounded capacity,
- verified time/deadline data,
- retry counts,
- service/arrival rates,
- tenant budgets,
- explicitly provided utility/cost vectors.

Its output may recommend:
- admission,
- defer,
- shed,
- degraded-mode proposal,
- ordering,
- capacity allocation.

It may **not**:
- authorize final release;
- override LAW, JUDGE, Safety Kernel, or canonical FSM transitions;
- synthesize unverified wall-clock time;
- convert host floats into authoritative Q64 values;
- mutate Canon merely because Lo4 returned a value.

## Module-boundary constraint

Current boundary tooling defines protected UI/API/CORE/LAW/SWARM/JUDGE/VAULT/AUTH/OBS edges. A future port must pass the repository's boundary checker. This proposal does not prescribe a new legal edge.

Initial experimental placement should remain outside Canon, for example an isolated experimental package, until a promotion decision chooses the legal module and updates the authoritative source.

## Promotion acceptance gates

Before any NEXY mutation or Canon adoption:
1. ported implementation must use existing NEXY Q64.64 semantics byte-for-byte at the raw-value boundary;
2. cross-language golden vectors must match the verified Python reference for every engine;
3. signed minimum/maximum and overflow paths must match fail-closed behavior;
4. deterministic tie-breaking and canonical serialization must be identical across repeated runs;
5. NEXY module-boundary, typecheck, static-determinism and applicable test suites must pass;
6. current DOC-C/Canon must explicitly permit the integration point;
7. exact-head evidence must bind tests to the promoted bytes;
8. Lo4 status remains non-governing until formal promotion.

## Verification status

- Q64.64 semantic alignment with current NEXY Core: **VERIFIED BY READ-ONLY SOURCE REVIEW**
- Queue/control-plane relevance: **VERIFIED BY READ-ONLY SOURCE REVIEW**
- Legal future placement: **PROPOSAL / REQUIRES PROMOTION DECISION**
- Direct Python import into current NEXY runtime: **NOT COMPATIBLE / NOT CLAIMED**
- Rust/TypeScript port equivalence: **NOT VERIFIED**
- NEXY runtime integration/deployment: **NOT VERIFIED**
