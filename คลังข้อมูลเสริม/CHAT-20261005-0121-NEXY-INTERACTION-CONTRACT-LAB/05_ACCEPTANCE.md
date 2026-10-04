# Acceptance Criteria

- AC-01: valid clean contract produces `completion_gate=PASS` and retention score 100.
- AC-02: missing evidence for a mandatory directive blocks completion.
- AC-03: protected scope action produces a critical finding.
- AC-04: unlisted scope action produces unauthorized-scope finding.
- AC-05: clarification against an already-resolved directive is flagged.
- AC-06: action assumptions are surfaced.
- AC-07: explicit active conflict blocks completion.
- AC-08: PASS without evidence reference is flagged and reduces retention score.
- AC-09: duplicate directive IDs fail validation.
- AC-10: identical input produces byte-equivalent sorted JSON report in repeated analysis.
- AC-11: good CLI example exits 0 with `--fail-on-block`.
- AC-12: bad CLI example exits 2 with `--fail-on-block`.
- AC-13: implementation requires no third-party package.
- AC-14: no repository whose name contains `NEXY.AI` is mutated.
