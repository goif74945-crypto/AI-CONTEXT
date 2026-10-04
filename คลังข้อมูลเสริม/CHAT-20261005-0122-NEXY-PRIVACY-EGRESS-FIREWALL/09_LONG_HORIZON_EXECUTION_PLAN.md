# Long-Horizon Execution Plan

**Mission:** CHAT-20261005-0122-NEXY-PRIVACY-EGRESS-FIREWALL  
**Classification:** AI-PROPOSED / NON-GOVERNING  
**Execution rule:** one evidence-bearing wave at a time; refresh sibling overlap before each wave; TDD for behavior changes; no NEXY.AI repository mutation.

## Wave state vocabulary

`PLANNED | IN_PROGRESS | VERIFIED | SKIPPED_OVERLAP | BLOCKED | REJECTED`

A wave is `VERIFIED` only when its intended evidence class exists. File presence is not completion.

## Wave ledger

| Wave | Topic | Initial state | Minimum evidence |
|---:|---|---|---|
| 01 | Base NPCEF architecture, evaluator, consent/recipient binding, value-free receipts | VERIFIED | E0/E1/E2 |
| 02 | Recipient Capability Envelope: retention/training/region/deletion/logging declarations | PLANNED | schema + unit/adversarial |
| 03 | Capability-aware disclosure policy: recipient capability cannot create authority | PLANNED | E1/E2 |
| 04 | Revocation race simulator: grant revoked between evaluate and dispatch | PLANNED | deterministic simulation |
| 05 | Evaluation-to-dispatch binding / TOCTOU token | PLANNED | negative tests |
| 06 | Receipt metadata side-channel minimization | PLANNED | differential leakage audit |
| 07 | Grant bundling and least-authority batch consent | PLANNED | adversarial grant tests |
| 08 | Consent-fatigue safety model and bounded ASK UX rules | PLANNED | scenario corpus + falsification |
| 09 | Recipient alias/substitution/redirect attack model | PLANNED | adversarial tests |
| 10 | Purpose taxonomy drift/alias detector | PLANNED | deterministic conflict tests |
| 11 | Policy/version invalidation and stale-receipt replay | PLANNED | replay tests |
| 12 | Downstream retention/deletion attestation contract | PLANNED | schema + contradiction tests |
| 13 | Local preprocessing transform provenance without declassification claims | PLANNED | transformation tests |
| 14 | Attachment/binary/document egress envelope | PLANNED | typed fixtures |
| 15 | Streaming and partial-send revocation semantics | PLANNED | state-machine simulation |
| 16 | Queue/retry/idempotency for egress decisions | PLANNED | duplicate/retry tests |
| 17 | Audit-ledger retention minimization | PLANNED | metadata minimization audit |
| 18 | Cross-provider recipient capability negotiation | PLANNED | compatibility scenarios |
| 19 | Degraded/offline policy-store behavior: fail closed without deadlock fiction | PLANNED | fault simulation |
| 20 | Policy-conflict proof generator | PLANNED | conflict corpus |
| 21 | Differential-disclosure regression generator | PLANNED | property-oriented tests |
| 22 | Egress bypass-path architecture proof model | PLANNED | path inventory + negative proof plan |
| 23 | Performance/cost envelope that cannot relax privacy invariants | PLANNED | bounded benchmark harness |
| 24 | Shadow-mode adoption experiment and rollback gates | PLANNED | experiment protocol |
| 25 | Whole-lab contradiction scan, regression sweep, evidence index, final handoff | PLANNED | final audit |

## Explicit non-duplication boundary

Do not independently build CRF-owned derived-sensitivity, compartment, derived-purpose, or declassification-registry mechanisms unless a future task explicitly asks for comparison/interoperability. See `13_CONCURRENT_OVERLAP_BOUNDARY.md`.

## Per-wave execution loop

```text
REFRESH AI-CONTEXT + SIBLING SCAN
  -> LOAD CURRENT CHECKPOINT
  -> CLAIM NEXT PLANNED WAVE
  -> LOCK REQUIREMENTS + FAILURE CONDITIONS
  -> WRITE FAILING TEST / DECISIVE PROOF FIRST WHEN BEHAVIORAL
  -> IMPLEMENT SMALLEST COMPLETE CHANGE
  -> FOCUSED TEST
  -> REGRESSION + PROPERTY/NEGATIVE TEST
  -> READ-BACK / HASH EVIDENCE
  -> UPDATE REQUIREMENT + EVIDENCE + CHECKPOINT
  -> MARK VERIFIED | SKIPPED_OVERLAP | BLOCKED
```

## Stop conditions

Freeze rather than improvise if:
- any action would modify a repository whose name contains `NEXY.AI`;
- a sibling now owns the same planned mechanism and no complementary scope remains;
- current AI-CONTEXT authority conflicts with the wave;
- a secret/credential would be persisted;
- a required irreversible/high-impact action lacks explicit authority;
- verification evidence cannot support the intended claim.

## Long-horizon completion condition

The mission is not COMPLETE merely because Wave 01 passed. Long-horizon completion requires every wave to have an explicit terminal state and Wave 25 to re-audit the entire lab. `SKIPPED_OVERLAP` is legal when supported by fresh sibling evidence.
