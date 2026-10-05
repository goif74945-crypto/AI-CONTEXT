# RECERT Collision-Safe Path Integrity — Evidence

**Status: PASS for the exact standalone experimental artifact bytes below**

## Target

- Repository: `goif74945-crypto/AI-CONTEXT`
- Persisted code commit: `fcb7ed7f15a5afe6a31d9a3bbdb8e61bd291e89c`
- Verification time: `2026-10-05T19:38:10+07:00`
- Runtime: Python `3.12.14`, Linux isolated detached worktree
- Classification: `AI_PROPOSED_EXPERIMENTAL_NOT_CANON`

## Verified gap

Fresh reproduction against the original experimental RECERT returned
`CERTIFIED` for:

```text
before = {"a": {"b": 1}, "a.b": 9}
after  = {"a": {"b": 2}, "a.b": 9}
```

The literal dotted key overwrote the nested path during flattening. The new
certifier represents the values as distinct JSON Pointers `/a/b` and `/a.b`,
detects the nested change, and returns `FREEZE`. The conservative integration
adapter also freezes when original and pointer-safe certifiers disagree.

## Fresh commands

```text
python3 -m compileall -q frontier_assurance_lab.py obsure_runtime_assurance.py recert_path_integrity.py test_frontier_assurance_lab.py test_obsure_runtime_assurance.py test_recert_path_integrity.py
python3 -m unittest -v test_frontier_assurance_lab.py test_obsure_runtime_assurance.py test_recert_path_integrity.py
```

## Results

- E1 compile: `PASS`
- E2 unit/negative/adversarial: `PASS`
- E3 integration: `PASS`
- Total: `58/58 PASS`, `0 failures`, `0 errors`
- New RECERT path-integrity tests: `18/18 PASS`
- Prior regression suites: `40/40 PASS`
- Determinism: `100` shuffled mapping-order pairs produced identical output
- Post-persistence execution source: detached worktree at exact code commit

Coverage includes exact nested recovery, JSON Pointer escaping, integer-only
nondecreasing mode, PRESENT/ABSENT/ANY, segment-boundary ignore, dotted-key
alias attack, boolean/integer type confusion, deep array type confusion,
invalid pointer escape, root-wide ignore, policy hidden by ignore, non-string
and mixed-type keys, cyclic state, deterministic mapping permutations, normal
dual-certifier agreement, and legacy false-certification disagreement.

## Failure / repair record

1. The confirmed pre-existing defect was the dotted-path alias that allowed a
   false `CERTIFIED` result.
2. After the first new suite passed `56/56`, self-audit found two untested
   hardening gaps: mixed-type mapping keys could fail during sorting before the
   intended `FreezeError`, and Python list equality could equate `[True]` with
   `[1]`. Key validation was moved before sorting; EXACT comparison now uses
   canonical stable hashes; two regression tests were added.
3. Fresh full rerun after repair passed `58/58`.

No assertion, gate, or scope boundary was weakened to obtain PASS.

## Exact byte binding

| Artifact | SHA-256 | Git blob | Persisted read-back |
|---|---|---|---|
| `RECERT_PATH_INTEGRITY_DESIGN.md` | `0ccf7581717607efd96650d6f9e6e1071f2a6cf7e446f1c462c5950240f042e0` | `ae7d1fe2b494ae95da6dfc12f1513b4c47c73fb2` | exact |
| `recert_path_integrity.py` | `ea4c5a79d16be1bcb6a11fb884bf89be5797842502291a0bc2152175f050eccb` | `e445b5b6fe31f97fc7ac74d5a9feeafcd8713e4d` | exact |
| `test_recert_path_integrity.py` | `91897bac8f7c72ea79ace7a62b17e51601f2ebce9321a6306ba5724b2b8e09d5` | `90cc3edce3a5c58dc6feb55cd85f168d4c30a788` | exact |

GitHub base64 read-back at the exact code commit matched all locally tested
bytes. The successful post-persistence run reported detached HEAD
`fcb7ed7f15a5afe6a31d9a3bbdb8e61bd291e89c`.

## Concurrency evidence

After code persistence, repository head advanced to
`1854c6d7b1598123eb70bd7776cf240add9e22e9`. GitHub comparison proved it was
18 commits ahead with `fcb7ed7...` as merge base; all listed changes were under
`NEXY-BUILD-CONTROL/**`, not this mission root. Mission-state blob remained
`7497f09754e7666c3176194791ca6d5b4d810200` before this checkpoint update.

## Evidence boundary

This proves only the behavior of these exact standalone bytes over bounded
in-memory mapping snapshots. It does not prove snapshot authenticity, atomic
capture, live-store recovery, NEXY.AI integration, canonical adoption,
deployment, or production safety.
