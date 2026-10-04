# NEXY Verification Frontier Lab

**Work ID:** `CHAT-20261005-0155-NEXY-VERIFICATION-FRONTIER-LAB`  
**Status:** AI-PROPOSED / AUXILIARY / NON-CANONICAL  
**Storage target:** `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม`  
**Protected implementation repositories:** any repository whose name contains `NEXY.AI` is out of mutation scope for this work.

## Objective

Build five standalone, executable engineering prototypes that can strengthen future NEXY.AI verification and reliability without changing NEXY.AI itself.

The suite targets five different gaps:

1. **Failure Witness Distiller (FWD)** — shrink a failing structured input into a smaller reproducible witness while preserving the exact failure signature.
2. **Verification Portfolio Optimizer (VPO)** — select the exact minimum-cost set of checks that satisfies explicit evidence-class obligations.
3. **Boundary Payload Pathology Lab (BPPL)** — reject structurally dangerous or ambiguous JSON before it reaches an authority-bearing core.
4. **Contract Mutation Adequacy Engine (CMAE)** — mutate structured contracts and measure whether verification oracles actually detect semantic damage.
5. **Negative-Space Coverage Analyzer (NSCA)** — detect prohibitions/FREEZE rules that have no real negative-path test evidence.

## Why these five

NEXY's project context emphasizes one verified output or freeze, explicit authority, evidence matching, deterministic behavior, and no guessing. Existing supplemental work already covers proof sensitivity, model conformance, semantic patch governance, context fidelity, shadow execution, blast radius, capability leasing, collision guards, and migration safety. This lab therefore avoids creating yet another renamed copy of those systems.

The five systems are intentionally orthogonal:

| System | Primary question |
|---|---|
| FWD | What is the smallest reproducible input that still demonstrates this exact failure? |
| VPO | Which checks are sufficient to prove these claims at the allowed evidence classes with minimum cost? |
| BPPL | Can this boundary payload be parsed and canonicalized without ambiguity/pathology? |
| CMAE | Would our verifier notice if the contract were semantically damaged? |
| NSCA | Do our "must not / deny / freeze" requirements have real negative-path proof? |

## Authority and truth labels

- `SOURCE_FACT` — derived from authoritative AI-CONTEXT project context.
- `REPO_FACT` — observed in current AI-CONTEXT repository state.
- `RUNTIME_FACT` — produced by executed local tests for this exact artifact set.
- `PROPOSAL` — architecture or integration idea in this folder.
- `UNKNOWN` / `NOT_VERIFIED` — preserved when evidence is unavailable.

Nothing here is current NEXY.AI law. Promotion requires explicit project authority.

## Runtime profile

- Language: Python 3, standard library only.
- Network: not required.
- Filesystem: not required by core engines.
- Hidden model behavior: not required.
- External dependencies: none.
- Intended use: CI/preflight/offline verification tooling, not direct authority-bearing runtime mutation.

## Validation

Reproduce from the lab root:

```bash
python -m compileall -q .
python -m unittest discover -s . -p 'test_*.py' -v
```

Additional determinism replay uses multiple `PYTHONHASHSEED` values. Exact observed evidence is stored under `evidence/` and summarized in `VALIDATION_REPORT.md`.

## Integration boundary

These prototypes should integrate by explicit data contracts only. They do not require NEXY.AI source mutation and they never elevate themselves to authority. See `02_INTEGRATION_CONTRACT.md`.

## Known limitations

- FWD is a deterministic greedy reducer, not a proof of a globally minimal witness.
- VPO is exact but caps claim count to bound exponential state space.
- BPPL is strict JSON tooling, not a complete parser for every external protocol.
- CMAE's mutation operators are deterministic and useful but not exhaustive.
- NSCA requires structured requirement/evidence metadata; it does not infer canonical obligations from arbitrary prose.

Those limits are deliberate fail-closed boundaries, not hidden placeholders.
