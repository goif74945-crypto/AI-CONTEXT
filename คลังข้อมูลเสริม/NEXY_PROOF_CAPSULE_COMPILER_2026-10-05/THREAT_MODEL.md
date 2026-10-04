# Threat Model — PROPOSAL ONLY

| Threat | Required defense |
|---|---|
| Evidence flooding | authority-first filtering + deterministic cover; budget overflow freezes |
| Evidence-class laundering | exact accepted classes; E6 does not automatically satisfy E2 |
| Version smuggling | exact target/version equality |
| Freshness replay | explicit timezone-aware `as_of`, `observed_at`, `valid_until` |
| Conflict hiding | equal strongest material disagreement freezes |
| Dissent erasure | weaker FAIL/CONFLICT can be disclosed |
| Budget downgrade | never truncate required proof to fit UX budget |
| Unknown-reference injection | strict reference gate by default |
| Mutable source path | canonical SHA-256 digest is required by default and committed to identity |
| Same IDs, changed semantics | input commitment includes claim/evidence semantics, not IDs alone |
| Hash/canonicalization drift | locked cross-language vectors; formal canonicalization required before adoption |

Residual risks: authority ranks are trusted policy inputs; greedy cover is not globally minimal; digest format validation does not verify source bytes; there is no signature/access-control layer; local tests are not NEXY runtime evidence.
