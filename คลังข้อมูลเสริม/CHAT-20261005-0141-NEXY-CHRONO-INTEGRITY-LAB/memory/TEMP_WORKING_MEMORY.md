# Temporary Working Memory / Resumption Checkpoint

## Mission

Create one novel supplemental NEXY-compatible engineering project without touching a NEXY.AI repository.

## Chosen gap

Clock/deadline integrity. Existing supplemental work already covers temporal truth, knowledge decay, delegation leases, counterfactuals, evidence, intent, side-effect transactions, and tool contract drift. The new project is lower-level and narrower: deterministic TTL/deadline semantics under wall-clock instability.

## Distinction to preserve

- Temporal truth: determines whether a proposition is still valid based on authority/dependencies/time.
- Delegation lease: constrains executable authority to a bounded plan.
- Chrono Integrity: supplies clock continuity and elapsed-deadline semantics only.

Do not collapse these into one subsystem.

## Locked semantics

- monotonic elapsed drives activation/expiration;
- wall time is a cross-check, not TTL authority;
- exact expiration boundary is closed: `elapsed >= timeout`;
- epoch mismatch, clock-ID mismatch, monotonic rollback, or excessive wall/monotonic divergence => `FREEZE`;
- child time budget may only narrow parent remaining budget;
- strict canonical serialization; unknown fields rejected;
- proposal is non-canonical and has no adoption authority.

## Local evidence before publication

- compileall: PASS;
- unittest: PASS 42/42;
- demo: PASS;
- randomized corpora: 1,000 valid-semantics cases + 500 over-skew freeze cases executed inside tests.

## Protected boundary

Never mutate any repository whose name contains `NEXY.AI` for this workstream.

## Next resume point

Verify all published files in `AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0141-NEXY-CHRONO-INTEGRITY-LAB`, compare Git blob identities against the tested local publish set, record repository evidence, and retain E3+ integration/deployment claims as NOT_VERIFIED.
