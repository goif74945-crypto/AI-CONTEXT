# Policy Contract

## Classification defaults

### PUBLIC
Necessary + purpose-allowed → raw disclosure allowed.

### INTERNAL
- LOCAL_CORE → raw allowed;
- TRUSTED_PROCESSOR / EXTERNAL_MODEL → transformation required; no transform → FREEZE.

### PRIVATE
- LOCAL_CORE → raw allowed under local policy;
- TRUSTED_PROCESSOR → explicit `private_to_trusted_processor` consent + transform;
- EXTERNAL_MODEL → explicit `private_to_external_model` consent + transform by default;
- raw external private value requires separate `private_raw_to_external_model` consent and a rule that has no transform path. This is intentionally difficult and should likely be narrowed further in production policy.

### SECRET
- LOCAL_CORE → raw allowed inside local trust boundary;
- TRUSTED_PROCESSOR → explicit `secret_to_trusted_processor` consent, with transform where available;
- EXTERNAL_MODEL → always FREEZE in this reference policy.

### CREDENTIAL
Never added to disclosure bundle. Use `BROKER_OUT_OF_BAND`. If recipient value is declared required, FREEZE.

## Consent semantics
Consent tokens are inputs from an authoritative upstream consent/authority subsystem. NMDPC does not create consent based on natural-language guesswork and does not infer consent from prior behavior.

## Retention semantics
Per disclosed field:
`effective_retention = min(requested_retention_seconds, max_retention_seconds)`.

A real deployment must also enforce deletion/expiry at storage/provider boundaries. The prototype only plans the allowed maximum; it does not prove downstream deletion.

## Purpose semantics
Purpose identifiers should be stable registry IDs, not free-text slogans. Exact membership in `allowed_purposes` is required.

## Recipient semantics
A production trust registry should bind recipient ID to:
- processor/provider identity;
- contract/DPA scope if relevant;
- region/tenant constraints;
- approved purpose classes;
- retention guarantees;
- model-training/logging settings;
- current verification state.

The prototype accepts the trust class as authoritative input and therefore cannot prove that a real recipient actually satisfies it.
