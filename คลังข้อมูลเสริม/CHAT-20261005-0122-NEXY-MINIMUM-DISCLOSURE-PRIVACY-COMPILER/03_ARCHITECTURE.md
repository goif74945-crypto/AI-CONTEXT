# Architecture — NEXY Minimum-Disclosure Privacy Compiler

**Authority:** AI_PROPOSED_CONCEPT  
**Implementation:** isolated reference prototype  
**Product integration:** NOT_VERIFIED

## 1. Purpose
NMDPC is a deterministic preflight between task planning and any context disclosure to another model, processor, or tool boundary.

```text
Task Contract
   │
   ├── purpose
   ├── requested capabilities
   ├── recipient identity + trust class
   ├── requested retention
   └── explicit consents
          │
          v
Data Policy Rules ──> Minimum-Disclosure Compiler
          │                  │
          │                  ├── ALLOW
          │                  ├── TRANSFORM
          │                  └── FREEZE
          │                         │
          v                         v
   field sensitivity         explicit reason set
   allowed purposes
   capability necessity
   transform policy
   max retention
```

## 2. Boundary law
The compiler is not an AI authority. It is deterministic policy machinery. Model output may propose what context it wants, but the policy layer decides what is legally/architecturally disclosable under the supplied policy.

## 3. Input contracts
### TaskRequest
- `purpose`: non-empty exact purpose identifier;
- `capabilities`: requested capability set;
- `recipient`: stable identifier + trust class;
- `requested_retention_seconds`: non-negative;
- `consents`: explicit consent tokens where required.

### DataRule
- `field_name`;
- `classification`: PUBLIC / INTERNAL / PRIVATE / SECRET / CREDENTIAL;
- `allowed_purposes`;
- `required_for_capabilities`;
- `recipient_value_required_for`;
- `preferred_transform`: NONE / MASK / TOKENIZE;
- `max_retention_seconds`.

## 4. Output contract
Each field receives one action:
- `INCLUDE_RAW`;
- `INCLUDE_TRANSFORMED`;
- `OMIT_NOT_NEEDED`;
- `BROKER_OUT_OF_BAND`;
- `FREEZE`.

Plan decision:
- any field/precondition freeze → `FREEZE`;
- otherwise any transformed necessary field → `TRANSFORM`;
- otherwise → `ALLOW`.

## 5. Core invariants
### I-01 Necessity first
A field not required for requested capabilities is omitted before sensitivity/consent escalation.

### I-02 Purpose binding
A required field whose policy does not allow the task purpose freezes. No silent purpose broadening.

### I-03 Recipient identity/trust required
Unknown trust is a material ambiguity and freezes.

### I-04 Credential non-disclosure
Credentials are brokered out-of-band and never emitted in the disclosure bundle. If the recipient itself must receive the credential value, freeze.

### I-05 External secret ban
SECRET → EXTERNAL_MODEL is forbidden in the reference policy.

### I-06 Private external consent
PRIVATE → EXTERNAL_MODEL requires explicit consent and transformation unless raw external disclosure is separately explicit in a case where policy allows it.

### I-07 Retention clamp
Field retention = `min(task_requested, field_max)`.

### I-08 No raw payload in plan
Policy fingerprint/audit plan contains metadata only. Raw values enter only during bundle construction.

### I-09 Frozen plan is non-executable
Bundle construction from a frozen plan raises and emits nothing.

### I-10 Deterministic canonicalization
Rule order does not change canonical plan JSON or fingerprint.

## 6. Trust model
`LOCAL_CORE` is a local trusted enforcement domain. `TRUSTED_PROCESSOR` is a named processor with a pre-established trust/contract relationship. `EXTERNAL_MODEL` is an external AI/model context boundary. `UNKNOWN` always freezes.

Trust classification itself must come from an authoritative registry in a real product. This prototype does not infer trust from a hostname, brand, or model name.

## 7. Transform semantics
### MASK
Replaces the value with a deterministic structural redaction marker. Suitable only when the recipient needs field presence/type context rather than identity.

### TOKENIZE
Uses caller-supplied HMAC key at bundle-build time. The key is never persisted by the compiler. This is a reference pseudonymous token, not a claim of formal anonymization.

## 8. State machine
```text
UNCOMPILED
  -> PRECONDITION_CHECK
      -> FREEZE (invalid task/recipient/rule)
      -> FIELD_EVALUATION
          -> FREEZE (material policy conflict)
          -> PLAN_ALLOW
          -> PLAN_TRANSFORM

PLAN_ALLOW / PLAN_TRANSFORM
  -> BUILD_BUNDLE
      -> ERROR (missing required runtime transform key/value)
      -> BUNDLE_READY

FREEZE
  -> no bundle construction
```

## 9. Observability contract
Audit records should contain:
- plan fingerprint;
- task purpose;
- recipient ID/trust class;
- capability names;
- field names/classifications/actions;
- freeze reasons;
- retention decisions.

They should not contain raw payload values, secrets, or credentials.

## 10. Integration candidates
Non-governing future candidates:
- before NEXY::SWARM/model dispatch;
- provider gateway/context builder;
- NEXY::PULSE privacy receipt for high-risk transfers;
- VAULT data policy metadata;
- NEXY::GUARD / policy gate for sensitive disclosure.

No integration is claimed to exist.
