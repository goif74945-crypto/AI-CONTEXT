# Verification Evidence

## Environment

- Node: `v22.16.0`
- npm: `10.9.2`
- available TypeScript: `5.8.3`
- compiler target: ES2022, Node16 module/moduleResolution, strict, exactOptionalPropertyTypes, noUncheckedIndexedAccess, noImplicitReturns

## E1 static

Command:

```text
tsc -p tsconfig.json
```

Observed: exit 0 with no TypeScript diagnostics.  
Status: `PASS` for the standalone package under TypeScript 5.8.3.

Exact current NEXY package manifest declares TypeScript `^6.0.3`. Attempted command:

```text
npx -y -p typescript@6.0.3 tsc -p tsconfig.json
```

The isolated environment timed out while fetching the compiler before it reported a compiler version or build result.  
Status: `NOT_VERIFIED` for exact TypeScript 6.0.3 parity. The 5.8.3 PASS must not be promoted into 6.0.3 evidence.

## E2 unit/regression

Command:

```text
node dist/tests/run-tests.js
```

Observed summary: `passed=26 failed=0`.

Coverage includes positive behavior, negative/fail-closed behavior, mandatory-budget blocking, malformed contract quarantine, disagreement policy validation, Shapley conservation, and order invariance for all five proposal systems.

## E3 standalone composition

Executed test: `observed-contract output composes with verification scheduling without authority promotion`.

Observed: OCM preserved `NOT_VERIFIED` and `UNKNOWN`; VVS selected the mandatory deployment-proof claim; no marker became PASS.  
Status: `PASS` for local OCM→VVS component composition only.

## Collision evidence

Exact lexical collision searches for the selected mechanism terms returned no exact implementation hits at scan time. This supports `no obvious exact collision observed`, not `globally novel`.

## NEXY protected-scope evidence

NEXY implementation repo was only read. No create/update/delete/branch/commit/merge/ref mutation tool was used against `goif74945-crypto/NEXY.AI-`.

## Limitations

- No NEXY native integration was run.
- No database/API/browser/runtime/deployment test was run against NEXY.
- SEG floating-point thresholds remain advisory.
- COCL depends on externally justified coalition values and is not causal proof.
- VVS expected-risk reduction is only as good as its explicit input estimates.
