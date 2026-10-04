# OBSURE Runtime Witness Certification — Evidence

**Status: PASS for the exact standalone experimental artifact bytes below**

## Target

- Repository: `goif74945-crypto/AI-CONTEXT`
- Persisted code commit: `136f066c86dd6a3cf33354e1786fe072436e08a1`
- Verification time: `2026-10-05T06:27:44+07:00`
- Runtime: Python `3.12.14`, Linux isolated worktree
- Classification: `AI_PROPOSED_EXPERIMENTAL_NOT_CANON`

## Tested contract

The new assurance slice deepens OBSURE by certifying actual bounded runtime
side-effect witnesses after the existing specification sufficiency gate. It
does not add a sixth mission concept.

## Fresh commands

```text
python3 -m compileall -q frontier_assurance_lab.py obsure_runtime_assurance.py test_frontier_assurance_lab.py test_obsure_runtime_assurance.py
python3 -m unittest -v test_frontier_assurance_lab.py test_obsure_runtime_assurance.py
```

## Results

- E1 compile: `PASS`
- E2 unit/negative/adversarial: `PASS`
- E3 integration: `PASS`
- Total: `40/40 PASS`, `0 failures`, `0 errors`
- New tests: `14/14 PASS`
- Determinism: `100` shuffled schema/event permutations produced the same result
- Existing regression suite: `26/26 PASS`

Covered runtime-witness cases include success, failed effect with required
compensation, missing phase, contradictory terminal, correlation drift,
missing actual field value, lifecycle reordering, duplicate sequence,
unexpected compensation, invalid expectation, forged/unadmitted event,
critical-risk specification + runtime integration, and fail-closed rejection
of an insufficient specification.

## Failure -> correction -> rerun

The first post-persistence command was launched from the detached worktree root
instead of the mission directory. `compileall` could not list the four target
files and unittest returned two `ModuleNotFoundError` loader errors. This was a
verification-path defect, not a code defect. The working directory was
corrected to the exact mission root at commit `136f066...`; the full compile
and 40-test suite then passed.

## Exact byte binding

| Artifact | SHA-256 | Git blob | Persisted read-back |
|---|---|---|---|
| `OBSURE_RUNTIME_DESIGN.md` | `d876e75accb29877b927e0beb0d7db0753e75e8dd914b67b11121ada5cb4c91b` | `e4f5b78f3d168efe46067b52f79484fa20174ad8` | exact |
| `obsure_runtime_assurance.py` | `7a9c1cca5449d9aa8184909718a2ec933a81b773cf7fa03f3d673fd838637505` | `891b09d4ae5b94cc643dabe5aeadf4327328a2b6` | exact |
| `test_obsure_runtime_assurance.py` | `b1244f492f048caac71cd2f37b600c67d33b0be442a80340f6cafaa01790cead` | `859257a6fb2a8b9dca48a779789195e055c04bf3` | exact |

GitHub base64 read-back at the exact commit matched every locally tested byte.
The detached worktree reported HEAD `136f066c86dd6a3cf33354e1786fe072436e08a1`
before the successful post-persistence run.

## Concurrency evidence

The first candidate commit was deliberately not published because `main`
moved after target lock. The tree was rebuilt on current head
`e1cc03b1b73dd0d000dde6580c44fe60492f8019` and updated with non-force
fast-forward semantics. A later comparison showed current head
`844d5fa07f834db3dee8d018a2aa4f05995a8c9c` was three commits ahead of the
persisted code commit with the code commit as merge base; those concurrent
commits changed only a different mission root.

## Evidence boundary

This proves only the stated behavior of these exact standalone bytes. It does
not prove telemetry authenticity, NEXY.AI integration, canonical adoption,
deployment, production safety, or live runtime behavior.
