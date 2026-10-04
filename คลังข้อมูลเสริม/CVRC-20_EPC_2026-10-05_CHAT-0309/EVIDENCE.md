# CVRC-20 Evidence

## Target evidence
- NEXY repo: `goif74945-crypto/NEXY.AI-`
- branch: `NEXY.ai`
- locked commit: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
- source Canon SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`

### Read-only NEXY blobs inspected
- `packages/contracts/state.ts`: `04efcc7161c5415922e11e16174013d1d4ea40a3`
- `packages/core/vnext-state-matrix.ts`: `27e1281fba330784cc3bf2c30e9e1e82f951479b`
- `core-kernel/src/kernel/vnext_matrix.rs`: `c55e13839f2bed01a29749f226edef82d1929a4a`
- `packages/contracts/envelope.ts`: `daf1156b3431150e667b5e18727d8abe9bdc9b75`
- `packages/contracts/evidence.ts`: `6b50f4cf9c0ca7e4c056fc546976e6e5a52d5895`
- `packages/contracts/errors.ts`: `b6a1737688399cf0571236f23c0b5ce0f7de5847`
- `packages/swarm/adapters/types.ts`: `30e5129a0b8ec2674f75ff3056ea0bf848814c82`
- `packages/queue/payload.ts`: `f46513b1123d2a4bef277c6ce08a72656e5d9306`
- `packages/queue/jobs.ts`: `e90ac64acc446c5bbd24a710e0208fc76bce9089`
- `packages/queue/run-state.ts`: `e162efc8b2a45014bcefbd60dc67a95d8a1e1003`
- `vault/repository.ts`: `197698c5514da02af251640aa51ad80597710c8f`
- `packages/phase-f/sovereign/versioning-law.ts`: `d0ddd66611868289571263b10cd32a77ce0703da`
- `tests/contract/module-boundaries.test.ts`: `b5db76d5ce6621c51f9216b52636b20e660a1956`
- `tests/contract/fixed128-overflow-scope-law.test.ts`: `83ff7cbe53988c4fb49f2ff2f251928955cf1abb`

## RED evidence
Initial unit run failed:
- observed raw Q64.64: `18446744073709551615`
- incorrect expected: `18446744073709551616`
- vector: `q64Mul(q64FromRatio(3,2), q64FromRatio(2,3))`
- root cause: 2/3 is not exactly representable in Q64.64.
- correction: test oracle only, expected `Q64_ONE - 1`.

## Final local runtime evidence
Environment: Node `v22.16.0`.

### Syntax
PASS for all source and test modules.

### Unit
```json
{"status":"PASS","suite":"cvrc20-unit","gates":20,"targetCommit":"9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43","assertions":83}
```

### Malformed corpus
```json
{"status":"PASS","suite":"cvrc20-malformed","cases":26}
```

### Deterministic adversarial stress
```json
{"status":"PASS","suite":"cvrc20-stress","iterations":5000,"rejected":5000,"deterministicMatches":5000,"seedFinal":"56d99c20f11482d4"}
```

### Benchmark
One observed run:
```json
{"status":"OBSERVATION","suite":"cvrc20-benchmark","iterations":20000,"keep":20000,"elapsedMs":3520.62237,"evalsPerSecond":5680.813759074081,"authoritative":false}
```
Wall-clock performance is explicitly non-authoritative.

## Deterministic receipt
- candidate hash: `cfbdf447e65895992b0288c4f155a888077d5e7301a255550af5a4d1bed186cb`
- report hash: `fda2807d4723e0294bddde0a06d1410f34dfb5586372f50a1d2963588692dbe0`

## Truth labels
FACT: the runs above executed against the local CVRC working copy and passed after the recorded repairs.
FACT: no NEXY.AI repository mutation was performed.
ASSUMPTION: the normalized candidate object is an integration representation, not a current NEXY runtime API.
UNKNOWN: production behavior after future integration into NEXY.AI.
NOT VERIFIED: deployment, production load, and complete 837-requirement coverage.
