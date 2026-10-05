# GHOSTEDGE Controlled Campaign Sufficiency — Evidence

**Status: PASS for the exact standalone experimental artifact bytes below**

## Target

- Repository: `goif74945-crypto/AI-CONTEXT`
- Persisted code commit: `8c7e5c6ef4058e07981bf770c302ee3a402ed0da`
- Verification time: `2026-10-05T20:36:45+07:00`
- Runtime: Python `3.12.14`, Linux isolated detached worktree
- Classification: `AI_PROPOSED_EXPERIMENTAL_NOT_CANON`

## Verified gap

Fresh execution against the original experimental GHOSTEDGE proved:

- zero experiments returned `CLEAN`; and
- two intervention failures out of two produced `CANDIDATES_FOUND` without
  any sham/control evidence.

The controlled extension instead freezes insufficient campaigns and requires
an exact observation matrix, intervention/sham evidence floors, and a declared
integer failure-rate lift over sham baseline.

## Fresh commands

```text
python3 -m compileall -q frontier_assurance_lab.py obsure_runtime_assurance.py recert_path_integrity.py ghostedge_campaign_assurance.py test_frontier_assurance_lab.py test_obsure_runtime_assurance.py test_recert_path_integrity.py test_ghostedge_campaign_assurance.py
python3 -m unittest -v test_frontier_assurance_lab.py test_obsure_runtime_assurance.py test_recert_path_integrity.py test_ghostedge_campaign_assurance.py
```

## Results

- E1 compile: `PASS`
- E2 unit/negative/adversarial: `PASS`
- E3 integration: `PASS`
- Total: `76/76 PASS`, `0 failures`, `0 errors`
- New GHOSTEDGE campaign tests: `18/18 PASS`
- Prior regression suites: `58/58 PASS`
- Determinism: `100` experiment-order permutations produced identical output
- Post-persistence execution source: detached worktree at exact code commit

Coverage includes controlled excess-failure candidate detection, complete clean
campaign, declared dependency suppression, empty campaign, insufficient shams,
intervention and sham coverage omissions, unknown source, duplicate experiment
ID, malformed declared parent collection, duplicate observation, non-string ID,
string-as-observation abuse, permutation determinism, sham-confounded signal,
controlled integration, original-vs-controlled disagreement, and empty-campaign
integration freeze.

## Failure / repair record

1. The confirmed pre-existing evidence gaps were zero-evidence `CLEAN` and
   candidate emission without sham baseline.
2. The initial new suite passed `74/74`. Pre-seal self-audit then found two
   boundary-validation weaknesses: a non-string experiment ID could raise
   `AttributeError` rather than `FreezeError`, and a string observation could
   be treated as an iterable of characters. Both inputs are now explicitly
   rejected and two regression tests were added.
3. Fresh full rerun after repair passed `76/76`.

No assertion, threshold, or gate was weakened to obtain PASS.

## Exact byte binding

| Artifact | SHA-256 | Git blob | Persisted read-back |
|---|---|---|---|
| `GHOSTEDGE_CAMPAIGN_DESIGN.md` | `bea7944b27dcba253c617ab3064610152e0037a09ad3e24f9411b8cad420145c` | `3819b9625b2ecac80d71c5cf37208f1cfa01b292` | exact |
| `ghostedge_campaign_assurance.py` | `1d7f2e04423087ea74eaa8ef228d74942d4f7936253a144a7bc1123211622378` | `60e4a7ce1fb11ae96bc56dae24c728b08d10d22c` | exact |
| `test_ghostedge_campaign_assurance.py` | `0fee4bdee9fe570b39b9a4635b2ce7c46c531040d4865c6dd29c20b97be1f3ee` | `815a8705f5935d19553a53926d805cbde09f5af7` | exact |

GitHub base64 read-back at the exact code commit matched all locally tested
bytes. The successful post-persistence run reported detached HEAD
`8c7e5c6ef4058e07981bf770c302ee3a402ed0da`.

## Concurrency evidence

After code persistence, repository head advanced to
`5c64680a29bad8ca050b432fb8752b9ddabbe7fa`. GitHub comparison proved it was
one commit ahead with `8c7e5c6...` as merge base; that commit changed only
`คลังข้อมูลเสริม/CHAT-20261005-0114-NEXY-CAPACITY-ECONOMICS/**`.
Mission-state blob remained `3269ea9547a7feb8ce107a66cccc378035072810`
before this checkpoint update.

## Evidence boundary

This proves only the stated behavior of these exact standalone bytes over
bounded supplied experiment records. It does not prove experiment assignment,
environment equivalence, observation authenticity, statistical causality,
NEXY.AI integration, canonical adoption, deployment, or production safety.
