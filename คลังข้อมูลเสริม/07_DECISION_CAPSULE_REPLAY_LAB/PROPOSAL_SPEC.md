# Proposal Specification — Decision Capsule & Replay v0.1

Status: **AI PROPOSAL**  
Authority: advisory only; cannot override NEXY project law or build spec.

## Objective

Provide a deterministic record format and replay validator for a single AI/control decision so later systems can answer:

- What request was being handled?
- Which context and authority identity governed it?
- Was execution legally allowed or frozen?
- Which side-effect intents were issued and which results matched them?
- What verification states existed before terminal output?
- Has any event, authority reference or output been modified?
- Does a counterfactual capsule structurally diverge from the original?

## Required properties

1. Capsule identity is content-derived, not clock-derived.
2. Authority references are hashed into a normalized fingerprint.
3. Events form an ordered tamper-evident chain.
4. Every tool result must reference a unique prior intent.
5. Tool execution is forbidden after a FREEZE decision.
6. PASS requires verification evidence inside the capsule model.
7. Final output is represented by a digest even when UI exposes only a receipt.
8. AI proposal status is immutable in v0.1 serialization.
9. Invalid structure fails closed with explicit exceptions / non-zero CLI exit.
10. Replays have no network/filesystem/random/clock dependency beyond reading the provided capsule file.

## Event protocol

Legal high-level path:

`REQUEST -> CONTEXT_SELECTED -> AUTHORITY_RESOLVED -> DECISION`

If `DECISION=ALLOW`:

`[TOOL_INTENT -> TOOL_RESULT]* -> VERIFICATION+ -> FINAL`

If `DECISION=FREEZE`:

`FINAL(FREEZE)`

v0.1 intentionally keeps the grammar narrow. A future version may support richer parallel tool DAGs, retries and multiple authority checkpoints, but those are not silently accepted today.

## Terminal semantics

- `PASS`: ALLOW exists; >=1 verification; all verification states PASS.
- `FAIL`: requires at least one FAIL verification.
- `BLOCKED`: requires at least one BLOCKED verification.
- `FREEZE`: requires FREEZE decision or non-PASS verification freeze signal.
- `NOT_VERIFIED`: valid when proof is absent or explicitly NOT_VERIFIED; it must never be auto-promoted to PASS.

## Proposal isolation rule

Serialized capsules carry:

`AI_PROPOSAL_NOT_CANONICAL_NEXY_REQUIREMENT`

The loader rejects a rewritten value such as `CANONICAL_NEXY_REQUIREMENT`. Promotion, if ever authorized, requires a different governance process and likely a new schema version.
