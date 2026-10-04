# OXC Failure, Security and Privacy Model

Classification: **EXPERIMENTAL / AI-PROPOSED**

## Threat model

OXC sits near a high-leverage human control surface. Bugs can mislead the operator even if backend authorization remains correct.

Primary threats:

1. denied action rendered as enabled;
2. FREEZE/STOP visually suppressed;
3. presentation preference changing authority;
4. unsupported role/state guessed into a permissive meaning;
5. stale snapshot shown as current;
6. malicious action metadata lowering friction;
7. renderer ignoring disabled/hidden reasons;
8. localization changing control semantics;
9. persistent preference store becoming covert behavioral profiling;
10. frontend treating OXC output as backend authorization.

## Fail-closed controls in reference

- strict supported-value validation;
- duplicate action-id rejection;
- explicit backendAllowed gate;
- explicit role and state allow-lists;
- read-only VIEW rule for MUTATE/RECOVERY;
- hard FREEZE mutation block;
- hard STOP mutation/recovery block;
- verified-truth requirement;
- monotonic friction;
- mandatory critical-state signals.

## Important residual risks

### Stale snapshot risk

OXC cannot prove freshness. A caller could compile an old Core snapshot.

Required integration mitigation:
- bind snapshot to a revision/state version;
- reject stale actions server-side;
- re-authorize every mutation at execution time.

### Malicious/incorrect descriptor risk

If authoritative backend metadata labels a destructive action LOW + REVERSIBLE, OXC cannot discover the lie from this contract alone.

Mitigation:
- risk classification should be backend-governed and schema-validated;
- high-impact action classes may need canonical minimums outside UI code;
- integration tests should compare known dangerous operations against expected friction.

### Frontend trust confusion

OXC output must never become an authorization credential.

Backend must independently enforce:
- identity;
- role;
- policy;
- state;
- concurrency/version;
- action legality.

### Localization risk

Translated labels may be misleading while action IDs remain correct.

Mitigation:
- stable machine action id;
- controlled translation catalogs;
- security-critical wording review;
- never parse translated labels back into authority decisions.

## Privacy model

The reference PreferenceEnvelope contains only presentation choices.

Forbidden proposal extensions without separate authority/review:

- hidden personality scoring;
- emotional profiling;
- attachment optimization;
- behavioral manipulation;
- collecting unrelated PII;
- using a “preference shadow” to mutate truth or policy.

## Abuse tests required before production promotion

At minimum E3/E4 should cover:

- tampered `backendAllowed`;
- stale snapshot / version race;
- unauthorized role;
- FREEZE transition between render and click;
- localization tampering;
- renderer dropping mandatory signal;
- browser storage poisoning;
- replay of an old enabled plan;
- server re-authorization after UI enablement;
- preference mutation during an action flow.

## Recovery principle

If OXC cannot validate the contract, return an explicit error and render no privileged control from that plan.

Do not silently coerce unknown values into defaults.
