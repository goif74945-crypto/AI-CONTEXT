# ECRPF-20 Design Contract

## Problem

Current NEXY already has several strong configuration components, but they live at different truth boundaries:

- `packages/api/vnext-config.ts` defines canonical API defaults.
- `packages/config/runtime-config.ts` versions mutable runtime configuration and explicitly freezes immutable references.
- `packages/api/live-config.ts` serializes config update/rollback and emits evidence.
- `scripts/deployment-provider-contract.ts` requires explicit provider/project/token inputs and refuses to invent them.
- `core-kernel/build.rs` binds normalized build environment into `NEXY_BUILD_ENV_HASH`.
- `packages/api/middleware/rate-limit.ts` states that fail-open is development-only and production defaults fail-closed.
- process environment variables remain distributed across boot, queue, provider, security, and runtime surfaces.

ECRPF targets the seam **between** those systems: proving that a proposed effective configuration is coherent across sources before the existing authoritative update/deployment path is invoked.

## State model

`LOAD RULES -> VALIDATE SNAPSHOTS -> RESOLVE PRECEDENCE -> CHECK CLOSURES -> CHECK SAFETY -> CHECK ROLLOUT -> SCORE BLAST RADIUS -> COMPILE PROOF -> VERIFY-ONLY HANDOFF`

Any malformed rule, ambiguous same-source value, invalid Q64 ratio, negative runtime version, or authoritative contradiction fails closed.

## Data invariants

- Keys are canonical uppercase identifiers.
- Rule IDs are unique.
- Each source has a deterministic precedence rank per key.
- Same key/source may not produce two candidate values.
- Sensitive values are reference-only and must originate from `SECRET_PROVIDER`.
- Production cannot activate a `FAIL_OPEN_DEV_ONLY` mode.
- Build-immutable keys cannot change across candidate runtime rollout.
- Dependency references must point to defined rules.
- Rollout fractions and criticality are Q64.64 `[0,1]`.
- Rollout step comparison allows exactly one raw Q64 ULP only to compensate for independent rational truncation (for example encoded 0.2 minus encoded 0.1); a two-ULP excess fails.
- Candidate ordering cannot change proof bytes.
- Proof output is advisory Lo4 evidence only.

## Threat model

ECRPF is designed to detect or block: configuration key typos, missing production requirements, forbidden dev-only settings, invalid type/range values, plaintext secret injection, precedence ambiguity, hidden default shadowing, dependency gaps, mutually-exclusive modes, production fail-open, build/runtime drift, nondeterministic cohort assignment, unsafe rollout jumps, broken rollback targets, schema dependency orphaning, and unbounded configuration blast radius.

It does not authenticate callers, fetch secrets, execute deployment providers, read live infrastructure, replace NEXY authorization, or prove production behavior.
