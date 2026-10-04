# NEXY Human Authority & Interaction Integrity Lab

**Status: AI_PROPOSED_CONCEPT / REFERENCE IMPLEMENTATION / NOT ADOPTED / NOT NEXY RUNTIME**

Durable session code: `CHAT-20261005-0121-NEXY-HUMAN-AUTHORITY-LAB`

This isolated lab explores one question: **can NEXY make human control simpler without weakening truth, scope, authority, or freeze semantics?**

It is additive research under `AI-CONTEXT/คลังข้อมูลเสริม`. It does not modify a NEXY.AI repository, does not claim adoption, and does not claim implementation/runtime/deployment evidence for NEXY.AI.

## Why this is distinct

Sibling labs already cover proof scheduling, evidence graphs, failure atlases, temporal validity, uncertainty, migration, reliability budgets, compatibility, replay/idempotency, and related proof infrastructure. This lab targets a different interface-control axis:

- deterministic objective-drift detection from declared outcome IDs;
- one-shot aggregation of material questions instead of repeated interruptions;
- exact consent binding for irreversible actions;
- role/state-aware progressive disclosure;
- mandatory visible FREEZE and false-success detection;
- evidence-bearing outcome acceptance;
- interaction-trace conformance and friction metrics.

## Source-grounded constraints

The design is motivated by current AI-CONTEXT NEXY context, especially:

- `projects/NEXY.AI/deep/human-control-surface.md`: visible != editable != executable; frozen system must look frozen; UX may guide attention but not decide reality; one guided question is allowed when needed but missing material facts must not be invented.
- `projects/NEXY.AI/deep/doc-d-product-design.md`: UI may not fabricate success, hide FREEZE, or substitute attractive UX for verified system truth.
- `projects/NEXY.AI/deep/doc-c-vnext-build-spec.md`: OWNER/OPERATOR/AUDITOR/SYSTEM permissions, explicit external-use input, FREEZE/STOP semantics, and UI truth requirements.
- `rules/VERIFICATION.md`: evidence class must match the claim.

Those are source facts. Every mechanism introduced by this lab is an **AI_PROPOSED_CONCEPT** until separately reviewed and adopted by authorized project authority.

## Reference engine

The TypeScript engine is intentionally dependency-free and offline. It evaluates a declared `IntentContract` plus an `ActionRequest` and returns one of:

- `ALLOW`
- `ASK`
- `FREEZE`

It never uses model confidence or semantic guessing. Scope, objective alignment, permission, external I/O, material unknowns, and irreversible consent are all represented explicitly.

The lab also provides:

- deterministic canonical JSON hashing;
- progressive disclosure planning;
- presentation truth checks;
- acceptance/evidence checks;
- trace/friction checks;
- 21 adversarial scenario fixtures;
- unit/adversarial tests;
- JSON Schemas for interchange.

## Run locally

```bash
npm test
npm run validate
node dist/src/cli.js examples/scenario.json
```

Expected CLI decision for the included example: `ALLOW` with reason `CONTRACT_CONFORMANT`.

## Evidence boundary

The local verification for this lab can prove only properties of this exact reference implementation. It cannot prove:

- NEXY.AI currently implements these mechanisms;
- the mechanisms improve real user satisfaction;
- the approach is production-safe under live traffic;
- the proposed contracts are compatible with every one of the 837 normalized source requirements;
- deployment readiness.

Those remain `NOT_VERIFIED` or `UNKNOWN` until the appropriate evidence exists.
