# Concurrent Overlap Boundary

**Status:** AI-PROPOSED coordination record  
**Purpose:** prevent this mission from duplicating a sibling lab that appeared concurrently after NPCEF began.

## Observed concurrent sibling

A later AI-CONTEXT commit created:
`คลังข้อมูลเสริม/CHAT-20261005-0122-NEXY-CONTEXT-RELEASE-FIREWALL/03_PRIVACY_CONTRACT.md`

That sibling CRF contract overlaps NPCEF on:
- explicit purpose + consumer binding;
- minimization/default deny;
- required-item atomic non-release;
- expiry;
- value-free receipts;
- deterministic canonical receipt/fingerprint behavior.

It additionally owns or already specifies areas that NPCEF should **not independently re-invent** without a specific comparative task:
- compartment monotonicity;
- derived sensitivity monotonicity;
- derived compartment monotonicity;
- derived purpose non-broadening;
- trusted declassification registry semantics;
- field provenance requirements.

## NPCEF differentiation lock

Future waves in this mission should focus on complementary concerns:
1. `ASK` and human release-consent lifecycle;
2. exact recipient grant/revocation semantics;
3. recipient capability envelopes: retention, training-use, region, deletion, logging;
4. evaluation-to-dispatch TOCTOU protection;
5. queued/retried/duplicated egress and revocation races;
6. audit-receipt metadata side-channel minimization;
7. purpose taxonomy drift and alias attacks;
8. downstream retention/deletion attestations;
9. streaming/partial-send revocation behavior;
10. consent-fatigue and grant-bundling safety;
11. policy-version invalidation and replay;
12. shadow/adoption experiments and operational evidence design.

## Coordination law

Before every future substantial wave:
- refresh recent sibling work;
- if another project now owns the planned topic, mark that wave `SKIPPED_OVERLAP` or pivot to an explicitly complementary experiment;
- never edit the sibling project;
- never merge sibling proposals into NEXY authority automatically;
- preserve provenance: independent concurrent invention does not increase authority.

This boundary is coordination metadata, not NEXY governing architecture.
