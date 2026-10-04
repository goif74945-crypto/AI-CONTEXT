# 04 — Protocol and State Model

## Engine states
- `EMPTY`: no active directive yet.
- `ACTIVE`: actions may be prepared/committed subject to policy.
- `REVOKED`: authority explicitly revoked; old actions are invalid.
- `FROZEN`: protocol invariant failed; mutation must stop until governed recovery.

## Directive operations

### NEW
Legal only from `EMPTY`. Establishes epoch 1 and initial authority.

### REPLACE
Replaces active authority and advances epoch. Requires an `expected_epoch` compare-and-set precondition.

### NARROW
Advances epoch while only reducing the allowed action-kind set. Any attempted expansion FREEZEs.

### REVOKE
Advances epoch and moves state to `REVOKED`. No previously prepared action remains current.

## Prepared action contract
A prepared action stores:
- `action_id`
- `kind`
- `payload`
- `action_digest`
- `prepared_epoch`
- `directive_hash`
- `lineage_hash`
- optional `approval_binding`

## Commit-gate order
1. Ensure engine is ACTIVE.
2. Recompute action digest; mismatch -> FREEZE.
3. Compare prepared epoch to current epoch; mismatch -> FREEZE.
4. Compare directive hash; mismatch -> FREEZE.
5. Compare authority lineage; mismatch -> FREEZE.
6. Confirm action kind remains allowed; mismatch -> FREEZE.
7. If irreversible, verify exact approval binding; missing/wrong -> REJECT.
8. Otherwise ALLOW.

The distinction between REJECT and FREEZE is deliberate: missing approval is a normal unmet precondition, whereas stale/tampered authority represents an integrity failure in this strict reference policy.

## Idempotency
`event_id` is content-address checked:
- same ID + same event digest => idempotent replay of the prior accepted transition;
- same ID + different digest => FREEZE.

## Recovery
Recovery is permitted only from `FROZEN` in this reference system and requires:
- operation `REPLACE`;
- `expected_epoch` equal to the frozen epoch;
- fresh directive identity/content.

Recovery advances epoch and therefore invalidates every old prepared action.

## Journal replay
Replay processes each record in exact index order and verifies:
- expected index;
- previous-record hash;
- record hash;
- reproduced protocol outcome code;
- reproduced resulting state hash.

Any mismatch raises `ProtocolError`; replay never auto-heals or silently skips a corrupt record.
