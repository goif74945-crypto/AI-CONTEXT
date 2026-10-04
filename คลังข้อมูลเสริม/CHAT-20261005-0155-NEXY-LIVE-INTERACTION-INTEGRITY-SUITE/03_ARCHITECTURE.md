# Architecture — Live Interaction Integrity Suite

## Status
Reference implementation only. Compatible-by-contract design; not integrated into NEXY.AI.

## Boundary
The suite guards the live boundary between user-facing/adaptor surfaces, reusable intermediate results and candidate output release:

```text
User / UI / Voice / Attachments
          |
          v
 [Input Cohesion Gate]
          |
          v
 [Intent Equivalence Gate]
          |
          v
 [Interrupt Epoch Gate] ---- newer directive/cancel ----> invalidates old epoch
          |
          +---- [Cache Provenance Firewall]
          |
          v
 InteractionSnapshot (deterministic digest)
          |
          v
 Candidate model/tool stream
          |
          v
 [Completion Boundary Integrity Gate]
          |
          v
 Existing NEXY LAW / JUDGE / release / execution paths (future integration only)
```

## Core invariants
1. **No stale epoch commit**: an action prepared under epoch N cannot commit after epoch N+1 exists.
2. **No permissive cache substitution**: provenance mismatch is never converted into a hit.
3. **No silent cross-modality reconciliation**: critical intent mismatch freezes.
4. **EOF is not completion**: release requires a contiguous, identity-consistent stream plus an explicit final marker and matching full-payload digest.
5. **Missing material input is not guessed**: required resource gaps freeze.
6. **Extras are quarantined**: unreferenced resources do not enter the bound input set.
7. **No wall-clock authority**: current reference uses logical epochs and explicit contract hashes, avoiding hidden time dependence.
8. **Canonical fingerprints**: canonical JSON uses sorted keys and compact UTF-8 serialization; fingerprints use SHA-256.

## Components
### `common.py`
Canonical JSON/digest, decision vocabulary, input validation.

### `interrupt_epoch.py`
Mutable session-local epoch gate. Tokens and action leases are immutable dataclasses. Commit is single-use.

### `cache_provenance.py`
Reference in-memory cache. A production adapter may use Redis/database/object storage only if it preserves the exact namespace/integrity contract.

### `multimodal_intent.py`
Explicit intent-contract comparison. Raw ASR/OCR/vision semantics are OUT OF SCOPE and remain adapter responsibilities.

### `completion_boundary.py`
Verifies stream sequence, run/contract identity, final-marker placement, expected chunk count and final assembled byte digest. It never promotes transport EOF into semantic completion.

### `input_cohesion.py`
Explicit resource requirements and observed-resource matching. Unreferenced resources are quarantined.

### `coordinator.py`
Builds a deterministic `InteractionSnapshot` from a current epoch token, passing intent equivalence, passing input cohesion, and a policy hash.

## State machines
### Interrupt
`NO_ACTIVE -> ACTIVE(epoch n) -> ACTIVE(epoch n+1)` on new directive.  
`ACTIVE -> NO_ACTIVE(epoch n+1)` on cancellation.  
Any lease from an older epoch becomes invalid.

### Completion boundary
`EMPTY -> RECEIVING(seq 0..n) -> FINAL_MARKED -> VERIFIED_RELEASE`

Any missing/duplicate/out-of-order sequence, mixed run identity, mixed contract, illegal final marker placement, wrong expected count or final digest mismatch -> `FREEZE`.

### Cache
`MISS -> PUT -> EXACT_HIT` only under identical namespace+input.  
Foreign explicit entry validation -> `FREEZE`.

## Failure model
- integrity mismatch: `FREEZE`;
- ordinary absence where safe recomputation is possible: `REJECT`/cache miss;
- malformed construction: exception at boundary, forcing caller to correct explicit input;
- no auto-heal that changes semantics.

## Security/trust boundary
- hashes prove identity/integrity inside the reference protocol, not source authenticity by themselves;
- production must authenticate actors and store mutable state in durable, isolated backends;
- raw secrets should not be embedded in canonical digest payloads if fingerprints may be logged;
- stream digest validates bytes, not semantic truth; LAW/JUDGE verification remains a separate downstream authority;
- modality adapters are untrusted producers until their `IntentContract` passes equivalence checks.

## Concurrency law for future integration
Reference mutable objects are not thread-safe. A production adapter must serialize mutation by session/run/cache namespace or use atomic compare-and-set/transaction semantics. Concurrency is intentionally not hidden behind convenience locks in this reference because NEXY's canonical ordering law should own that decision.

## Version/evolution law
Every serialized envelope must be versioned before production use. A contract change that changes canonical fields invalidates old fingerprints unless an explicit migration verifier proves equivalence. Cache namespace version, intent schema and stream contract hash must evolve independently rather than relying on “compatible enough” parsing.

## Build order
1. canonical digest contract;
2. input cohesion + intent equivalence;
3. epoch preemption;
4. interaction snapshot;
5. cache namespace binding;
6. completion-boundary release gate;
7. persistent/concurrent adapters only after reference semantics are accepted.
