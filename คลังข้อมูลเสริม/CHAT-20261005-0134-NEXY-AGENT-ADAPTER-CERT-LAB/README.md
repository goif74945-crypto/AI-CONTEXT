# NEXY Agent Adapter Certification Lab

**Session/work code:** `CHAT-20261005-0134-NEXY-AGENT-ADAPTER-CERT-LAB`

## Status
Standalone engineering lab stored in `AI-CONTEXT`. It does **not** modify the NEXY.AI implementation repository and does **not** claim current integration.

## Why this exists
NEXY treats external models as workers, while NEXY remains the authority that validates, verifies, judges and releases. A provider adapter can therefore become a hidden authority-escalation path if it is allowed to release output directly, write VAULT directly, mutate CORE state, retry itself silently, use unsupported modes, or violate canonical timeout behavior.

This lab provides a deterministic preflight tool for candidate `AgentAdapter` manifests plus a small replay simulator for source-grounded failure semantics.

## What PASS means
`PASS` means only that the manifest satisfies this lab's static preflight rules. It does **not** prove implementation, integration, runtime behavior, security, deployment, provider correctness, or release eligibility.

## Core source-grounded checks
- supported modes are `fast`, `strict`, `audit`;
- timeout is 10–60 seconds;
- critical adapter timeout is 30 seconds;
- adapter exposes `execute`, `cancel`, `healthcheck`;
- no automatic retry by default;
- worker output remains candidate-only and cannot release directly;
- SWARM-side adapter cannot write VAULT directly;
- provider secrets are runtime-injected and not persisted in adapter artifacts;
- critical timeout freezes;
- noncritical timeout may exclude the worker only when quorum still passes;
- invalid agent result schema freezes;
- provider/dependency failure freezes;
- unknown quorum state freezes instead of guessing.

## Run
```bash
PYTHONPATH=src python -m nexy_adapter_cert validate fixtures/valid-noncritical.json
PYTHONPATH=src python -m nexy_adapter_cert simulate fixtures/valid-noncritical.json --event timeout --quorum-possible true
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Integration posture
This package is designed as an **external preflight/certification utility**. A future NEXY integration can invoke the JSON contract or port the deterministic rules to TypeScript/Zod. Promotion into the real NEXY codebase requires an explicit user-authorized implementation task plus repository/runtime evidence.

## TypeScript bridge
`bridge/typescript/adapter-contract.ts` mirrors the core preflight rules for the DOC-C reference stack. It is dependency-free and can be typechecked independently before any authorized NEXY integration.

```bash
cd bridge/typescript
tsc -p tsconfig.json --noEmit
rm -rf .build && tsc -p tsconfig.json && node .build/adapter-contract.test.js
```
