# Failure Model

| Failure | Risk | Current response |
|---|---|---|
| Stable freeze becomes candidate release | unsafe action / law bypass | FAIL |
| Authority removed or reordered | user/system law laundering | FAIL |
| Candidate proof tied to old revision | stale PASS | FAIL |
| Candidate silently drops proof class | evidence downgrade | FAIL |
| Candidate repeats different results for same case | nondeterminism / hidden state | FAIL |
| Candidate missing baseline case | blind coverage | FAIL |
| Policy changed without rebaseline | invalid comparison | FAIL |
| Candidate adds new unbaselined case | unknown semantics | NOT_VERIFIED |
| Candidate freezes where stable released | availability/usability regression | NOT_VERIFIED |
| Identical duplicate candidate record | collection/replay defect | NOT_VERIFIED |
| Raw input accidentally included by adapter | privacy leak | OUTSIDE current parser guarantee; adapter must prevent |
| Malicious reference string | log/report metadata injection | JSON encoding prevents structural injection; UI rendering still must escape |

## Fail-safe rule
The lab never transforms a finding into execution permission. Unknown or incomparable proof contexts do not PASS.
