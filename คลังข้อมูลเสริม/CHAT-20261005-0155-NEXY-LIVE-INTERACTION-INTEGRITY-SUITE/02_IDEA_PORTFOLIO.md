# Five AI-Proposed Concepts

Classification for every item below: **AI_PROPOSED_CONCEPT / EXPERIMENTAL / NOT ADOPTED**.

## 1. Interrupt Epoch Preemption Kernel (IEPK)
### Problem
A user can supersede an in-flight directive while an agent/tool chain is still working. Without an explicit preemption law, stale work may finish after the user's newer instruction and create the exact kind of “I told it to stop and it still acted” failure that destroys trust.

### Design
Every directive advances a logical epoch. Work carries an epoch token. Side-effect preparation creates a single-use action lease bound to session, directive, epoch, directive digest and action digest. A newer directive or cancellation invalidates older leases without relying on wall-clock time.

### User value
- immediate, deterministic stop/supersede semantics;
- prevents stale sends/writes after user correction;
- makes interruption auditable and replayable.

### NEXY fit
Matches USER LAW, explicit state, deterministic ordering and FREEZE-on-integrity-failure principles.

## 2. Cache Provenance Isolation Firewall (CPIF)
### Problem
AI/tool results are tempting to cache. A cache hit from another user, project, policy revision, model contract or tool contract can be fast and catastrophically wrong.

### Design
Cache keys and entry envelopes bind project, user scope, policy hash, model-contract hash, tool-contract hash, schema version and exact input digest. Foreign entries fail closed; normal exact-key absence is a cache miss, not an invented fallback.

### User value
- speed without cross-context truth leakage;
- stale provider/tool results are naturally invalidated when contracts change;
- easier provenance audits.

### NEXY fit
Extends source provenance and explicit authority into performance optimization without letting cache become hidden authority.

## 3. Multimodal Intent Equivalence Gate (MIEG)
### Problem
The same user intent may enter through text, voice, image-derived controls, or future interfaces. Different adapters can disagree on target, external-access permission, deterministic requirement, mode or constraints.

### Design
Each modality adapter must emit an explicit `IntentContract`. The gate compares critical fields exactly after conservative normalization. It does not infer from raw media. Any material divergence freezes for clarification or adapter repair.

### User value
- voice/image convenience cannot silently change what RUN will do;
- external-access and target mismatches become visible before execution;
- supports future multimodal UX while preserving Core semantics.

### NEXY fit
Keeps presentation/input flexibility below deterministic authority.

## 4. Completion Boundary Integrity Gate (CBIG)
### Problem
Streaming model/tool output can stop because of token ceilings, network interruption, provider timeout, process failure, adapter bugs or chunk loss. A transport EOF is not proof that the semantic result is complete. Releasing a truncated JSON object, partial patch or half-written answer as FINAL would violate NEXY's truth surface.

### Design
The producer emits ordered `StreamChunk` records carrying one `run_id` and one `contract_hash`. Sequences must be contiguous from zero. Exactly one final marker must exist and it must be the last chunk. Only the final chunk carries the SHA-256 of the complete assembled byte payload. The gate reassembles bytes, verifies expected chunk count when supplied, then verifies the final digest. Missing final marker, sequence gap, duplicate sequence, mixed run identity, mixed contract, misplaced final marker or hash mismatch freezes.

### User value
- incomplete streamed results cannot masquerade as complete;
- token/network truncation becomes an explicit integrity event instead of a mysterious malformed artifact;
- streaming UX remains possible without weakening the release boundary.

### NEXY fit
Implements “one legal verified output or freeze” at the stream-to-final transition and reinforces DOC-D's rule that pending/loading state must not imply success.

## 5. Input Cohesion Gate (ICG)
### Problem
Users often reference “the file above”, an attachment, a URL, or a prior artifact. If the expected resource is missing, duplicated, tampered, wrong-kind, or low-trust, an AI may hallucinate around the gap. Extra attachments can also be silently consumed when they were not intended for the task.

### Design
The directive carries explicit `InputRequirement` records. Observed resources are bound only when id/kind/trust/digest constraints match. Missing or ambiguous required resources freeze. Unreferenced resources are quarantined, never auto-included.

### User value
- fewer “it used the wrong file” failures;
- no pretending an attachment exists when it does not;
- clearer, minimal data exposure.

### NEXY fit
Directly implements the later strict source law: do not guess missing material data.

# Why these five belong together
They form a live-interaction integrity chain with two release-side guards:

`INPUTS COHESIVE → INTENT EQUIVALENT → DIRECTIVE EPOCH CURRENT → PROVENANCE-SAFE REUSE → STREAM COMPLETION VERIFIED → RELEASE CANDIDATE`

They are deliberately narrow and composable. None claims to replace NEXY LAW/JUDGE/SWARM, side-effect transaction orchestration, deployment evidence, or existing authorization systems.
