# Task Contract

## Objective
Create a distinct supplemental engineering project that can later help NEXY coordinate many concurrent AI workstreams without silent duplicate work or overlapping writes.

## Target
Only `คลังข้อมูลเสริม/CHAT-20261005-0137-NEXY-WOCF/**` in `goif74945-crypto/AI-CONTEXT`.

## Authority
1. Current user directive.
2. AI-CONTEXT `AI-EXECUTION-KERNEL.md`, `rules/*`, and selected workflows.
3. `projects/NEXY.AI/overview.md` for NEXY principles only.
4. This lab's design, which remains EXPERIMENTAL and has no authority over NEXY.

## Immutable requirements
- Never mutate any repository whose name contains `NEXY.AI`.
- Never modify sibling workstreams.
- Mark future-facing NEXY ideas as AI-proposed.
- Build real reference code, execute tests, fix failures, and retain evidence.
- Fail closed on malformed manifests or protected targets.
- Keep the core decision deterministic and independent of external AI inference.

## Acceptance criteria
- Architecture, contracts, failure behavior, and requirement ledger exist.
- Reference implementation is parseable/compilable.
- Unit/adversarial tests execute and pass.
- CLI demonstrates both admissible and frozen scenarios.
- Final repo artifacts are re-read after write.
- No NEXY.AI repo mutation occurs.

## Out of scope
Production integration, changing NEXY canonical law, GitHub locking, background daemons, cross-process distributed consensus, embeddings/LLM novelty classification, or deployment claims.
