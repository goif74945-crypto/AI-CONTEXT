# Reference API Contracts

These contracts describe the current standalone reference implementation, not NEXY canon.

## Interrupt Epoch
**Inputs**: session id, directive id, explicit directive payload; later action payload.  
**Outputs**: immutable `EpochToken`, optional `ActionLease`, `GateDecision`.  
**Invariant**: token/lease epoch must equal current session epoch and embedded digests must recompute exactly.  
**Mutation**: begin/cancel advances logical epoch; committed lease becomes consumed.

## Cache Provenance
**Inputs**: `CacheNamespace`, logical input value, cached value.  
**Output**: deterministic key/envelope or decision + value on verified hit.  
**Invariant**: project/user/policy/model/tool/schema/input identity must match exactly.  
**Safe absence**: normal exact-key miss is REJECT/MISS, not FREEZE.

## Multimodal Intent
**Inputs**: one explicit `IntentContract` per required modality.  
**Output**: PASS/FREEZE plus stable equivalence fingerprint.  
**Invariant**: required modalities are unique/present and critical normalized fields equal.  
**Forbidden**: deriving missing semantics from raw media inside the gate.

## Completion Boundary
**Inputs**: ordered `StreamChunk` list and optional expected chunk count.  
**Output**: PASS/FREEZE plus stable release fingerprint.  
**Invariant**: one run, one contract, contiguous sequences from zero, one tail final marker, correct complete-payload hash.  
**Forbidden**: treating EOF, timeout or “looks complete” syntax as completion evidence.

## Input Cohesion
**Inputs**: explicit requirement list and observed resource list.  
**Output**: bound resource IDs, quarantined extra IDs, stable fingerprint or FREEZE.  
**Invariant**: each required id resolves uniquely with exact kind/trust/digest constraints.

## Interaction Coordinator
**Inputs**: current epoch token, passing intent result, passing input result, policy hash.  
**Output**: `InteractionSnapshot`.  
**Invariant**: snapshot is built only from current/passing gates and has a canonical deterministic digest.
