# Negative-Space & Bypass Atlas
Status: PROPOSAL / AI-PROPOSED CONCEPT

## Thesis
An audit should preserve not only what was tested but also what was not tested, unreachable, unavailable, or capable of bypassing the canonical path.

## Gap classes
untested transition; role/permission combination; failure timing; environment; provider/model; rollback path; hidden feature flag; direct API/storage mutation; stale cache/replica; background worker; admin path; replay path.

## Proposed record
Gap = {id, surface, expected_contract, reason_unverified, reachable_by, affected_claims, severity_if_exploited, evidence_needed, status}

## Bypass law
For each critical invariant, enumerate known mutation entrances. Strong verification requires coverage of every authorized entrance plus proof that unauthorized entrances are blocked at the required evidence class.

## Important limit
Absence from this atlas never proves absence from the system. Completeness is legal only against a declared, versioned surface inventory.
