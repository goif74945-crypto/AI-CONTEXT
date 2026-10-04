# NEXY Lo4 — Evolution Compatibility Proof Compiler (ECPC-20)

Status: **AI-PROPOSED Lo4 reference lab / NON-CANONICAL / NON-GOVERNING**.

ECPC-20 is an isolated deterministic TypeScript/BigInt reference implementation for proving cross-version compatibility of schemas, APIs, events, WAL shapes, evidence contracts and migration plans before any future NEXY promotion decision.

It does **not** mutate NEXY state, does **not** replace CORE/JUDGE, does **not** auto-promote anything, and was built outside the NEXY repository.

## Why it exists
NEXY's architecture depends on versioned contracts, replay, evidence, deterministic state, freeze semantics, rollback and exact-head proof. Interface evolution can silently invalidate those guarantees even when each version looks locally correct. ECPC-20 turns compatibility from a vague boolean into reproducible proof artifacts.

## Numeric law
All authoritative risk/budget arithmetic uses signed-i128-carried Q64.64 via BigInt. JS Number is not accepted by the canonical hash layer. ECPC-20 fails closed on i128 overflow rather than wrapping or saturating.

## Build / verify
```sh
npm run typecheck
npm run build
npm test
```

Runtime has no third-party dependency; tests use Node's built-in test runner. Building requires TypeScript 5.8.3 (declared as a devDependency) or an equivalent verified compiler environment.

## Identity
- CHAT_ID: `CHAT-20261005-0310-NEXY-LO4-EVOLUTION-COMPAT-Q64-20`
- Platform-native chat ID: `UNKNOWN_NOT_EXPOSED_TO_AVAILABLE_TOOLS`
- NEXY read-only baseline: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
- Canonical NEXY source corpus SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`
- Sealed source archive SHA-256: `ef83a3ca988a4177b15f8a61910305bef7a5465a31d04f64aa5245ab1e9905be`
