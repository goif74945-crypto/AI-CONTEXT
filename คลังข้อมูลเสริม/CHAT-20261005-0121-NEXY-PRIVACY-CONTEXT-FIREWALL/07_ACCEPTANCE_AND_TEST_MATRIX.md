# Acceptance and Test Matrix

## Evidence boundary

This matrix applies only to the standalone PCF reference implementation in this mission folder.

| AC | Requirement | Primary evidence | Expected |
|---|---|---|---|
| AC01 | Unknown classification freezes | `test_unknown_classification_freezes` | FREEZE + `UNKNOWN_CLASSIFICATION` |
| AC02 | Unknown purpose freezes | `test_unknown_purpose_freezes` | FREEZE + `UNKNOWN_PURPOSE` |
| AC03 | Unknown destination freezes | `test_destination_identity_mismatch_freezes` | FREEZE + `UNKNOWN_DESTINATION` |
| AC04 | Non-required fields removed | `test_allow_minimizes_payload_and_bounds_retention` | payload has only required fields |
| AC05 | Destination classification ceiling | `test_destination_max_classification_is_enforced` | FREEZE |
| AC06 | Field destination ACL | `test_field_egress_deny_freezes` | FREEZE |
| AC07 | SECRET/CREDENTIAL denied externally | `test_external_secret_and_credential_freeze` | FREEZE |
| AC08 | Bounded retention leases | `test_allow_minimizes_payload_and_bounds_retention`, local no-retain test | min bounds / zero |
| AC09 | Denied values absent from audit/result | secret leak test + verifier fixture | secret literal absent |
| AC10 | Stable decision receipt | deterministic and field-order tests | stable HMAC digest |
| AC11 | Malformed inputs fail closed | non-JSON policy/profile/value + invalid time tests | FREEZE, no uncaught path in covered cases |
| AC12 | CLI emits JSON and meaningful exit | `PrivacyContextCliTests` | JSON, 0/2 exits |
| AC13 | Positive/negative/determinism/privacy/edge coverage | full unittest discovery | all tests pass |
| AC14 | Persisted artifacts read back | GitHub blob-SHA reconciliation | exact match |
| AC15 | No completion before verification | final completion certificate | state gate enforced |

## Additional regression checks

- duplicate IDs freeze;
- policy version mismatch freezes;
- required field missing freezes;
- required field purpose mismatch freezes;
- missing/short receipt key freezes;
- wildcard destination admission is explicit;
- semantically equivalent field ordering has stable result ordering/receipt;
- external FREEZE fixture does not expose canary secret;
- source compiles with Python compileall;
- every JSON schema and fixture parses as JSON.

## Deliberately unproven

- JSON Schema semantic validation by an independent schema engine;
- integration into a real NEXY request path;
- provider deletion/retention behavior;
- transport encryption;
- production key management;
- concurrency/load behavior;
- live privacy incident response;
- legal compliance.

Those require evidence classes above this lab's E1/E2 boundary.
