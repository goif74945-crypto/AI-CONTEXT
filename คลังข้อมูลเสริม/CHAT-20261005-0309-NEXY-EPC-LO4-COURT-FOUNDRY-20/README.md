# NEXY EPC — CourtScript-Q64 Policy Compiler Lab

CHAT_ID: `CHAT-20261005-0309-NEXY-EPC-LO4-COURT-FOUNDRY-20`
Status: **Lo4 AI-PROPOSED / NON-CANON / NON-GOVERNING / STANDALONE VERIFIED REFERENCE**
Primary candidate: **EPC CourtScript-Q64**
Deferred baseline: **EPC Court Foundry 20 core reference**

## Purpose
CourtScript-Q64 is a deterministic, typed, bounded policy profile/compiler for the proposed NEXY Evolutionary Proposal Court (EPC). It converts explicit advisory court criteria into canonical bytecode and evaluates them in a side-effect-free VM. It cannot consume a real EPC vote, promote Canon, mutate CORE/JUDGE/LAW, touch the protected NEXY repository, deploy, or execute external effects.

The design exists to solve a problem not covered by merely adding another proposal evaluator: **how do we make EPC's own evaluation policy explicit, statically checkable, replayable, revision-diffable, and unable to acquire hidden authority?**

## Authority boundary
- NEXY source law remains external authority.
- DOC-B governs system law; DOC-C build authority; DOC-E deployment proof.
- NEXY exact read-only implementation head used for compatibility: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43` on branch `NEXY.ai`.
- CourtScript authority is fixed to `ADVISORY_ONLY`.
- Outputs are only `REVIEW_ELIGIBLE` or `DEFER`; review targets are `KEEP_REVIEW` / `CUT_REVIEW`, never real KEEP/CUT consumption.
- CUT review requires WIP immunity and substantive-basis proof declaration.
- UNKNOWN inputs propagate to DEFER rather than being guessed.

## Verification summary
- CourtScript strict TypeScript build: PASS.
- CourtScript executed tests: **39/39 PASS**.
- Q64 deterministic integer property loop: **50,000 cases PASS**.
- Byte-identical trace replay: **5,000 repeated evaluations PASS**.
- AST digest and bytecode digest repeatability: 500 repetitions each PASS.
- Clean extracted source archive re-verification: **39/39 PASS**.
- Static forbidden-capability scan: no network/fs/process/env/random/clock/eval usage in source/tests.
- CourtScript source archive SHA-256: `9f6c9b6f29ec23b52bc65f7db63dc46fc3cd8dbf1726a4bfd2e5c3af4f5aa4c8`.
- CourtScript source-manifest aggregate SHA-256: `42ccccd2b17bb1fdf5468c621065fca33217fb4b42920c6a46a1bef08ea0b29b`.

The deferred Court Foundry reference independently passed 57/57 tests but is not the novelty candidate because current AI-CONTEXT contains overlapping EPC infrastructure work.
