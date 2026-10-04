# Threat Model

**Status:** AI-PROPOSED / reference threat model

## Assets
User/project context values; credentials/secret material; purpose/recipient policy metadata; consent/release grants; receipts/audit lineage; recipient registry identity.

## Trust boundaries
1. Vault/context store -> selector.
2. selector -> firewall.
3. policy/grant registry -> firewall.
4. firewall -> downstream recipient.
5. receipt -> audit store / UI.

## Abuse cases

### Context over-collection
A planner sends the entire project history “just in case.” Mitigation: every datum must satisfy exact purpose and recipient constraints; field rules remove unrelated keys.

### Recipient substitution
A malicious/injected workflow changes `model-a` to `connector-x` after approval. Mitigation direction: grants and data policy bind exact recipient; production request must be integrity-protected through dispatch.

### Consent laundering
A broad old grant is reused for a new purpose. Reference defense: item/purpose/recipient/expiry binding and revocation state.

### Secret smuggling
A secret is marked required to force release. Reference defense: required semantics cannot override hard secret-external prohibition.

### Audit leakage
Receipts copy raw values for “debugging.” Reference defense: receipt schema never accepts values; bounded non-echo tests pressure this invariant.

### Wildcard recipient metadata
Sensitive data declares `*` as recipient. Reference defense: default policy treats absent/wildcard binding as invalid metadata and freezes.

### Prompt injection requests “include all context”
Reference defense: natural-language task text has no authority to change datum policy; the evaluator accepts structured policy metadata only.

## Residual risks
Item IDs/field names may themselves be sensitive; sensitive data can hide in public strings; nested/binary/streaming values are not recursively minimized; library callers can bypass unless architecture enforces the boundary; downstream behavior cannot be controlled here; classifiers/metadata can be wrong; over-conservative policy can cause denial-of-service; receipt digests are not signatures.

## Production hardening candidates
Signed policy snapshots, opaque IDs, mandatory gateway enforcement, schema-aware recursive minimization, content classifiers with explicit uncertainty, taint/provenance tracking, revocation propagation, downstream retention attestations, and abuse-focused E3/E4/E5 tests.
