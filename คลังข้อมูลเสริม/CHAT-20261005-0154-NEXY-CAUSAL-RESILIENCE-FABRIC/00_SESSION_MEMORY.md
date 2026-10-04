# SESSION MEMORY — NEXY Causal Resilience Fabric

## Identity
- Durable execution reference: `CHAT-20261005-0154-NCRF`
- Created: 2026-10-05 01:54 +07:00
- Status: IN_PROGRESS
- Classification: AI-PROPOSED CONCEPTS + STANDALONE REFERENCE IMPLEMENTATION
- Persistence mode: DURABLE_RESUMABLE in `goif74945-crypto/AI-CONTEXT`

## Objective
Design, implement, test, and evidence five novel supplemental systems that can integrate beside NEXY.AI without modifying the NEXY.AI repository.

## Authority / protected scope
1. Current user directive.
2. AI-CONTEXT INDEX.md + AI-EXECUTION-KERNEL.md + rules.
3. AI-CONTEXT NEXY.AI project context.
4. Read-only current repository observations from `goif74945-crypto/NEXY.AI-`.
5. Local executed test evidence for the standalone implementation.

### MUTABLE
Only unique files under:
`คลังข้อมูลเสริม/CHAT-20261005-0154-NEXY-CAUSAL-RESILIENCE-FABRIC/`

### PROTECTED
`goif74945-crypto/NEXY.AI-` is READ-ONLY. No code, branch, issue, workflow, setting, commit, PR, or other mutation is authorized there.

## Current NEXY read-only target observation
- Repository: `goif74945-crypto/NEXY.AI-`
- Branch: `NEXY.ai`
- Observed HEAD: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
- Stack observed: TypeScript/Node, Vitest, Zod, Prisma, BullMQ/Redis; Rust core also exists.
- Integration surfaces observed:
  - `packages/contracts/evidence.ts` blob `6b50f4cf9c0ca7e4c056fc546976e6e5a52d5895`
  - `packages/contracts/envelope.ts` blob `daf1156b3431150e667b5e18727d8abe9bdc9b75`
  - `packages/swarm/pipeline.ts` blob `b6bfadfb473b675928fa8df476b2180ac749e335`
  - `packages/core/vnext-state-matrix.ts` blob `27e1281fba330784cc3bf2c30e9e1e82f951479b`
  - `packages/law/freeze.ts` blob `e2e62e29553b9c62b6de5aef5082c68fe54d478d`

## Novelty scan already observed in AI-CONTEXT
Existing sibling work includes Proposal Forge, Intent Integrity Lab, Human Agency Lab, Directive Epoch Firewall, Trust/UX Contract Lab, Chrono Integrity Lab, Shadow Assurance Lab, Context Release Firewall, Privacy Egress Firewall, Operator Contract Compiler, Interaction Economics Lab, Deterministic Interchange Kernel, Semantic Localization Integrity, Accessibility Integrity, PEPSA, PCF, NCVG, NOCC/NPCEF and proof-capsule hardening.

## Five candidate concepts (locked for implementation unless direct collision is discovered)
1. Evidence Dependency Revocation Engine (EDRE)
2. Swarm Independence Quorum Gate (SIQG)
3. Action Blast-Radius Compiler (ABRC)
4. Safe Partial Execution Frontier (SPEF)
5. Recovery Route Proof Engine (RRPE)

## Invariants
- No NEXY.AI mutation.
- No claim that these concepts are part of current NEXY authority.
- Every concept must be explicitly labeled AI-PROPOSED.
- Deterministic canonical output; no wall clock/RNG in authoritative functions.
- Fail closed on missing authority inputs.
- Tests must be actually executed locally; simulated output is forbidden.
- Final evidence must include exact commands, outputs, file hashes, limitations, and read-back proof after publication.

## Next actions
1. Finish novelty and interface analysis.
2. Write TypeScript reference implementation with zero runtime dependencies.
3. Compile with strict TypeScript.
4. Execute focused + integration + adversarial tests.
5. Execute deterministic benchmark/fuzz matrix.
6. Fix failures and rerun.
7. Publish Design + Code + Test + Evidence under this folder.
8. Read back critical files and audit manifest.
