# Adoption Gates

**All gates are proposals. None are currently NEXY build obligations.**

A project authority considering NPCEF should require at least:

1. **Authority gate:** explicit owner adopts policy semantics and defines who may change them.
2. **Ontology gate:** sensitivity, purpose, recipient, and provenance vocabularies are versioned and unambiguous.
3. **Identity gate:** recipient IDs and grant issuers are authenticated.
4. **Enforcement gate:** no alternate outbound path bypasses the firewall.
5. **Recursive-data gate:** nested, binary, streamed, transformed, and derived data have defined minimization behavior.
6. **Revocation gate:** revocation reaches dispatch before reuse, including queued/retried work.
7. **Audit-privacy gate:** item IDs, field names, reasons, and metadata are checked for side-channel leakage.
8. **Cryptographic-lineage gate:** receipts bind exact policy/registry/code versions and are authenticated where evidence integrity matters.
9. **Integration gate:** E3 tests prove dispatch receives exactly the approved payload.
10. **E2E gate:** E4 tests prove user consent/block/freeze flows cannot be bypassed.
11. **Operational gate:** E5 tests cover failure, retry, concurrency, stale policy, policy-store outage, and revocation races.
12. **Legal/privacy review gate:** appropriate human/legal privacy review maps application semantics to actual obligations; the prototype itself is not a compliance determination.
13. **Performance gate:** latency/memory/load are measured without weakening fail-closed behavior.
14. **Rollback gate:** enforcement can be rolled back without silently reverting to unconstrained egress.

Failure of any hard gate should retain this lab as research rather than promote it into governing architecture.
