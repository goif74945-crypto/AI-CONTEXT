# Wave 01–09 Validation Report

**Mission:** CHAT-20261005-0122-NEXY-PRIVACY-EGRESS-FIREWALL  
**Validated scope:** NPCEF reference prototype only  
**Verdict:** PASS for E0/E1/E2 reference-prototype claims; NOT_VERIFIED for NEXY integration/runtime/deployment/legal compliance.

## Wave 09 — recipient alias/substitution/redirect attack model

Status at this checkpoint: **LOCAL_VERIFIED_PENDING_REMOTE_READBACK**.

Wave 08 was marked `SKIPPED_OVERLAP` after fresh SHA-bound evidence showed that IX-Lab already owns interaction budgets, deterministic ASK/CONFIRM/FREEZE routing, protected confirmations, and confirmation-fatigue research. Wave 09 was the next bounded non-overlapping topic. All new route mechanisms remain **AI-PROPOSED / NON-GOVERNING**.

### TDD evidence

RED was observed before implementation:

`PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_recipient_route -v`

Observed: import failure because `RecipientRouteProof` did not exist; 1 loader error; exit 1.

After the smallest complete implementation, the same focused suite observed 12/12 PASS; exit 0.

### Fresh executed verification

| Check | Exact command | Observed result |
|---|---|---|
| Focused recipient-route suite | `PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_recipient_route -v` | 12/12 PASS; exit 0 |
| Full regression | `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v` | 68/68 PASS; exit 0 |
| Existing property audit | `PYTHONDONTWRITEBYTECODE=1 python -m tools.property_audit` | 1,280 cases; 0 failures; exit 0 |
| Existing batch-consent audit | `PYTHONDONTWRITEBYTECODE=1 python -m tools.batch_consent_audit` | 18 cases; 0 failures; exit 0 |
| Recipient-route audit | `PYTHONDONTWRITEBYTECODE=1 python -m tools.recipient_route_audit` | 52 cases; 52 deterministic replays; 52 expected outcomes; 52 value non-echo checks; 0 failures; exit 0 |
| Static compilation | `PYTHONPYCACHEPREFIX=/tmp/npcef_wave09_pycache python -m compileall -q src tests tools` | PASS; exit 0 |
| JSON/static checks | `python -m json.tool fixtures/adversarial_cases.json`; `python -m json.tool evidence/release_evidence.json`; `git diff --check` | PASS; exit 0 |

### Wave 09 candidate blob bindings

These local Git object IDs bind the tested code. They are pending remote E0 read-back at this checkpoint.

| File | Candidate blob SHA |
|---|---|
| src/npcef/__init__.py | 24e8159d16525c2ff932d8f951e2c13173aec6ac |
| src/npcef/model.py | 284ab7c56db98336e63bc6a6c911b4385e1c1466 |
| src/npcef/core.py | a0b3e697f7c92ad20748d1a7c8e284b0aaefe470 |
| src/npcef/receipt.py | ed51acd941e95fee6637405ebf8b4dadd487997c |
| tests/test_privacy_firewall.py | aa0d7b45bafd21bc59779bc4d25718891a8f07b2 |
| tests/test_release_contract.py | 2cd6bd4e1fd02c7da5eee27afb51163508f9d5fa |
| tests/test_batch_consent.py | 7f6c464f85f636c44fa9b62e60207963adcf30d2 |
| tests/test_recipient_route.py | 90ec21082db0645ad9d5484082e393815979287a |
| tools/property_audit.py | 15a4a70e398e16377d3df20b4fbff927638eb6a1 |
| tools/batch_consent_audit.py | 3d2c877517458ad4b8cb23d0ccb55728999ac574 |
| tools/recipient_route_audit.py | 1659a2a2a6997e5be0de6e04c021dd0a7ce1a534 |

### Truth boundary

The reference evaluator requires explicit external route metadata and accepts only a direct exact route. It does not authenticate the resolver, independently observe DNS/HTTP/service-mesh behavior, establish alias equivalence, or bind evaluation to dispatch. E3–E6, NEXY.AI integration, legal compliance, and production privacy/security remain NOT_VERIFIED.

## Wave 07 — exact-scope batch consent

Status at this checkpoint: **VERIFIED_E0_E1_E2_REFERENCE_PROTOTYPE**.

Atomic implementation/evidence commit: `b55246d4307263d80d82a35786e9df410fc29d6d`.

