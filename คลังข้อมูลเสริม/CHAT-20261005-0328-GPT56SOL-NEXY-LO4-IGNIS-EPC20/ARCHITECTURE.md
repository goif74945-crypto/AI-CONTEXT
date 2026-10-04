# ARCHITECTURE

`caller -> future adapter -> canonical input -> evaluate(Sxx) -> PASS|FREEZE + evidence_root`

The kernel is side-effect free. It cannot enqueue, cancel, revoke, export, release, mutate Canon, mutate CORE, or promote itself.

## Q64.64 law
- representation: signed i128 raw integer with 64 fractional bits;
- range: `[-2^127, 2^127-1]` raw;
- overflow: fail closed, never saturate;
- divide by zero: fail closed;
- underflow/rounding: integer truncation toward zero after exact scaling;
- comparison: signed raw integer;
- serialization: `q64:<signed-decimal-raw>`;
- binary floating point: forbidden anywhere in evaluator authority input;
- NaN/Infinity/silent wrap/silent saturation: no authority.

## Determinism
Canonical JSON-like inputs only, deterministic Unicode scalar ordering, SHA-256 semantic receipt, no wall clock/random/network/filesystem/database/environment/locale dependencies.

## Current NEXY compatibility observation
At commit `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`, Lo3 has checked bigint Q64, while current prerelease/consensus/run-state paths also use JavaScript `number`, and run-state converts via rounding/clamping. This Lo4 kernel therefore requires an explicit adapter and forbids silent inheritance of float/clamp semantics.
