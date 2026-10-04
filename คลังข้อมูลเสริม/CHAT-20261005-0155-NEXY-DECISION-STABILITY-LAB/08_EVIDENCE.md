# Verification Evidence

## Verified code revision
`a1bd30487c8af56c9350695a748111834f41a030`

The source/test bytes executed in the sandbox were independently checked using the Git blob hash formula and matched the blob SHAs returned by GitHub for the exact revision above.

## E1 — Static / compile
Command class:
`python -m py_compile code/*.py tests/*.py`

Result: **PASS**

Environment:
- Python 3.13.5
- Linux x86_64 (kernel string observed: Linux-6.18.44-x86_64-with-glibc2.41)

## E2/E3 — Unit + negative + integration
Run A:
`PYTHONHASHSEED=1 python -W error -X dev tests/test_lab.py`

Result: **21/21 PASS**

Run B:
`PYTHONHASHSEED=999 python -W error -X dev tests/test_lab.py`

Result: **21/21 PASS**

Coverage includes core canonicalization, duplicate conflicts, NaN rejection, MONO positive/negative cases, IRIS order/noise detection, EDGE determinism/truncation, MDE minimum subsets, DAMP dwell/fingerprint/safety/replay, five-system integration, exhaustive 4-atom fingerprint permutations, and 100 fixed-seed MONO property cases.

## Stress
Both hash seeds executed:
- 5,000 MONO randomized cases
- 5,000 fingerprint shuffle cases
- 50,000 temporal transitions
- 2,821 worsening/safety regressions observed and verified immediate

Seed 1 elapsed: 0.597442 s
Seed 999 elapsed: 0.601393 s

Timing is sandbox evidence only, **not** a production performance claim.

## Determinism probe
Both hash seeds produced byte-identical normalized output:

`{"edge":1,"fingerprint":"7e410011cc7a1187454e0de662ed2a0740dc2d6e9c2715455a59dc5627f05698","mde":2,"temporal":["FREEZE","RELEASE","FREEZE"]}`

SHA-256:
`4b577bd21dbf048a4bbc4953faa088d1440289ee212a213806c27f81bfa04f06`

## Remote re-read
At verified code revision, GitHub returned these exact blob SHAs:
- code/core.py: 80e412484a40583d6f32bcd2e439474e584dda63
- code/mono.py: 37bc24819ce3f7a2c74c0686a1b41fcaa452cf20
- code/iris.py: bea248c368a35a316af3c8b7755659c3f26289fa
- code/edge.py: 2307d85ab799027f16ee67fb34d940fb525db473
- code/mde.py: e0c626b56af654ae2e45b6d3af1fb48d5c7ed42f
- code/damp.py: 29bf09300a434c67e0573497da2efb63d6a26c37
- code/suite.py: db115a4774e7c0e6b369383690cc8673b5fdbed5
- tests/test_lab.py: 184db7b382fca5de84ccd9f5a8ecd59a4781adf6
- tests/stress_lab.py: fe577a14e24eaf4c2c5d874cd0216e7c60442feb

## Failure / recovery evidence
1. Early integration test: 16 PASS / 1 FAIL due an incorrect expectation about two identical RELEASE fingerprints. The test vector was corrected rather than weakening DAMP. Rerun passed.
2. Re-audit found canonical duplicate tag-order and pre-oracle canonicalization risks. Implementation was corrected and property coverage added.
3. First committed modular artifact compiled but test execution failed with `ModuleNotFoundError: core` because test import path pointed to `tests/code`. The exact committed failure was reproduced.
4. Import path was corrected to sibling `../code`; corrected test/stress Git blob identity was verified and all gates rerun.
5. Multiple Git branch races (409/422) occurred because concurrent chats moved `main`. Recovery used immutable blobs plus non-force optimistic fast-forward retries. No history was force-written.

## Evidence classes not claimed
- NEXY runtime integration: NOT VERIFIED
- UI/browser behavior: NOT VERIFIED
- Production provider behavior: NOT VERIFIED
- Deployment/production security: NOT VERIFIED
- E4/E5/E6 production evidence: NOT VERIFIED
