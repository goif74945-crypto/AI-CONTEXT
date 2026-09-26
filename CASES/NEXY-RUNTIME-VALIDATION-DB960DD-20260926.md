# NEXY runtime validation case — 2026-09-26

- Target: `goif74945-crypto/NEXY.AI-`
- Branch: `astra/omega-full-spec-convergence`
- Exact head: `db960dd163a9f50373b747ac922d735d1250cf3a`
- Scope: isolated Railway validation only

## Observed

The builder resolved Node 22.23.2 and completed the web build. The fresh diagnostic deployment `69718a63-2b50-42d0-a59c-1f4554087250` reported a PATH containing `/mise/shims`, but did not resolve `node`, `npm`, or `npx`; the checked Node installation directory was absent. Earlier runtime attempts consequently returned exit 127 for Node-based gates.

The source subset is not release-clean: API branch coverage was 84.92% against an 85% threshold. Redis preparation passed in the isolated dependency setup. Browser E2E, E7, auth-abuse, incident-drill, release-attestation, and production-provider proof remain unverified.

## Decision

Classify as `PARTIAL_NON_DEPLOYABLE`. Keep production blocked. Do not infer runtime or release readiness from the successful builder/source subset.

## Recovery

Provide a provider-supported runtime image/configuration containing Node 22, npm, and npx, then rerun all exact-head runtime gates. Repair coverage and restore a working exact-head execution host before reconsidering release status.

## Trace

`NEXY-RUNTIME-VALIDATION-DB960DD-20260926`
