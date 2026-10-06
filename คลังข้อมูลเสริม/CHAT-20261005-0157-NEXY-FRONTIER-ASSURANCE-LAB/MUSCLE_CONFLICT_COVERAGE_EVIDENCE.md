# MUSCLE Exhaustive Conflict Coverage — Verification Evidence

Status: **AI-PROPOSED / EXPERIMENTAL / NOT CANON / NOT DEPLOYED / NOT A NEXY.AI IMPLEMENTATION**

Verification timestamp: `2026-10-06T13:22:34+07:00`

## Persisted tested revision

- Repository: `goif74945-crypto/AI-CONTEXT`
- Parent revision: `d157845e90fdcc4cf47635bb63954f8b664a5370`
- Code-bearing revision: `f32d52397571644017789f7207f1a83c944afd39`
- Tested tree: `0ebee6f9ea80b512bd91b35418a058b1a944a614`
- Verification checkout: detached fresh worktree at the code-bearing revision
- Protected repositories whose names contain `NEXY.AI`: no writes

## Exact artifact binding

| Artifact | Git blob | SHA-256 |
|---|---|---|
| `MUSCLE_CONFLICT_COVERAGE_DESIGN.md` | `7b9c332ac12cbf19304519d5703db53d711bf92f` | `2c4eb0b0fbfeda8480d2a735e7886e5a9cc67a3f144a6a2eabd604756b346ff7` |
| `muscle_conflict_coverage.py` | `7d2185ac82bf0447f10a4bcd67578870a76c2e16` | `071de79e468b6d51a6a1a802086846cb15740a22a82cb02edb2a23f20f6a8876` |
| `test_muscle_conflict_coverage.py` | `340fe2a5c22a316b9ff3b809f02044eb408d54ef` | `a880b6e1bb822ee83d5c43f7a98e84fb9628434157e1eb8d66be515f77da64e7` |
| `frontier_composed_assurance.py` | `ce0f7482e6114241c235766b1e07c6dfd9c96bc8` | `dd50b0d4d9aa00662ed97d02cce4e80a258a0fde4281d87a2b505a62b2b3915b` |
| `test_frontier_composed_assurance.py` | `456d1f59be7d8c035d9321ee57775dd3a164193d` | `6556836812b7300179c8b1dbc08c7371e50525eb3dfef12355fd9dea05163885` |

All five persisted blobs were read back through the repository API. Each remote blob identifier exactly matched `git hash-object` for the tested local file.

## Verified pre-existing gap

The inherited adapter was executed with two independent contradictory variables:

- `a`: `EQ safe` and `EQ fast`
- `b`: `EQ on` and `EQ off`

Observed inherited result:

- status `UNSAT`
- final domains for both `a` and `b` empty
- reported variable only `a`
- reported core only `a-fast, a-safe`

This proves the precise assurance gap: the result is correct but does not provide conflict-certificate coverage for every independently unsatisfiable variable.

## TDD evidence

The new standalone and composed tests were written first. The red run produced the expected `ModuleNotFoundError` / explicit missing-implementation failures for `muscle_conflict_coverage`, and the composed suite could not import its new dependency. No production code existed at that point.

After implementation and integration, the green run passed.

## Fresh exact-revision verification

Commands were executed from only the mission root in the detached checkout of `f32d52397571644017789f7207f1a83c944afd39`:

```text
python -m compileall -q .
python -m unittest discover -s . -p 'test_*.py'
python -m unittest -v test_muscle_conflict_coverage test_frontier_composed_assurance
```

Results:

- Mission compile: `PASS`
- Full mission suite: `185/185 PASS` in `0.176s`
- Focused standalone + composed suite: `36/36 PASS` in `0.091s`
- New tests in this slice: `15` (`13` standalone, `2` composed)
- Prior regression tests: `170/170 PASS`
- `git diff --check`: `PASS` before persistence
- Verification worktree after test-cache cleanup: clean

The direct exact-revision probe returned:

```text
status=UNSAT
reason=EXHAUSTIVE_MINIMUM_CONFLICT_COVERAGE
unsat_variables=[a,b]
core_counts={a:1,b:1}
subset_checks_executed=6
result_hash=febb6738c2db47f2f85beec2bcb38d3e045fd271aa201f50de25663d85ed46a7
```

## Test-category coverage

- Positive: all independent UNSAT variables, all alternate minimum cores, deletion witnesses, SAT empty coverage.
- Negative: boolean contract limit, foreign contract, malformed inherited MUSCLE input.
- Adversarial: per-variable output explosion, total output explosion, 100 shuffled input orders, contract-only binding change.
- Integration: original selected-core membership, direct gap reproduction/closure, composed MUSCLE gate coverage, distinct composed budget freeze.
- Determinism: all 100 constraint permutations produced the identical complete result.

## Logical Role Court review

- Prosecutor objection: claiming all conflicts would be unsound if only the first variable or first core were retained. Repair: enumerate every empty variable and retain every conflict at the first UNSAT cardinality.
- Prosecutor objection: output caps could silently truncate an allegedly exhaustive family. Repair: any per-variable or total core overflow returns FREEZE with an empty family and explicit gaps.
- Defender case: the inherited validator, input hash, search budget, and exact constraint semantics remain authoritative; the new layer adds coverage without changing satisfiability behavior.
- Judge boundary: the phrase “exhaustive” is accepted only for minimum-cardinality cores. Larger inclusion-minimal cores remain outside the claim and are documented as a residual limit.

## Scope correction

An initial repository-wide compile command encountered unrelated, pre-existing syntax errors in other supplemental projects. It was not treated as a mission failure or repaired. Generated `__pycache__` directories from that overly broad command were removed, and all subsequent compilation and verification were confined to this mission root. The evidence claim is therefore exactly mission-scoped.

## Conclusion

At the code-bearing revision, the experimental MUSCLE deepening provides deterministic, bounded, fail-closed coverage of every minimum-cardinality conflict for every unsatisfiable variable, with deletion witnesses and composed-pipeline integration. This evidence does not claim canon, deployment, or implementation in NEXY.AI.
