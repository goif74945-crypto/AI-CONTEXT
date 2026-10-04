# EPC Deterministic Interop Court 20 (DIC20)

**Status:** Lo4 AI proposal / experimental / non-Canonical / non-governing  
**Chat work ID:** `CHAT-20261005-0314-GPT56SOL-EPC-DIC20`

DIC20 is a standalone deterministic reference oracle for evaluating whether an experimental NEXY/EPC proposal preserves the same semantics across language, runtime, numeric, serialization, and migration boundaries.

It is deliberately **not** a promotion engine. It cannot mutate NEXY Core state, Canon, LAW, JUDGE, SWARM state, repositories, or production. Its final verdict is advisory evidence only.

## Why this exists

NEXY currently spans TypeScript and Rust surfaces and uses Fixed128/Q64.64 in authoritative paths. A proposal can be individually correct yet become unsafe when one runtime rounds, normalizes Unicode, orders keys, encodes integers, maps errors, or migrates state differently. DIC20 treats those boundary differences as first-class proof obligations.

## Twenty court systems

`DIC01` Q64 arithmetic parity · `DIC02` overflow boundary · `DIC03` division/rounding · `DIC04` canonical i128 decimal codec · `DIC05` canonical JSON · `DIC06` Unicode NFC · `DIC07` key ordering · `DIC08` domain-separated hashing · `DIC09` schema projection · `DIC10` error semantics · `DIC11` state enum wire tags · `DIC12` tick/time fence · `DIC13` null/absent/default · `DIC14` signedness/width · `DIC15` decimal-to-Q64 parser · `DIC16` golden vectors · `DIC17` replay transcript · `DIC18` deterministic reducer · `DIC19` versioned migration · `DIC20` non-authoritative verdict aggregator.

## Deterministic numeric law

- signed Q64.64 raw domain: conceptual signed i128;
- scale: `2^64`;
- integer-only arithmetic;
- multiplication/division truncate toward zero;
- overflow and divide-by-zero fail closed;
- binary floating point is forbidden in the authoritative court core;
- i128 values cross JSON boundaries as canonical decimal strings/tags;
- untagged JSON integers are restricted to the cross-runtime safe interval `[-(2^53-1), +(2^53-1)]`.

## Run

```bash
./scripts/run_all.sh
python3 scripts/static_determinism_audit.py
node interop/node_verify.mjs evidence/golden-vectors.json
```

## Evidence boundary

A local PASS proves only this standalone package at the tested bytes. It does **not** prove NEXY integration, deployment, Canon promotion, or production readiness. Formal NEXY integration must be separately reviewed and promoted by authorized NEXY governance.
