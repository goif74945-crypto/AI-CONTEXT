# Validation Report

## Status before repository commit
**LOCAL_REFERENCE_PROTOTYPE: PASS (E1/E2)**  
**GitHub E0 commit verification: PENDING at this record revision**  
**NEXY.AI integration/runtime/deployment: NOT_VERIFIED**

## Environment
- isolated local working directory generated for this task;
- Python 3 standard-library implementation;
- no external network calls by the prototype/tests;
- no production secret or credential value used.

## Executed command
```bash
PYTHONPATH=src python validate.py
```

## Observed result
- return code: `0`;
- unittest cases: `22`;
- passed: `22`;
- failed/errors: `0`;
- JSON files parsed: `5`;
- Python source/test/validator files compiled: `7`.

Raw output: `evidence/validation-20261005.txt`  
Raw output SHA-256: `be4e8e9496d043c1938491145647de2d16786c864d8a8e39a6ff935f23b69bfe`

## Key executed proofs
1. credential uses broker path and does not appear in disclosure bundle;
2. recipient-required credential value freezes;
3. secret → external model freezes across transform/consent combinations;
4. private → external model without explicit consent freezes;
5. private external mask/tokenize paths do not echo raw value;
6. tokenization requires a runtime HMAC key;
7. irrelevant sensitive fields are omitted before consent escalation;
8. purpose mismatch freezes;
9. unknown recipient trust freezes;
10. duplicate field policy freezes;
11. negative retention freezes;
12. retention is never greater than request or field maximum across 250 deterministic randomized cases;
13. policy fingerprint/JSON remain identical across 100 shuffled rule permutations;
14. frozen plans cannot build bundles;
15. example CLI policy compiles to the expected field action mix without accepting payload values.

## Exact local hashes
### Python
- `src/nmdpc/__init__.py`: `d88b563871bb505873c0bf957177c34aa015fba502ad4619b749e2c924b18619`
- `src/nmdpc/cli.py`: `9ce5becd927c581c792f773cf1326f6c0afe2558f91ee6500c0eb32a4a2f56ad`
- `src/nmdpc/compiler.py`: `a9bc3a4a411aa8b8061677dfe0dea6b165cb7870dcef24bb24de7a3627c4df74`
- `tests/test_cli.py`: `170734c164bd360364080f18da558f354d3bd11fdec25d880dc3e4a1e8c8462c`
- `tests/test_compiler.py`: `df329cdbdf7b87ad4a6d208ae15ce18509ed8d1592ad4cfc59e39addde26a40d`
- `tests/test_invariants.py`: `478bb9dbbb9400d0460096e0210a774213f97465b4a89d60881070356f7b5351`
- `validate.py`: `e5c85a7aefd54efa2ffc737326e8a8fc51eb8646180fc08c96e3602054777225`

### JSON
- `examples/support_case_policy.json`: `6d96e4759f069191aec5203f908ca9569da27f0dbfc0d2c3d863e59f4e1859bc`
- `fixtures/adversarial_cases.json`: `ef51fa041a56b4ef8badb4370f563311f65305b2217f85ac3018f14c5b9119e7`
- `requirements.json`: `0735e85c4b3ac60a5702ef683856d7e5b2b1d6d78c032bb675e6f52b6250f85f`
- `schemas/disclosure-plan.schema.json`: `513e71c0b8f81d7c7385cfde7ef0a0522ced5f35adf5baf2723d7aaaa510a45e`
- `schemas/disclosure-policy.schema.json`: `662b1b7c56cb65b9388b3ab74ddd45c762374919ced0746b2fc629c88e36b01b`

## Evidence interpretation
E1/E2 validates only the isolated reference implementation and its stated invariants. It does not establish actual NEXY provider-gateway enforcement, user UX, operational retention/deletion, privacy compliance, or deployment behavior.
