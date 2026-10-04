# Threat Model

## Protected assets

- private project/user context;
- credentials and secrets;
- personal/sensitive fields;
- destination policy integrity;
- purpose declaration integrity;
- retention bounds;
- decision/audit integrity.

## Adversaries and failure sources

### A1. Over-broad task context
A caller assembles a giant context window because it is convenient.

**Control:** explicit `required_fields` projection. Non-required fields are pruned.

### A2. Prompt injection requests more context
Untrusted text asks the system to include unrelated secrets or memory.

**Control:** raw prompt text does not redefine field classification, purpose, destination ACL, or policy.

**Residual risk:** if an upstream authority incorrectly labels a field as required/allowed, PCF will enforce the bad metadata faithfully. Authority quality remains critical.

### A3. Provider substitution weakens privacy
A router swaps to another provider with different retention or data boundaries.

**Control:** envelope destination must match an explicit destination profile; provider identity/profile is part of the decision receipt.

### A4. Secret leaks through denial logs
A system blocks a secret but logs the raw denied value in an error or receipt.

**Control:** FREEZE material contains field metadata and violation codes, not raw field values; explicit leak test exists.

### A5. Unknown classifications silently pass
New classification labels appear after policy evolution.

**Control:** unknown class => typed FREEZE.

### A6. Stale policy replay
An old envelope is compiled under a newer/different policy.

**Control:** exact `policy_version` match required.

### A7. Retention inflation
A field requests a very large retention period.

**Control:** effective retention is bounded by both global policy and destination limits; non-retaining destinations force zero.

### A8. Receipt forgery or accidental weak key
An attacker attempts to construct plausible audit material.

**Control:** HMAC-SHA256 with caller-supplied key, minimum 32-byte key gate.

**Residual risk:** this lab does not provide key rotation, HSM/KMS integration, per-tenant key isolation, or compromise recovery.

### A9. Serialization ambiguity
Equivalent objects serialize differently or non-JSON values enter receipt material.

**Control:** canonical JSON with sorted keys, compact separators, NaN rejection, and stable field ordering.

### A10. Malformed policy crashes the control path
A weird object/type throws before a safe decision is produced.

**Control:** malformed/non-canonical destination/policy inputs freeze rather than raise for covered cases.

## Important residual risks

1. **Classification authority risk:** PCF does not discover sensitive data automatically.
2. **Purpose honesty risk:** a malicious authorized caller can misdeclare a purpose unless another authority validates it.
3. **Destination truth risk:** profiles describe expected capabilities; they do not prove provider behavior.
4. **Side channels:** this lab does not prove timing, memory, crash-dump, swap, telemetry, or transport secrecy.
5. **Post-egress use:** once an admitted payload leaves the boundary, enforcement needs provider/API/runtime controls.
6. **Composition:** integration with retrieval, caching, agents, observability, and retry systems can reintroduce data that PCF did not admit.

## Security conclusion

PCF is best understood as a deterministic **admission control boundary**, not a complete privacy system. It reduces accidental disclosure and makes policy decisions inspectable, while keeping unsupported guarantees explicitly outside scope.
