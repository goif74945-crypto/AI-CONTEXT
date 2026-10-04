# 09 — Validation Report

**Project:** NEXY Commitment Integrity Kernel (NCIK)  
**Classification:** AI-PROPOSED supplementary reference system  
**Chat code:** `CHAT-20261005-0143-NEXY-COMMITMENT-INTEGRITY-KERNEL`  
**Platform chat ID:** `UNKNOWN_NOT_EXPOSED`

## 1. Verification boundary

This report verifies only the standalone reference artifacts in this project folder. It does **not** prove that NCIK is integrated into, deployed with, or adopted by NEXY.AI.

Required evidence for this workstream:

- `E0_PRESENCE` — required artifacts exist.
- `E1_STATIC` — Python source compiles; JSON assets parse; forbidden runtime imports are absent from the reference core under the tested rule set.
- `E2_UNIT` — deterministic gate behavior, state transitions, revision law, evidence binding, adversarial cases, and ledger integrity are executed locally.

No `E3+` claim is made.

## 2. Test environment

Observed runtime for the final local gate:

- Python: `3.13.5`
- OS/kernel: Linux x86_64, kernel `6.18.44`
- Network/model calls by reference core: none by design and checked by static invariant tests.
- Wall-clock/randomness dependency in reference core: none by design and checked by static invariant tests.

## 3. Executed gates

| Gate | Evidence class | Result | Evidence |
|---|---|---:|---|
| Python source compilation | E1 | PASS | `evidence/final-gate.txt` |
| JSON fixture/example/schema parse | E1 | PASS | `evidence/final-gate.txt` |
| Forbidden-import invariant | E1/E2 | PASS | `tests/test_invariants.py`, `evidence/final-gate.txt` |
| Unit + invariant suite | E2 | PASS — 53/53 | `evidence/final-gate.txt` |
| Adversarial commitment corpus | E2 | PASS — 30/30 | `fixtures/adversarial_cases.json`, `evidence/final-gate.txt` |
| 1,000-repeat deterministic decision check | E2 | PASS | `tests/test_invariants.py` |
| Temporal-mode / binding mapping | E2 | PASS | `tests/test_invariants.py` |
| Terminal-state immutability | E2 | PASS | `tests/test_invariants.py` |
| Evidence non-substitution | E2 | PASS | `tests/test_invariants.py` |
| Ledger tamper/reorder detection | E2 | PASS | `tests/test_ledger.py` |

## 4. Behaviors proven by E2

The reference implementation was executed to prove that authority conflict freezes; unresolved authority asks; malformed commitments freeze; protected-scope collision freezes; future commitments require exact durable temporal bindings; schedule/trigger metadata is mandatory where relevant; unavailable capabilities freeze; revisions require exact lineage; fulfillment requires PASS evidence bound to exact fingerprint/revision and all declared evidence classes; evidence classes do not silently substitute; terminal states do not revive; ledger tamper/reorder is detected; and normalized equivalent inputs remain deterministic.

## 5. Evidence-class discipline

NCIK treats evidence classes as semantic labels, not a scalar ranking. For example, `E6_DEPLOYMENT` does not automatically satisfy `E4_E2E`.

## 6. Negative-path coverage

The adversarial corpus contains 30 named cases covering malformed identity, scope, authority, execution-binding, temporal-mode, durability, schedule/trigger, capability and evidence failures plus valid immediate/scheduled/conditional/recurring cases. Result: `30/30 PASS`.

## 7. Source integrity artifacts

- `evidence/SHA256SUMS.txt` records project hashes after finalization.
- Repository-bound E1/E2 evidence requires uploaded Git blob identities to match locally tested bytes.

## 8. Explicitly NOT VERIFIED

Real NEXY authentication/RBAC/LAW integration; real scheduler persistence; distributed cancellation; crash recovery/exactly-once fulfillment; provider-specific idempotency; cryptographic attribution; real UI/user studies; E2E/deployment behavior; and compatibility against every normalized NEXY requirement row remain NOT_VERIFIED.

## 9. Verdict

**Standalone reference system:** `PASS` for declared E0/E1/E2 scope.  
**NEXY integration / production:** `NOT_VERIFIED`.
