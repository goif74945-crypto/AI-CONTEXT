# Capability Negotiation Protocol
## Goal
Let agents, tools, models, services, and clients evolve independently without assuming universal behavior.
## Advertisement
participant_id; protocol_versions; capabilities; limits; required_preconditions; side_effect_classes; evidence_classes; failure_modes; data_classes; latency_class; cost_class; deprecation_flags.
Caller declares required and optional capabilities. Selection succeeds only when every required capability is satisfied.
## Naming
Capabilities describe behavior, not vendor identity.
## Side-effect classes
READ_ONLY, REVERSIBLE_WRITE, DURABLE_WRITE, EXTERNAL_COMMUNICATION, PRIVILEGE_CHANGE, DESTRUCTIVE, FINANCIAL_OR_LEGAL.
Policy gates attach to classes.
## Failure semantics
NEGOTIATION_FAILED, PRECONDITION_FAILED, POLICY_DENIED, TEMPORARILY_UNAVAILABLE, UNSUPPORTED_VERSION, PARTIAL_RESULT. Recovery differs, so do not flatten them into generic failure.
## Downgrade
Optional capability loss may use a declared downgrade. Required capability loss stops execution. Downgrade may never weaken immutable safety, authority, evidence, or data-integrity requirements.
## Compatibility fixtures
old caller/new provider; new caller/old provider; missing optional; missing required; unknown capability; deprecated capability; malformed advertisement; provider claiming a capability but failing a conformance probe.
## Payoff
Product semantics become insulated from model/tool churn; migrations become measurable.
