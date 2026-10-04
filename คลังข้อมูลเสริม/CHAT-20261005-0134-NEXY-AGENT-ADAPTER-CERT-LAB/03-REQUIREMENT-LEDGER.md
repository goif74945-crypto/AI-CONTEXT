# Requirement Ledger

| ID | Requirement | Authority class | Implementation | Evidence target |
|---|---|---|---|---|
| R1 | Only AI-CONTEXT may be mutated | USER_DIRECTIVE | repository path isolation | GitHub final diff/state |
| R2 | NEXY.AI repository must not be mutated | USER_DIRECTIVE | no NEXY.AI write calls | execution record |
| R3 | Adapter modes = fast/strict/audit | SOURCE_FACT | validator | E2 unit |
| R4 | Agent timeout 10–60s | SOURCE_FACT | validator | E2 unit |
| R5 | Critical timeout = 30s | SOURCE_FACT | validator | E2 unit |
| R6 | execute/cancel/healthcheck declared | SOURCE_FACT | validator | E2 unit |
| R7 | No automatic retry by default | SOURCE_FACT | authority contract | E2 unit |
| R8 | Worker cannot directly release | SOURCE_FACT/derived invariant | authority contract + simulator | E2 unit |
| R9 | SWARM/adapter cannot write VAULT directly | SOURCE_FACT | authority contract | E2 unit |
| R10 | Critical timeout freezes | SOURCE_FACT | simulator | E2 unit |
| R11 | Noncritical timeout excludes only if quorum survives | SOURCE_FACT | simulator | E2 unit |
| R12 | Unknown quorum freezes rather than guesses | SOURCE_FACT | simulator | E2 unit |
| R13 | Invalid agent schema freezes | SOURCE_FACT | simulator | E2 unit |
| R14 | Provider/dependency failure freezes | SOURCE_FACT | simulator | E2 unit |
| R15 | Deterministic reports | PROPOSED_GUARD | canonical SHA-256 | E2 unit |
| R16 | No embedded/persisted provider secrets | SOURCE_FACT/security | manifest contract | E2 unit |
| R17 | PASS must not imply runtime/deploy integration | AI-CONTEXT verification law | report scope statement | static review + tests |
