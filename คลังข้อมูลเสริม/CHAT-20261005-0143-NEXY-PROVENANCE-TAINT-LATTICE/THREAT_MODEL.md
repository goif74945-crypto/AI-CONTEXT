# THREAT MODEL

> AI-PROPOSED CONCEPT. Scope is the standalone reference kernel.

## Assets
- provenance integrity;
- authority floor integrity;
- assurance integrity;
- taint continuity;
- deterministic release decisions;
- artifact/receipt identity.

## Adversarial or faulty behaviors

| Threat | Example | Mitigation |
|---|---|---|
| Trust laundering | rewrite weak model output repeatedly | sticky taints + non-promotional authority/assurance |
| Mixed-lineage promotion | merge canonical + low-authority source | authority floor uses minimum |
| Assurance invention | transform labels output `verified` | intersection + preservation allowlist |
| Receipt rebinding | receipt for A applied to B | exact artifact ID binding |
| Receipt tamper | change verifier/assurance after issue | content-addressed receipt ID |
| Unknown origin hiding | blank origin later rewritten | `UNKNOWN_ORIGIN` protected taint |
| Conflict hiding | contradictory lineage summarized away | `CONFLICT` protected taint |
| External trust spoof | untrusted external source marked clean later | protected `EXTERNAL_UNTRUSTED` |
| Schema smuggling | extra wire field changes semantics | exact-key fail-closed parser |
| Stale release | old artifact reused after validity window | epoch freshness policy |
| Future timestamp | invalid clock/epoch ordering | future-artifact/receipt checks |
| Nondeterministic release | stochastic transform treated as stable | `NONDETERMINISTIC` taint + policy gate |
| Object tamper | authority edited in memory/record | artifact identity revalidation |

## Explicitly not solved

1. **Verifier authentication**: a content-addressed receipt proves integrity, not who is authorized to issue it. A production adapter must authenticate/sign verifier authority.
2. **Canonical NEXY authority law**: this lab uses caller-defined numeric ranks solely as a reference domain.
3. **Distributed storage attacks**: no durable graph/database is implemented.
4. **Transitive graph cycle verification**: direct identity tampering/self-cycle is checked; a durable graph service would be required for arbitrary historical graph validation.
5. **Cryptographic non-repudiation**: SHA-256 identity is not a digital signature.
6. **Production performance/SLA**: local benchmark results are environment-specific and are not deployment proof.
