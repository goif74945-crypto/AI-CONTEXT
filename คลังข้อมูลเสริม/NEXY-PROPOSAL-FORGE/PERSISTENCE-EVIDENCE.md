# Persistence Evidence — NEXY Proposal Forge v0.1.0

## Scope

This record proves persistence of the tested supplemental artifacts in `goif74945-crypto/AI-CONTEXT` only. It does not prove or claim any NEXY.AI implementation, deployment, or runtime state.

## Merge evidence

- Pull request: `#27` — NEXY Proposal Forge supplemental tool
- Proposal Forge branch head before merge: `552eff8a576f932dad65f3eb5b2508983c332782`
- GitHub merge result: `merged = true`
- Merge commit: `f078c15ec2e59fee501be497b5fc53022186543b`
- Merge mode: server-side GitHub merge
- Force push: not used

## Post-merge byte verification

GitHub `main` directory listings were read after the merge and compared against `FILE-MANIFEST.sha256`.

Result: `29/29 PASS` for immutable artifacts.

Verified groups:

- root documentation/schema/package files;
- `src/nexy_proposal_forge/` — 9/9 expected source files;
- `tests/` — 4/4 test files;
- `examples/` — 4/4 fixtures;
- `scripts/benchmark_catalog.py` — exact expected blob SHA.

Every observed Git blob SHA matched the locally computed Git blob SHA recorded before persistence.

## Local execution evidence

After the repository-persistence workflow, the local tested workspace was re-run with:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Result: `29/29 PASS`.

Earlier verification also established:

- `python3 -m compileall -q src tests scripts` -> PASS;
- strict JSON parsing -> PASS;
- self-proposal evaluation -> `PROMOTE_FOR_HUMAN_REVIEW` / advisory-only / non-authoritative;
- work-manifest collision fixture -> `CLEAR`;
- synthetic 837-entry catalog repeat -> deterministic;
- local synthetic scale observation -> ~70 ms in that container only, not an SLA.

## Protected-repository boundary

`goif74945-crypto/NEXY.AI-` was used only for read-only context. No branch, file, commit, merge, PR, issue, workflow, setting, or other mutation action was issued against that repository.
