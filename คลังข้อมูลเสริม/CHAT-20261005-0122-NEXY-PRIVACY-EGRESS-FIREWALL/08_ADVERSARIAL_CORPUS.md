# Adversarial Corpus Design

The machine-readable corpus is in `fixtures/adversarial_cases.json`. It is a reusable scenario catalog, not proof by itself.

Scenario families:
- purpose drift;
- recipient substitution;
- stale/expired data;
- revoked/expired/misbound grant;
- secret external egress;
- optional versus required semantics;
- field-level over-sharing;
- duplicate identifiers;
- missing/wildcard recipient binding;
- receipt-value leakage;
- permutation/determinism pressure.

The executable unit suite encodes the current decisive cases. The property audit then enumerates a bounded Cartesian product across sensitivity, recipient class, requiredness, explicit consent mode, purpose match, recipient match, expiry, and grant validity.

A finite corpus cannot prove absence of all privacy failures. It proves only the enumerated invariants over the exercised model.
