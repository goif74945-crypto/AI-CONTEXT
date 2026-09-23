# PLAYBOOK — Audit Determinism

## PURPOSE
Determine whether the claimed deterministic domain has hidden nondeterminism or evidence gaps.

## SCOPE FIRST
Identify the domain before applying rules:
- Constitutional/Core canonical mutation;
- DOC-C orchestration;
- Game authoritative simulation;
- non-authoritative rendering/sandbox;
- robotics normalized decision path.

Do not incorrectly apply one domain's numeric/randomness law to another.

## PROCEDURE
1. Resolve governing determinism laws/invariants.
2. Identify authoritative state mutator(s).
3. Trace ordering/concurrency/async boundaries.
4. Inspect time sources.
5. Inspect RNG/entropy sources.
6. Inspect numeric model/overflow behavior.
7. Inspect environment/compiler/allocator/config dependencies.
8. Inspect filesystem/directory/order iteration.
9. Inspect replay/state-hash behavior.
10. Inspect queue/event ordering and idempotency.
11. Run repeatability tests on same input/state.
12. Run cross-process/cross-build/cross-architecture tests where the claim requires them.
13. Compare state/output hashes.

## RED FLAGS
- unordered map/directory iteration in authoritative path;
- system clock read in Core;
- hidden RNG;
- floating point where prohibited;
- scheduler timing affecting state;
- concurrent canonical mutators;
- retry that duplicates mutation;
- environment-dependent branch;
- replay that skips corrupted history;
- game/render nondeterminism leaking into sovereign state.

## PASS
Requires repeatable observed evidence matching the claim scope. Design law/code inspection alone = NOT_VERIFIED.
