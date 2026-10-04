# Proposed NEXY Integration Contract

## Status

`AI_PROPOSED_INTEGRATION_CONTRACT` only. No NEXY implementation mutation has been performed.

## Intended placement

```text
Human / Project / Vault context
          |
          v
 NEXY task decomposition
          |
          v
 Context requirement declaration
          |
          v
 +--------------------------+
 | Privacy Context Firewall |
 +--------------------------+
       | ALLOW        | FREEZE
       v              v
 Provider/tool      NEXY freeze surface
 adapter            with typed reasons
       |
       v
 Downstream verification / judge
```

PCF belongs **before provider/tool egress**, not after provider output. Output verification cannot undo disclosure that already happened.

## Caller obligations

A future NEXY adapter must supply:
1. canonical task purpose;
2. exact destination identity;
3. exact required context field IDs;
4. authoritative classification and egress metadata for every candidate field;
5. current policy version;
6. controlled decision timestamp;
7. HMAC key through a server-side secret boundary.

The adapter must not silently synthesize missing classification metadata from an LLM guess.

## Output handling

### ALLOW
The adapter may forward only `payload`. It should persist/attach:
- receipt digest;
- policy version;
- decision/freeze metadata;
- leases;
- trace/task identity outside PCF if required.

### FREEZE
The adapter must not forward the original envelope or candidate field values as a fallback. The freeze is a control decision, not a prompt asking another model whether the firewall was being too strict.

## Provider abstraction

Provider adapters should expose a normalized destination profile independent of vendor APIs. This supports model hot-swap without allowing substitution to silently weaken privacy constraints.

A provider/profile change is a policy-relevant state change. Cached ALLOW evidence for provider A cannot prove admission to provider B.

## Vault interaction

Proposed rule:
- Vault/source data stays canonical and unmodified;
- PCF produces an ephemeral projection for one purpose/destination;
- durable audit stores field identities, policy version, decision, receipt, and violation codes;
- denied raw values are not copied into the privacy audit record.

## Failure mapping

Suggested NEXY-facing codes:
- `PCF_POLICY_UNKNOWN`
- `PCF_PURPOSE_UNKNOWN`
- `PCF_DESTINATION_UNKNOWN`
- `PCF_CLASSIFICATION_UNKNOWN`
- `PCF_EGRESS_DENIED`
- `PCF_REQUIRED_CONTEXT_UNAVAILABLE`
- `PCF_RECEIPT_AUTHORITY_MISSING`

The reference implementation retains more granular internal violation codes; an integration layer may map them without losing raw evidence records.
