# Verification Evidence

Status vocabulary follows AI-CONTEXT: PASS / FAIL / PARTIAL / BLOCKED / NOT_VERIFIED / UNKNOWN / CONFLICT.

## Target
Standalone ATOQ reference implementation.
Local working directory during verification: /mnt/data/nexy_active_truth_ops_q5
NEXY implementation baseline inspected read-only: 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43

## Environment
Node v22.16.0
npm 10.9.2
TypeScript 5.8.3
Python 3.13.5

## E1 static evidence
Command: npm run typecheck
Observed: PASS, zero TypeScript diagnostics.

Static audit observed:
- source imports only node:crypto plus relative project imports;
- no filesystem/network/subprocess/process runtime surface in src;
- no direct protected NEXY.AI repository import;
- no TODO/TBD/PLACEHOLDER/FIXME/HACK marker in src/tests;
- audited source/tests/config size: 2025 lines.
Status: PASS.

## E2 unit/adversarial
Command: npm run test:unit
Observed: 26/26 PASS.
Coverage includes positive and fail-closed cases for AEAP, RCTC, IDW, CDPP, CRG and structural NEXY adapters.
Status: PASS.

## E2 property/invariance
Command: npm run test:property
Observed: 5/5 PASS.
Properties include:
- AEAP all 3! x 3! = 36 need/probe permutations preserve output;
- CDPP all 3! x 3! = 36 hypothesis/probe permutations preserve output;
- IDW trace permutations preserve candidates, lineage and fingerprint;
- RCTC dedupe/schema-key order invariance;
- CRG consumer permutations preserve output.
Status: PASS.

## E3 integration
Command: npm run test:integration
Observed: 2/2 PASS.
Status: PASS.

## Full regression
Command: npm test
Observed:
tests 33
pass 33
fail 0
cancelled 0
skipped 0
todo 0
Status: PASS.

## Defect -> fix -> rerun history
D1 TypeScript widened RCTC outputIntent to string.
Fix: bind outputIntent to CompiledMonitor outputIntent literal union.
Rerun: E1 PASS.

D2 AEAP selected set lacked dependency-safe execution order.
Fix: deterministic topological execution order plus cycle rejection.
Rerun: regression PASS.

D3 IDW initially relied too much on TypeScript for primitive trace values.
Fix: runtime primitive validator.
Rerun: regression PASS.

D4 CRG FREEZE path hid known HOLD reasons.
Fix: preserve known HOLD reasons and add per-gate checks even when epistemic FREEZE dominates.
Rerun: regression PASS.

D5 Initial advisory alarm adapter proposed a new alarm enum member not present in observed NEXY current alarm union.
Fix: map advisory violation to existing RELEASE_POLICY_FAILURE and use supplementalKind SUPPLEMENTAL_CONTRACT_VIOLATION in payload.
Rerun: regression PASS.

D6 First static-audit shell one-liner had a quoting syntax error.
Fix: standalone run_static_audit.sh.
Rerun: static audit PASS.
This was verification tooling, not product behavior.

## Bounded local benchmark
AEAP exact search at 20-probe bound: about 1768.089 ms on this container, result PLAN.
CDPP exact search at 20-probe bound with 6 hypotheses: about 1157.011 ms, result PLAN.
These are local observations only, not production SLOs.

## Evidence ceiling
Proven: E0 after repository readback, E1, E2, E3 for the standalone reference package.
NOT VERIFIED: NEXY native integration, browser/E2E behavior, operational load/recovery, deployment, production security, or physical behavior.
No E4/E5/E6/E7 claim is made.
