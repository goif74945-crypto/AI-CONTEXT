# Integration Notes — Proposal Only

This file describes possible future integration patterns. It does not instruct modification of NEXY.AI now.

## Candidate product value

### User-facing trust receipt
A NEXY result could optionally expose a compact receipt:
- verified / freeze state;
- authority fingerprint;
- evidence-status counts;
- number of external actions;
- output digest;
- capsule ID for audit/replay.

The UI would show trust metadata without exposing hidden internal reasoning or sensitive raw tool payloads.

### Debugging / support
Given a capsule ID, engineers could compare a failing run with a known-good run and identify whether divergence came from authority identity, context/event payload, tool path, verification or final output.

### Regression corpus
High-value real failures could be preserved as capsules and replayed after code/policy changes. A changed replay result becomes a deterministic regression signal.

### Safe action audit
Tool intent/result pairing creates a compact side-effect ledger. In a future authorized integration, capability policy could be bound into each intent digest so a result cannot be detached from the exact action contract that authorized it.

## Integration gate

Before any NEXY.AI integration, require:
1. explicit project-authority approval;
2. mapping to current DOC-C obligations or an authorized future scope;
3. security review;
4. performance tests against realistic trajectory sizes;
5. signature/authentication design if capsules cross trust boundaries;
6. privacy classification for stored payloads;
7. migration/versioning law;
8. runtime evidence at the exact NEXY revision.
