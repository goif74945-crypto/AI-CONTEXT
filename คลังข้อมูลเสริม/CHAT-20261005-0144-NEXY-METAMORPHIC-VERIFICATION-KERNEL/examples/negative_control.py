from nexy_mvk import Case, Observation, VerificationEngine, deterministic_replay

state = {"count": 0}


def drifting_adapter(_case: Case) -> Observation:
    state["count"] += 1
    return Observation(status="PASS", released=True, payload={"counter": state["count"]})


result = VerificationEngine(drifting_adapter).run_relation(Case(prompt="same input"), deterministic_replay())
print(f"{result.status.value}: {result.reason}")
raise SystemExit(0 if result.status.value == "FAIL" else 1)
