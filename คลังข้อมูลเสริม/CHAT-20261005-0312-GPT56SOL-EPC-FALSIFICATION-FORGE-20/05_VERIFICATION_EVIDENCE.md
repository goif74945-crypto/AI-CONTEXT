# Verification Evidence — EPC Falsification & Experimental Design Forge 20

CHAT_ID: `CHAT-20261005-0312-GPT56SOL-EPC-FALSIFICATION-FORGE-20`
Authority class: `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING`

## Evidence classes

- **E0 repository presence/readback:** PASS for production source, tests, scripts and config persisted at AI-CONTEXT commit `d260b12b0ec86f0da0731f08b2881df7511af666`. GitHub readback matched all 18 expected Git blob SHAs.
- **E1 static/type:** PASS on the exact tested bytes.
- **E2 unit/property/negative:** PASS on the exact tested bytes.
- **E3 standalone package integration/replay:** PASS.
- **E4 NEXY end-to-end integration:** NOT_VERIFIED and deliberately out of scope because NEXY.AI- is protected read-only.
- **E5 production operational behavior:** NOT_VERIFIED.
- **E6 deployment:** NOT_VERIFIED.

## TDD and repair chain

1. Tests were executed before production implementation. The first RED run failed because `dist/index.js` did not exist.
2. Initial implementation reached GREEN.
3. Exact read-only NEXY source inspection exposed a Q64 compatibility defect: the forge originally rounded a ratio while inspected NEXY fixed-point ratio construction truncates using integer division.
4. Q64 ratio/decimal ingestion was repaired to truncate toward zero.
5. Minimal Falsifier Planner was strengthened from greedy selection to exact bounded dynamic programming over total Q64 cost.
6. Experiment Independence Auditor was strengthened to emit a deterministic root-disjoint subset.
7. A modular refactor intentionally preserved a failing compiler log when imports were incomplete; only import-boundary defects were repaired, then the full suite was rerun.
8. Final verification after documentation updates remained GREEN.

## Final local verification

Command:

```text
npm run verify
```

Observed result:
- strict TypeScript compilation: PASS;
- static scan: `STATIC_VERIFY_PASS files=10 forbidden_patterns=0 mechanism_registry=20 authority_boundary=present`;
- automated tests: **36 PASS / 0 FAIL**;
- deterministic replay: **1000/1000 identical**;
- replay capsule checksum: `88a0bc16733ba135`;
- replay checksum algorithm: `FNV1A64_NON_SECURITY` (explicitly non-security; SHA-256 is used for artifact identity outside the runtime helper).

## Persisted exact-byte proof

The following 18 production/test/config files were read back from GitHub at `d260b12b0ec86f0da0731f08b2881df7511af666` and their Git blob SHAs matched the blobs created from the locally tested bytes:

- 10 TypeScript source files under `src/`;
- 4 Node test files under `tests/`;
- 2 verification scripts under `scripts/`;
- `package.json`;
- `tsconfig.json`.

Readback summary: **18/18 exact Git blobs**.

The SHA-256 identities of the tested source/test/script bytes are preserved in `evidence/13_FINAL_MODULAR_TESTED_SHA256.txt`.

## Protected-repository scope

The mission has not written to `goif74945-crypto/NEXY.AI-`. NEXY source was used only for read-only compatibility/authority inspection. No claim of production integration is made.

## FACT / ASSUMPTION / UNKNOWN

**FACT**
- exactly 20 mechanism IDs are statically locked and test-covered;
- authoritative quantitative paths use Q64.64 BigInt representation with signed-128 range checks;
- no `Math.random`, `Date.now`, `performance.now`, `parseFloat`, `Number(...)`, crypto randomness or network I/O appears in the authoritative source scan;
- PEDC is advisory and `autoPromote=false`;
- exact tested production/test/config bytes are persisted and read back.

**ASSUMPTION**
- a future authorized NEXY adapter can consume these deterministic contracts without changing their authority boundary.

**UNKNOWN / NOT VERIFIED**
- full NEXY import/build compatibility;
- cross-language exhaustive Q64 conformance across every signed edge case;
- production database/queue/UI/provider integration;
- deployment performance and operational behavior.
