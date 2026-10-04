# Threat / Failure Model

## Assets protected
- NEXY authority hierarchy;
- release integrity;
- VAULT write boundary;
- provider credentials;
- deterministic failure semantics;
- quorum/release gates.

## Threats addressed by this lab
| Threat | Example | Control |
|---|---|---|
| authority escalation | adapter claims direct release | manifest hard rejection |
| storage bypass | worker writes VAULT itself | direct_vault_write=false |
| hidden retry | provider call silently retries | automatic_retry=false |
| mode drift | provider introduces `turbo` path | exact mode allowlist |
| timeout drift | critical adapter waits 60s | critical timeout check |
| schema trust | malformed worker output accepted | schema-invalid -> FREEZE simulation |
| quorum guessing | timeout occurs with unknown remaining quorum | FREEZE, never optimistic continue |
| credential embedding | API key packaged with adapter | runtime injection declaration + no persistence |
| cross-language drift | Python and TS disagree | parity test against shared fixtures |

## Not solved here
- malicious provider responses;
- prompt injection inside model output;
- network egress enforcement;
- actual secret-manager configuration;
- process/container isolation;
- real cancellation races;
- streaming protocol correctness;
- provider billing/rate-limit behavior;
- live SWARM/JUDGE/LAW integration.

These require runtime/integration evidence and are deliberately not faked by this lab.
