# Proposed NEXY Integration Contract

**Status:** AI-PROPOSED / NOT INTEGRATED / NOT A CURRENT BUILD CLAIM

## Intended host boundary
The current DOC-C architecture places provider workers behind `SWARM` through an `AgentAdapter` contract. If this lab is ever promoted into the real implementation, the narrowest compatible location is therefore **before a candidate adapter becomes enabled in SWARM**, not in UI, VAULT, JUDGE or LAW.

## Proposed promotion sequence
1. Candidate provider implementation exists on an explicitly authorized NEXY branch.
2. Build emits or maintains an `AgentAdapterManifest` matching this lab contract.
3. TypeScript/Zod boundary validation checks the manifest.
4. Certification rules reject unsupported mode/timeout/authority/retry/secret semantics.
5. Adapter unit tests prove `execute/cancel/healthcheck` behavior.
6. Integration tests prove SWARM invokes the adapter without forbidden direct dependencies.
7. Runtime fault tests prove timeout/cancel/provider failure behavior.
8. Only then can a real NEXY task decide whether the adapter is enabled.

## Hard compatibility boundaries
A promoted implementation must preserve current DOC-C behavior:
- `SWARM -> VAULT` remains forbidden;
- adapter output is candidate material, not a release token;
- LAW/JUDGE/CORE remain downstream authorities;
- result data is revalidated at boundaries;
- no automatic retry is silently introduced;
- critical timeout remains canonical unless a newer authority explicitly changes it;
- provider secrets stay server-side/runtime-injected.

## Evidence needed for any future integration claim
- **E1:** TypeScript compile/typecheck + Zod/static contract proof.
- **E2:** adapter unit suite.
- **E3:** real SWARM adapter integration tests.
- **E5:** real runtime timeout, cancellation, provider outage and health behavior.
- **E6:** only if claiming deployment of the exact build.

This lab currently provides E1/E2 only for itself. It provides no E3/E5/E6 evidence for NEXY.AI.
