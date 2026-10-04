from nulf.outcome import ObjectiveContract, WorkItem, analyze


def test_pass_complete_traceability():
    result = analyze(
        ObjectiveContract("o", ("c1", "c2"), ("forbidden",)),
        (
            WorkItem("a", ("c1",), "lab/a"),
            WorkItem("b", ("c2",), "lab/b", ("a",)),
        ),
    )
    assert result["verdict"] == "PASS"
    assert result["coverage"]["ratio_ppm"] == 1_000_000


def test_orphan_freezes():
    result = analyze(ObjectiveContract("o", ("c1",)), (WorkItem("a", (), "lab"),))
    assert result["verdict"] == "FREEZE"
    assert "ORPHAN_WORK_ITEM" in result["reason_codes"]


def test_forbidden_scope_freezes():
    result = analyze(ObjectiveContract("o", ("c1",), ("NEXY.AI-",)), (WorkItem("a", ("c1",), "NEXY.AI-/src"),))
    assert result["verdict"] == "FREEZE"
    assert result["forbidden_items"] == ["a"]


def test_dependency_cycle_freezes():
    result = analyze(
        ObjectiveContract("o", ("c1",)),
        (WorkItem("a", ("c1",), "x", ("b",)), WorkItem("b", ("c1",), "x", ("a",))),
    )
    assert result["verdict"] == "FREEZE"
    assert "DEPENDENCY_CYCLE" in result["reason_codes"]


def test_unknown_criterion_freezes():
    result = analyze(ObjectiveContract("o", ("c1",)), (WorkItem("a", ("nope",), "x"),))
    assert "UNKNOWN_ACCEPTANCE_CRITERION" in result["reason_codes"]


def test_input_order_does_not_change_fingerprint():
    contract = ObjectiveContract("o", ("c1", "c2"))
    a = WorkItem("a", ("c1",), "x")
    b = WorkItem("b", ("c2",), "x", ("a",))
    assert analyze(contract, (a, b))["fingerprint"] == analyze(contract, (b, a))["fingerprint"]
