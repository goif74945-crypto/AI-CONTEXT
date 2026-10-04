# Temporary Execution Memory — NEXY Self-Calibration & Recovery Lab

Status: IN_PROGRESS until GitHub read-back and final audit are complete.
Classification: EXPERIMENTAL / AI_PROPOSAL / NOT_NEXY_CANON.
Conversation identifier: `PROJECT-CONVERSATION-2026-10-05T01:54+07:00`.
Identifier note: the ChatGPT UI internal chat ID is not exposed to available tools; this deterministic identifier is used for durable resumption.
Repository target: `goif74945-crypto/AI-CONTEXT` / `main`.
Write root: `คลังข้อมูลเสริม/CHAT-20261005-0154-NEXY-SELF-CALIBRATION-RECOVERY-LAB/`.
Protected scope: every repository whose name contains `NEXY.AI`; no mutation is authorized there.

## Objective
Build five non-canonical, executable auxiliary concepts that help a future NEXY integration discover latent behavior, pause safely, detect correlated evidence, minimize failures, and measure confidence calibration.

## Current work graph
- Context/authority inspection: PASS
- Collision/novelty review against sibling labs: PASS with limitations documented in `02_NOVELTY_MATRIX.md`
- Five designs: PASS locally
- Five reference implementations: PASS locally
- Static compilation: PASS locally
- Unit/adversarial/integration tests: PASS locally; final rerun pending after documentation
- Demo: PASS locally
- Performance smoke: PASS locally; observational only
- GitHub persistence/read-back: PENDING
- Final audit: PENDING

## Defects found and repaired
1. Contract Archaeologist originally validated mapping type after consuming the iterable. Fixed by materializing once and validating before normalization.
2. Failure Atomizer originally located a chunk by value, which could target the wrong position when duplicate values existed. Fixed by reducing over explicit index ranges.
3. Contract Archaeologist originally risked Python equality collisions such as `True == 1`. Fixed with explicit scalar type tags.
4. Contract Archaeologist accepted non-finite floats. Fixed by rejecting NaN/Infinity.
5. PauseSafe originally accepted duplicate step IDs. Fixed with explicit uniqueness validation.
6. Failure Atomizer's ddmin phase did not itself guarantee arbitrary-predicate 1-minimality. Added a deterministic single-removal post-proof loop.
7. Benchmark direct-file execution failed import resolution. No production path hack was added; canonical invocation is module mode: `python -m integration.benchmark_smoke`.
8. Adversarial test name incorrectly said 64 trigger pairs while the exhaustive 8-choose-2 matrix is 28. Renamed to describe the exact 28 cases.

## Resume rule
Read this file, `01_TASK_CONTRACT.json`, `02_NOVELTY_MATRIX.md`, and `03_PORTFOLIO_ARCHITECTURE.md`. Re-run the exact verification commands in `README.md`, verify GitHub source identity, then continue from the first non-PASS item. Never promote these proposals to NEXY canon without explicit authority.
