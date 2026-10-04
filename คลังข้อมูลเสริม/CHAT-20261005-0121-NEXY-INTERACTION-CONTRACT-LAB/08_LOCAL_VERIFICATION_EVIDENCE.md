# Local Verification Evidence

Evidence class: executed local validation against the exact artifact set prepared for persistence.

## Environment boundary
- Python standard library only.
- No NEXY.AI repository mutation.
- Analysis core performs no network/model/random/clock hidden I/O.

## Executed commands

```text
PYTHONPATH=. python -m unittest discover -s tests -v
PYTHONPATH=. python -m compileall -q interaction_contract tests
PYTHONPATH=. python -m interaction_contract.cli examples/good_session.json --fail-on-block
PYTHONPATH=. python -m interaction_contract.cli examples/bad_session.json --fail-on-block
```

## Results
- Unit tests: **14 passed / 0 failed**.
- `compileall`: **PASS**.
- Good example: exit `0`, `completion_gate=PASS`, `retention_score=100`.
- Good input fingerprint: `108559f939e4ac29cad2b9608f13f3401eb95391ea070f59439e79de20ea2acd`.
- Bad example: exit `2`, `completion_gate=BLOCK`, `retention_score=0`.
- Bad input fingerprint: `e1006ef5726f2a5ef9da9f9ae17d02dbb3ca2e2af846a3222c58a153c36fe45b`.
- Bad example finding codes observed:
  - `ACTION_WITH_ASSUMPTION`
  - `DIRECTIVE_UNEVIDENCED`
  - `PREMATURE_COMPLETION_CLAIM`
  - `PROTECTED_SCOPE_TOUCHED`
  - `REDUNDANT_CLARIFICATION`

## Evidence boundary
This proves the reference implementation behaved as stated in the local execution environment. It does **not** prove integration with NEXY.AI, production behavior, UX quality, or semantic intent extraction accuracy.
