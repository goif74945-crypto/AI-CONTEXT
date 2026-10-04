# Task Contract

## Objective

Create a large, useful supplemental project for future NEXY.AI development, stored only under `AI-CONTEXT/คลังข้อมูลเสริม`, while keeping every repository whose name contains `NEXY.AI` read-only.

The selected project is a **Cross-Runtime Contract Forge** that reduces semantic drift between TypeScript and Rust representations of shared system contracts.

## Target

Durable target:

`goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0138-NEXY-CROSS-RUNTIME-CONTRACT-FORGE/`

Read-only compatibility target:

`goif74945-crypto/NEXY.AI-`, branch `NEXY.ai`, observed exact commit `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`.

## Authorized scope

- create a new unique supplemental folder under `AI-CONTEXT/คลังข้อมูลเสริม`;
- write design, code, tests, generated artifacts, evidence, and temporary session memory into that folder;
- read NEXY.AI source/context necessary to design compatibility;
- run local sandbox tests against the standalone tool.

## Protected scope

- **No writes of any kind to repositories whose name contains `NEXY.AI`.**
- No branch, commit, PR, issue, workflow, setting, tag, release, file, or metadata mutation in NEXY.AI repositories.
- No modification of unrelated AI-CONTEXT supplemental projects.
- No promotion of AI-generated proposal text into NEXY canonical law.

## Authority sources used

1. current user directive;
2. `AI-CONTEXT/AI-BOOTSTRAP.md`;
3. `AI-CONTEXT/AI-EXECUTION-KERNEL.md`;
4. `AI-CONTEXT/INDEX.md` and `WORK-ROUTER.md`;
5. `AI-CONTEXT/rules/GLOBAL.md`, `SECURITY.md`, `VERIFICATION.md`;
6. `AI-CONTEXT/projects/NEXY.AI/overview.md`;
7. `AI-CONTEXT/projects/NEXY.AI/source-normalization/CURRENT-SYSTEM-FEATURE-BUILD-MATRIX.md`;
8. exact read-only NEXY.AI source at commit `9e615b04...`.

## Success invariants

1. NEXY.AI remains unchanged by this work.
2. The supplemental folder contains design + code + tests + evidence + resumable state.
3. Manifest validation fails closed on malformed or ambiguous semantics.
4. Semantic normalization is deterministic and input-order independent for set-like structures.
5. Semantic fingerprint changes only when contract semantics represented by the normalized semantic object change.
6. TypeScript and Rust outputs are generated from the same validated normalized source object.
7. Recompiling identical input produces byte-identical artifacts.
8. Runtime snapshot drift causes a non-zero audit result with path-level evidence.
9. Generated TypeScript passes strict compilation.
10. No Rust compilation PASS is claimed without a Rust compiler.
11. The NEXY example manifest is labeled as an observed compatibility fixture, not authority.
12. Every completion claim maps to captured evidence.

## Required evidence

- E0 presence: expected files exist;
- E1 static: Node syntax and strict TypeScript compile;
- E2 unit: test suite validates individual validation/compiler/auditor behavior;
- E3 integration: CLI compile to artifacts, deterministic double-build diff, snapshot self-audit, injected drift failure;
- repository write evidence: exact AI-CONTEXT commit and final remote tree verification after durable write.

## Stop conditions

Freeze rather than guess if:

- current NEXY authority conflicts with observed implementation semantics;
- writing NEXY.AI would be required;
- target AI-CONTEXT path collides with another existing project;
- a completion claim lacks its matching evidence class;
- a toolchain is absent and no safe local proof exists.
