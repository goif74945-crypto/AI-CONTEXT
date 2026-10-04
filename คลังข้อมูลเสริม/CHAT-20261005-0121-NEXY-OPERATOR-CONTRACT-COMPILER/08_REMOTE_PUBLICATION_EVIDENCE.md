# NOCC Remote Publication Evidence

Work ID: `CHAT-20261005-0121-NEXY-OPERATOR-CONTRACT-COMPILER`

Status: **PASS for supplemental artifact publication and E1/E2 reference implementation validation**
Classification: **AI_PROPOSAL / NOT current NEXY.AI runtime truth**

## Publication lineage

- Isolated publication branch: `nocc/chat-20261005-0121`
- Publication commit: `f4a06c904d22461530d46eebca2102de5329f361`
- Pull request: `#25`
- Merge commit: `7a8569142fd1ef75f4571b5f34cb9de7c805b429`
- Merge method: normal non-force merge
- Target repository: `goif74945-crypto/AI-CONTEXT`
- Target namespace: `คลังข้อมูลเสริม/CHAT-20261005-0121-NEXY-OPERATOR-CONTRACT-COMPILER/`

The first direct ref-update attempt was rejected as non-fast-forward because `main` changed concurrently. No force update was used. The work was republished through an isolated branch + pull request so concurrent work was preserved.

## Byte identity evidence

Local verified bundle:
- SHA-256: `920e3fcd795e75ac320bc05299d2873a42fac925a60d4100c10810b77ad00141`
- local `git hash-object`: `9dc73896c5533b46a9b5fe6f433922d30212f858`

Remote `main` observation after merge:
- `NOCC_FULL_SOURCE.tar.gz` Git blob SHA: `9dc73896c5533b46a9b5fe6f433922d30212f858`
- remote blob size: `29181` bytes
- `BUNDLE_SHA256.txt` records the same SHA-256 as the local verified bundle.
- `REMOTE_INDEX.md` re-read successfully from `main`.

The matching Git blob SHA proves the remote archive bytes are identical to the locally tested archive bytes.

## Verification rerun after remote publication

Executed again against the local source tree whose exact archive was published:

- `python -m compileall -q src tests tools` -> PASS, exit 0
- `PYTHONPATH=src python -m unittest discover -s tests -v` -> PASS, 36/36
- `PYTHONPATH=src python tests/test_matrix.py -v` -> PASS, 12/12
- JSON parse validation across project JSON artifacts -> PASS
- policy scenarios -> 120
- policy matrix semantic digest -> `18582b915709a4a30f1955b063456b341c5a197f14828494dd0d5ff04111022c`

## Evidence class

- E0 Presence: PASS
- E1 Static/parser/compile/schema-shape checks: PASS
- E2 Unit/negative/determinism/policy behavior: PASS
- E3 Integration with NEXY.AI: NOT_VERIFIED / NOT_PERFORMED
- E4 Browser/user flow: NOT_VERIFIED / NOT_PERFORMED
- E5 Runtime/operational behavior: NOT_VERIFIED / NOT_PERFORMED
- E6 Deployment: NOT_VERIFIED / NOT_PERFORMED

## Protected-scope audit

This execution did not intentionally mutate any repository whose name contains `NEXY.AI`.

All durable writes were made only to `goif74945-crypto/AI-CONTEXT` under the isolated supplemental namespace above.

## Resume point

Future work should begin from `REMOTE_INDEX.md`, verify `BUNDLE_SHA256.txt`, extract `NOCC_FULL_SOURCE.tar.gz`, read the bundle's `README.md`, `02_ARCHITECTURE_SPEC.md`, `04_REQUIREMENT_EVIDENCE_LEDGER.md`, and `05_ADOPTION_PLAN.md`, then rerun the tests before changing policy semantics.

Promotion into a real NEXY build requires explicit authoritative specification approval and E3+ evidence. Presence of this supplemental project is not such approval.
