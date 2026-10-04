# Architecture — Purpose-Bound Context Egress Firewall

**Status:** AI-PROPOSED / NON-GOVERNING

## 1. Boundary model

```text
Trusted Context/Vault
       |
       v
 [Context Selector]
       |
       v
 [NPCEF Evaluator] <---- [Policy Snapshot]
    |      |  ^          [Consent Grants]
    |      |  |          [Recipient Registry]
    |      |  +----------[Purpose Registry]
    |      |
    |      +--> value-free Egress Receipt
    v
 Minimal Allowed Payload
       |
       v
 Model / Connector / Export / Trusted Local Consumer
```

The firewall must sit on the **last trusted release boundary** before data leaves the trusted context domain. Earlier planners may propose context; they do not authorize its egress.

## 2. Inputs

An `EgressRequest` contains stable request ID, exact purpose ID, exact recipient identity/class, timezone-aware evaluation time, candidate data items, and currently valid consent/release grants.

A `DataItem` contains opaque item ID, value, sensitivity class, allowed purposes/recipients, optional expiry, explicit-consent mode, required/optional semantics, and optional top-level field-purpose map.

## 3. Decision precedence

Fail-closed precedence:
1. malformed request/item metadata -> `FREEZE`;
2. expired / purpose mismatch / recipient mismatch -> remove optional or `BLOCK` required;
3. secret external egress -> remove optional or `BLOCK` required;
4. missing required consent -> `ASK`; optional item is removed;
5. field minimization -> remove fields unrelated to purpose;
6. required mapping with zero purpose-necessary fields -> `BLOCK`;
7. if any required block exists, overall `BLOCK` wins over `ASK`;
8. otherwise required consent gap -> `ASK`;
9. otherwise any removal -> `REDACT`;
10. otherwise `ALLOW`.

`BLOCK` precedence over `ASK` avoids asking for consent when another hard prohibition already makes the request impossible.

## 4. Determinism

The reference engine sorts item IDs, redaction lists, field names, and reason codes before receipt construction. A canonical JSON representation is hashed into the receipt digest. The digest is **not a signature** and gives no authenticity by itself; production would require signed/version-bound receipts or an authenticated audit channel.

## 5. Privacy-safe receipts

Receipts record release metadata only: item IDs, included/redacted/blocked/consent-needed sets, field names removed, reason codes, policy fingerprint, and decision digest. They never echo raw values. Production adoption must also require opaque/non-sensitive item identifiers; otherwise an identifier itself could become a side channel.

## 6. Consent/release grants

A grant is valid only for the exact item, purpose, recipient, and unexpired time window and must not be revoked. The reference model intentionally does not infer legal basis, user identity, authority delegation, or jurisdiction. Those belong to a higher-order policy/identity system.

## 7. Failure semantics

- Bad metadata: `FREEZE`, no payload.
- Required datum forbidden: `BLOCK`, no payload.
- Required datum requires grant: `ASK`, no payload.
- Optional datum forbidden/ungranted: redact it and continue.
- Tool/network failure: out of scope for the pure evaluator; a caller must fail closed rather than bypass.

## 8. Security boundary

The engine is pure: no network, storage, environment-variable, or subprocess access. This limits the reference attack surface and makes deterministic replay straightforward. Production integration must ensure callers cannot skip the boundary, mutate evaluated payload after release, forge recipient IDs, or reuse stale policy snapshots.

## 9. Evolution law

Any policy/version change invalidates prior policy-bound evidence. Compatibility requires explicit policy-version semantics. A future signed receipt should bind request hash, policy version, classifier version, recipient-registry version, and monotonic decision timestamp.
