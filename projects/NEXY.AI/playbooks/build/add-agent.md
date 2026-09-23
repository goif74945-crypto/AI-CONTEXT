# PLAYBOOK — Add AI Agent / Model Adapter

## PRECONDITIONS
- Agent/model use is authorized.
- Provider/tool data-sharing boundary is understood.
- Agent cannot become final authority.
- AgentAdapter contract exists or is intentionally versioned.

## REQUIRED CONTEXT
- Lo3 Agent Orchestrator;
- AgentAdapter contract;
- context sharding;
- trust/evaluation;
- timeout/critical-agent policy;
- data masking/security boundary;
- release policy;
- current provider adapter implementation/tests.

## IMPLEMENTATION SEQUENCE
1. Define stable adapter ID/provider/version.
2. Declare supported modes/capabilities.
3. Declare deterministic-capable truthfully.
4. Declare critical vs noncritical role.
5. Define timeout and context capacity.
6. Implement execute/cancel/healthcheck contract.
7. Normalize provider output into canonical untrusted result schema.
8. Sanitize/provider-isolate data.
9. Ensure provider result cannot write VAULT/authority directly.
10. Integrate trust/health routing.
11. Add timeout/schema/cancel/health degradation tests.
12. Add cross-verification with at least one independent path when required.
13. Verify release still passes through JUDGE/LAW/release policy.

## NEGATIVE TESTS
- malformed provider response;
- hallucinated tool/result fields;
- timeout;
- provider unavailable;
- prompt injection in model output;
- critical-agent failure;
- data-leak boundary violation;
- model disagreement.

## DONE
Adapter behavior is proven while authority remains outside the model.
