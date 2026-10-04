# NEXY READ-ONLY GROUND-TRUTH AUDIT — 9e615b04

STATUS: PARTIAL / RELEASE_BLOCKED / AUTHORITY_CONFLICT_FROZEN
MODE: READ-ONLY against goif74945-crypto/NEXY.AI-
SOURCE_REPO_MUTATION_BY_THIS_AUDIT: NONE

## Identity lock

- Repository: goif74945-crypto/NEXY.AI-
- Branch: NEXY.ai
- Frozen checkpoint: 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43
- Railway tested tree: a809bc5f4cc2d8f806e500d1d3a09a4e66450c7c
- Railway deployment: 6ebf2acb-1889-450c-874a-1114b4f51531
- Authoritative design SHA-256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

## Exact-head execution

Railway source identity matched the exact checkpoint and the Docker validation advanced through:
- prisma generate
- cargo check -p core-kernel
- cargo test -p core-kernel -- --nocapture
- cargo check -p nexy-daemon
- npm run typecheck
- npm run test:contract
- selected Phase-F integration validation
- npm run test:experimental
- npm run test:integration
- npm run check:phase-f
- npm run check:static-determinism
- npm run check:six-system-spec
- npm run test:coverage

Blocking gate:
- npm run check:coverage -> FAIL
- api PASS: lines=93.68 statements=92.38 functions=97.66 branches=85.49 threshold=85
- core FAIL: lines=93.88 statements=92.41 functions=95.65 branches=83.13 threshold=90
- law PASS: lines=100.00 statements=94.87 functions=100.00 branches=96.83 threshold=90
- judge PASS: lines=96.52 statements=95.52 functions=100.00 branches=93.41 threshold=90

Not reached because coverage stopped the Dockerfile:
- npm run check:doc-c
- npm run build:web
- apps/web/.next/BUILD_ID assertion
- runtime DOC-E campaign

## Critical finding F-RNG-001 — Core entropy conflict

packages/core/ulid.ts blob aa379e7fa8a4139df7de922f2f6e3feabd724ee9:
- imports randomBytes from node:crypto
- generateUlid() uses randomBytes(10) / 80 CSPRNG bits
- comments claim DOC-C forbids deterministic SHA-256(tick) tail

Authoritative design evidence:
- Layer 9 says Core has no randomness / RNG / entropy source.
- DOC-C ID Strategy says all primary IDs = ULID; reason sortable + unique + string-safe.
- authoritative spec search found no randomBytes, CSPRNG, node:crypto, or SHA-256(currentTick) prohibition.

Verdict: AUTHORITY_CONFLICT_FREEZE. Do not select CSPRNG or deterministic tail by preference.

## Critical finding F-RNG-002 — entropy propagates into audit chain

packages/storage/soft-delete.ts blob 0ba532f1efb01cfa7d0cde599a37468339c234cb:
- newAuditUlid(tick) uses randomBytes(10)
- tx.auditLog.create persists id=newAuditUlid(tick)

prisma/migrations/20260922222000_audit_chain_head/migration.sql blob b3309de0e3e7d14cb8aaf61620fe957b3ffbcb03:
- locks current headId
- chain hash includes previous tail_id
- validates previousEntryId against tail_id
- SET headId = NEW.id

Therefore an entropy-derived current audit ID can become an input to the next persisted chainHash. Deterministic replay identity is blocked unless canon explicitly excludes this chain from deterministic state identity.

## Gate gap F-GATE-001

scripts/check-static-determinism.ts blob fb4cfe5484e91de7c8c74bdefa1a295e910aba52:
- AUTHORITATIVE_ROOTS includes packages/core and packages/storage.
- CORE_NO_RANDOMNESS detects Math.random and randomUUID forms.
- randomBytes is not detected.
- exact-head static determinism gate passed while core/ulid.ts still used randomBytes.

Verdict: proven false-negative coverage in deterministic gate.

## Internal ULID contradiction F-ULID-001

