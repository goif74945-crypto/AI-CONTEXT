# LBCC Failure Model

| Failure | Detection | Behavior | Evidence path |
|---|---|---|---|
| duplicate atom ID | input validation | exception / CLI error | unit test |
| malformed truth class | parser | exception / CLI error | unit test |
| protected atoms exceed budget | exact serialized size | FREEZE | unit test |
| loss exceeds policy | computed ppm | FREEZE | unit test |
| likely credential in input | secret scanner | FREEZE by default | unit test |
| capsule/source mismatch | SHA-256 recomputation | verification FAIL | unit test |
| retained atom altered | source equality/hash | verification FAIL | unit test |
| loss ledger altered | root recomputation | verification FAIL | unit test |
| unknown schema version | parser/verifier | fail closed | unit test |
| CLI invalid input | strict parse | nonzero exit | integration test |

## Recovery

The codec never mutates source data, so recovery is retry with a corrected policy/input. A caller may:
- increase byte budget;
- increase authorized loss budget;
- explicitly change protection policy;
- remove sensitive content upstream;
- split the source bundle into authority-approved shards.

The codec itself never decides to weaken policy after a failure.
