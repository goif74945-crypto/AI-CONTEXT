# NEXY Implementation Reality Cartographer 20 (IRC-20)

**Status:** `Lo4_AI_PROPOSAL_ONLY / REFERENCE_IMPLEMENTATION / NON_CANONICAL / NON_GOVERNING`

IRC-20 is a deterministic implementation-reality analyzer for a future NEXY integration review. Its central rule is deliberately boring and therefore useful:

> **Source presence is not implementation proof. Build inclusion is not reachability. Reachability is not test proof. Test proof is not runtime/deployment proof.**

IRC-20 consumes an explicit repository manifest, constructs a build-filtered dependency closure, executes exactly twenty evidence mechanisms, emits a per-module truth matrix, and seals the result into a deterministic SHA-256 capsule. It does not modify a repository, promote a proposal, grant execution authority, or replace NEXY LAW/CORE/JUDGE.

## Why this exists

The current NEXY source and AI-CONTEXT both distinguish design, implementation, runtime and deployment evidence. The current NEXY repository also contains a direct module-boundary checker. That checker answers an important but narrower question: **is a forbidden direct import present?** IRC-20 answers a different question: **does the declared implementation actually close from source to build to production reachability to tests/evidence, and where does that chain break?**

## Architecture

```text
repository bytes / build metadata / registries / tests / evidence
                         |
                  adapter / manifest
                         |
                 strict normalization
                         |
        +----------------+----------------+
        |                                 |
  dependency graph                    Q64.64
  + build closure              checked signed-i128 raw
        |                                 |
        +------------ IRC-20 -------------+
                         |
              20 mechanism results
                         |
                module truth matrix
                         |
             non-compensatory gate
                         |
          deterministic truth capsule
```

## The five truth dimensions

Every module is represented independently as:
- `present`
- `buildIncluded`
- `productionReachable`
- `testLinked`
- `evidenceBound` + `maxEvidenceClass`

No later dimension is inferred from an earlier one.

## Twenty mechanisms

1. ENTRYCLOSURE64
2. IMPORTGRAPH64
3. BUILDSET64
4. REACH64
5. EXPLEAK64
6. DEADIMPL64
7. REGISTRY64
8. ORPHANTEST64
9. ORPHANEVID64
10. TESTLINK64
11. FREEZEPATH64
12. CONFIGUSE64
13. SCHEMAUSE64
14. AUTHPATH64
15. MIRRORPAIR64
16. MIRRORDRIFT64
17. CYCLE64
18. SIDEFX64
19. CLOSURE64
20. TRUTHCAPSULE64

## Numeric law

Quantitative coverage/closure metrics are checked Q64.64 with signed-i128 raw bounds. Decimal parsing never passes through IEEE-754. Multiplication/division use nearest, ties-to-even rounding. Overflow and divide-by-zero fail closed. Q64 metrics are informational only: a mandatory finding cannot be averaged away by a high score.

## Run

```bash
npm run verify
node dist/src/cli.js examples/healthy-manifest.json
node dist/src/cli.js examples/broken-manifest.json
```

Expected CLI codes:
- 0: analyzed manifest closes under the declared IRC contract;
- 1: valid manifest analyzed but mandatory implementation-reality findings remain;
- 2: malformed/unsupported input caused fail-closed freeze.

## Discovery helper

`discoverModules()` provides conservative repository-internal static discovery for TypeScript/JavaScript relative imports and Rust `mod` declarations. Unresolved internal references remain explicit unknown graph targets. Complex Rust `use crate::...` references are surfaced as `unsupportedReferences`; a production adapter must resolve them with Cargo/module metadata rather than guessing.

## Evidence boundary

The included evidence proves the isolated reference implementation at the tested bytes. It does **not** prove full NEXY repository integration, production runtime behavior, deployment behavior, semantic equivalence of TS/Rust mirrors, or Canon promotion. Those require fresh evidence against the exact NEXY commit being considered.