vault/repository.ts blob 197698c5514da02af251640aa51ad80597710c8f:
- intentionally derives ULID random component deterministically from sha256(tick + seed)
- comments state zero OS entropy is introduced

packages/core/ulid.ts:
- explicitly says this deterministic approach is forbidden
- uses CSPRNG

Single-truth violation until authority is reconciled.

## Time state

Positive:
- commit 20dcec8ece81264a193dd17cb442acd2d70a5e18 removes queue Date.now stale-time dependency and requires TSA batch time.
- currentTsaBatchTimeMs() fails closed with TSA_BATCH_TIME_REQUIRED.
- f544cf263e96c54a330e86d8253040b92e361261 adds TSA injection in LO2 test setup.
- ab65b9bb0f925e7c2892b23f0aa592e61cea6efb locks queue TSA-only test expectations.

Still blocked:
- production verified TSA authority -> injectTsaBatchTime call path not proven.
- Layer 9 TSA-only wording vs G19 invariant-TSC wording remains scope/precedence conflict.

## Floating-point scope conflict

packages/swarm/pipeline.ts blob b6bfadfb473b675928fa8df476b2180ac749e335:
- confidence/trust uses JavaScript number
- uses floating operations and BigInt(Math.round(score * 1_000_000))

DOC-C itself types confidence as number and defaults 0.85/0.90.
Layer 9 says floating point forbidden in Core.
Evidence does not yet prove SWARM is inside that exact Core numeric-law scope.

Verdict: SCOPE_CONFLICT / DO_NOT_AUTO_PATCH.

The static determinism checker has no float/double enforcement, so it cannot enforce Layer 9 wherever that law applies.

## Coverage repair target

Exact V8 report:
- canonical-json.ts branches=88.23%; uncovered lines shown 16,26
- canonical-order.ts branches=62.50%; uncovered 22,30
- tick.ts branches=79.16%; uncovered 28,48,71,90
- ulid.ts = 100% all metrics
- vnext-state-matrix.ts branches=95.45%; uncovered 179

High-value reachable test targets:
1. requireTickRange rejects > TICK_MAX
2. injectTsaBatchTime rejects regression below active TSA batch
3. currentTick overflow after reaching TICK_MAX
4. setEpochBase rejects regression below LAST_RETURNED
5. canonical text prefix/equality/multi-codepoint branch edges
6. strict guard-context parsing/error branches

Do not lower the coverage threshold.

## Stale matrix correction

The older 301-control matrix and conservative 66/301 figure are not current completion metrics.
Current code is hundreds of commits ahead and old negative claims are stale.

Global Anchor:
- current static implementation/tests cover 5 regions, 3/5 quorum, TSA 2/3, canonical FSM, degraded bounds and finalization.
- classify STATIC_IMPLEMENTED / RUNTIME_PROVIDER_PROOF_PENDING, not MISSING.

Economy:
- current static implementation/tests cover fixed supply, deterministic split, escrow/dispute proof, account-local freeze, marketplace bond/fees, app-to-app binding, degraded anchor queue and finalized-anchor checks.
- classify STATIC_IMPLEMENTED / RUNTIME_AND_CONTROL_REVALIDATION_PENDING.

## Required next order

1. Fix core branch coverage without threshold reduction.
2. Resolve ULID/Core RNG authority before changing entropy behavior.
3. Add gate enforcement matching the resolved RNG law.
4. Prove production TSA verifier -> injectTsaBatchTime path.
5. Resolve TSA vs invariant-TSC scope.
6. Resolve SWARM numeric scope vs Core fixed-point law.
7. Rebuild the 301-control matrix against one frozen SHA.
8. Run check:doc-c + build:web + DOC-E on the same frozen SHA/tree.

STOP CONDITION:
Do not claim release-ready while any authority conflict is unresolved, exact-head coverage fails, later Docker gates are not reached, or DOC-E does not authorize the same SHA/tree.
