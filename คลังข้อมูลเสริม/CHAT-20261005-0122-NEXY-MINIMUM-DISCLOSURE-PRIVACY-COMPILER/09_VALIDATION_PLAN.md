# Validation Plan

## E1 Static checks
1. compile every `.py` file with `py_compile`;
2. parse adversarial JSON;
3. enforce unique adversarial case IDs;
4. hash exact source/test/fixture files.

## E2 Unit/invariant checks
The test suite must cover:
- public necessary disclosure;
- necessity omission;
- credential brokering;
- credential recipient-value prohibition;
- private external consent;
- mask/tokenize behavior;
- tokenization runtime-key requirement;
- secret external freeze;
- trusted-processor secret consent;
- purpose mismatch;
- unknown recipient;
- duplicate rules;
- negative retention;
- deterministic order independence;
- randomized retention invariant;
- transformed value non-echo;
- frozen-plan bundle prohibition.

## Pass criteria
- validator return code 0;
- all unittest cases PASS;
- no source/test/fixture hash missing;
- committed contents re-fetched from GitHub;
- no write outside authorized folder attributable to this task.

## Evidence classes not claimed
E3 integration, E4 end-to-end, E5 runtime/operational, E6 deployment.
