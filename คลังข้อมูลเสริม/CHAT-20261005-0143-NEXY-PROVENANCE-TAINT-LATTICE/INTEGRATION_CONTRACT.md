# FUTURE INTEGRATION CONTRACT

> **AI-PROPOSED FUTURE CONCEPT ONLY. No NEXY.AI integration was performed.**

## Intended adapter boundary

A future NEXY-side adapter could use the lab without importing internal Python objects by exchanging the strict v1 JSON records:

- `nexy.provenance-taint.artifact/v1`
- `nexy.provenance-taint.receipt/v1`
- `nexy.provenance-taint.release-decision/v1`

## Suggested conceptual mapping

This is a proposal, not current truth:

- candidate model/tool output → source artifact;
- NEXY-controlled transform → `TransformContract`;
- verified claim/evidence → assurance tags;
- unresolved ambiguity/conflict/untrusted source → taints;
- final output boundary → `ReleasePolicy` + `release_decision()`;
- judge/verifier result → authenticated wrapper around a verification receipt;
- audit/Vault record → store artifact ID, receipt ID, decision record, and referenced evidence.

## Required production hardening before adoption

1. Replace free-form verifier identity with authenticated/signature-backed verifier credentials.
2. Compile canonical NEXY authority law into a domain representation. Do not adopt the reference numeric ranks as canonical law by accident.
3. Define assurance-tag registry and exact claim-to-evidence mapping.
4. Add durable lineage storage with transitive graph validation.
5. Add version negotiation and migration rules for wire schemas.
6. Add target-runtime load/fault/recovery tests.
7. Add adapter-level integration/E2E tests inside an explicitly authorized NEXY environment.

## Compatibility rule

The lab must remain optional and fail-closed. If an adapter cannot understand a schema, taint, assurance, receipt, or policy requirement, it should freeze rather than silently drop the unknown state.
