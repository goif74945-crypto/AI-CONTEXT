# Evidence — Artifact Referential Integrity Guard

- Evidence class: E1 static + E2 unit
- Final unit command: `python -m unittest -v test_src.py`
- Final result: PASS, 5 tests, 0 failures/errors.

## Red/green lineage
Initial RED occurred before implementation. Second RED showed empty manifests incorrectly returned PASS. The status law was corrected to `NOT_VERIFIED` for empty graphs, then regression passed.

## Proven behaviors
- valid requirement→test→evidence graph with matching hash passes;
- missing references fail;
- stale hashes fail;
- duplicate IDs fail closed;
- orphan artifacts are reported;
- empty graph is not verified.

## Limitation
The manifest describes proof topology; it does not itself prove that a referenced test semantically satisfies a requirement.
