# Source Alignment and Truth Classification

## SOURCE_FACT
From `projects/NEXY.AI/deep/human-control-surface.md` and current deep context:

- NEXY is a deterministic control hub, not a chat model as authority.
- Core authority and human-facing presentation are separate.
- Presentation may change wording/tone/pacing, but not truth, decision logic, validation, verification, law, security, or safety.
- UI must reflect real state.
- A frozen system must look frozen.
- The operator should know current position, permitted actions, and consequences without guessing.
- `visible ≠ editable ≠ executable`.
- FREEZE UI must expose primary incident, trigger, blocking layer, and recoverability.
- Loading/skeleton state cannot imply success.
- Product should make truth, authority, failure, and next legal action obvious without exposing all internal machinery.

## SOURCE_FACT
From current DOC-C context:

- System status includes `OK`, `DEGRADED`, `FREEZE`, `STOP`.
- Execution state includes `INIT`, `READY`, `RUNNING`, `VERIFYING`, `CONSENSUS`, `STABLE`, `FREEZE`, `STOP`.
- FREEZE blocks release.
- STOP is irreversible in the current build model and requires manual/admin intervention.
- Release requires specific gates; a state label alone is not proof of legal release.
- UI is truth rendering only; backend authorization remains authoritative.

## PROPOSAL
The Trust Card schema, exact display-mode names, exact deterministic copy, SHA-256 presentation fingerprint, and reference Python implementation are AI-proposed mechanisms for making those source rules executable at a presentation boundary.

## NOT VERIFIED
- NEXY currently uses this Trust Card schema.
- NEXY currently has the reference implementation.
- The proposed wording is final product copy.
- The proposal is compatible with every current frontend component without integration work.
- The proposal meets production accessibility, localization, or E2E requirements.

## Authority rule
If any proposal conflicts with canonical DOC-B/DOC-C/DOC-D or verified implementation behavior, the proposal loses. It must be revised or discarded rather than silently overriding project truth.
