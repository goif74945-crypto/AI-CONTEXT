# Temporary Mission Memory — NEXY Lo4 Q64 Formal Envelope Foundry

Status: ACTIVE_CHECKPOINT
Conversation code: `CHAT-20261005-0223-NEXY-LO4-Q64-FORMAL-ENVELOPE`
Created: 2026-10-05T02:23+07:00
Last checkpoint: 2026-10-05T02:34+07:00
Target repository: `goif74945-crypto/AI-CONTEXT`
Target branch: `main`
Persistence mode: DURABLE_RESUMABLE
Platform-internal ChatGPT chat ID: UNKNOWN_NOT_EXPOSED

## Objective
Create five novel Lo4 AI-proposed, non-canonical systems useful to future NEXY.AI integration, with executable Q64.64 reference code, tests, evidence, design, and a clean resumption point. No repository whose name contains `NEXY.AI` may be mutated.

## Authority loaded
- root `INDEX.md`, `AI-BOOTSTRAP.md`, `AI-EXECUTION-KERNEL.md`, `WORK-ROUTER.md`
- `rules/GLOBAL.md`, `rules/AI-BEHAVIOR.md`, `rules/SECURITY.md`, `rules/VERIFICATION.md`
- `workflows/system-design.md`, `workflows/implementation.md`, `workflows/verification.md`, `workflows/memory-update.md`
- `projects/NEXY.AI/overview.md`
- `projects/NEXY.AI/deep/INDEX.md`
- `projects/NEXY.AI/deep/constitutional-locks.md`
- `projects/NEXY.AI/deep/final-architecture-cross-system.md`
- `projects/NEXY.AI/deep/human-control-surface.md`
- `projects/NEXY.AI/source-normalization/CURRENT-SYSTEM-FEATURE-BUILD-MATRIX.md`

## Source facts / immutable mission law
- NEXY separates design, implementation, runtime, and deployment truth.
- AI worker output is not final authority.
- Later architecture prefers bounded truth, explicit uncertainty, verified outputs, and FREEZE when proof is insufficient.
- Constitutional source-design forbids floating point in canonical Core and specifies signed 128-bit fixed/integer arithmetic with overflow -> FREEZE.
- Lo4 work here is proposal-only and cannot silently become Canon.
- Protected repositories containing `NEXY.AI` are READ-ONLY for this mission.

## Five systems implemented locally
1. HYPERBOX-64 — affine guard certification over Q64.64 uncertainty boxes.
2. REACHTUBE-64 — finite-horizon affine interval reachability with per-step guard certification.
3. CONSERVE-64 — linear invariant drift certification using exact raw-product accumulation.
4. FUSEBOX-64 — exact quorum interval fusion on the discrete Q64.64 raw lattice.
5. DESCENT-64 — weighted-L1 potential decrease certification.

A sixth composition surface, FormalEnvelopePipeline, gates all five and returns READY/REJECT/FREEZE without side effects.

## Q64.64 substrate now implemented
- 64 fractional bits, signed-128 raw domain.
- Python float forbidden.
- production package contains no Fraction arithmetic/import.
- decimal/ratio input is projected into Q64.64 using explicit REQUIRE_EXACT/FLOOR/CEIL/HALF_EVEN policy.
- addition/subtraction/negation/multiplication overflow is fail-closed.
- interval multiply uses outward directed rounding.
- huge decimal exponent is rejected before ratio expansion.
- canonical evidence JSON rejects binary floats and has stable SHA-256 digest.

## TDD / failure evidence so far
- RED: Q64 module absent -> expected failing bootstrap test.
- GREEN: initial Q64 contract -> 10/10.
- RED: five Lo4 engine modules absent -> expected failing bootstrap.
- RED: 22/22 behavior tests failed against NOT_IMPLEMENTED skeleton.
- GREEN: Q64 + five engines -> 33/33.
- RED/GREEN: pipeline bootstrap and three pipeline behaviors.
- RED/GREEN: canonical evidence layer.
- RED: numeric purity test found production `fractions` import.
- FIX: removed Fraction from production; test-only Fraction oracle retained.
- REGRESSION: automated test refactor corrupted two oracle expressions; full suite became 47 pass + 1 error.
- FIX/RETEST: oracle corrected; full suite 48/48.
- RED: exponent-bound test proved rejection happened only after ratio expansion.
- FIX: early exponent guard added.
- FRESH FULL SUITE: 54/54 PASS.
- independent property verification includes 2,400 brute-force FUSEBOX cases, Fraction-oracle directed multiplication checks, interval-corner enclosure proof, and permutation digest invariance.
- compileall: PASS.
- static grep: no float constructor/random/network/subprocess/eval/time/Fraction dependency found in production package.

## Local workspace
`/mnt/data/nexy_lo4_q64_envelope`

Current production modules:
- q64foundry/q64.py
- interval.py
- model.py
- hyperbox.py
- reachtube.py
- conserve.py
- fusebox.py
- descent.py
- pipeline.py
- canonical.py

Current tests:
- test_q64.py
- test_q64_security.py
- test_numeric_purity.py
- test_engines.py
- test_properties.py
- test_pipeline.py
- canonical/pipeline/engine bootstrap tests

## Persistence incident
Initial AI-CONTEXT checkpoint write hit HTTP 409 because concurrent chats advanced main. It was recovered by refresh + retry with no force update and no overwrite outside this unique folder.

## Truth boundary
Local E1/E2/E3 evidence is emerging for the standalone prototype only.
NEXY.AI integration/runtime/deployment remains NOT_VERIFIED.
No production promotion is authorized.

## Next action
1. build static auditor + deterministic validation runner;
2. add adversarial/limit tests and performance characterization;
3. write README/contracts/compatibility/promotion/evidence/final audit;
4. run fresh final suite and compute exact file hashes;
5. persist exact tested bytes to this folder;
6. read back and bind Git blob hashes to local tested bytes;
7. only then declare mission completion.

## Stop/freeze conditions
- any required write leaves this unique folder;
- any operation mutates a repository containing `NEXY.AI`;
- unsupported arithmetic silently wraps/saturates/guesses;
- persisted bytes differ from tested bytes;
- completion lacks fresh proof.
