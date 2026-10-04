# MMCRC20 — Multi-Model Contract Resilience Court 20

Status: Lo4 AI proposal / standalone reference implementation / non-canonical / non-governing.

MMCRC20 is a deterministic pre-promotion court for NEXY multi-model adapters. It evaluates whether provider adapter manifests and captured provider traces preserve the current NEXY AgentAdapter boundary across model/provider substitution. It does not call providers, store credentials, mutate NEXY, mutate Core/JUDGE/LAW state, or promote anything.

The package exists because NEXY already has a canonical AgentAdapter contract and OpenAI, Gemini, and Anthropic adapter implementations. A provider-specific adapter can be individually valid yet still be unsafe as a substitute if its context ceiling, timeout behavior, response schema, evidence provenance, cancellation, health classification, identity pin, or failover behavior diverges.

All decision-relevant quantitative logic in this lab is checked signed Q64.64. Binary floating point is not used in the deterministic court logic.

The exact tested source, tests and raw evidence logs are preserved in `sealed/MMCRC20-BUNDLE.tar.gz.b64`. Decode base64 and gunzip/untar it, then verify against `SHA256SUMS`.

Standalone PASS is evidence only for this reference implementation and its fixtures. It is not production-provider, NEXY-runtime, deployment, or network evidence.
