# 05 — Deterministic Replay Capsule & Differential Oracle (DRCDO)

**Class:** `Lo4_AI_PROPOSAL_ONLY`

## Purpose
Bind enough execution identity to replay a task across two or more executors and detect semantic output drift, executor faults, and replay poisoning.

## Capsule contents
- request object;
- state object;
- policy SHA-256;
- exact tool name/version manifest;
- deterministic seed;
- capsule identity.

The capsule hash uses canonical serialization.

## Differential oracle
Executors run in lexical executor-id order. Successful output is canonicalized and hashed. The first successful executor is the deterministic reference. Any output-hash mismatch or executor failure freezes the report.

## Replay isolation hardening
Each executor receives a freshly deep-canonicalized capsule copy. An executor that mutates nested input cannot poison the original capsule or later replays. This was explicitly added during the verification/fix loop.

## Invariants
- same canonical input identities produce same capsule hash;
- mapping/key order does not affect output hash;
- executor exception becomes explicit FREEZE evidence;
- one executor cannot mutate a later executor's capsule view.

## Limits
Deterministic replay of stochastic external models requires an explicit equivalence envelope. This prototype compares concrete canonical outputs and therefore should not be misused as proof that an inherently nondeterministic model is deterministic.

## Code/Test
- code: `src/nexy_lo4_frontier/drcdo.py`
- tests: `tests/test_drcdo.py`
