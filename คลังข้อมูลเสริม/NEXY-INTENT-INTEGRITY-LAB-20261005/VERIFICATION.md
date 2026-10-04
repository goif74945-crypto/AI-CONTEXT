# Verification Record

**Status:** PRE-MERGE VERIFIED / FINAL MAIN FETCH PENDING  
**Artifact:** NEXY Intent Integrity & Change Guard Lab  
**Classification:** AI-PROPOSED CONCEPT / RESEARCH PROTOTYPE / ADVISORY ONLY  
**Session code:** `NEXY-INTENT-INTEGRITY-LAB-20261005-0121-TH`  
**Platform chat ID:** UNKNOWN — not exposed by available conversation/tool interfaces.

This record separates local execution evidence, repository byte-identity evidence, concurrency observations, and limitations. It does not claim that current NEXY.AI implements this research concept.

## 1. Unit, invariant, CLI, and state-binding tests

Final local command:

```bash
PYTHONPATH=src python -m unittest discover -s tests -q
```

Observed final result after the TOCTOU execution-seal expansion and README/manifest refresh:

```text
Ran 40 tests in 0.146s
OK
```

Status: **PASS**

Coverage includes:

- passing proposal;
- protected repository identity;
- unauthorized repository identity;
- protected/out-of-scope/unlisted paths;
- mandatory requirement omission;
- unknown requirement references;
- missing/weak evidence;
- assumption-to-fact escalation;
- NOT_VERIFIED completion rejection;
- path traversal rejection;
- canonical digest invariance;
- 50 deterministic ordering seeds;
- unauthorized contract drift;
- immutable requirement drift;
- exact approval and non-blanket approval;
- stale approval review;
- 200 semantic contract mutations that must all FREEZE;
- 150 invalid execution-proposal mutations that must all FREEZE;
- execution seal exact-state PASS;
- repository/ref/revision mismatch FREEZE;
- contract/proposal digest mismatch FREEZE;
- tampered seal FREEZE;
- non-passing proposal cannot be sealed;
- CLI digest/check/create-seal/verify-seal behavior.

## 2. Compilation

Command:

```bash
PYTHONPATH=src python -m compileall -q src tests tools
```

Observed result: exit code `0`, no compile error output.

Status: **PASS**

## 3. JSON Schema validation

Validator observed locally: `jsonschema 4.26.0`.

Executed:

- Draft 2020-12 schema self-check for three schemas;
- base intent-contract fixture validation;
- all execution-proposal fixtures validation.

Observed result: **PASS**

Schemas:

1. `intent-contract.schema.json`
2. `execution-proposal.schema.json`
3. `execution-seal.schema.json`

## 4. Artifact self-integrity manifest

Command:

```bash
PYTHONPATH=src python tools/verify_manifest.py
```

Observed result:

```text
MANIFEST_VERIFY=PASS byte_exact=27 json_semantic=0
```

The manifest binds the exact Git blob SHA-1 of 27 source, test, fixture, schema, documentation, package, benchmark, and verifier files that passed local verification.

The manifest is evidence metadata only. It is not authentication, authorization, or a digital signature.

## 5. Repository byte-identity fetch verification

The 27 manifest-listed files were fetched from branch:

`chat/nexy-intent-integrity-20261005-0121`

against repository:

`goif74945-crypto/AI-CONTEXT`

Fetch verification was split into three connector batches due a per-call tool limit.

Observed result:

- Batch 1: 9/9 Git blob SHAs matched.
- Batch 2: 9/9 Git blob SHAs matched.
- Batch 3: 9/9 Git blob SHAs matched.
- Total: **27/27 matched**.

After README documentation was expanded, it was re-tested locally, the manifest was regenerated, and both GitHub update responses plus fetch-back reported:

- README SHA: `78d6fe3728f11821bfe7fe634acf1a73beab7798`
- Manifest SHA: `374dd4d3adcf8c0210e72ecefa8566bf1e2c923b`

