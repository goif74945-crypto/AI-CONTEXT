from nulf.demo import build_demo_report


def test_demo_all_engines_pass():
    report = build_demo_report()
    assert set(report) == {
        "goal_contribution_graph",
        "verified_capability_composer",
        "artifact_consumer_fitness_gate",
        "supply_chain_trust_gate",
        "mastery_path_compiler",
    }
    assert all(engine["verdict"] == "PASS" for engine in report.values())
