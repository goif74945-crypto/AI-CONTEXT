# NEXY.AI First-Class Handoff System

## Purpose
Provide versioned, machine-readable, resumable packages for deterministic role transfer without trusting hidden reasoning or generic "done" claims.

## Canonical artifacts
- `handoff.schema.json` — package contract (v2.0.0).
- `registry.json` — discoverable handoff types and semantic rules.
- `examples/auditor-to-builder.json` — golden Auditor → Builder package.
- `examples/builder-to-auditor.json` — golden Builder → Auditor result package.
- `examples/negative-stale-head.json` — stale-head negative case.
- `PROTOCOL.md` — lifecycle, freshness, supersession, resume and security law.
- `validation-report.md` — current structural validation evidence.
- `example.json` — compatibility alias to the canonical Auditor → Builder example.

## Directional contracts
### AUDITOR → BUILDER
Carries audit/finding identity, exact target HEAD, claims/proofs, affected requirements/entities/invariants, dependency closure, allowed/forbidden scope, acceptance/tests/security/evidence obligations, rollback and stop conditions.

### BUILDER → AUDITOR
Carries command/handoff reference, exact start/end HEAD, changed files/commits/actions, executed tests/results/evidence, failures/residual risks/blockers, rollback state and status.

## Freshness law
Receiver MUST compare `CURRENT_HEAD == EXPECTED_HEAD` before executing an Auditor → Builder package.
Mismatch ⇒ **STALE**; do not mutate from the original package. Revalidate semantic diff + impact, then issue a superseding package or block.

## Supersession law
Packages are immutable history. A new package may list prior `handoff_id` values in `supersedes`.
Supersession cycles are invalid.

## Security law
Never embed secrets, tokens, credentials, private keys, recovery codes, or secret-bearing environment values.

## Authority law
Handoff packages are execution/navigation objects only. Current user directive, governance, canonical spec/requirements and current evidence retain authority.
