from __future__ import annotations

import json
import random
import sys

from nexy_lo4_frontier import (
    AuthorityRule,
    Capability,
    DecisionCase,
    EvidenceArtifact,
    ForbiddenPrivilegeSet,
    Observation,
    ProofClaim,
    ReplayCapsule,
    analyze_capability_composition,
    assess_evidence_debt,
    differential_oracle,
    mine_shadow_invariants,
    simulate_authority_change,
)


def shuffled(rng, items):
    out = list(items)
    rng.shuffle(out)
    return out


def run(seed: int, iterations: int = 1000):
    rng = random.Random(seed)
    base_rules = [
        AuthorityRule("deny-delete", 100, "DENY", "delete", "*"),
        AuthorityRule("allow-public", 90, "ALLOW", "read", "public/*"),
        AuthorityRule("deny-private", 90, "DENY", "read", "private/*"),
    ]
    cases = [
        DecisionCase("c1", "u", "read", "public/a"),
        DecisionCase("c2", "u", "read", "private/a"),
        DecisionCase("c3", "u", "delete", "public/a"),
    ]
    base_wind = simulate_authority_change(base_rules, base_rules, cases).fingerprint

    claims = [
        ProofClaim("root", 2, 50, ("root.py",)),
        ProofClaim("api", 3, 30, ("api.py",), ("root",)),
    ]
    evidence = [
        EvidenceArtifact("root-u", ("root",), 2, (("root.py", "v1"),)),
        EvidenceArtifact("api-i", ("api",), 3, (("api.py", "v1"),)),
    ]
    base_debt = assess_evidence_debt(claims, evidence, {"root.py": "v1", "api.py": "v1"}).fingerprint

    caps = [
        Capability("read", frozenset({"auth"}), frozenset({"secret-read"}), "p"),
        Capability("http", frozenset({"auth"}), frozenset({"http"}), "p"),
        Capability("send", frozenset({"http"}), frozenset({"network-egress"}), "p"),
    ]
    forbidden = [ForbiddenPrivilegeSet("exfil", frozenset({"secret-read", "network-egress"}))]
    base_cap = analyze_capability_composition(caps, ["auth"], forbidden, allowed_scopes=frozenset({"p"})).fingerprint

    obs = [
        Observation("1", (("state", "PASS"), ("a", 1), ("b", 1))),
        Observation("2", (("state", "PASS"), ("a", 2), ("b", 2))),
        Observation("3", (("state", "PASS"), ("a", 3), ("b", 3))),
    ]
    base_mine = mine_shadow_invariants(obs).fingerprint

    capsule = ReplayCapsule("r", {"values": [1, 2, 3]}, {"mode": "strict"}, "a" * 64, (("calc", "1"),), seed)
    def ex1(c): return {"result": sum(c.request["values"]), "state": c.state["mode"]}
    def ex2(c): return {"state": "strict", "result": 6}
    base_replay = differential_oracle(capsule, {"ex1": ex1, "ex2": ex2}).fingerprint

    for _ in range(iterations):
        if simulate_authority_change(shuffled(rng, base_rules), shuffled(rng, base_rules), shuffled(rng, cases)).fingerprint != base_wind:
            raise AssertionError("CAWT_NONDETERMINISM")
        if assess_evidence_debt(shuffled(rng, claims), shuffled(rng, evidence), {"api.py": "v1", "root.py": "v1"}).fingerprint != base_debt:
            raise AssertionError("EDEL_NONDETERMINISM")
        if analyze_capability_composition(shuffled(rng, caps), ["auth"], shuffled(rng, forbidden), allowed_scopes=frozenset({"p"})).fingerprint != base_cap:
            raise AssertionError("CCF_NONDETERMINISM")
        if mine_shadow_invariants(shuffled(rng, obs)).fingerprint != base_mine:
            raise AssertionError("SIMF_NONDETERMINISM")
        if differential_oracle(capsule, dict(shuffled(rng, [("ex1", ex1), ("ex2", ex2)]))).fingerprint != base_replay:
            raise AssertionError("DRCDO_NONDETERMINISM")

    return {"seed": seed, "iterations": iterations, "checks": iterations * 5, "status": "PASS"}


if __name__ == "__main__":
    seeds = [1, 42, 777, 20261005]
    iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    result = {"runs": [run(seed, iterations) for seed in seeds]}
    result["total_checks"] = sum(x["checks"] for x in result["runs"])
    result["status"] = "PASS"
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