Waves 02–06 were marked `SKIPPED_OVERLAP` after a fresh, SHA-bound sibling scan. Wave 07 was the next bounded non-overlapping topic: exact-scope grant bundling for consent-required items. The mechanism remains **AI-PROPOSED / NON-GOVERNING**.

### TDD evidence

RED was observed before production implementation:

`PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_batch_consent -v`

Observed: import failure because `ConsentBundleGrant` did not exist; 1 loader error; exit 1.

After the smallest complete implementation, the same focused suite observed 12/12 PASS; exit 0.

### Fresh executed verification

| Check | Exact command | Observed result |
|---|---|---|
| Focused batch-consent suite | `PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_batch_consent -v` | 12/12 PASS; exit 0 |
| Full regression | `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v` | 56/56 PASS; exit 0 |
| Existing property audit | `PYTHONDONTWRITEBYTECODE=1 python -m tools.property_audit` | 1,280 cases; 0 failures; exit 0 |
| Batch-consent audit | `PYTHONDONTWRITEBYTECODE=1 python -m tools.batch_consent_audit` | 18 cases; 18 deterministic replays; 18 expected outcomes; 18 value non-echo checks; 9 order-invariance pairs; 0 failures; exit 0 |
| Static compilation | `PYTHONPYCACHEPREFIX=/tmp/npcef_wave07_pycache python -m compileall -q src tests tools` | PASS; exit 0 |
| Fixture parse | `python -m json.tool fixtures/adversarial_cases.json` | PASS; exit 0 |
| Evidence parse | `python -m json.tool evidence/release_evidence.json` | PASS before this update; exit 0 |
| Whitespace/static diff check | `git diff --check` | PASS; exit 0 |

### Wave 07 candidate blob bindings

These Git object IDs bind the bytes tested above and matched GitHub read-back from the exact atomic commit.

| File | Candidate blob SHA |
|---|---|
| src/npcef/__init__.py | 7ffea5c8548a19883124c6db0dd1621e9a14c97e |
| src/npcef/model.py | 94bf716eb7ef3f1dd1d2494be76f25c3d99da658 |
| src/npcef/core.py | d3b2c1f2f3d5ece2e1c5ebcb0be4daf3b9ff775c |
| tests/test_batch_consent.py | 188347bda56644054845b86f7f36972153977f62 |
| tools/batch_consent_audit.py | 246d94e3c08b23ca2d4f5c9871ffb53c9d68ffa4 |

### Remote E0 read-back

All 13 files changed by Wave 07 were fetched from exact commit `b55246d4307263d80d82a35786e9df410fc29d6d` as base64 and compared byte-for-byte with the locally tested candidate: 13/13 exact matches. This includes the five source/test/tool bindings above plus the eight requirement, policy, threat, plan, overlap, validation, evidence, and checkpoint records.

### Behavioral boundary

- A live bundle is valid only for the exact request, purpose, recipient, expiry/revocation state, and the exact full set of consent-required item IDs.
- Under-scoped or over-scoped active bundles fail closed with `BUNDLE_SCOPE_NOT_EXACT`.
- Multiple active matching bundles, or active single grants overlapping an active exact bundle, fail closed with `AMBIGUOUS_GRANT_COVERAGE`.
- Expired, revoked, or binding-mismatched bundles are inert and do not create ambiguity.
- A bundle cannot override the existing hard block on external SECRET egress.
- Receipts remain value-free and deterministic.

This prototype does not authenticate grant issuers, establish human comprehension, prove legal consent, integrate with NEXY.AI, or establish E3–E6 or production-security evidence.

## Evidence discipline

This report deliberately separates:
- **E0 presence/read-back** from behavior;
- **E1 compile/parse** from runtime behavior;
- **E2 unit/property execution** from integration/E2E/production;
- AI-PROPOSED architecture from canonical NEXY law.

## TDD / defect history

### RED-01 — no production module
The first unit run was executed before implementation and failed with `ModuleNotFoundError`. This established the initial red state.

### GREEN-01
A minimal pure evaluator was implemented and the first suite reached 24 passing tests.

### RED-02 — sensitive wildcard recipient binding
Independent adversarial review found that a Sensitive+ item with `allowed_recipients={"*"}` could reach a REDACT path rather than treating policy metadata as unsafe. A regression test expected `FREEZE` and failed against the pre-fix implementation.

### GREEN-02
Sensitive+ wildcard recipient metadata became a validation failure. Suite reached 25 passing tests.

### RED-03 — runtime type hints are not a boundary
Five malformed-metadata regression cases demonstrated crashes for non-string request/item metadata, invalid sensitivity enum, naive grant expiry, and invalid field-purpose entries.

