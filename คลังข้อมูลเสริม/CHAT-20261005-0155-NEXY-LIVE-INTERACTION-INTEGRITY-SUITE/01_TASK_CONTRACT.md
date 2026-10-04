# Task Contract

## Objective
Design and implement five new, useful, testable NEXY-compatible reference systems, store them only in AI-CONTEXT supplemental storage, and produce evidence without touching NEXY.AI implementation repositories.

## Target
`goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0155-NEXY-LIVE-INTERACTION-INTEGRITY-SUITE/**`

## Authorized scope
- new documents, code, tests, fixtures/scripts and evidence under the target directory;
- read-only inspection of AI-CONTEXT and NEXY context stored inside AI-CONTEXT;
- local isolated execution of new reference code.

## Protected scope
- all repositories with `NEXY.AI` in the repository name;
- all pre-existing sibling supplemental directories;
- repository history outside ordinary additive commits;
- credentials/secrets.

## Authority sources
1. current explicit user request;
2. AI-CONTEXT execution/rules/workflows;
3. AI-CONTEXT NEXY project context;
4. observed repository state;
5. local runtime evidence for this reference implementation.

## Success invariants
- exactly five distinct concepts are documented;
- concepts are explicitly labeled AI-proposed, not adopted canon;
- each concept has executable reference behavior;
- critical fail-closed paths have unit/adversarial tests;
- integration behavior across the concepts is tested;
- deterministic fingerprints do not vary with Python hash seed in the probe;
- no NEXY.AI repository mutation occurs;
- committed bytes can be matched to locally tested bytes;
- known verification gaps remain explicit.

## Forbidden behavior
- edit/push/merge/branch/configure NEXY.AI repositories;
- call design prose production implementation;
- claim runtime/deployment integration;
- guess missing intent;
- silently consume unreferenced inputs;
- reuse cached values across provenance boundaries;
- allow stale interrupted actions to commit;
- treat network EOF or a partial stream as verified completion;
- persist secrets.

## Required evidence
- E0: repository files exist at target path;
- E1: Python compile evidence;
- E2: executed unit/adversarial tests;
- E3-reference: one integration test crossing multiple suite modules;
- deterministic probe across multiple `PYTHONHASHSEED` values;
- post-write Git blob identity check.

## Stop conditions
Stop with BLOCKED/PARTIAL rather than invent proof if repository writes fail, committed bytes differ from tested bytes, required target becomes ambiguous, or completing work would require a NEXY.AI mutation.
