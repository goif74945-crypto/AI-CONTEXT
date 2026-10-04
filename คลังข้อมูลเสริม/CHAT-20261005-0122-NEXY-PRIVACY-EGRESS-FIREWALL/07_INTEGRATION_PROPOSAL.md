# Integration Proposal

**NON-GOVERNING. Adoption requires explicit project authority.**

## Suggested insertion points

1. **Context assembly:** candidate data gets stable IDs, purpose tags, sensitivity/provenance, and field policy.
2. **Pre-dispatch egress gate:** NPCEF evaluates exact downstream recipient identity immediately before outbound serialization.
3. **Dispatch lock:** payload is immutable or re-hashed between gate and transport so a caller cannot append context after approval.
4. **Audit:** value-free receipt is appended with policy/registry versions.
5. **UI:** `ASK` becomes a narrowly scoped consent/release decision; `BLOCK/FREEZE` becomes explicit reasoned state.

## Interfaces a production system would need

Purpose Registry; Recipient Registry; Data Policy Envelope; Grant Service; mandatory Egress Gateway; privacy-minimized Receipt Ledger.

## Compatibility strategy

Adopt in shadow mode first: evaluate but do not enforce; compare proposed release with existing context dispatch and measure false-positive/false-negative risk without recording raw payloads. Then enable enforcement for a narrow connector/model class, with explicit rollback. Do not globally flip enforcement until bypass analysis and negative-path integration tests exist.

## No hidden fallback

If the firewall is unavailable or policy identity cannot be resolved, production behavior should fail closed for protected egress. A “temporarily send everything” fallback defeats the entire boundary.
