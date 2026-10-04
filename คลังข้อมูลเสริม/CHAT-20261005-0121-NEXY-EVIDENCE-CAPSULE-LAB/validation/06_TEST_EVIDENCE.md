# Test Evidence

## Tested artifact
Compact dependency-free reference implementation:
- `reference/reference_impl.py`
- `reference/test_reference_impl.py`

## Local execution environment
Python 3.13.5 was used in the isolated task sandbox.

## Static evidence
`python -m py_compile reference_impl.py test_reference_impl.py` → PASS.

## Unit/adversarial evidence
`python test_reference_impl.py` → 20 tests, 20 PASS.

Covered behavior:
- canonical key-order determinism;
- float rejection;
- non-string key rejection;
- deterministic capsule fixture;
- empty record rejection;
- short signing key rejection;
- allowed public disclosure;
- denied internal disclosure for PUBLIC_USER;
- OWNER secret disclosure;
- unknown role fail closed;
- valid end-to-end selective proof;
- disclosed value tamper detection;
- header tamper detection;
- audience mismatch rejection;
- required-field enforcement;
- capsule expiry rejection;
- presentation staleness rejection;
- replay rejection;
- wrong signing key rejection;
- corrupted Merkle proof rejection.

## Byte identity linkage
The tested local Git blob IDs were:
- reference implementation: `6b7a899d1f65b89fd0ded881f105b843ef60e187`
- test file: `0b0401e592ebc1420e88fd4e53e5c3ab4f397630`

GitHub `create_blob` returned the exact same blob IDs before the commit tree was built. This links the executed local bytes to the repository blobs.

## Evidence boundary
This is E1 + E2 for the standalone reference code only. It is NOT evidence of NEXY runtime integration, production security, deployment readiness, or cryptographic suitability.