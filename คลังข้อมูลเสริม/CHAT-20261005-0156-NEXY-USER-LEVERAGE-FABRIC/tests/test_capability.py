from nulf.capability import Capability, CompositionRequest, compose


def cap(cid, inputs, outputs, risk=1, cost=1, status="AVAILABLE", data=("internal",), perms=("read",)):
    return Capability(cid, status, frozenset(inputs), frozenset(outputs), frozenset(data), frozenset(perms), risk, cost)


def req(**kwargs):
    base = dict(
        available_types=frozenset({"text"}),
        target_type="pdf",
        allowed_data_classes=frozenset({"internal"}),
        allowed_permissions=frozenset({"read"}),
        max_risk_units=10,
        max_cost_units=10,
        max_steps=5,
    )
    base.update(kwargs)
    return CompositionRequest(**base)


def test_composes_two_step_plan():
    result = compose(req(), (cap("a", ("text",), ("md",)), cap("b", ("md",), ("pdf",))))
    assert result["verdict"] == "PASS"
    assert result["plan"] == ["a", "b"]


def test_prefers_lower_risk_then_cost_then_lexical():
    result = compose(req(), (
        cap("z", ("text",), ("pdf",), risk=3, cost=1),
        cap("b", ("text",), ("pdf",), risk=1, cost=2),
        cap("a", ("text",), ("pdf",), risk=1, cost=2),
    ))
    assert result["plan"] == ["a"]


def test_disallowed_permission_is_excluded():
    result = compose(req(), (cap("danger", ("text",), ("pdf",), perms=("admin",)),))
    assert result["verdict"] == "FREEZE"
    assert "danger" not in result["eligible_capabilities"]


def test_unavailable_capability_not_used():
    result = compose(req(), (cap("offline", ("text",), ("pdf",), status="UNAVAILABLE"),))
    assert result["verdict"] == "FREEZE"


def test_cost_budget_blocks_plan():
    result = compose(req(max_cost_units=1), (cap("expensive", ("text",), ("pdf",), cost=2),))
    assert result["verdict"] == "FREEZE"


def test_capability_input_order_does_not_change_result_or_fingerprint():
    caps = (cap("a", ("text",), ("md",)), cap("b", ("md",), ("pdf",)))
    one = compose(req(), caps)
    two = compose(req(), tuple(reversed(caps)))
    assert one == two
