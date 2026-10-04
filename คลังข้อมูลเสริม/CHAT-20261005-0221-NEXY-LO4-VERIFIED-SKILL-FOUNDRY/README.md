# Lo4 Verified Skill Foundry (VSF)

**Status:** AI-PROPOSED / EXPERIMENTAL / NON-CANONICAL  
**Mission:** `NEXY-LO4-VSF-20261005-0221`  
**Chat reference code:** `CHAT-20261005-0221-NEXY-LO4-VERIFIED-SKILL-FOUNDRY`  
**Authority:** advisory only. This lab has zero authority to overwrite Canon, activate a capability, patch runtime, weaken gates, or self-promote.

## Objective
Explore a fail-closed Lo4 mechanism that can transform repeated verified execution history into reusable **skill candidates** without allowing observed frequency or utility to become authority.

## Five systems
1. **TPM — Trace Pattern Miner**: mines exact repeatable patterns only from distinct evidenced PASS records. Duplicate record IDs cannot inflate support.
2. **PCSC — Proof-Carrying Skill Compiler**: compiles a pattern into deterministic `SkillCandidate(status=PROPOSED)` with provenance, contracts, dependencies, evidence and mandatory forbidden behaviors.
3. **CCE — Counterexample Curriculum Engine**: converts evidenced failures into deterministic negative curriculum cases while preserving distinct counterexamples and minimizing secret-like payload material.
4. **VEE — Validity Epoch Engine**: marks a candidate `STALE` when authority or dependency identity changes, disappears, or expands beyond declarations.
5. **SPA — Shadow Promotion Arena**: compares candidate vs baseline over explicit curriculum with full identity/coverage/invariant gates. Strongest output is `PROMOTION_PROPOSAL`, never ACTIVE or PROMOTED.

## Authority boundary
`verified history -> Lo4 candidate -> counterexamples -> epoch validation -> shadow evaluation -> PROMOTION_PROPOSAL -> external authoritative promotion path`

There is deliberately no autonomous transition from this lab into NEXY Canon or runtime.

## Verification performed
- static core guard: PASS across 7 core Python files;
- Python compile: PASS;
- 31 unit/adversarial/integration tests: PASS twice;
- deterministic test-output comparison: PASS;
- stress reference: 20,000 execution records, 5,000 failure cases, 2,000 arena cases: PASS;
- local durable-file SHA-256 manifest: PASS;
- clean source bundle rebuilt after rejecting an archive that contained cache directories.

The executed tests prove only this isolated reference implementation. They do not prove NEXY integration, production readiness, deployment behavior, or Lo4 promotion safety in a real NEXY runtime.

## Durable source
The complete Design + Code + Test + Evidence tree is stored as eight exact base64 parts under `bundle/`. See `BUNDLE_INDEX.md` and `RECONSTRUCT.sh`.

No repository whose name contains `NEXY.AI` is a mutation target of this mission.
