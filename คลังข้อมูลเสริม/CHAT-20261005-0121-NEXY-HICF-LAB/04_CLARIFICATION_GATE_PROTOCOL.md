# 04 — CLARIFICATION GATE PROTOCOL

## Objective

Make “ask vs act vs freeze” explicit and auditable.

## Gate sequence

### Gate A — authority
- `CONFLICT` → FREEZE.
- `UNRESOLVED` + mutation/high-impact/irreversible → ASK.

### Gate B — prohibition
If the next capability is explicitly prohibited by the scoped contract → FREEZE.

### Gate C — unknown materiality
- CRITICAL → FREEZE.
- MATERIAL → ASK.
- NON_MATERIAL → may continue if other gates allow.

### Gate D — reversibility and impact
Even a noncritical unknown is promoted to clarification when the action is irreversible or critical-impact.

### Gate E — friction advisory
Only after the hard decision is known, inspect whether the interaction itself is becoming wasteful. Friction findings can change *how* questions are grouped or phrased, not whether required questions disappear.

## Required reason codes

Every non-PROCEED state should expose machine-readable reason codes. A UI may render friendly text, but should not replace the underlying reason record.

## Example

User objective: inspect a repository. Target branch is missing.

- read-only repository inventory: branch ambiguity may be non-material if default branch is authoritative → PROCEED;
- delete a file: branch ambiguity becomes material and mutation is irreversible → ASK/FREEZE depending authority and prohibition.

The same unknown can therefore have different action-relative materiality in a fuller future implementation. The v0 prototype stores materiality in the intent record and does not yet compute it dynamically.
