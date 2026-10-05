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

## Fresh sibling scan — Wave 07 selection (AI-CONTEXT HEAD `4d90806b30648073eb4920ecd87867bb24c47a93`)

The following earlier planned waves are `SKIPPED_OVERLAP` at this checkpoint:

- **Wave 02 / 03:** Privacy Context Firewall `03_POLICY_AND_DATA_MODEL.md` blob `06fd6768fc2dd06251e081eca9c5375481aa369e` and Minimum-Disclosure Privacy Compiler `05_POLICY_CONTRACT.md` blob `2fd81107ecff532eee50cd375df09078e772fe3a` already specify destination/recipient retention, region, training/logging, deletion/expiry and capability-constrained disclosure boundaries.
- **Wave 04:** active sibling `CHAT-20261005-0327-GPT56SOL-NEXY-LO4-REVOCATION-CONVERGENCE-20/00_EXECUTION_MEMORY.md` blob `05270e37b7137133d5c0d7751283bf45f70bd8e1` explicitly owns revocation propagation, in-flight containment and stale-state detection.
- **Wave 05:** Directive Epoch Firewall `README.md` blob `3194c37695ea2d07cd3312720c515987f8e86145` and Edge Contracts novelty record blob `72e590a955cef22f0a1b10cd3d48d66a061e35cc` already implement/define commit-time stale-authority and exact approval-to-execution TOCTOU binding.
- **Wave 06:** Context Release Firewall `src/nexy_crf/engine.py` blob `9fcbd6ae109f612ccf5bc6ed203037cf8a983943` excludes values and unrequested-field metadata so receipts do not become unrelated-context correlation oracles.

A targeted current-tree search for grant bundling, batch consent and least-authority consent found no implementation outside this NPCEF plan; the only nearby external hit was an NMDPC research backlog about when a consent prompt is necessary. This is bounded search evidence, not a universal novelty claim. Wave 07 was therefore selected as the first inspected non-overlapping PLANNED wave.

## Fresh sibling scan — Wave 09 selection (AI-CONTEXT HEAD `6f34a9dfe750dd8eb29e757e65913f51dbf7337c`)

- **Wave 08 is `SKIPPED_OVERLAP`.** NEXY Interaction Economics Lab requirement/architecture already owns configurable friction budgets, deterministic `ASK_CLARIFICATION` / `CONFIRM` / `FREEZE` routing, preservation of law-required confirmations, and confirmation-fatigue regression research. Exact observed blobs: `01_CONCEPT_AND_REQUIREMENTS.md` `f942ecbe5c1ce047803244aa0a222606690d5612`; `README.md` `389a439282a0dd2a695dc4aa4aefacdb15951884`; `04_RESEARCH_BACKLOG.md` `8b1925423123549bb79cdc76438f3f000a2add3f`.
- **Wave 09 selected.** A bounded current-tree search for recipient alias/substitution/redirect resolution found no implemented privacy-egress route-binding mechanism outside NPCEF. Delegation Lease Lab mentions provider resource-alias canonicalization only as `NOT_VERIFIED`; provider/model-substitution labs address model semantics rather than the final privacy recipient route. This is bounded coordination evidence, not a universal novelty claim.
