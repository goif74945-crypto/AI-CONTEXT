# 02 — AI-Proposed System: Directive Epoch / Instruction Supersession Firewall

## Classification
**PROPOSAL.** This is an AI-designed future integration candidate, not a current NEXY requirement and not implementation evidence for NEXY.AI.

## Problem
Autonomous systems often separate planning from mutation. A worker can prepare a side effect under directive D1 while another control path accepts a newer directive D2. If the worker later commits without rechecking authority, D1 can act after it has lost authority.

This is an instruction-authority TOCTOU race:

`authorize/prepare under D1 -> D2 supersedes D1 -> stale D1 side effect commits`

Normal idempotency does not solve this. Idempotency controls duplicate execution of an operation; it does not prove that an operation remains authorized under the latest directive.

## Proposed primitive
Introduce a monotonically increasing **Directive Epoch** owned by the authoritative control plane.

Every prepared action carries a proof-of-context tuple:

`(action_digest, prepared_epoch, directive_hash, authority_lineage_hash)`

The mutation boundary checks the tuple against the current authoritative state. It must never infer a new authorization for an old action.

## Design laws
1. **Authority is checked twice:** once when preparing, again immediately before committing.
2. **Supersession is explicit:** NEW, REPLACE, NARROW and REVOKE are state transitions, not text heuristics.
3. **Epochs only advance:** accepted authority transitions create a new logical generation.
4. **Narrow means subset:** a NARROW operation cannot increase action kinds.
5. **Stale means stop:** epoch/hash/lineage mismatch FREEZEs the reference engine.
6. **Payload identity matters:** mutation payload is included in the action digest.
7. **Irreversible approval is exact:** approval binds action ID, epoch, action digest and authority lineage.
8. **Approval binding is not authentication:** identity/signature verification remains outside this core.
9. **Recovery creates fresh authority:** a frozen execution does not resume old prepared work.
10. **Replay includes attempts:** commit failures capable of freezing state are part of protocol history.

## Expected product benefit if adopted later
- Fast operator cancellation/supersession propagation.
- Safer long-running agents and queued work.
- Less chance that a user changes scope but an old worker still writes.
- Auditable explanation for why a side effect was blocked.
- Model/provider-independent authority semantics.
- Compatibility with deterministic replay and freeze-first operation.

## Non-goals
- Solving user intent extraction.
- Replacing RBAC/AUTH.
- Distributed consensus implementation.
- Network cancellation protocol.
- Persistence/database design.
- Automatically deciding whether two natural-language directives are semantically equivalent.
