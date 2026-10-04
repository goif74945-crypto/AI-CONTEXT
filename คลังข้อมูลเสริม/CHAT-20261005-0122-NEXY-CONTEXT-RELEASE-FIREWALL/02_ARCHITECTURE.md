# AI-Proposed Architecture — NEXY Context Release Firewall (CRF)

Classification: **AI_PROPOSED_CONCEPT**
Implementation status in NEXY.AI: **NOT_VERIFIED**
Reference implementation: this lab only.

## 1. Problem
A multi-agent control hub gains power by giving workers context. It also gains risk by giving workers too much context.

The dangerous default is:
`task + giant project dump + secrets + unrelated history → external model`

CRF replaces that with:
`explicit request + explicit policy + labeled context + trusted grants → deterministic least-context release or FROZEN`

The firewall is not an LLM prompt. It is an authority boundary.

## 2. Placement
Conceptual path:

```text
USER / TASK GRAPH
      |
      v
NEXY authority / task planner
      |
      | explicit ReleaseRequest
      v
+----------------------------+
| Context Release Firewall   |
| - request validation       |
| - policy validation        |
| - taint/provenance checks  |
| - purpose binding          |
| - compartment gate         |
| - sensitivity gate         |
| - declassification trust   |
| - atomic release           |
+----------------------------+
      | RELEASED payload + receipt
      | or FROZEN + receipt
      v
MODEL / AGENT / SERVICE
```

CRF never decides the user's purpose. The upstream authority layer must provide it explicitly.

## 3. Core objects

### ContextField
A named context object with:
- value;
- sensitivity;
- provenance;
- compartments;
- allowed purposes;
- derived-from edges;
- optional expiry.

### ContextSet
Immutable mapping from key to ContextField for one evaluation.

### ReleaseRequest
Explicit request from an upstream authority:
- request id;
- consumer identity;
- purpose;
- required keys;
- optional keys;
- requested compartments.

### ReleasePolicy
Consumer boundary:
- permitted consumer id;
- explicit purposes;
- maximum sensitivity;
- permitted compartments;
- whether declassification is even eligible.

### DeclassificationGrant
An explicit, purpose/consumer/time/field-bound lowering authorization.
The reference engine accepts one only when its canonical digest already exists in a trusted registry supplied at engine construction time.

### ReleaseReceipt
Value-free policy evidence:
- status;
- request/policy/context-metadata hashes;
- payload hash only when payload is actually released;
- field decision reason codes;
- evaluation time;
- engine version;
- receipt hash.

Blocked values and per-blocked-field value hashes are intentionally absent.

## 4. Sensitivity lattice

Reference ordering:

```text
PUBLIC < INTERNAL < CONFIDENTIAL < PRIVATE < SECRET < RESTRICTED
```

This is an AI-proposed reference vocabulary, not a claim that NEXY Canon currently mandates these six levels.

A consumer policy is a ceiling. A field above that ceiling is blocked unless an exact trusted declassification grant permits lowering to a level at or below the ceiling.

## 5. Compartment model
Sensitivity answers “how sensitive?”. Compartments answer “which domain?”.

Examples:
- `project-alpha`
- `billing`
- `security-response`

A field may carry multiple compartments. Release is allowed only when all field compartments are included in the request's permitted compartments, and the request itself may not ask outside the policy's allowed compartments.

## 6. Purpose binding
Purpose is exact data, not inferred intent.

A field with no explicit purpose list is unrestricted by this dimension. A field with a purpose list may be released only for a matching request purpose.

A ReleasePolicy must always carry at least one explicit allowed purpose. There is no wildcard policy in the reference implementation.

## 7. Derived-data taint
A summary, embedding, transformed document, or feature vector may still reveal its sources. CRF therefore validates metadata before release.

For a derived field:
- sensitivity >= maximum source sensitivity;
- compartments include the union of source compartments;
- if any source restricts purpose, the derived purpose set cannot be empty and must be a subset of the intersection of inherited restrictions;
- the dependency graph must be acyclic and all source keys must exist.

This is conservative by design. A future formally proven transformation could justify controlled downgrading, but that belongs behind an explicit governed declassification mechanism, not an optimistic metadata edit.

## 8. Atomicity rule
If any **required** key is missing or blocked:

```text
status = FROZEN
payload = {}
payload_hash = null
```

This prevents a consumer from receiving half of a supposedly complete context bundle and then improvising around missing authority-bearing information.

Optional failures do not freeze the release. They are recorded as BLOCK decisions and omitted.

## 9. Determinism
Reference canonicalization:
- UTF-8 JSON;
- object keys sorted;
- compact separators;
- set/frozenset sorted deterministically;
- floats rejected;
- SHA-256 over canonical bytes.

Floats are rejected because NaN/Infinity and cross-runtime formatting semantics are a needless ambiguity at an authority boundary. Numeric measurements can use integers plus units or canonical decimal strings in a future contract.

## 10. Declassification trust separation
A grant object is not authority merely because it exists.

CRF is instantiated with:
`trusted_grant_digests = {grant_id: canonical_grant_sha256}`

At release time a supplied grant must:
- match field key;
- match original sensitivity;
- lower to <= policy ceiling;
- match consumer and purpose;
- be inside its time window;
- have an exact digest already in the trust registry.

Tampering with any field changes the digest and invalidates the grant.

Production-grade cryptographic signature verification is deliberately not faked in this reference. In a real NEXY integration, the trusted digest set should be populated only by the governing authority/signature path.

## 11. Failure semantics
Primary reason codes:
- `MISSING_REQUIRED`
- `MISSING_OPTIONAL`
- `EXPIRED`
- `PURPOSE_MISMATCH`
- `COMPARTMENT_MISMATCH`
- `SENSITIVITY_EXCEEDS_POLICY`
- `POLICY_ALLOW`
- `DECLASSIFIED`

Structural validation raises explicit errors for:
- consumer mismatch;
- purpose not in policy;
- request compartment escalation;
- noncanonical values;
- derived cycles;
- unknown derivation source;
- taint downgrades/broadening.

## 12. Trust boundaries
CRF does not trust:
- caller-supplied grant claims;
- context metadata that violates derivation invariants;
- consumer-requested compartments beyond policy;
- unspecified purpose;
- stale/expired fields.

CRF does trust, by construction:
- the ReleasePolicy object supplied by the upstream policy authority;
- the trusted grant digest registry supplied at engine construction;
- the caller-supplied evaluation timestamp only for this standalone reference.

A production integration should source time from an authoritative clock and policy/grant state from governed NEXY components.

## 13. What this system does not solve
- semantic inference of what context a task truly needs;
- secret discovery/classification from raw unlabeled text;
- cryptographic identity/signature infrastructure;
- secure deletion;
- provider-side retention/training policy;
- encrypted transport;
- endpoint compromise;
- side channels;
- production authorization.

CRF starts **after** context classification and **before** boundary release.

## 14. Integration hypothesis
If later promoted, a sensible integration point is between task decomposition and model-provider dispatch:

1. task planner declares purpose + required/optional context keys;
2. policy layer selects consumer policy;
3. Vault/context layer provides labeled ContextSet;
4. CRF returns RELEASED/FROZEN;
5. dispatcher may send only RELEASED payload;
6. receipt is attached to task evidence without blocked values.

This is a proposal, not current NEXY implementation truth.
