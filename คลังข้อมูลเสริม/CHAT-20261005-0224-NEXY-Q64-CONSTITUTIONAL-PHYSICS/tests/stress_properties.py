from qcp.fixed import Q64
from qcp.robustness import LinearFeature, DecisionRobustnessEngine
from qcp.uncertainty import UncertaintyStage, UncertaintyMassCompiler

q = Q64.from_decimal


def main():
    checks = 0
    engine = DecisionRobustnessEngine()
    for i in range(1, 501):
        center = Q64.from_ratio(i, 1000)
        radius = Q64.from_ratio(i % 17, 10000)
        f = LinearFeature("x", q("1"), center, radius)
        a = engine.certify([f], bias=q("0"), threshold=q("0.5"))
        b = engine.certify([f], bias=q("0"), threshold=q("0.5"))
        assert a == b
        assert a.lower_bound <= a.nominal <= a.upper_bound
        checks += 1

    compiler = UncertaintyMassCompiler()
    for i in range(1, 501):
        incoming = Q64.from_ratio(i, 1000)
        resolved = Q64.from_ratio(i % 11, 10000)
        introduced = Q64.from_ratio(i % 7, 10000)
        outgoing = incoming + introduced - resolved
        d = compiler.compile([UncertaintyStage("s", incoming, introduced, resolved, outgoing, ("E",) if resolved > Q64.zero() else ())])
        assert d.status == "PASS"
        checks += 1

    print(f"STRESS_PASS {checks}")


if __name__ == "__main__":
    main()
