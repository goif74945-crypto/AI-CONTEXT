# 04 — Failure and Threat Model

## Trust boundary
Generated plans, agent output, tool arguments, resource IDs, destinations, costs, and external responses are untrusted until validated.

| ID | Threat | Required response | Prototype |
|---|---|---|---|
| T-01 | Confused deputy | scope-bound block | PARTIAL |
| T-02 | Post-approval plan mutation | plan-hash freeze | PASS |
| T-03 | Destination laundering | destination drift freeze | PASS |
| T-04 | Effect escalation | effect/high-impact block | PASS |
| T-05 | Wildcard delegation escalation | provable subset or reject | PASS reference |
| T-06 | Replay stale lease | expiry/revocation | PARTIAL |
| T-07 | Cost/action runaway | finite budgets | PASS |
| T-08 | Policy downgrade | version mismatch freeze | PASS |
| T-09 | Journal tamper | hash-chain failure | PASS prototype |
| T-10 | Resource alias bypass | provider canonical identity | NOT_VERIFIED |
| T-11 | TOCTOU revocation race | atomic guard/dispatch | NOT_VERIFIED |
| T-12 | Distributed stale cache | revocation propagation | NOT_VERIFIED |
| T-13 | Forged lease | issuer authentication/signature | NOT_VERIFIED |
| T-14 | Underreported cost | independent accounting | NOT_VERIFIED |
| T-15 | Action splitting | effect adapter contracts | NOT_VERIFIED |
| T-16 | Provider credential bypass | guard before provider call | NOT_VERIFIED |
| T-17 | Silent auto-renewal | forbidden | design |
| T-18 | Approval dark pattern | neutral effect summary | design |

## Production gaps
- **Resource canonicalization:** generic glob matching is insufficient for provider identities and aliases.
- **Atomic check-and-use:** revocation check, budget reservation, and dispatch need a race-safe protocol.
- **Cryptographic attribution:** a plain lease object is data, not authenticated authority.
- **Distributed revocation:** stale executors need bounded/fail-closed semantics.
- **Provider adapters:** raw provider calls must not bypass the represented action contract.

## Fail-safe rule
When the system cannot prove an action is inside an active legal lease, execution is blocked pending a legal authorization path.