### GREEN-03
Runtime validation was added for request, item, grant, enum, flag, scope-set, expiry, and field-rule metadata. Suite reached 30 passing tests.

### RED-04 — malformed terminal receipt / fake grant object
Two final boundary tests exposed:
- an invalid recipient-class object whose `.value` was not JSON serializable, causing receipt construction to crash;
- a partial fake grant with `grant_id` but missing required attributes, causing attribute access to crash.

### GREEN-04
Receipt construction now recognizes only the real `RecipientClass` enum and otherwise emits the literal `INVALID`; grant validation requires an actual `ConsentGrant` object before field access.

## Fresh executed verification

### Comprehensive local regression suite
`python -m unittest discover -s tests -v`

Observed:
- 44 tests run
- 44 PASS
- exit 0

This includes the exact-byte release-contract suite plus the broader adversarial suite. Because the broad historical test file had a local/GitHub byte mismatch after concurrent editing, it is **not** used as the exact-byte evidence anchor.

### Exact-byte release-contract suite
`python -m unittest tests.test_release_contract -v`

Observed:
- 12 tests run
- 12 PASS
- exit 0
- local Git blob SHA: `e7a0b8d24f4511485d59799306e2f66f54bac38c`
- GitHub read-back blob SHA: `e7a0b8d24f4511485d59799306e2f66f54bac38c`

### Bounded deterministic property audit
`python -m tools.property_audit`

Observed:
- bounded cases: 1,280
- deterministic replays: 1,280
- receipt non-echo checks: 1,280
- secret external egress checks: 192
- terminal payload checks: 592
- order permutations: 24
- assertion failures: 0
- tool local/GitHub blob SHA: `3a4cc12c48100a69ef170511f26eb11a361821b9`

### Static compilation
`python -m compileall -q src tests tools`

Observed: exit 0.

### Fixture parse
`python -m json.tool fixtures/adversarial_cases.json`

Observed: exit 0.

## Exact source binding

Local Git object hashes were compared with GitHub read-back blob hashes and matched for the release-relevant source set:

| File | Blob SHA |
|---|---|
| src/__init__.py | cb41d00bb2c7c26bbd8b7ca3a7800e2a27d55293 |
| src/privacy_firewall.py | edfe506a219a07b1d3ca020510191aadc9a9289e |
| src/npcef/__init__.py | f1234d2363ff1f9ebd455073bbbb94ada0908218 |
| src/npcef/model.py | b737a405862891eedf594db6a6e7b3dee67f8764 |
| src/npcef/receipt.py | 756307d5b2a2333108636397ee8be73b139d7c8c |
| src/npcef/utils.py | 50910998bb44af05cbf0bf767c23af3bdeafe4d0 |
| src/npcef/core.py | 8a971f51970b1dfb46a433a6a729d83e165544dc |
| tests/test_release_contract.py | e7a0b8d24f4511485d59799306e2f66f54bac38c |
| tools/__init__.py | e69de29bb2d1d6434b8b29ae775ad8c2e48c5391 |
| tools/property_audit.py | 3a4cc12c48100a69ef170511f26eb11a361821b9 |
| fixtures/adversarial_cases.json | 2fa02aa6690148cd24f9b025d667ad88e0c27423 |

## Sandbox clone limitation

A separate attempt to `git clone` the public repository at an exact main HEAD failed because the execution sandbox could not resolve `github.com`. That failed attempt is **not counted as evidence**. Exact-file binding instead uses Git object hashes plus GitHub connector read-back.

## Concurrent-work safety

One early GitHub write received HTTP 409 because another chat moved `main` concurrently. No force push or overwrite was used. Subsequent writes refreshed current state and retried only additive files/authorized paths.

A concurrent sibling Context Release Firewall later appeared with overlapping privacy-release concepts. Future NPCEF work is constrained by `13_CONCURRENT_OVERLAP_BOUNDARY.md` to complementary topics and must rescan sibling work before each wave.

## Claim status

- E0 repository presence/read-back: **PASS**
- E1 Python compile + JSON parse: **PASS**
- E2 release-contract unit behavior: **PASS**
- E2 bounded property invariants: **PASS**
- E3 integration with NEXY/real connector/model: **NOT_VERIFIED**
- E4 end-to-end user flow: **NOT_VERIFIED**
- E5 runtime/operational security: **NOT_VERIFIED**
- E6 deployment: **NOT_VERIFIED**
- Legal/regulatory compliance: **NOT_VERIFIED**
- Production privacy/security guarantee: **NOT_VERIFIED**
