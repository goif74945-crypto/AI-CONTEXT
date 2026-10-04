# NEXY Compatibility and Authority Proof

## Exact read-only baseline

- Repository: `goif74945-crypto/NEXY.AI-`
- Branch: `NEXY.ai`
- Inspected commit: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
- Inspected tree: `a809bc5f4cc2d8f806e500d1d3a09a4e66450c7c`
- Canonical NEXY-IGNIS source SHA-256 from AI-CONTEXT: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`
- Current normalized source matrix: 837 requirement rows.

No file in NEXY.AI- is a mutation target of this package or this mission.

## Q64.64 compatibility evidence

### NEXY core
`core-kernel/src/engine/fixed128_math.rs` at inspected commit, blob `e0e1d4b3fa47d40ac9b30ae14ea8b7ae0ac58313`:
- declares signed Q64.64 using `i128` raw representation;
- declares `1.0 = 1 << 64`;
- freezes on overflow and divide-by-zero;
- uses wide intermediate reasoning for multiplication and extended division;
- truncates signed numeric conversion toward zero.

### NEXY Lo3 governor
`packages/phase-f/lo3/governor.ts`, blob `7270c90a1debbf9c3ce3aada2aef6222b322c58c`:
- declares authoritative numeric scoring as signed Q64.64 carried by bigint;
- bounds raw values to signed i128 range;
- `q64FromRatio` uses integer fixed-point division;
- explicitly rejects divide by zero.

### Forge alignment
`src/q64.ts` therefore uses:
- raw bounds `[-2^127, 2^127-1]`;
- scale `2^64`;
- truncation toward zero for ratio/division;
- explicit errors on overflow/divide-by-zero;
- no binary floating-point authoritative calculations.

The forge is a reference package, not proof of byte-for-byte arithmetic equivalence across every NEXY implementation language. Cross-language conformance would be a separate E3/E4 integration task after adoption.

## Authority compatibility evidence

`packages/core/vnext-state-matrix.ts`, blob `27e1281fba330784cc3bf2c30e9e1e82f951479b`, assigns:
- `boot` and `execute` to CORE;
- `agents_done` to SWARM;
- `verified`, `accepted`, `rejected` to JUDGE.

`packages/intelligence/trinity.ts`, blob `055c056bd1e9e768565ecc9165702e37b171a305`, fixes:
- publisher = `EXTERNAL_JUDGE`;
- `implicitOverride = false`;
- `lo2MayOverrideCurrentDecision = false`;
- release = `JUDGE_PENDING` or `FREEZE`.

The forge mirrors that boundary by exposing only `ADVISORY_ONLY`, `READY_FOR_EXTERNAL_REVIEW`, `FALSIFIED`, `INSUFFICIENT_EVIDENCE` and `CONTINUE`. It contains no NEXY FSM actor or state-transition function.

## Intended future adapter location

A future authorized integration can place a thin adapter after Lo4 proposal creation and before external promotion/JUDGE review:

`Lo4 proposal -> forge experiment plan -> external execution/evidence -> PEDC dossier -> existing verification/JUDGE path`

The adapter must translate Forge exceptions into an existing fail-closed NEXY error/freeze path. It must not map `READY_FOR_EXTERNAL_REVIEW` directly to `accepted`.

## Out-of-scope compatibility claims

NOT VERIFIED:
- production NEXY import/build compatibility;
- database persistence integration;
- queue orchestration;
- UI integration;
- deployment performance;
- cross-language byte-for-byte Q64 equivalence for all signed edge cases;
- behavior in production provider/network environments.

Those claims require authorized integration and matching E3-E6 evidence and are intentionally not fabricated here.
