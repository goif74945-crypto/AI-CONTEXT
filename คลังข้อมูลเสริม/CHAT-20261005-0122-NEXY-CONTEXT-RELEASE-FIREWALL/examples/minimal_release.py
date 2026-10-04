from nexy_crf import (
    ContextField,
    ContextReleaseFirewall,
    ContextSet,
    ReleasePolicy,
    ReleaseRequest,
    Sensitivity,
)

context = ContextSet({
    "task": ContextField(
        key="task",
        value="Review the parser module for correctness.",
        sensitivity=Sensitivity.INTERNAL,
        provenance="task:example",
        allowed_purposes=frozenset({"code_review"}),
    ),
    "unrelated_secret": ContextField(
        key="unrelated_secret",
        value="this-value-is-never-requested",
        sensitivity=Sensitivity.SECRET,
        provenance="vault:example",
    ),
})

request = ReleaseRequest(
    request_id="example-1",
    consumer_id="agent:reviewer",
    purpose="code_review",
    required_keys=("task",),
)

policy = ReleasePolicy(
    policy_id="reviewer-policy",
    consumer_id="agent:reviewer",
    allowed_purposes=frozenset({"code_review"}),
    max_sensitivity=Sensitivity.INTERNAL,
    allowed_compartments=frozenset(),
)

result = ContextReleaseFirewall().release(
    context,
    request,
    policy,
    evaluated_at="2026-10-05T01:30:00+07:00",
)

print(result.status.value)
print(dict(result.payload))
print(result.receipt.public_dict())
