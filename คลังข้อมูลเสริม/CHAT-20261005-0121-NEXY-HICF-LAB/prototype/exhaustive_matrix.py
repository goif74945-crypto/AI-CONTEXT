from hicf import (
    ActionCandidate, AuthorityState, ClarificationGate, GateDecision,
    Impact, IntentEnvelope, Materiality, Reversibility, Unknown
)


def main() -> None:
    gate = ClarificationGate()
    total = 0
    counts = {d.value: 0 for d in GateDecision}

    for authority in AuthorityState:
        for materiality in [None, *Materiality]:
            for impact in Impact:
                for reversibility in Reversibility:
                    for mutates in (False, True):
                        for prohibited in (False, True):
                            unknowns = () if materiality is None else (Unknown("u", materiality),)
                            envelope = IntentEnvelope.build(
                                objective="matrix",
                                unknowns=unknowns,
                                prohibited=("danger",) if prohibited else (),
                                authority_state=authority,
                            )
                            action = ActionCandidate(
                                "matrix-action",
                                "danger mutation" if prohibited else "safe operation",
                                impact,
                                reversibility,
                                mutates,
                            )
                            result = gate.evaluate(envelope, action)
                            total += 1
                            counts[result.decision.value] += 1

                            if authority is AuthorityState.CONFLICT:
                                assert result.decision is GateDecision.FREEZE
                            if prohibited and authority is not AuthorityState.CONFLICT:
                                assert result.decision is GateDecision.FREEZE
                            if materiality is Materiality.CRITICAL and authority is AuthorityState.RESOLVED and not prohibited:
                                assert result.decision is GateDecision.FREEZE
                            if materiality is Materiality.MATERIAL and authority is AuthorityState.RESOLVED and not prohibited:
                                assert result.decision is GateDecision.ASK
                            if (
                                materiality is None
                                and authority is AuthorityState.RESOLVED
                                and not prohibited
                            ):
                                assert result.decision is GateDecision.PROCEED

    print(f"TOTAL_CASES={total}")
    for key in sorted(counts):
        print(f"{key}={counts[key]}")
    print("MATRIX_STATUS=PASS")


if __name__ == "__main__":
    main()
