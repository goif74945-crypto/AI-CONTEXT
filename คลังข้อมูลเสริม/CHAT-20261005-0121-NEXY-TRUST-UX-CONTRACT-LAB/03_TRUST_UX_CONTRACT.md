# Trust UX Contract

**Classification:** AI-PROPOSED architecture/reference contract.

## Objective
Transform an authoritative backend envelope into a compact human-facing presentation model while preserving truth, authority, and failure semantics.

## Non-goals
The compiler does not:
- decide release policy;
- authenticate or authorize;
- recover the system;
- mutate Core state;
- infer missing intent;
- manufacture evidence;
- choose a better answer than the backend supplied;
- reinterpret unknown incident codes.

## Input contract
Minimum fields:
- `status` — canonical system status;
- `state` — canonical execution state;
- `request_id`;
- `trace_id`;
- `data` — optional backend payload;
- `error` — optional structured error;
- `freeze` — optional freeze metadata;
- caller-supplied role.

The role is used only to determine which request/read actions may be *shown*. It does not grant permission.

## Output contract
A Trust Card contains:
- exact backend `system_status` and `system_state`;
- deterministic `display_mode`;
- direct headline/summary;
- whether the UI must block release;
- whether a result may be shown;
- at most one primary action;
- bounded secondary actions;
- request/trace identity;
- incident/freeze fields when applicable;
- evidence/integrity indicators when supplied;
- deterministic fingerprint;
- truth flags explaining enforced invariants.

## Display modes

### RESULT
Allowed only when the supplied authoritative STABLE envelope also carries explicit proposal-level release proof fields:
- `accepted == true`;
- `releaseable == true`;
- non-empty `integrity_hash`.

This local reference gate is intentionally stricter than merely checking `STABLE`. It does **not** replace DOC-C release policy.

### HOLD
Used when backend state is STABLE but the supplied envelope does not carry enough release proof for the presentation reference to expose the result.

HOLD is a **presentation withholding mode**, not a new Core state.

### FREEZE
Mirrors authoritative FREEZE. Result is always hidden. Incident and blocking information are surfaced. OWNER may be shown a Recover request only when backend metadata says recovery is allowed.

### STOP
Mirrors authoritative STOP. No automatic Recover action is emitted.

### PENDING
Used for INIT/RUNNING/VERIFYING/CONSENSUS. Never displays result as successful.

### READY
Used for READY. Operator/Owner may be shown New Directive; read-only roles get a read action.

## Determinism
The reference implementation uses no clock, randomness, network, filesystem mutation, model call, or external dependency in the compilation function.

For the same normalized input object and same role, the output is byte-stable under canonical JSON serialization and yields the same SHA-256 presentation fingerprint.

## Failure semantics
Unknown state/status or malformed critical fields raise `ContractError`.

Unknown incident/error code is preserved as an opaque identifier and rendered generically. The compiler must not guess a causal interpretation.

## Security/authority invariant
Every emitted mutation-like action is only a UI request affordance and carries `requires_backend_authorization=true`. Backend permission checks remain mandatory.
