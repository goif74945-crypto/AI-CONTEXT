# TASK
TASK_ID: NEXY-SPEC-CONVERGENCE-A3E75C76-20261005
SUPERSEDES: NEXY-SPEC-CONVERGENCE-6F4920E8-20261005
MODE: EXECUTE/CROSS
TARGET_REPO: goif74945-crypto/NEXY.AI-
TARGET_BRANCH: NEXY.ai
HEAD: a3e75c760c1add35c78750203332874f8635b4b4
TREE: 229cd2ac3e0da848c23f23dd11252de2d48cfdfc
SPEC_SHA256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
STATUS: PARTIAL / TEST_INFRA_BLOCKED / AUTHORITY_CONFLICT_FROZEN

## Delta after the 6f4920e8 checkpoint
- 310b799f53f31f62e2e2d0d2583d4a7df5d4e919 repaired validation/attestation contract regressions and explicitly bound Phase-F to advisory/experimental scope.
- d60946c3a9e34dbc51cf7745bcbf1eba3f2e4212 extended canonical ordering repairs into G20/G25/economy paths.
- a3e75c760c1add35c78750203332874f8635b4b4 corrected the static determinism release gate so Phase-F remains scanned but EXPERIMENTAL/OBSERVE instead of silently becoming a blocking current-build authority.

## a3e75c76 repair
scripts/check-static-determinism.ts:
- current DOC-C roots remain blocking AUTHORITATIVE;
- Phase-F sovereign/Lo2/Lo3/L1o/economy/game/universe remain scanned as EXPERIMENTAL;
- experimental findings remain observable but do not become current release failures;
- packages/vault remains in the actual current authoritative roots.

tests/contract/static-determinism-gate.test.ts:
- locks Phase-F outside current release-authoritative roots;
- preserves Phase-F scan coverage as EXPERIMENTAL/OBSERVE;
- preserves current-root FAIL behavior;
- path fixture helper uses dirname() rather than Unix-only '/' slicing.

## Exact-head execution evidence
At a3e75c760c1add35c78750203332874f8635b4b4:
- 37222271602 Exact HEAD test evidence: failure before exposed steps/logs
- 37222271654 NEXY CI / Deploy Gate: first-wave jobs failure before exposed steps/logs; downstream DOC-C/release/deploy skipped
- 37222271587 Six-system exact HEAD evidence: failure before exposed steps/logs
- 37222271599 Layer8 Cargo lock evidence: failure before exposed steps/logs

Connector job records expose steps=null and logs_url=null. Do not claim any npm/cargo/build/test command executed.

## Remaining blockers
1. Exact-head execution infrastructure unavailable.
2. Layer-9 Core clock authority and later G19 hardware CLOCK SOURCE wording remain unresolved in scope/precedence.
3. Production injectTsaBatchTime caller remains unproven; baseline full-repo negative proof plus reviewed deltas did not add one.
4. Whole-project runtime/build/deploy completion cannot be proven until exact-head commands execute.
5. Repository is under concurrent mutation by other authorized work; all future repair must re-freeze HEAD before write and refuse non-fast-forward replacement.

## Stop
No further mutation that depends on runtime output or unresolved authority is allowed from this checkpoint. Resume from exact HEAD, then re-run evidence once a runner is available.
