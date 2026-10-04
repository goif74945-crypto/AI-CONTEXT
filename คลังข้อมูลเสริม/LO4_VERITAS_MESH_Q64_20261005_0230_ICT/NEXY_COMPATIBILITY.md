# NEXY.AI Compatibility Audit

Status: **READ-ONLY REPO FACT + INTEGRATION PROPOSAL**

## Read-only source evidence

Observed from `goif74945-crypto/NEXY.AI-`, branch `NEXY.ai`:

1. `core-kernel/src/engine/fixed128_math.rs`
   - blob SHA: `e0e1d4b3fa47d40ac9b30ae14ea8b7ae0ac58313`
   - defines signed Q64.64 as `i128`, `raw / 2^64`.
   - multiplication uses an exact 256-bit decomposition.
   - division is extended and fail-closed.
   - core overflow behavior diverges to `freeze()`.

2. `packages/phase-f/game/numeric-law.ts`
   - blob SHA: `62ec68ae19ec5554c7c357d5f9cae2838d1dba01`
   - uses `bigint` Q64.64.
   - defines `Q64_ONE = 1n << 64n`.
   - TypeScript profile uses deterministic saturating clamp.
   - division by zero fails closed.

3. `tsconfig.json`
   - blob SHA: `4f878346b620f042392958f4490f0e086576f3cb`
   - strict TypeScript, ES2022, Node16 resolution, exact optional types, unchecked indexed access enabled.

4. `package.json`
   - blob SHA: `972cd03ed7878ff6eb0cb4813e459cb0c29cd1e7`
   - TypeScript/Vitest/tsx toolchain exists in NEXY.AI.

5. `README.md`
   - blob SHA: `c1e8a04474c7bb5f4f3f30d8e201529be9381280`
   - explicitly distinguishes experimental/Phase-F material from canonical authority.

## Compatibility conclusion

### FACT

The raw Q64.64 ABI used here is compatible in representation with NEXY's observed Rust and TypeScript Q64.64 code: signed raw integer, 64 fractional bits, `1.0 = 1 << 64`.

### IMPORTANT POLICY DIFFERENCE

NEXY Rust core and TypeScript G15 do not share the same generic overflow action:

- Rust core: overflow -> `freeze()`.
- TypeScript G15: overflow -> saturating clamp.

VERITAS therefore does **not** claim generic arithmetic-policy identity with the Rust core.

### Safe integration boundary

All actual concept scoring inputs and outputs are `UnitQ64` in `[0,1]`. Weighted sums use arbitrary-precision `bigint` intermediates before dividing back into `[0,1]`. In that bounded scoring domain there is no signed-i128 overflow.

Recommended integration:

1. Keep VERITAS in experimental/Lo4 scope.
2. Exchange only validated raw Q64.64 strings or `bigint` values in `[0, 2^64]`.
3. Map to NEXY `Fixed128`/`fromRaw` only at a boundary that checks the unit invariant.
4. Treat the result as advisory evidence for promotion review, never as Canon authority.
5. If moved toward Rust core, reimplement formulas using canonical `Fixed128` and core freeze semantics, then rerun cross-language golden vectors.

## NOT VERIFIED

- No code from this project was inserted into NEXY.AI.
- No NEXY.AI integration test was run.
- No cross-language Rust/TypeScript golden-vector test was run because Rust toolchain is unavailable in the local execution sandbox.
- Therefore "drop-in integrated with NEXY core" is NOT VERIFIED.

The standalone TypeScript implementation is reusable immediately as an external/experimental package, but Canon integration still requires its own authorized change and evidence.
