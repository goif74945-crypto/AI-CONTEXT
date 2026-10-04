# ECRPF-20 Integration Contract for NEXY

## Proposed position

ECRPF is a **preflight-only adapter**. A future integration may translate NEXY's current configuration sources into an ECRPF snapshot, run the deterministic proof, and pass the proof capsule to the existing VERIFY/JUDGE/Core-authorized workflow. ECRPF itself may not commit runtime config, write environment variables, call deployment providers, update NEXY state, or authorize rollout.

## Current NEXY compatibility anchors (read-only inspection)

At NEXY commit `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`:

- `packages/api/vnext-config.ts` blob `a3141a649be7e40ec79f417f53bba9b73081232b` centralizes canonical defaults and forbids route-level magic numbers.
- `packages/config/runtime-config.ts` blob `43be034d5938137d8d29a5506ba25d356d79e66a` separates immutable config, validates committed runtime versions, and computes deterministic diffs.
- `packages/api/live-config.ts` blob `2801bba4644a71b2eedc2a9ddc64e561eb31a33f` uses serializable transactions, expected-version checks, idempotency, rollback targets, and evidence emission.
- `packages/api/bootstrap.ts` blob `d6292374efca4b55bb3865e7151175674ad06b3e` binds environment-selected providers and freezes on bootstrap dependency/integrity failure.
- `packages/queue/jobs.ts` blob `e90ac64acc446c5bbd24a710e0208fc76bce9089` currently resolves Redis host/port from process environment with defaults.
- `packages/api/middleware/rate-limit.ts` blob `ce16bc2746e9d360b410f598d5cd0c9af7fe9826` explicitly describes fail-open as dev-only and production default as fail-closed.
- `core-kernel/build.rs` blob `63fc3061acf0a82dd52d5dcc88837a23567fc30d` hashes normalized build environment and compiler/target inputs into build identity.
- `packages/phase-f/resilience/guardian.ts` blob `db1778e649558921c7422f9d59937311dfabdd94` folds normalized environment identity into build hash and forbids environment mutation by design comment.

## Non-overlap

ECRPF does not replace live runtime-config versioning, rollback transactions, deployment adapter resolution, secret storage, NEXY build hashing, or rate-limit logic. Its unique output is a cross-source/cross-environment **configuration coherence proof** plus deterministic Q64 rollout/blast-radius evidence before those existing systems act.

## Required future adapter behavior

A future adapter must:

1. normalize only metadata and secret references, never secret plaintext;
2. preserve exact source provenance (`BUILD`, `ENV`, `RUNTIME`, `DEFAULT`, `SECRET_PROVIDER`);
3. bind the snapshot to exact NEXY code/config version;
4. map current NEXY immutable/mutable config semantics without weakening them;
5. reject any candidate ECRPF PASS if NEXY VERIFY or Canon disagrees;
6. never interpret ECRPF PASS as deployment permission.
