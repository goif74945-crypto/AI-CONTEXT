from nulf.mastery import MasteryRequest, SkillNode, compile_path


def nodes():
    return (
        SkillNode("basics", (), "learn basics", "explain freeze"),
        SkillNode("verify", ("basics",), "inspect evidence", "identify evidence class"),
        SkillNode("operate", ("verify",), "run guided task", "complete dry run"),
    )


def test_known_prereq_is_skipped():
    result = compile_path(MasteryRequest("operate", frozenset({"basics"}), 5), nodes())
    assert result["verdict"] == "PASS"
    assert [s["skill_id"] for s in result["steps"]] == ["verify", "operate"]


def test_nothing_is_inferred_known():
    result = compile_path(MasteryRequest("operate", frozenset(), 5), nodes())
    assert [s["skill_id"] for s in result["steps"]] == ["basics", "verify", "operate"]


def test_unknown_goal_freezes():
    result = compile_path(MasteryRequest("missing", frozenset(), 5), nodes())
    assert result["verdict"] == "FREEZE"


def test_cycle_freezes():
    cyc = (SkillNode("a", ("b",), "a", "a"), SkillNode("b", ("a",), "b", "b"))
    result = compile_path(MasteryRequest("a", frozenset(), 5), cyc)
    assert "PREREQUISITE_CYCLE" in result["reason_codes"]


def test_step_budget_freezes_instead_of_truncating():
    result = compile_path(MasteryRequest("operate", frozenset(), 2), nodes())
    assert result["verdict"] == "FREEZE"
    assert result["steps"] == []


def test_node_input_order_does_not_change_result_or_fingerprint():
    ns = nodes()
    one = compile_path(MasteryRequest("operate", frozenset({"basics"}), 5), ns)
    two = compile_path(MasteryRequest("operate", frozenset({"basics"}), 5), tuple(reversed(ns)))
    assert one == two
