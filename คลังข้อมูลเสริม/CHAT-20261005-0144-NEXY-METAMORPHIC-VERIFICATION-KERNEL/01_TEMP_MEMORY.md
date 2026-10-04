# Temporary Execution Memory

This file exists to make the work resumable without relying on hidden model state.

## Current state
- Work ID: `CHAT-20261005-0144-NEXY-METAMORPHIC-VERIFICATION-KERNEL`
- Target repository: `goif74945-crypto/AI-CONTEXT`
- Target folder: `คลังข้อมูลเสริม/CHAT-20261005-0144-NEXY-METAMORPHIC-VERIFICATION-KERNEL`
- Protected repository class: any repo name containing `NEXY.AI`
- Chosen concept: Metamorphic Verification Kernel (MVK)
- Proposal origin: AI-proposed, not canonical NEXY requirement

## Collision check summary
Existing supplemental work already covers evidence capsules, counterfactual systems, tool-contract drift, side-effect transactions, human authority, privacy firewalls, resource governors, semantic contracts, concurrency, causal merge, accessibility, and related areas. MVK targets a different gap: relation-based verification where exact expected outputs are unavailable or unstable.

## Failure log
1. Initial test run: 14 failures, 11 passes.
2. Root cause: `dataclasses.asdict()` deep-copied `MappingProxyType` and raised `TypeError: cannot pickle 'mappingproxy' object`.
3. Repair: canonicalizer now enumerates dataclass fields directly and recursively canonicalizes values without deepcopy.
4. Reverification: 25/25 tests PASS; compileall PASS; fixture CLI PASS.

## Remaining at checkpoint
- Run packaging/install and multi-relation integration harness.
- Capture final evidence.
- Persist full project atomically to AI-CONTEXT.
- Re-read written tree and key files.

## Final local verification checkpoint
- Final pytest: 38/38 PASS.
- Coverage: 97%.
- compileall: PASS.
- console fixture validation: PASS.
- local multi-relation harness: 4/4 PASS.
- negative control: correctly detected FAIL.
- NEXY E3+ integration: NOT_VERIFIED / OUT OF SCOPE.
