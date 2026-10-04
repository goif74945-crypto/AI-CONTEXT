# 05 — Commitment State Machine and Invariants

## States

- `DRAFT` — candidate obligation; not yet accepted.
- `ACCEPTED` — legally accepted by the reference gate, but not necessarily executing.
- `ACTIVE` — execution/watch is active.
- `BLOCKED` — temporarily unable to proceed; obligation still exists.
- `FULFILLED` — terminal; matching PASS evidence exists.
- `FAILED` — terminal; execution failed.
- `CANCELLED` — terminal; obligation was cancelled.
- `EXPIRED` — terminal; legal temporal window ended.
- `SUPERSEDED` — terminal; replaced by a separately evaluated revision.

## Legal transitions

```text
DRAFT --ACCEPT--> ACCEPTED
ACCEPTED --ACTIVATE--> ACTIVE
ACTIVE --BLOCK--> BLOCKED
BLOCKED --RESUME--> ACTIVE
ACTIVE --COMPLETE + matching evidence--> FULFILLED
ACTIVE/BLOCKED --FAIL--> FAILED
ACCEPTED/ACTIVE/BLOCKED --CANCEL--> CANCELLED
ACCEPTED/ACTIVE/BLOCKED --EXPIRE--> EXPIRED
ACCEPTED/ACTIVE/BLOCKED --SUPERSEDE--> SUPERSEDED
```

Any other transition is rejected.

## Safety invariants

Let `C` be a commitment and `F(C)` its canonical SHA-256 fingerprint.

- **I-01 Backing:** `ALLOW_COMMITMENT => binding_type(C) matches temporal_mode(C)`.
- **I-02 Capability:** `ALLOW_COMMITMENT => binding_type(C) ∈ capability_manifest.bindings`.
- **I-03 Future durability:** `mode(C) != IMMEDIATE => binding(C).durable = true`.
- **I-04 Authority:** `ALLOW_COMMITMENT => authority_state(C) = RESOLVED`.
- **I-05 Provenance:** `ALLOW_COMMITMENT => authority_refs(C) != ∅`.
- **I-06 Protected scope:** `ALLOW_COMMITMENT => scope(C) ∩ protected_scope(C) = ∅` under case-insensitive exact identity.
- **I-07 Effect capability:** `ALLOW_COMMITMENT => effect(C) ∈ supported_effects`.
- **I-08 Evidence producibility:** every required evidence class must be declared producible by the current environment.
- **I-09 No evidence substitution:** `E_x` does not satisfy `E_y` unless `E_y` itself is present.
- **I-10 Fulfillment target:** `FULFILLED => evidence.target_fingerprint = F(C)`.
- **I-11 Fulfillment revision:** `FULFILLED => evidence.revision = C.revision`.
- **I-12 Fulfillment proof:** `FULFILLED => required_evidence(C) ⊆ evidence.classes ∧ evidence.result = PASS ∧ refs != ∅`.
- **I-13 Revision lineage:** legal revision `C(n+1)` references exactly `F(Cn)`.
- **I-14 Party stability:** revision does not silently change issuer or beneficiary.
- **I-15 Terminal immutability:** no terminal state transitions back to a live state.
- **I-16 Ledger lineage:** each event hash commits to previous hash, sequence, identity, revision, state, event and payload.

## Liveness boundary

The reference model chooses truthful failure over optimistic liveness. A false freeze is preferable to a false promise until stronger production evidence exists.