Status: **PASS**

## 6. CLI smoke path

A positive proposal check returned `PASS`.

A protected-path proposal returned:

```text
decision=FREEZE
finding=PROTECTED_SCOPE_TOUCH
exit code=2
```

The execution-seal flow returned `PASS` when repository/ref/revision matched and `FREEZE` when revision changed.

Status: **PASS**

## 7. Editable package smoke test

Initial command:

```bash
python -m pip install -e .
```

Observed result: **FAIL before package build** because pip build isolation attempted network access for `setuptools>=68`, while the sandbox could not resolve/download from the package index.

Recovery command:

```bash
python -m pip install -e . --no-build-isolation
```

Observed result: **PASS** using the already installed local build tooling.

After installation, console-entry-point commands `digest`, `create-seal`, and `verify-seal` executed successfully.

Interpretation: the isolated-install failure is an environment/network dependency failure, not hidden as a package success.

## 8. Synthetic scalability observation

Final local run remained `PASS` for synthetic contracts with 100, 500, and 1000 requirements/criteria.

Latest observed approximate times:

| Requirements + criteria | Decision | Digest | Evaluate |
|---:|---|---:|---:|
| 100 | PASS | 0.00114 s | 0.00307 s |
| 500 | PASS | 0.00420 s | 0.01262 s |
| 1000 | PASS | 0.00978 s | 0.02808 s |

These are local observations only, not an SLA, throughput guarantee, or evidence about NEXY.AI runtime.

## 9. Concurrency evidence and recovery

Multiple GitHub Contents API writes to `main` returned HTTP `409` because other concurrent work advanced the branch between observation and mutation.

Response taken:

1. no force update;
2. no overwrite of unrelated files;
3. switch to a dedicated branch;
4. continue additive changes there;
5. verify branch diff before merge;
6. convert the observed TOCTOU failure class into the Execution Seal research module.

Immediately before this verification record was written, comparison against current `main` reported:

- branch status: `diverged`;
- branch ahead: 18 commits;
- branch behind: 436 commits;
- changed files in comparison: 16;
- changed files outside `คลังข้อมูลเสริม/NEXY-INTENT-INTEGRITY-LAB-20261005/`: **0**.

Status: **PASS for scope containment**.

## 10. Protected-repository boundary

All mutation tool calls in this work targeted:

`goif74945-crypto/AI-CONTEXT`

No mutation tool call was issued against a repository whose name contains `NEXY.AI`.

Read-only NEXY.AI project context inside AI-CONTEXT was used only to align the concept with the project's documented principles.

Status: **PASS based on the executed mutation log in this session**.

## 11. Duplicate-concept check

Immediately before initial repository write, searches inside `goif74945-crypto/AI-CONTEXT` returned no result for:

- `Intent Integrity Change Guard`
- `PROTECTED_REPOSITORY_TARGET`
- `semantic drift exact approval`
- `NEXY-INTENT-INTEGRITY-LAB-20261005`

This is evidence of a limited vocabulary-based duplicate check, not proof that no remotely related idea exists under different terminology.

## 12. Known limitations

- Natural-language semantic equivalence is not proven.
- Evidence classes use a simplified total ordering.
- Repository identity is a string, not authenticated cryptographic identity.
- Execution seals are deterministic digests, not digital signatures.
- No replay nonce or authenticated human approval exists.
- Path-glob checks are not an OS sandbox.
- A proposal can lie about implementation coverage unless external evidence is bound to claims.
- This prototype is not integrated into NEXY.AI runtime and makes no such implementation claim.
- Final `main` merge + post-merge fetch evidence is pending at this record revision.

## Final gate for completion

Do not mark repository delivery COMPLETE until:

1. PR/merge into current `main` succeeds without scope violation;
2. critical files are fetched from `main` after merge;
3. final checkpoint records the resulting main commit/revision and any remaining limitation.
