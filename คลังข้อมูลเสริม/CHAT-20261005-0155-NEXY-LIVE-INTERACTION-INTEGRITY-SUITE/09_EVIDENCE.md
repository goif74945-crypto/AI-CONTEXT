# Evidence Record — Repository Seal

Status: **SEALED_REFERENCE_PASS**

Durable session code: `CHAT-20261005-0155-NEXY-LIVE-INTERACTION-INTEGRITY-SUITE`

## Scope and repository facts
- writable repository used by this work: `goif74945-crypto/AI-CONTEXT`
- target: `คลังข้อมูลเสริม/CHAT-20261005-0155-NEXY-LIVE-INTERACTION-INTEGRITY-SUITE/**`
- repositories whose names contain `NEXY.AI`: treated as protected/read-only and were not mutation targets
- repository snapshot observed during post-write seal: `9bcc55cafed8bdd60f70fb9668adb19ce4e88121`
- concurrent writers existed; one multi-file ref update correctly failed non-fast-forward and was not forced. Remaining documentation was written through additive file-level commits.

## E0 — presence
Post-write directory enumeration confirmed:
- design/task/memory documents `00` through `08`;
- `README.md`;
- `pyproject.toml`;
- `IMPLEMENTATION_MANIFEST.json`;
- `scripts/`;
- `src/`;
- `tests/`.

This record and the final audit are added after that enumeration.

## E1 — static execution
Local verifier command:

```bash
python3 scripts/verify.py
```

Observed:
- `STATIC_COMPILE: PASS`
- implementation manifest generation PASS

The static step uses Python `compileall` across the source package.

## E2 — executable verification
Latest local suite:
- **59 / 59 tests PASS**
- unit, adversarial, validation-boundary and integration-reference tests
- no test failure in the final tested byte set

Coverage diagnostic:
- Coverage.py 7.13.3
- branch-aware source package total: **97%**
- captured source totals: 454 statements, 10 missed, 138 branches, 8 partial branches

Coverage is a test-surface metric only, not deployment proof.

## E3-reference — composition
`tests/test_integration.py` crosses:
1. current directive epoch;
2. multimodal intent equivalence;
3. explicit input cohesion;
4. deterministic interaction snapshot;
5. stream completion boundary;
6. provenance-bound cache reuse;
7. superseding directive invalidation.

A dedicated regression test proves a stale/superseded epoch cannot be used to construct an `InteractionSnapshot`.

This is standalone reference integration evidence, not evidence of integration into NEXY.AI.

## Determinism evidence
`scripts/determinism_probe.py` executed in separate Python processes with:
- `PYTHONHASHSEED=1`
- `PYTHONHASHSEED=2`
- `PYTHONHASHSEED=777`

Observed serialized fingerprints were identical for all three processes.

## Byte-identity seal
`IMPLEMENTATION_MANIFEST.json` contains SHA-256, byte count and computed Git blob SHA-1 for **19** config/source/script/test files.

After repository write, all 19 files were fetched from GitHub `main` and each observed blob SHA was compared with the locally generated expected Git blob SHA.

Result: **19 / 19 MATCH, 0 mismatches**.

This proves that the committed implementation/test/config bytes checked on GitHub are exactly the bytes represented by the locally generated manifest used after the passing test run.

## Primary work commits
Interleaved concurrent commits from other sessions exist. Commits directly produced for this suite include:

- `464f3c3163056209c9527f945a429e0b0e383cb3` — core skeleton
- `8c2fc5b46b8e9d45b2902fcb8aaee3203d84a6ac` — epoch/cache gates
- `08639bc026d20b48c6aaaa2d9ca427e90736e49e` — intent/input/completion gates
- `ff1a93ae7e9bf746515b814d2a0397b30ffae4b3` — verifier/core tests
- `caf58466f1553cd16b50858e6c13fc2e101fba0f` — cohesion/completion/integration tests
- `ddd4d85df9896bd85c37989501e20f46aa977c78` — adversarial/boundary tests
- `3fc525b93a625847221344f2bf383bd23c7e3a73` — implementation manifest
- `ca594c210fbd83de024490ff4a6eddffb009b856` — README/task/memory
- `600da25237fd65582f0e099f4c0b4c047c0bab0b` — idea portfolio
- `37c59d38f6455f290dab1b7beed1fde19795a6f6` — architecture
- `d51b8329fde997d928886baa82c06aaf2994cd77` — requirement ledger
- `a1a6de6e4ba4f1e6cebdcff4d91a45301803d385` — failure/threat model
- `aa25af238ce7e59083d09d29a90d32ece340c931` — integration guide
- `f093fa4395c7abfb8f48a991edd5f6e823b88afd` — API contracts
- `01621c2cdbc6d7c31081487e080072b6cb95e5f6` — verification plan

## Failure / repair evidence
Two material issues were found and corrected before final seal:
1. proposed Recipient-Bound Approval Capsule overlapped an existing side-effect transaction lab. It was removed and replaced by Completion Boundary Integrity Gate.
2. initial coordinator API could construct a snapshot from a token without independently checking current epoch state. Coordinator was changed to validate against `InterruptEpochGate`; a stale-token regression test was added.

A concurrent repository race also caused one non-fast-forward update failure. Force was not used. The write strategy was changed to additive file-level commits.

## Verification gaps / known limits
- `ruff` unavailable: no lint PASS claimed.
- `mypy` unavailable: no static type-check PASS claimed.
- no real NEXY.AI adapter/runtime/deployment was changed or tested.
- no distributed concurrency, crash recovery, database/Redis/provider/browser workload or production load test exists.
- hashes establish byte/integrity identity within this protocol, not actor authenticity or semantic truth.
- all five systems remain **AI_PROPOSED_CONCEPT / EXPERIMENTAL / NOT ADOPTED** until authorized separately.
