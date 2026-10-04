# Roadmap — AI Proposal

## P0 — evidence binding
Bind each VERIFICATION event to explicit evidence objects: evidence class, source identity, command/tool identity, artifact hash and verifier identity.

## P0 — streaming format
Add NDJSON streaming integrity/replay so long multi-agent trajectories can be verified without loading the full capsule into memory.

## P0 — signed envelope
Add signature abstraction with algorithm agility and key identity. Keep hash-chain identity separate from signer trust.

## P1 — capability binding
Extend TOOL_INTENT with capability grant digest, scope, expiry/lease and protected resource identity.

## P1 — semantic counterfactuals
Add policy-controlled substitutions such as changed authority ref, changed evidence state or changed tool result and report the earliest replay divergence.

## P1 — privacy compartments
Separate public receipt, restricted metadata and encrypted private payloads. Define retention and redaction rules.

## P2 — cross-agent DAG
Move beyond the single ordered chain to deterministic parent-linked subtraces for parallel agents while preserving a canonical merge law.

## Promotion rule
No roadmap item becomes NEXY current requirement merely because this document proposes it.
